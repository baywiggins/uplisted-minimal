# Copilot prompt: Stage 12 — Independent evaluation harness and grader self-tests

Implement only Stage 12. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md` if it exists, the product brief, the relevant canonical contracts, and this stage's evaluation requirements. Inspect the actual current code and previous check results before editing. Do not assume a previous stage is complete because a chat said so.

Start by listing the contracts this change relies on and the files you will touch. If a prerequisite stage is incomplete, report the exact missing interface/check and repair that prerequisite before dependent implementation. Keep the chosen architecture.

The stage specification follows verbatim:

## Stage 12 — Independent evaluation harness and grader self-tests

**Files:** create `evals/__main__.py`, `schema.py`, `runner.py`, `graders.py`, `report.py`; `tests/evals/test_scenarios.py`, `test_harness.py`, `test_graders.py`; scenario builder/driver modules under `src/uplisted/evals/cases/`; `docs/GRADER-CALIBRATION.md`.

**Consumes:** all 30 public scenario specifications, the fixed baseline, scripted coordinator, outcome snapshots, and the complete evaluation plan.

**Produces:** validated CASE_REGISTRY, typed executable cases, CLI commands, resettable isolated trials, independent deterministic graders, redacted reports, and optional human scoring forms.

- [ ] Validate JSONL IDs/families/drivers and implement a reviewed builder for every ID. Service, agent and browser cases remain separately counted. Browser cases link actual Playwright output; missing output is not a pass.
- [ ] Build each trial in a new temporary database with fixed clock/fixtures, clean budgets/cache, and hidden evaluator labels. Use barriers for the specified races and injected transports for failures. The agent receives no `expected`, `grading`, or scenario ID shortcuts.
- [ ] Grade persisted outcomes and trace independently. Implement separate arithmetic/template/ref/approval assertions; do not call production validation to decide success.
- [ ] Mutation-test graders: valid counterpart passes; corrupt price/unit/room ref/citation value/dependency/approval fails. Include missing-output, grader-exception, unknown-ID, duplicate-ID, zero-selection, missing-family and offline-network failures. Use defined nonzero exit codes.
- [ ] Implement coverage manifest, trusted external case-registry loading, browser-result import, human score import, and finalize protocol from evaluation plan. Pending required semantic scores are incomplete, never passing. Write manifests/trials/summaries/reports with real counts, raw-versus-repaired outputs, exception records, mode labels, and unknown costs. A scripted run is labeled application testing, not model performance.
- [ ] Add human semantic scoring form and 24-output calibration specification. A judge model is optional; if added later it cannot override deterministic failures and its spend is separate.

**Gate:** `uv run pytest -q tests/evals`; run `evals validate`, service/scripted CLI runs from evaluation plan. Import required human scores before finalizing agent trials. Inspect one deliberately failing report and one pending-score report and verify they are nonzero/incomplete rather than green. All expected public registry cases must be implemented; do not silently skip hard ones.

**Interview focus:** A valid evaluator is itself a tested system. Explain why final database state, trajectory, and semantic quality need different graders.

At completion, report:
- Implemented behavior and changed files.
- Exact commands executed and observed results; explicitly identify unrun checks.
- Which failure cases the tests exercise and what they do not prove.
- Any deviations or unresolved issues.
- A short explanation I can use in the interview.

Update `docs/BUILD-PROGRESS.md`. Inspect the diff and whitespace checks. Prepare a scoped checkpoint commit after passing checks and review; do not push or deploy. Stop before the next stage. Do not fill benchmark fields with invented numbers.


Learning checkpoint: read `learning/sections/05-evaluations.md` before implementation. After the stage gate, fill `learning/checkpoints/12.md` with actual code/test evidence, explain the change, ask two short teach-back questions, and stop. Track learning separately from implementation. Use `./scripts/with-tools.sh` for each terminal command.
