import asyncio
import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from time import time
from typing import Any

import httpx


logger = logging.getLogger(__name__)

# Global async lock to prevent concurrent token refresh attempts
_refresh_lock = asyncio.Lock()

# GitHub Copilot public OAuth client id (matches VSCode Copilot auth patterns)
COPILOT_CLIENT_ID = "Iv1.b507a08c87ecfe98"

# Must match what Copilot expects (VSCode-mimic)
# Headers must be lowercase to match litellm spec
COPILOT_DEFAULT_HEADERS: dict[str, str] = {
    "user-agent": "GitHubCopilotChat/0.32.4",
    "editor-version": "vscode/1.105.1",
    "editor-plugin-version": "copilot-chat/0.32.4",
    "copilot-integration-id": "vscode-chat",
}

DEVICE_FLOW_USER_AGENT = "GitHubCopilotChat/0.35.0"


@dataclass
class CopilotOAuthInfo:
    # Matches plugin naming: refresh is the GitHub OAuth device-flow token
    refresh: str
    access: str
    expires: int
    enterprise_url: str | None = None


def _normalize_domain(url_or_domain: str) -> str:
    s = url_or_domain.strip()
    s = s.removeprefix("https://").removeprefix("http://")
    return s.removesuffix("/")


def _get_urls(domain: str) -> dict[str, str]:
    return {
        "DEVICE_CODE_URL": f"https://{domain}/login/device/code",
        "ACCESS_TOKEN_URL": f"https://{domain}/login/oauth/access_token",
        "COPILOT_API_KEY_URL": f"https://api.{domain}/copilot_internal/v2/token",
    }


def copilot_openai_base_url(*, enterprise_domain: str | None) -> str:
    # For github.com, Copilot uses https://api.githubcopilot.com
    # For enterprise, Copilot uses https://copilot-api.<enterpriseDomain>
    if enterprise_domain:
        return f"https://copilot-api.{enterprise_domain}"
    return "https://api.githubcopilot.com"


def _now_ms() -> int:
    return int(time() * 1000)


def default_token_store_path() -> Path:
    # Use XDG config dir if available; fallback to ~/.config
    base = Path(os.getenv("XDG_CONFIG_HOME", str(Path.home() / ".config")))
    return base / "strix" / "copilot_auth.json"


def _load_oauth_info_from_disk(path: Path) -> CopilotOAuthInfo | None:
    try:
        if not path.is_file():
            return None
        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            return None
        refresh = raw.get("refresh")
        if not refresh:
            return None
        return CopilotOAuthInfo(
            refresh=str(refresh),
            access=str(raw.get("access") or ""),
            expires=int(raw.get("expires") or 0),
            enterprise_url=raw.get("enterpriseUrl") or raw.get("enterprise_url"),
        )
    except Exception as e:  # noqa: BLE001
        logger.warning("Failed to load Copilot token store: %s", e)
        return None


def _save_oauth_info_to_disk(path: Path, info: CopilotOAuthInfo) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "type": "oauth",
        "refresh": info.refresh,
        "access": info.access,
        "expires": info.expires,
    }
    if info.enterprise_url:
        payload["enterpriseUrl"] = info.enterprise_url
        payload["enterprise_url"] = info.enterprise_url

    # Best-effort permissions (0600)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload), encoding="utf-8")
    import contextlib

    # Best-effort set secure permissions on the temporary file; ignore failures.
    with contextlib.suppress(Exception):
        tmp.chmod(0o600)
    tmp.replace(path)


async def _ensure_ok(resp: httpx.Response, err: str) -> None:
    if 200 <= resp.status_code < 300:
        return
    raise RuntimeError(f"{err} (status={resp.status_code}) body={resp.text}")


async def _start_device_flow(*, domain: str) -> Any:
    urls = _get_urls(domain)
    async with httpx.AsyncClient(timeout=30.0, trust_env=False) as http:
        resp = await http.post(
            urls["DEVICE_CODE_URL"],
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": DEVICE_FLOW_USER_AGENT,
            },
            json={"client_id": COPILOT_CLIENT_ID, "scope": "read:user"},
        )
        await _ensure_ok(resp, "Failed to initiate device authorization")
        return resp.json()


