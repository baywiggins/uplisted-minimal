# Copilot stage 14

Read COPILOT-START.md, AGENTS.md, docs/08-microsoft-agent-framework.md and the mapped learning section/checkpoint first. Execute only this stage. Teach concepts before asking one optional understanding question at a time. Record actual results and stop.

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
