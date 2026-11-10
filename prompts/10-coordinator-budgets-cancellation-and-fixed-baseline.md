# Copilot stage 10

Read COPILOT-START.md, AGENTS.md, docs/08-microsoft-agent-framework.md and the mapped learning section/checkpoint first. Execute only this stage. Teach concepts before asking one optional understanding question at a time. Record actual results and stop.

## Stage 10 — Coordinator, budgets, cancellation, and fixed baseline

**Files:** create `agent/coordinator.py`, `agent/budget.py`, `agent/prompts.py`, `agent/baseline.py`; extend scripted gateway; `tests/integration/test_coordinator.py`, `test_budget.py`, `test_cancellation.py`, `test_baseline.py`, `test_run_ownership.py`.

**Consumes:** dispatcher, repositories, MAF runtime contract, exact limits/run states in contracts §6.

**Produces:** `Coordinator.run(ctx, request) -> RunOutcome`; `RunBudget.reserve_model(...)`, `reserve_tool(...)`, `record_usage(...)`, `check_deadline()`; `FixedWorkflow.run(ctx, request)`. Model reservations include helper and repair calls.

- [ ] Implement Coordinator as a lifecycle adapter around MAF Agent.run, with no handwritten model/tool iteration. Use the real framework with ScriptedChatClient. Test public middleware hooks and terminal exception propagation; never mock away Agent.run.
- [ ] Use scripted model turns to test read → tool → observation → final flow and an appropriate clarification. A model final message cannot create completion artifacts. Handle malformed/unknown calls and tool failures explicitly.
- [ ] Enforce one active run per case, serial tool execution, call-ID correspondence, per-run opaque provider continuation state, max attempts, deadline, and at most one repair. Test a helper consumes the last model allowance; further repair/coordinator calls are blocked.
- [ ] Cancellation sets a durable flag, halts further dispatch, and blocks late acceptance. Barrier tests cover cancel before dispatch, while provider in flight, and after one artifact committed. Retain successful earlier artifacts.
- [ ] Renew the 30-second DB lease every 5 seconds during async model/tool work. Lease loss stops dispatch and commits; expired-run reconciliation marks only expired owners interrupted without automatic paid replay. Usage/cost may be unknown. Disable SDK retries later; gateway protocol makes attempts visible now.
- [ ] Implement a fair fixed baseline supporting narrow task categories. It shares tools, helper settings and guardrails; do not fetch RentCast for photos-only. Unknown intent asks a bounded clarification.
- [ ] Write system instructions describing tools, untrusted data, factual limits, progress honesty, and clarification. Keep them versioned and hashed. Do not put grading labels or scenario-specific answers in prompts.

**Gate:** `uv run pytest -q tests/integration/test_maf_smoke.py tests/integration/test_coordinator.py tests/integration/test_budget.py tests/integration/test_cancellation.py tests/integration/test_baseline.py tests/integration/test_run_ownership.py`; all prior backend tests. Use fake clocks and event barriers, no long sleeps.

**Interview focus:** Explain where the agent has discretion, why serial execution is sufficient, how nested costs accumulate, and when a fixed workflow is preferable.
