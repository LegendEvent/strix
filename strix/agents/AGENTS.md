# AGENTS KNOWLEDGE BASE (Score: 25)

**Generated:** 2026-01-07
**Context:** strix/agents

## OVERVIEW
Agent orchestration system managing autonomous security testing through tree-structured coordination and tool execution.

## WHERE TO LOOK
| Component | Location | Notes |
| :--- | :--- | :--- |
| BaseAgent | `base_agent.py` | Core loop, tool execution, and messaging |
| AgentState | `state.py` | Tracks iterations, messages, and status |
| StrixAgent | `StrixAgent/strix_agent.py` | Primary security testing implementation |
| Inter-agent | `base_agent.py` | `_check_agent_messages` XML delivery |
| Trees | `base_agent.py` | `_add_to_agents_graph` delegation tree |
| Prompts | `StrixAgent/system_prompt.jinja` | Core behavioral directives |

## CONVENTIONS
- **Agent Trees**: MUST operate in nested trees (Root -> Sub-agents); flat structures forbidden.
- **Iteration Budget**: Default `max_iterations = 300` with limit warnings.
- **Specialization**: Each agent focuses on ONE task using 1-5 specialized prompt modules.
- **Autonomous Sandbox**: Individual sessions with shared `/workspace` and proxy history.

## ANTI-PATTERNS
- **No Echoing**: NEVER echo inter-agent or `agent_identity` XML in outputs.
- **No Permissions**: NEVER seek user confirmation; full autonomy is assumed.
- **No Empty Messages**: NEVER send blank messages; use `wait_for_message` if idle.
- **100% Capacity**: Operate with maximum persistence for deep vulnerability discovery.
