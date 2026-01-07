# PROJECT KNOWLEDGE BASE: tests

## OVERVIEW
Comprehensive test suite mirroring the `strix/` structure to ensure robust agent coordination and tool execution.

## STRUCTURE
```
./
├── agents/      # Agent logic and tree coordination tests
├── interface/   # CLI and TUI component verification
├── llm/         # Provider mocks and token management tests
├── runtime/     # Docker sandbox and process management tests
├── telemetry/   # Logging and metrics verification
├── tools/       # 14 modular toolset functional tests
└── conftest.py  # Global fixtures and pytest configuration
```

## WHERE TO LOOK
| Target | Location | Notes |
|--------|----------|-------|
| New Tests | `tests/` | Primary location for all new test development |
| Legacy Tests | `strix/tests/` | Older tests being migrated to root suite |
| Mocking | `conftest.py` | Shared `mocker` and `respx` configurations |
| Coverage | `htmlcov/` | Reports generated via `make test-cov` |

## CONVENTIONS
- **Async**: `pytest-asyncio` with `asyncio_mode = "auto"`
- **Mocking**: `mocker` (pytest-mock) and `respx` for network isolation
- **Parametrization**: Extensive use of `@pytest.mark.parametrize`
- **Fixtures**: Layered `conftest.py` for scoped dependency injection
- **Dual Locations**: `tests/` (primary) and `strix/tests/` (legacy)

## ANTI-PATTERNS
- **Implicit types**: Omit type annotations in test functions
- **Sync in async**: Blocking calls inside async test logic
- **Fixture pollution**: Broad-scoped fixtures in module files
- **Direct network**: Actual HTTP calls (must use `respx` or `mocker`)
