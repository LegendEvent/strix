# PROJECT KNOWLEDGE BASE

**Generated:** 2026-01-07 23:30:00
**Commit:** c7d1b0c
**Branch:** feature/copilot-device-flow

## OVERVIEW
Autonomous security testing agent (Strix) written in Python that coordinates multiple AI agents through a CLI interface to perform vulnerability discovery and exploitation. Uses OpenAI-compatible LLMs with a tree-structured agent system.

## STRUCTURE
```
./
├── containers/          # Docker/Kali Linux sandbox for penetration testing
├── htmlcov/             # Coverage reports (generated)
├── scripts/             # Utility scripts
├── strix/               # Main source package
│   ├── agents/          # Agent logic and system prompts
│   ├── interface/       # CLI interface and TUI components
│   ├── llm/             # LLM integration (OpenAI, litellm proxy)
│   ├── prompts/         # Jinja2 templates for agent coordination
│   ├── runtime/         # Agent runtime and execution management
│   ├── telemetry/       # Logging and metrics
│   ├── tests/           # Legacy test location (use tests/ instead)
│   └── tools/           # Agent tool implementations (14 modules)
├── strix_runs/          # Runtime outputs/logs (gitignored)
└── tests/               # Main test suite (mirrors strix/ structure)
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| CLI entry point | `strix/interface/main.py` | `main()` function, Poetry entry: `strix` |
| Agent prompts | `strix/prompts/` | Jinja2 templates with strict DO NOT/NEVER rules |
| Tool implementations | `strix/tools/` | 14 modular tools (terminal, browser, python, etc.) |
| LLM integration | `strix/llm/` | OpenAI client, litellm proxy setup, Copilot auth |
| Agent coordination | `strix/agents/` | Base agent, StrixAgent, tree structure |
| Runtime management | `strix/runtime/` | Docker sandbox, tool server, agent lifecycle |
| Tests | `tests/` | Mirrors strix/ structure, pytest with async support |
| Docker sandbox | `containers/` | Kali Linux with security tools (nmap, nuclei, sqlmap) |
| Build config | `strix.spec` | PyInstaller spec for executables |

## CONVENTIONS

**Deviations from standard Python:**
- Dual type checking: mypy (strict) AND pyright (required for CI)
- Test files can exceed 500 lines (security tool integration tests)
- Parallel test structure: `tests/` and `strix/tests/` both exist
- Runtime outputs stored in `strix_runs/` (not `logs/` or `outputs/`)
- PyInstaller `strix.spec` for building executables (non-standard)

**Agent system rules:**
- Agents operate in tree structures, never alone
- 100% autonomy: never ask for permission or confirmation
- Tool invocation uses XML syntax only (no non-XML)
- Finish tool: NEVER use when child agents running
- Terminal commands: NEVER kill on timeout (run indefinitely)

**LLM Integration:**
- Multi-provider support via litellm (OpenAI, Anthropic, Gemini, GitHub Copilot)
- Copilot device-flow OAuth with `strix auth login/logout` commands
- Non-interactive CI auth via `STRIX_COPILOT_ACCESS` or `STRIX_COPILOT_TOKEN` env vars
- XML-based tool invocation parsing with `<function name="...">...</function>` tags
- Memory compression for long conversations (100k token limit, max 3 images)

**Testing & Quality:**
- Pytest with `asyncio_mode = "auto"`
- Mocking: pytest-mock for general, respx for HTTP
- Coverage reports: term, html, xml (htmlcov/ directory)
- Security scanning: Bandit with medium severity
- Ruff + Black for formatting (line length 100)

## ANTI-PATTERNS (THIS PROJECT)

**FORBIDDEN in agent behavior:**
- Echoing inter-agent messages in outputs
- Using "Strix" or identifiable markers in HTTP requests/payloads
- Manual payload iteration for trial-heavy vectors (SQLi, XSS, XXE, SSRF, RCE, auth/JWT, deserialization)
- Relying solely on static code analysis (must include dynamic testing)
- Giving up early on targets (persistent attacker mindset required)
- Using certain reporting actions marked "DO NOT USE"
- Root agent: vulnerability testing and detailed reports (coordination only)

**ALWAYS required:**
- Create agents in tree structures
- Use "think" tool for reasoning before actions
- Explore all possible attack vectors
- Operate at 100% capacity with maximum effort

**LLM Integration:**
- Direct litellm.completion calls bypass request queue and error handling
- Non-XML tool invocations: use `LLMResponse.tool_invocations` instead
- Ignore budget: always check `self.usage_stats` for real-time cost monitoring
- Streaming in core: defaults to `stream=False` for reliability

**Testing:**
- Implicit types: omit return types or argument types in test functions
- Sync in async: blocking calls inside async test functions
- Fixture pollution: defining broad-scoped fixtures in module files instead of conftest.py
- Legacy additions: new tests in strix/tests/ instead of primary tests/ root

## UNIQUE STYLES

**Prompt engineering:**
- Jinja2 templates with strict behavioral directives (DO NOT/NEVER/ALWAYS)
- XML-based tool/parameter invocation syntax
- System prompts emphasize full autonomy and persistent attacker mindset
- Specialized prompt modules injected dynamically (1-3 per agent, max 5)

**Tool design:**
- Each tool in `strix/tools/` is a self-contained module with `__init__.py`
- Tool actions defined in XML schema files
- Tools support async operations
- 12 toolsets: agents_graph, browser, file_edit, finish, notes, proxy, python, reporting, terminal, thinking, todo, web_search

**Runtime:**
- All tool calls proxied through FastAPI tool_server inside Docker sandbox
- Each agent ID mapped to dedicated `multiprocessing.Process`
- Random ports for Caido and Tool Server to avoid collisions
- Shared `/workspace` directory and proxy history across agents in same scan tree

**Testing:**
- Parametrized tests with `@pytest.mark.parametrize`
- Type annotations in test functions
- Coverage-driven with HTML reports
- Dual test locations: tests/ (primary) and strix/tests/ (legacy)

## COMMANDS
```bash
# Development
make format          # Ruff formatting (auto-fix)
make lint            # Ruff + Pylint
make type-check      # MyPy + PyRight (dual type checking)
make security        # Bandit security scanning
make test            # Pytest with verbose output
make test-cov        # Pytest with coverage reports (term, html, xml)
make check-all       # Run all checks (format, lint, type-check, security, test)
make clean           # Clean build artifacts

