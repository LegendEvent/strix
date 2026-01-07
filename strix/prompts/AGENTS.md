# PROMPT MODULES KNOWLEDGE BASE

## OVERVIEW
Central repository for Jinja2 system prompt templates and specialized modules defining agent personas and orchestration logic via dynamic XML-structured knowledge injection.

## STRUCTURE
```
strix/prompts/
├── cloud/, frameworks/, protocols/ # Domain-specific testing
├── coordination/                   # Root agent logic
├── reconnaissance/, scan_modes/    # Early-stage & depth config
├── vulnerabilities/                # Core exploit methodologies
└── technologies/, custom/          # 3rd-party & community modules
```

## WHERE TO LOOK
| Component | Location | Notes |
|-----------|----------|-------|
| Root Agent | `coordination/root_agent.jinja` | Coordination only; NO testing/reporting |
| Vuln Modules | `vulnerabilities/*.jinja` | Vector-specific methodologies |
| Stack Modules | `frameworks/`, `protocols/` | Technology-aware testing strategies |
| Base Logic | `../agents/StrixAgent/system_prompt.jinja` | Foundation for module injection |

## CONVENTIONS
- **XML Structuring**: Mandatory `<function name="...">` or `<knowledge>` tags for LLM parsability.
- **Specialization Limit**: 1-3 modules per agent; strict maximum of 5 to preserve focus.
- **Dynamic Injection**: Modules loaded at runtime based on discovered target technology stack.
- **Imperative Directives**: Use **ALWAYS/NEVER/DO NOT** for critical behavioral constraints.

## ANTI-PATTERNS
- **Message Echoing**: NEVER include `inter_agent_message` or identity XML in agent outputs.
- **Generic Agents**: DO NOT use >5 modules; spawn specialized sub-agents instead.
- **Root Testing**: `root_agent.jinja` FORBIDDEN from executing tests or writing technical reports.
- **Manual Loops**: NEVER iterate payloads manually in browser; use Python/Terminal tools.
