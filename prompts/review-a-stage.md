# Independent stage review prompt

Review the current stage's diff against `docs/01-product-brief.md`, `docs/02-contracts.md`, the stage in `docs/03-build-plan.md`, and the evaluation rules in 04. Treat claimed test success as unverified until you inspect the actual output or run the relevant check. Do not implement another feature.

Look for concrete failures in scope/authority, current dependency and destination-head checks, idempotency, cancellation, provider-mode labeling, shared nested budgets, fact provenance, sensitive-data projections, and independent evaluation. Check the browser behavior where the stage affects it. A disabled UI control is not a backend guarantee.

Report actionable findings with file/line, trigger, actual versus required behavior, severity, and a reproducing test. Separate bugs from optional improvements. Do not praise a large diff or a high test count as proof. If no issue is found, state what you inspected and the remaining verification limits. Do not approve skipped or unrun critical checks.