# Entry point
poetry run strix    # Or: python -m strix.interface.main

# Authentication
strix auth login     # Interactive GitHub Copilot OAuth
strix auth logout    # Remove stored tokens
```

## NOTES

**Gotchas:**
- Two test locations exist: `tests/` (primary) and `strix/tests/` (legacy)
- `strix_runs/` directory accumulates runtime outputs (not in gitignore by default?)
- No CI/CD configured yet (README mentions integration, but no .github/workflows)
- LSP servers not installed for Python (use mypy/pyright instead)
- PyInstaller spec file suggests executable distribution is planned
- Kali Linux container installs extensive security tools (nmap, nuclei, sqlmap, etc.)
- Agent prompts contain strict behavioral constraints - modifying them requires careful testing
- GitHub Copilot authentication supports both interactive device-flow and non-interactive CI tokens
- LLM rate limiting via `LLM_RATE_LIMIT_DELAY` (default: 4s) and `LLM_RATE_LIMIT_CONCURRENT` (default: 1)
- Memory compression preserves exact technical details (URLs, paths, parameters, errors) while summarizing verbose outputs

**Dependencies:**
- Poetry for dependency management
- OpenAI API compatible clients
- textual for TUI
- pytest with async support
- litellm for multi-provider LLM proxy
- httpx for HTTP client (with auth token refresh)
- FastAPI/Uvicorn for tool server
- Playwright for browser automation
- Caido for HTTP proxy

**File patterns:**
- Tool modules follow: `strix/tools/<name>/` with actions schema in XML
- Agent prompts: `*.jinja` files in `strix/prompts/`
- Tests: `test_*.py` in `tests/` mirroring source structure
- AGENTS.md documentation in root and all major subdirectories
