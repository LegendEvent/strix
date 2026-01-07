# LLM INTEGRATION (Score: 27)

## OVERVIEW
Unified multi-provider LLM interface with built-in rate limiting, context-aware memory compression, and specialized GitHub Copilot authentication.

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Main Client | `llm.py` | Litellm wrapper; handles vision, reasoning, and usage tracking |
| Copilot Auth | `copilot_auth.py` | Device-flow OAuth; CI token handling (`STRIX_COPILOT_ACCESS`) |
| Rate Limiting | `request_queue.py` | Global singleton; enforces `LLM_RATE_LIMIT_DELAY` (4s) |
| History Mgmt | `memory_compressor.py` | 100k token limit; preserves tech details in summaries |
| Tool Parsing | `utils.py` | Extracts XML `<function name="...">` from completions |
| Configuration | `config.py` | `LLMConfig` and `RequestStats` for cost/token tracking |

## CONVENTIONS
- **XML Tooling**: Use `LLMResponse.tool_invocations` for tool execution parsing.
- **Model Detection**: Regex-based detection for `reasoning_effort` (o1/o3) and `stop` suppression.
- **Copilot Auth**: Automatic token refresh on 401/403; CI overrides via `STRIX_COPILOT_ACCESS`.
- **Memory Mgmt**: Compresses at 100k tokens; preserves 15 recent messages and max 3 images.
- **Vision Support**: Non-vision models (e.g., o1-mini) have images replaced with text descriptions.
- **Error Handling**: Litellm errors unified into `LLMRequestFailedError` with original details.
- **Concurrency**: Singleton request queue enforces rate limits and max concurrent calls.

## ANTI-PATTERNS
- **Queue Bypass**: Calling `litellm.completion` directly (skips rate limits/metrics/errors).
- **Manual Auth**: Implementing custom OAuth logic; use `force_refresh_copilot_access_token()`.
- **Hardcoded Flags**: Hardcoding model features instead of updating regex lists in `llm.py`.
- **Stat Neglect**: Ignoring `self.usage_stats` leading to unmonitored costs/token usage.
- **Raw Large Logs**: Passing verbose logs without using `MemoryCompressor` for summarization.
