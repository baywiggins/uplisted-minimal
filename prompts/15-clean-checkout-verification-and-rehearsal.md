# Copilot prompt: Stage 15 — Clean-checkout verification and rehearsal

Implement only Stage 15. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md` if it exists, the product brief, the relevant canonical contracts, and this stage's evaluation requirements. Inspect the actual current code and previous check results before editing. Do not assume a previous stage is complete because a chat said so.

Start by listing the contracts this change relies on and the files you will touch. If a prerequisite stage is incomplete, report the exact missing interface/check and repair that prerequisite before dependent implementation. Keep the chosen architecture.

The stage specification follows verbatim:

## Stage 15 — Clean-checkout verification and rehearsal

**Files:** finalize README, `docs/BUILD-PROGRESS.md`, `docs/DEMO-SCRIPT.md`, `docs/RESULTS.md`, `docs/LIMITATIONS.md`, `.github/workflows/checks.yml`; optional local demo recording with synthetic data only.

**Consumes:** completed project and actual reports, plus the supplied interview playbook.

**Produces:** reproducible local project, offline CI, a backup fixture demo, a concise technical talk, and accurate evidence claims.

- [ ] In a new temporary checkout/environment, install from lockfiles, initialize synthetic data, and start backend/frontend using README only. Confirm no original Uplisted file or secret is required.
- [ ] Run complete backend, frontend, browser, and harness self-tests. CI runs scripted/fixture only with external network blocked during tests; dependency installation/browser installation are separate setup steps. Do not run paid evals on pull requests.
- [ ] Walk the live demo: useful request, source-linked sentence, schematic caveat, photos-only restraint, injection/failure handling, stale approval rejection, and measured report. Keep a fixture replay and screenshots/recording as a clearly labeled backup.
- [ ] Fill talk placeholders only with actual implementation details/results. Explain Copilot's role honestly and identify the contracts, reviews, tests, and fixes you personally understood and directed.
- [ ] Record limitations: local auth, process interruption, synthetic tasks, restricted listing grammar, unmeasured physical/market accuracy, incomplete live integrations, and any remaining failures. Remove unfinished UI claims or label them clearly.

**Gate:** clean-checkout commands reproduce the documented outcome, critical checks pass, and the ten-minute talk can be delivered without relying on Copilot to explain the code. Code exists only after implementation; this handoff itself does not satisfy the gate.

**Interview focus:** Show ownership of the design and evidence, including limitations. Framework names and code volume are secondary.

At completion, report:
- Implemented behavior and changed files.
- Exact commands executed and observed results; explicitly identify unrun checks.
- Which failure cases the tests exercise and what they do not prove.
- Any deviations or unresolved issues.
- A short explanation I can use in the interview.

Update `docs/BUILD-PROGRESS.md`. Inspect the diff and whitespace checks. Prepare a scoped checkpoint commit after passing checks and review; do not push or deploy. Stop before the next stage. Do not fill benchmark fields with invented numbers.


Learning checkpoint: read `learning/sections/06-ownership.md` before implementation. After the stage gate, fill `learning/checkpoints/15.md` with actual code/test evidence, explain the change, ask two short teach-back questions, and stop. Track learning separately from implementation. Use `./scripts/with-tools.sh` for each terminal command.
