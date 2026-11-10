# Copilot stage 12

Read COPILOT-START.md, AGENTS.md, docs/08-microsoft-agent-framework.md and the mapped learning section/checkpoint first. Execute only this stage. Teach concepts before asking one optional understanding question at a time. Record actual results and stop.

## Stage 12 — Independent evaluation harness and grader self-tests

**Files:** create `evals/__main__.py`, `schema.py`, `runner.py`, `graders.py`, `report.py`; `tests/evals/test_scenarios.py`, `test_harness.py`, `test_graders.py`; scenario builder/driver modules under `src/uplisted/evals/cases/`; `docs/GRADER-CALIBRATION.md`.

**Consumes:** all 30 public scenario specifications, the fixed baseline, scripted MAF agent, outcome snapshots, and the complete evaluation plan.

**Produces:** validated CASE_REGISTRY, typed executable cases, CLI commands, resettable isolated trials, independent deterministic graders, redacted reports, and optional human scoring forms.

- [ ] Validate JSONL IDs/families/drivers and implement a reviewed builder for every ID. Service, agent and browser cases remain separately counted. Browser cases link actual Playwright output; missing output is not a pass.
- [ ] Build each trial in a new disposable PostgreSQL test database/schema with fixed clock/fixtures, clean budgets/cache, and hidden evaluator labels. Use barriers for the specified races and injected transports for failures. The agent receives no `expected`, `grading`, or scenario ID shortcuts.
- [ ] Grade persisted outcomes and trace independently. Implement separate arithmetic/template/ref/approval assertions; do not call production validation to decide success.
- [ ] Mutation-test graders: valid counterpart passes; corrupt price/unit/room ref/citation value/dependency/approval fails. Include missing-output, grader-exception, unknown-ID, duplicate-ID, zero-selection, missing-family and offline-network failures. Use defined nonzero exit codes.
- [ ] Implement coverage manifest, trusted external case-registry loading, browser-result import, human score import, and finalize protocol from evaluation plan. Pending required semantic scores are incomplete, never passing. Write manifests/trials/summaries/reports with real counts, raw-versus-repaired outputs, exception records, mode labels, and unknown costs. A scripted run is labeled application testing, not model performance.
- [ ] Add human semantic scoring form and 24-output calibration specification. A judge model is optional; if added later it cannot override deterministic failures and its spend is separate.

**Gate:** `uv run pytest -q tests/evals`; run `evals validate`, service/scripted CLI runs from evaluation plan. Import required human scores before finalizing agent trials. Inspect one deliberately failing report and one pending-score report and verify they are nonzero/incomplete rather than green. All expected public registry cases must be implemented; do not silently skip hard ones.

**Interview focus:** A valid evaluator is itself a tested system. Explain why final database state, trajectory, and semantic quality need different graders.
