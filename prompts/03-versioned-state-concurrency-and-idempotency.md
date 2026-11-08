# Copilot prompt: Stage 03 — Versioned state, concurrency, and idempotency

Implement only Stage 03. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md` if it exists, the product brief, the relevant canonical contracts, and this stage's evaluation requirements. Inspect the actual current code and previous check results before editing. Do not assume a previous stage is complete because a chat said so.

Start by listing the contracts this change relies on and the files you will touch. If a prerequisite stage is incomplete, report the exact missing interface/check and repair that prerequisite before dependent implementation. Keep the chosen architecture.

The stage specification follows verbatim:

## Stage 03 — Versioned state, concurrency, and idempotency

**Files:** create `state/db.py`, `state/repository.py`, `cli.py`; `tests/integration/test_repository.py`, `test_idempotency.py`, `test_freshness.py`; define minimal run/event records needed by later stages.

**Consumes:** Stage 02 models and hashes. Use all repository signatures in contracts §3.

**Produces:** v1 SQLite schema; repository methods; `is_current(ref, case_id, clock) -> FreshnessResult`; idempotent `init-demo`; immutable property/artifact storage and target-head acceptance gate.

- [ ] Build short parameterized transactions, enable foreign keys and WAL, and store a schema version. Use an injected clock and temporary database in tests.
- [ ] Test and implement case-scoped retrieval; unknown/cross-case refs have equivalent safe results. Seed Case B with a unique private marker and assert it does not leak.
- [ ] Implement monotonic property revisions and per-kind artifact heads. A property edit invalidates all derived artifacts; artifact edits invalidate descendants through exact refs. Test dependency cycles are rejected or impossible by construction.
- [ ] Implement `accept_artifact` atomic checks for property/dependencies/target head and active, uncancelled run. Human edits use a separately authorized path through the same validation/version checks; they do not need an active agent run. Test stale source, changed destination head, and cancellation using controlled transaction ordering.
- [ ] Implement operation records before dispatch and atomic local completion receipts. Same key/same hash returns original result, different input or actor conflicts, pending returns pending. Test at most one effect from concurrent duplicate requests.
- [ ] Implement `init-demo` without overwriting existing state, and explicit local reset. Restart marks previously active work interrupted; it does not replay calls.

**Gate:** `uv run pytest -q tests/integration/test_repository.py tests/integration/test_idempotency.py tests/integration/test_freshness.py`; lint/type checks. Use two repository connections for race tests, not only mocks.

**Interview focus:** Be able to draw the transaction boundary and explain why an idempotency key alone does not solve stale writes or remote billing.

At completion, report:
- Implemented behavior and changed files.
- Exact commands executed and observed results; explicitly identify unrun checks.
- Which failure cases the tests exercise and what they do not prove.
- Any deviations or unresolved issues.
- A short explanation I can use in the interview.

Update `docs/BUILD-PROGRESS.md`. Inspect the diff and whitespace checks. Prepare a scoped checkpoint commit after passing checks and review; do not push or deploy. Stop before the next stage. Do not fill benchmark fields with invented numbers.


Learning checkpoint: read `learning/sections/01-foundations.md` before implementation. After the stage gate, fill `learning/checkpoints/03.md` with actual code/test evidence, explain the change, ask two short teach-back questions, and stop. Track learning separately from implementation. Use `./scripts/with-tools.sh` for each terminal command.
