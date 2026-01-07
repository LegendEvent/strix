# TELEMETRY KNOWLEDGE BASE
**Score:** 10 (Logging/metrics domain)

## OVERVIEW
Central telemetry hub managing execution tracking, LLM metrics aggregation, and security report generation for Strix agents.

## WHERE TO LOOK
| Component | Location | Notes |
|-----------|----------|-------|
| Tracer Singleton | `strix/telemetry/tracer.py` | Main state via `get_global_tracer()` |
| Run Data | `Tracer.get_run_dir()` | Persistence in `strix_runs/` session folders |
| Tool Lifecycle | `Tracer.log_tool_execution_*` | Execution start/update hooks |
| LLM Stats | `Tracer.get_total_llm_stats()` | Global token/cost aggregation |

## CONVENTIONS
- **Execution Lifecycle**: Wrap tools in `log_tool_execution_start/update` to capture duration and status.
- **Data Persistence**: All session data, vulnerabilities, and reports persisted in `strix_runs/`.
- **Time Standard**: Mandatory UTC ISO 8601 timestamps for all events.
- **Metrics Aggregation**: Aggregates LLM usage (tokens, cost) from all active agent instances.
- **Real-time Hooks**: Use `vulnerability_found_callback` for immediate UI/TUI notification on findings.
- **Vulnerability Storage**: Saved in `vulnerabilities/*.md` with centralized `vulnerabilities.csv` index.
- **Report Generation**: `save_run_data()` produces markdown and CSV reports upon finding discovery or scan completion.
- **Tracer Singleton**: Access global state via `get_global_tracer()` to ensure cross-process telemetry consistency.
