# STRIX INTERFACE KNOWLEDGE BASE

**Generated:** 2026-01-07 23:30:00
**Commit:** c7d1b0c

## OVERVIEW
Presentation layer managing CLI parsing, environment validation, and the Textual-based TUI.

## WHERE TO LOOK
| Component | Location | Notes |
|-----------|----------|-------|
| Textual TUI | `tui.py` | Main `StrixTUIApp` and splash screen. |
| Tool Renderer Registry | `tool_components/registry.py` | `@register_tool_renderer` decorator and lookup. |
| Rich Console | `cli.py` | `run_cli()` for non-interactive output via `rich.live`. |
| Target Resolver | `utils.py` | `infer_target_type()` and workspace pathing. |
| Copilot Auth | `main.py` | `handle_auth_login/logout()` handlers. |
| TUI Styles | `assets/tui_styles.tcss` | Centralized styling for all widgets. |

## CONVENTIONS
- **TUI Architecture**: Textual-based. Define widgets in `compose()`, style in `.tcss`.
- **Renderer Registration**: Inherit `BaseToolRenderer`, use `@register_tool_renderer`.
- **Dynamic Updates**: Use `textual.reactive` for real-time widget state changes.
- **Rich Integration**: Use `rich` for CLI-only output and TUI markup rendering.
- **Workspace Logic**: Multi-target scans must use `assign_workspace_subdirs`.

## ANTI-PATTERNS
- **Logic Leakage**: Keep agent decision/execution logic out of interface layer.
- **Standard I/O**: NEVER use `print()` or `input()`. Use `Rich` or `Textual` counterparts.
- **Manual CSS**: Avoid inline `styles=`. Use TCSS classes for consistency.
- **Hardcoded Markup**: Use `BaseToolRenderer.escape_markup()` for untrusted tool outputs.