async def _poll_device_flow(
    *,
    domain: str,
    device_code: str,
    interval_s: int,
    expires_in_s: int,
) -> str:
    urls = _get_urls(domain)
    deadline = time() + max(0, int(expires_in_s))

    async with httpx.AsyncClient(timeout=30.0, trust_env=False) as http:
        while True:
            if time() >= deadline:
                raise RuntimeError(
                    "Device flow expired. Please re-run and complete the browser authorization."
                )

            resp = await http.post(
                urls["ACCESS_TOKEN_URL"],
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "User-Agent": DEVICE_FLOW_USER_AGENT,
                },
                json={
                    "client_id": COPILOT_CLIENT_ID,
                    "device_code": device_code,
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                },
            )
            await _ensure_ok(resp, "Device flow polling failed")
            data = resp.json()

            access_token = data.get("access_token")
            if access_token:
                return str(access_token)

            err = data.get("error")
            if err == "authorization_pending":
                await asyncio.sleep(interval_s)
                continue

            if err == "slow_down":
                interval_s = int(interval_s) + 5
                await asyncio.sleep(interval_s)
                continue

            if err:
                raise RuntimeError(f"Device flow failed: {err}")

            await asyncio.sleep(interval_s)


async def login_via_device_flow_if_needed(
    *,
    token_path: Path | None = None,
    enterprise_url: str | None = None,
    interactive: bool = True,
) -> CopilotOAuthInfo:
    """Ensure we have a stored GitHub OAuth device-flow token."""

    token_path = token_path or default_token_store_path()
    existing = _load_oauth_info_from_disk(token_path)
    if existing and existing.refresh:
        return existing

    if not interactive:
        raise RuntimeError(
            "GitHub Copilot login required. Re-run with interactive login enabled "
            "or run `strix auth login` first."
        )

    domain = _normalize_domain(enterprise_url) if enterprise_url else "github.com"
    device_data = await _start_device_flow(domain=domain)

    verification_uri = device_data.get("verification_uri")
    user_code = device_data.get("user_code")
    interval_s = int(device_data.get("interval") or 5)
    expires_in_s = int(device_data.get("expires_in") or 900)

    msg_lines = [
        "GitHub Copilot login required (device flow)",
        f"Open: {verification_uri}",
        f"Enter code: {user_code}",
    ]
    for line in msg_lines:
        logger.error("%s", line)
        # Avoid printing in library code; log only. Clients can surface messages as needed.
        # print(line, file=sys.stderr)

    refresh_token = await _poll_device_flow(
        domain=domain,
        device_code=str(device_data.get("device_code")),
        interval_s=interval_s,
        expires_in_s=expires_in_s,
    )

    info = CopilotOAuthInfo(
        refresh=refresh_token,
        access="",
        expires=0,
        enterprise_url=domain if enterprise_url else None,
    )
    _save_oauth_info_to_disk(token_path, info)
    return info


