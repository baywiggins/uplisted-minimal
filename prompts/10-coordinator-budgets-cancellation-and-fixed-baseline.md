# Copilot prompt: Stage 10 — Coordinator, budgets, cancellation, and fixed baseline

Implement only Stage 10. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md`, the product brief, relevant canonical contracts/evaluation rules, and Azure architecture `docs/06-azure-architecture.md`. Inspect actual code and check results before editing. Use PostgreSQL and the Azure model/deployment architecture specified in the current documents.

Start by listing the contracts and files this stage touches. If a prerequisite is incomplete, report the exact missing interface/check and repair it before dependent implementation. Use the existing design. Do not create billable resources until the relevant cloud stage has the owner-supplied scope/limits; do not ask again for authorization already supplied for that scope.

The stage specification follows verbatim:

## Stage 10 — Coordinator, budgets, cancellation, and fixed baseline

**Files:** create `agent/coordinator.py`, `agent/budget.py`, `agent/prompts.py`, `agent/baseline.py`; extend scripted gateway; `tests/integration/test_coordinator.py`, `test_budget.py`, `test_cancellation.py`, `test_baseline.py`, `test_run_ownership.py`.

**Consumes:** dispatcher, repositories, model protocol, exact limits/run states in contracts §6.

**Produces:** `Coordinator.run(ctx, request) -> RunOutcome`; `RunBudget.reserve_model(...)`, `reserve_tool(...)`, `record_usage(...)`, `check_deadline()`; `FixedWorkflow.run(ctx, request)`. Model reservations include helper and repair calls.

- [ ] Use scripted model turns to test read → tool → observation → final flow and an appropriate clarification. A model final message cannot create completion artifacts. Handle malformed/unknown calls and tool failures explicitly.
- [ ] Enforce one active run per case, serial tool execution, call-ID correspondence, per-run opaque provider continuation state, max attempts, deadline, and at most one repair. Test a helper consumes the last model allowance; further repair/coordinator calls are blocked.
- [ ] Cancellation sets a durable flag, halts further dispatch, and blocks late acceptance. Barrier tests cover cancel before dispatch, while provider in flight, and after one artifact committed. Retain successful earlier artifacts.
- [ ] Renew the 30-second DB lease every 5 seconds during async model/tool work. Lease loss stops dispatch and commits; expired-run reconciliation marks only expired owners interrupted without automatic paid replay. Usage/cost may be unknown. Disable SDK retries later; gateway protocol makes attempts visible now.
- [ ] Implement a fair fixed baseline supporting narrow task categories. It shares tools, helper settings and guardrails; do not fetch RentCast for photos-only. Unknown intent asks a bounded clarification.
- [ ] Write system instructions describing tools, untrusted data, factual limits, progress honesty, and clarification. Keep them versioned and hashed. Do not put grading labels or scenario-specific answers in prompts.

**Gate:** `uv run pytest -q tests/integration/test_coordinator.py tests/integration/test_budget.py tests/integration/test_cancellation.py tests/integration/test_baseline.py tests/integration/test_run_ownership.py`; all prior backend tests. Use fake clocks and event barriers, no long sleeps.

**Interview focus:** Explain where the agent has discretion, why serial execution is sufficient, how nested costs accumulate, and when a fixed workflow is preferable.

At completion, report changed files, actual commands/results, unrun checks, what the tests prove, unresolved issues, and the interview lesson. Update `docs/BUILD-PROGRESS.md`, inspect the diff, and prepare a scoped checkpoint after verification. Do not push, deploy unrelated resources, or start another stage.

Learning checkpoint: read `learning/sections/04-agent-authority.md` before implementation. Fill `learning/checkpoints/10.md` with real code/test evidence, explain one path and test, ask two short questions, and stop. Use `./scripts/with-tools.sh` for terminal commands. Track learning separately from implementation.
