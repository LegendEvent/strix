import time

import pytest
import respx

from pathlib import Path

from strix.llm import copilot_auth


@pytest.mark.asyncio
async def test_env_access_token_returns_immediately(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("STRIX_COPILOT_ACCESS", "env-access-token-123")
    tok_path = tmp_path / "copilot_auth.json"
    if tok_path.exists():
        tok_path.unlink()

    token, base = await copilot_auth.get_copilot_access_token(
        token_path=tok_path, enterprise_url=None, interactive=False
    )
    assert token == "env-access-token-123"
    assert base.startswith("https://")


@pytest.mark.asyncio
async def test_env_refresh_token_triggers_exchange(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.delenv("STRIX_COPILOT_ACCESS", raising=False)
    monkeypatch.setenv("STRIX_COPILOT_TOKEN", "env-refresh-xyz")

    tok_path = tmp_path / "copilot_auth.json"

    domain = "github.com"
    urls = copilot_auth._get_urls(domain)

    with respx.mock as rsps:
        rsps.get(urls["COPILOT_API_KEY_URL"]).respond(
            200, json={"token": "access-456", "expires_at": int(time.time()) + 3600}
        )

        token, base = await copilot_auth.get_copilot_access_token(
            token_path=tok_path, enterprise_url=None, interactive=False
        )

    assert token == "access-456"
    assert tok_path.exists()


@pytest.mark.asyncio
async def test_non_interactive_without_token_raises(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.delenv("STRIX_COPILOT_ACCESS", raising=False)
    monkeypatch.delenv("STRIX_COPILOT_TOKEN", raising=False)

    tok_path = tmp_path / "copilot_auth.json"
    if tok_path.exists():
        tok_path.unlink()

    with pytest.raises(RuntimeError):
        await copilot_auth.get_copilot_access_token(
            token_path=tok_path, enterprise_url=None, interactive=False
        )