async def get_copilot_access_token(
    *,
    token_path: Path | None = None,
    enterprise_url: str | None = None,
    interactive: bool = True,
    force_refresh: bool = False,
) -> tuple[str, str]:
    """Return (access_token, base_url). Refreshes if expired or force_refresh=True.

    Environment overrides (useful for CI):
    - STRIX_COPILOT_ACCESS: provide a ready-to-use access token (returned immediately)
    - STRIX_COPILOT_TOKEN: provide a refresh-like token which will be exchanged for an access token
    - STRIX_COPILOT_ENTERPRISE: enterprise domain to use instead of github.com

    Args:
        token_path: Path to token storage file (default: ~/.config/strix/copilot_auth.json)
        enterprise_url: Enterprise domain for GitHub Copilot (default: github.com)
        interactive: Whether to allow interactive device flow (default: True)
        force_refresh: Force refresh regardless of expiration check (default: False)
            When True, uses thread-safe lock to prevent concurrent refreshes.
            Designed for automatic retry on API authentication failures (401/403/unauthorized).

    Returns:
        tuple[str, str]: (access_token, base_url)

    Raises:
        RuntimeError: If token refresh fails or no valid refresh token found
    """

    token_path = token_path or default_token_store_path()

    # Environment overrides (CI-friendly)
    env_access = os.getenv("STRIX_COPILOT_ACCESS")
    env_refresh = os.getenv("STRIX_COPILOT_TOKEN")
    env_enterprise = os.getenv("STRIX_COPILOT_ENTERPRISE") or enterprise_url

    enterprise_domain = _normalize_domain(env_enterprise) if env_enterprise else None
    base_url = copilot_openai_base_url(enterprise_domain=enterprise_domain)

    # If an access token is provided directly via env, use it immediately.
    if env_access:
        return env_access, base_url

    # If a refresh token is provided via env, prefer that and avoid device flow.
    if env_refresh:
        info = CopilotOAuthInfo(
            refresh=str(env_refresh),
            access="",
            expires=0,
            enterprise_url=enterprise_domain,
        )
    else:
        # Fall back to loading/storing on disk and device flow when necessary.
        info = await login_via_device_flow_if_needed(
            token_path=token_path,
            enterprise_url=enterprise_url,
            interactive=interactive,
        )

    # Compute base_url/domain (recompute if enterprise_url argument used and env not set)
    effective_enterprise = enterprise_domain or (
        _normalize_domain(enterprise_url) if enterprise_url else None
    )
    base_url = copilot_openai_base_url(enterprise_domain=effective_enterprise)

    # If forcing refresh or token is expired, perform refresh with lock
    if force_refresh or not (info.access and info.expires and info.expires > _now_ms()):
        async with _refresh_lock:
            if force_refresh:
                logger.info("Forcing Copilot access token refresh due to API failure")
            else:
                logger.info("Refreshing expired Copilot access token")

            info = _load_oauth_info_from_disk(token_path) if not env_refresh else info
    base_url = copilot_openai_base_url(enterprise_domain=effective_enterprise)

    # If forcing refresh or token is expired, perform refresh with lock
    if force_refresh or not (info.access and info.expires and info.expires > _now_ms()):
        async with _refresh_lock:
            if force_refresh:
                logger.info("Forcing Copilot access token refresh due to API failure")
            else:
                logger.info("Refreshing expired Copilot access token")

            # Reload token info to ensure we have latest state
            info = _load_oauth_info_from_disk(token_path) if not env_refresh else info

            if not info or not info.refresh:
                raise RuntimeError(
                    "Cannot refresh Copilot token: No valid refresh token found. "
                    "Please re-authenticate with 'strix auth login' or "
                    "set STRIX_COPILOT_TOKEN environment variable."
                )

            domain = (effective_enterprise) or "github.com"
            urls = _get_urls(domain)

            try:
                async with httpx.AsyncClient(timeout=30.0, trust_env=False) as http:
                    resp = await http.get(
                        urls["COPILOT_API_KEY_URL"],
                        headers={
                            "Accept": "application/json",
                            "Authorization": f"Bearer {info.refresh}",
                            **COPILOT_DEFAULT_HEADERS,
                        },
                    )
                    await _ensure_ok(resp, "Token refresh failed")
                    token_data = resp.json()

                info.access = str(token_data.get("token") or "")
                info.expires = int(token_data.get("expires_at") or 0) * 1000
                if effective_enterprise:
                    info.enterprise_url = domain

                _save_oauth_info_to_disk(token_path, info)

                if not info.access:
                    raise RuntimeError("Copilot token refresh returned empty token")

                logger.info("Successfully refreshed Copilot access token")
                return info.access, base_url

            except Exception as e:
                error_str = str(e).lower()

                if "401" in error_str or "403" in error_str or "unauthorized" in error_str:
                    raise RuntimeError(
                        "Copilot refresh token is invalid or expired. "
                        "Please run authentication again to get a new token."
                    ) from e

                raise

    return info.access, base_url
