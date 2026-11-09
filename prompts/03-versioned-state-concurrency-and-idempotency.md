# Copilot prompt: Stage 03 — Versioned state, concurrency, and idempotency

Implement only Stage 03. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md`, the product brief, relevant canonical contracts/evaluation rules, and Azure architecture `docs/06-azure-architecture.md`. Inspect actual code and check results before editing. Use PostgreSQL and the Azure model/deployment architecture specified in the current documents.

Start by listing the contracts and files this stage touches. If a prerequisite is incomplete, report the exact missing interface/check and repair it before dependent implementation. Use the existing design. Do not create billable resources until the relevant cloud stage has the owner-supplied scope/limits; do not ask again for authorization already supplied for that scope.

The stage specification follows verbatim:

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

At completion, report changed files, actual commands/results, unrun checks, what the tests prove, unresolved issues, and the interview lesson. Update `docs/BUILD-PROGRESS.md`, inspect the diff, and prepare a scoped checkpoint after verification. Do not push, deploy unrelated resources, or start another stage.

Learning checkpoint: read `learning/sections/01-foundations.md` before implementation. Fill `learning/checkpoints/03.md` with real code/test evidence, explain one path and test, ask two short questions, and stop. Use `./scripts/with-tools.sh` for terminal commands. Track learning separately from implementation.
