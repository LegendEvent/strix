# AGENTS KNOWLEDGE BASE: RUNTIME

**Score:** 18
**Context:** strix/runtime

## OVERVIEW
Manages isolated execution environments using Docker containers and a FastAPI-based tool server for secure, distributed agent operations.

## WHERE TO LOOK
| Component | Location | Notes |
|-----------|----------|-------|
| Runtime Base | `runtime.py` | Abstract interfaces and SandboxInfo |
| Docker Logic | `docker_runtime.py` | Container lifecycle, networking, workspace sync |
| Tool Server | `tool_server.py` | FastAPI/Uvicorn entry for sandboxed execution |

## CONVENTIONS
- **Sandboxed Execution**: Tools MUST run via `tool_server` inside Docker; host access is forbidden.
- **Process Isolation**: Each agent ID mapped to dedicated `multiprocessing.Process` via queues.
- **Dynamic Ports**: Assign random available ports for `TOOL_SERVER_PORT` and `CAIDO_PORT`.
- **Workspace Sharing**: All agents in a scan tree share `/workspace` and proxy history.
- **Tree Isolation**: Group agents by `scan_id` into shared Docker containers.

## ANTI-PATTERNS
- **No Host Tool Access**: Never execute security tools directly on the host machine.
- **No Static Ports**: Never hardcode port numbers; use `SandboxInfo` assignments.
- **No Manual Cleanup**: Avoid manual `docker rm/stop`; use `destroy_sandbox` methods.
- **No Shared Memory**: Communicating via queues only; no direct object sharing between processes.
