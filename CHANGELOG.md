# PR: Add Conditional Trigger support

## Summary
- Implements full Conditional Trigger API support and unit tests so this repository is PR-ready.

## What I changed
- Added: `src/dhanhq/_conditional_trigger.py` (new ConditionalTrigger wrapper)
- Updated: `src/dhanhq/__init__.py` (exported ConditionalTrigger)
- Updated: `src/dhanhq/dhanhq.py` (integrated ConditionalTrigger into composite client)
- Minor fixes to keep unit tests green:
  - `src/dhanhq/_historical_data.py` (minute interval validation)
  - `src/dhanhq/_super_order.py` (validation message alignment)
  - `src/dhanhq/_trader_control.py` (`kill_switch` request shape)
- Added tests: `tests/unit/test_dhanhq_conditional_trigger.py`

## Tests
- Unit tests: 70 passed, 1 warning (local run)
- Integration tests: failing locally (11 failing) because they require valid API credentials / environment. These should pass in CI or a developer environment with credentials configured.

## How to run unit tests locally
```powershell
$env:PYTHONPATH = "e:\\DhanHQ-py\\src"
python -m pytest tests/unit -q -o addopts=
```

## Branch
- Local branch: `feature/conditional-trigger` (committed locally). Push and open PR from your machine or CI since this environment could not push due to remote permissions.

## Pending items
- Push branch and open PR
- Address any additional reviewer comments (I applied conservative fixes; please share specific reviewer guidance if you'd like more changes)
- Re-run integration tests in CI or a credentials-enabled environment

## Suggested PR description (copy into GitHub PR body)

This PR adds support for the Conditional Trigger API and includes unit tests.

Key points:
- Adds `ConditionalTrigger` wrapper with methods to place, modify, delete, get-by-id, and list conditional orders.
- Integrates the wrapper into the `dhanhq` composite client and exports it from the package.
- Adds unit tests that mock HTTP client calls to verify correct endpoints and methods.
- Makes small, targeted fixes to existing modules so the unit test suite is green.

Notes:
- Unit tests pass locally (70 passed, 1 warning). Integration tests require real API credentials and fail locally — please run integration tests in CI or a developer machine with credentials.
- I could not push the local `feature/conditional-trigger` branch from this environment due to remote permission denied; please push and open the PR from your account or allow remote access.

If you'd like, I can also prepare a compact changelog entry or squash commits before you push.
