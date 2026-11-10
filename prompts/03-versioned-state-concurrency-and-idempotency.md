# Copilot stage 03

Read COPILOT-START.md, AGENTS.md, docs/08-microsoft-agent-framework.md and the mapped learning section/checkpoint first. Execute only this stage. Teach concepts before asking one optional understanding question at a time. Record actual results and stop.

## Stage 03 — Versioned state, concurrency, and idempotency

**Files:** create `state/db.py`, `state/repository.py`, `state/run_ownership.py`, `state/migrations/001_initial.sql`, `cli.py`; `tests/integration/test_repository.py`, `test_idempotency.py`, `test_freshness.py`; define minimal run/event records needed by later stages.

**Consumes:** Stage 02 models and hashes. Use all repository signatures in contracts §3.

**Produces:** v1 PostgreSQL schema; repository methods; `is_current(ref, case_id, clock) -> FreshnessResult`; idempotent `init-demo`; immutable property/artifact storage and target-head acceptance gate.

- [ ] Build short parameterized PostgreSQL transactions and numbered migrations with foreign keys and scoped unique indexes. Use psycopg 3 AsyncConnectionPool and async runtime repository methods with a consistent lock order; keep arithmetic/hashing synchronous. Test against a disposable PostgreSQL database/schema, with cleanup restricted to test namespaces; use an injected clock. Add run owner/fence/lease fields and transactional single-active-run admission from contracts §10.
- [ ] Test and implement case-scoped retrieval; unknown/cross-case refs have equivalent safe results. Seed Case B with a unique private marker and assert it does not leak.
- [ ] Implement monotonic property revisions and per-kind artifact heads. A property edit invalidates all derived artifacts; artifact edits invalidate descendants through exact refs. Test dependency cycles are rejected or impossible by construction.
- [ ] Implement `accept_artifact` atomic checks for property/dependencies/target head and active, uncancelled run with current unexpired owner/fence. Human edits use a separately authorized path through the same validation/version checks; they do not need an active agent run. Test stale source, changed destination head, and cancellation using controlled transaction ordering.
- [ ] Implement operation records before dispatch and atomic local completion receipts. Same key/same hash returns original result, different input or actor conflicts, pending returns pending. Test at most one effect from concurrent duplicate requests.
- [ ] Implement `init-demo` without overwriting existing state, and explicit local reset. Recovery interrupts only expired leases, not every active row. Test that a second process cannot interrupt a healthy owner; it does not replay calls.

**Gate:** `uv run pytest -q tests/integration/test_repository.py tests/integration/test_idempotency.py tests/integration/test_freshness.py`; lint/type checks. Use two PostgreSQL repository connections for race tests, not only mocks. Keep fixture/model tests externally offline.

**Interview focus:** Be able to draw the transaction boundary and explain why an idempotency key alone does not solve stale writes or remote billing.
