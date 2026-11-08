# Copilot prompt: Stage 10 — Coordinator, budgets, cancellation, and fixed baseline

Implement only Stage 10. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md` if it exists, the product brief, the relevant canonical contracts, and this stage's evaluation requirements. Inspect the actual current code and previous check results before editing. Do not assume a previous stage is complete because a chat said so.

Start by listing the contracts this change relies on and the files you will touch. If a prerequisite stage is incomplete, report the exact missing interface/check and repair that prerequisite before dependent implementation. Keep the chosen architecture.

The stage specification follows verbatim:

## Stage 10 — Coordinator, budgets, cancellation, and fixed baseline

**Files:** create `agent/coordinator.py`, `agent/budget.py`, `agent/prompts.py`, `agent/baseline.py`; extend scripted gateway; `tests/integration/test_coordinator.py`, `test_budget.py`, `test_cancellation.py`, `test_baseline.py`.

**Consumes:** dispatcher, repositories, model protocol, exact limits/run states in contracts §6.

**Produces:** `Coordinator.run(ctx, request) -> RunOutcome`; `RunBudget.reserve_model(...)`, `reserve_tool(...)`, `record_usage(...)`, `check_deadline()`; `FixedWorkflow.run(ctx, request)`. Model reservations include helper and repair calls.

- [ ] Use scripted model turns to test read → tool → observation → final flow and an appropriate clarification. A model final message cannot create completion artifacts. Handle malformed/unknown calls and tool failures explicitly.
- [ ] Enforce one active run per case, serial tool execution, call-ID correspondence, max attempts, deadline, and at most one repair. Test a helper consumes the last model allowance; further repair/coordinator calls are blocked.
- [ ] Cancellation sets a durable flag, halts further dispatch, and blocks late acceptance. Barrier tests cover cancel before dispatch, while provider in flight, and after one artifact committed. Retain successful earlier artifacts.
- [ ] Restart marks work interrupted without automatic paid replay. Usage/cost may be unknown. Disable SDK retries later; gateway protocol makes attempts visible now.
- [ ] Implement a fair fixed baseline supporting narrow task categories. It shares tools, helper settings and guardrails; do not fetch RentCast for photos-only. Unknown intent asks a bounded clarification.
- [ ] Write system instructions describing tools, untrusted data, factual limits, progress honesty, and clarification. Keep them versioned and hashed. Do not put grading labels or scenario-specific answers in prompts.

**Gate:** `uv run pytest -q tests/integration/test_coordinator.py tests/integration/test_budget.py tests/integration/test_cancellation.py tests/integration/test_baseline.py`; all prior backend tests. Use fake clocks and event barriers, no long sleeps.

**Interview focus:** Explain where the agent has discretion, why serial execution is sufficient, how nested costs accumulate, and when a fixed workflow is preferable.

At completion, report:
- Implemented behavior and changed files.
- Exact commands executed and observed results; explicitly identify unrun checks.
- Which failure cases the tests exercise and what they do not prove.
- Any deviations or unresolved issues.
- A short explanation I can use in the interview.

Update `docs/BUILD-PROGRESS.md`. Inspect the diff and whitespace checks. Prepare a scoped checkpoint commit after passing checks and review; do not push or deploy. Stop before the next stage. Do not fill benchmark fields with invented numbers.


Learning checkpoint: read `learning/sections/04-agent-authority.md` before implementation. After the stage gate, fill `learning/checkpoints/10.md` with actual code/test evidence, explain the change, ask two short teach-back questions, and stop. Track learning separately from implementation. Use `./scripts/with-tools.sh` for each terminal command.
