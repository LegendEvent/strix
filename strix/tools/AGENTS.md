# AGENTS KNOWLEDGE BASE: MODULAR TOOLS

**Generated:** 2026-01-07
**Score:** 157 (Highest complexity - 35 Python files, 26 tool modules)
**Context:** strix/tools

## OVERVIEW
12 modular toolsets (26 tools) providing agents with environment interaction, reasoning, and reporting via XML actions.

## STRUCTURE
Tools in `strix/tools/<name>/`: `__init__.py` entry, `<name>_actions.py` logic, `<name>_actions_schema.xml` schema.

- **agents_graph**: Multi-agent orchestration (create, message, wait)
- **browser**: Playwright-based web testing (auth, cookies, multi-tab)
- **file_edit**: Safe filesystem modifications (read, apply_edit)
- **finish**: Root agent termination and final report trigger
- **notes**: Structured knowledge/attack documentation storage
- **proxy**: Caido-integrated HTTP traffic manipulation (HTTPQL)
- **python**: Isolated code execution for exploit development
- **reporting**: Formal vulnerability discovery documentation
- **terminal**: Persistent tmux-based interactive shell access
- **thinking**: Structured reasoning/chain-of-thought scratchpad
- **todo**: Task tracking and session progress management
- **web_search**: Exa AI powered external reconnaissance

## WHERE TO LOOK
| Component | Location | Key Actions/Notes |
|-----------|----------|-------------------|
| Registry | `registry.py` | `@register_tool` decorator, tool discovery |
| Base Class | `base.py` | `BaseTool` & `Action` interface definitions |
| Terminal | `terminal/` | `terminal_execute` (persistent state) |
| Proxy | `proxy/` | `repeat_request`, `list_sitemap` |
| Reporting | `reporting/` | `create_vulnerability_report` (mandatory) |

## CONVENTIONS
- **XML Invocation**: `<function name="X"><param=K>V</param></function>`
- **Registration**: Mandatory `@register_tool` in `*_actions.py` modules
- **Persistence**: Terminal (tmux) and Browser (Playwright) maintain state
- **Schemas**: Auto-loaded from `*_actions_schema.xml` via `registry.py`
- **Async**: All tool actions MUST be `async def`

## ANTI-PATTERNS
- **No Blocking**: NEVER use `time.sleep`; use `asyncio.sleep`
- **Terminal**: NEVER kill on timeout; commands run in background
- **Finish**: NEVER exit with active sub-agents or pending reports
- **Reporting**: DO NOT use for status; only for validated vulnerabilities
- **State**: Tools MUST NOT store state in Python objects; use `notes`
