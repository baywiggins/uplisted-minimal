# Copilot prompt: Stage 14 — Baseline comparison, failure analysis, and frozen holdout

Implement only Stage 14. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md` if it exists, the product brief, the relevant canonical contracts, and this stage's evaluation requirements. Inspect the actual current code and previous check results before editing. Do not assume a previous stage is complete because a chat said so.

Start by listing the contracts this change relies on and the files you will touch. If a prerequisite stage is incomplete, report the exact missing interface/check and repair that prerequisite before dependent implementation. Keep the chosen architecture.

The stage specification follows verbatim:

## Stage 14 — Baseline comparison, failure analysis, and frozen holdout

**Files:** add reviewed regression cases under `evals/regression/`; create `docs/RESULTS.md`, `docs/FAILURE-ANALYSIS.md`; select redacted report artifacts. Holdout inputs/labels live in a separate evaluator workspace outside Copilot's tuning context.

**Consumes:** validated harness, real model, fixed evidence, fixed baseline, calibrated human/optional model judgments, and explicit evaluation-batch budget.

**Produces:** measured comparison, honest limitations, one reproducible failure → mitigation → independent regression chain, and clearly labeled holdout status.

- [ ] Freeze code/prompt/model/fixtures and budgets. Run baseline and agent on the same eligible tasks; include narrow requests and failures. Repeat stochastic cases five times from reset state if budget allows; if fewer, report the actual count.
- [ ] Populate metric numerators/denominators, unique scenarios/trials, outcome-specific latency, known/unknown cost, and harmful proposals/blocks/effects. Do not omit unsuccessful trials or overwrite their report with the rerun.
- [ ] Select an observed failure, reproduce it, explain its cause, change one responsible part, and add an independent regression. If no model failure was observed in the small sample, demonstrate an intentionally injected software fault labeled as such; do not invent an incident.
- [ ] Freeze improved configuration, run genuinely fresh owner/evaluator-held cases, and record their handling. Once inspected for tuning, those cases become regression; create replacement holdout. Report absence of holdout if it has not been created.
- [ ] Review critical deterministic failures separately from aggregate quality. Set any model-quality release threshold from a documented product requirement/baseline before the final evaluation; do not manufacture a favorable threshold afterward.

**Gate:** results files link real manifests and failed/passing trial IDs; denominators reconcile to selected cases; critical state/authority tests pass; rubric disagreements/unknown telemetry visible. A report of limitations is preferable to claiming broad reliability from a small suite.

**Interview focus:** The strongest story is why a particular metric caught a meaningful failure and how the fix changed measured behavior.

At completion, report:
- Implemented behavior and changed files.
- Exact commands executed and observed results; explicitly identify unrun checks.
- Which failure cases the tests exercise and what they do not prove.
- Any deviations or unresolved issues.
- A short explanation I can use in the interview.

Update `docs/BUILD-PROGRESS.md`. Inspect the diff and whitespace checks. Prepare a scoped checkpoint commit after passing checks and review; do not push or deploy. Stop before the next stage. Do not fill benchmark fields with invented numbers.


Learning checkpoint: read `learning/sections/05-evaluations.md` before implementation. After the stage gate, fill `learning/checkpoints/14.md` with actual code/test evidence, explain the change, ask two short teach-back questions, and stop. Track learning separately from implementation. Use `./scripts/with-tools.sh` for each terminal command.
