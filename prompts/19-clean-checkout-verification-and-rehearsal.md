# Copilot prompt: Stage 19 — Clean-checkout verification and rehearsal

Implement only Stage 19. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md`, the product brief, relevant canonical contracts/evaluation rules, and Azure architecture `docs/06-azure-architecture.md`. Inspect actual code and check results before editing. Use PostgreSQL and the Azure model/deployment architecture specified in the current documents.

Start by listing the contracts and files this stage touches. If a prerequisite is incomplete, report the exact missing interface/check and repair it before dependent implementation. Use the existing design. Do not create billable resources until the relevant cloud stage has the owner-supplied scope/limits; do not ask again for authorization already supplied for that scope.

The stage specification follows verbatim:

## Stage 19 — Clean-checkout verification and rehearsal

**Files:** finalize README, `docs/BUILD-PROGRESS.md`, `docs/DEMO-SCRIPT.md`, `docs/RESULTS.md`, `docs/LIMITATIONS.md`, `.github/workflows/checks.yml`; optional local demo recording with synthetic data only.

**Consumes:** completed project, actual Azure deployment/managed-agent lab reports, plus the supplied interview playbook.

**Produces:** reproducible local and Azure project, offline CI, an authenticated cloud demo plus backup fixture replay, a concise technical talk, and accurate evidence claims.

- [ ] In a new temporary checkout/environment, install from lockfiles, initialize synthetic data, and start backend/frontend using README only. Confirm no original Uplisted file or secret is required.
- [ ] Run complete backend, frontend, browser, and harness self-tests. CI runs scripted/fixture only with external network blocked during tests; dependency installation/browser installation are separate setup steps. Do not run paid evals on pull requests.
- [ ] Freeze the final runtime/dependency/prompt/schema bundle fingerprint. Re-run affected model, browser and cloud checks after Stages 15–18, and rerun the full required suite for the final snapshot if its runtime bundle changed. Earlier Stage 14 comparisons remain historical evidence. Use the compatibility rules in the evaluation plan; do not combine mismatched runtime evidence into a release claim.
- [ ] Execute `finalize --profile azure` with the model/service/browser/cloud reports and actual Foundry lab receipt, using the command in docs04. Resolve missing grades/results and distinguish quality failures from critical-control failures. Save the final status/limitations; a generated report is not a passing release.
- [ ] Recheck the Azure URL, allowed reviewer, resource expiry and cost/cleanup notes. Walk the live demo: useful request, source-linked sentence, schematic caveat, photos-only restraint, injection/failure handling, stale approval rejection, and measured report. Keep a fixture replay and screenshots/recording as a clearly labeled backup.
- [ ] Fill talk placeholders only with actual implementation details/results. Explain Copilot's role honestly and identify the contracts, reviews, tests, and fixes you personally understood and directed.
- [ ] Record limitations: local-development versus Entra cloud auth, lease-expiry interruption, synthetic tasks, restricted listing grammar, unmeasured physical/market accuracy, incomplete live integrations and managed-service accounting limits, and any remaining failures. Remove unfinished UI claims or label them clearly.

**Gate:** clean-checkout commands reproduce the documented outcome, critical checks pass, and the ten-minute talk can be delivered without relying on Copilot to explain the code. Azure deployment and the managed-agent lab must have actual evidence; neither is replaced by the offline backup. Code exists only after implementation; this handoff itself does not satisfy the gate.

**Interview focus:** Show ownership of the design and evidence, including limitations. Framework names and code volume are secondary.

At completion, report changed files, actual commands/results, unrun checks, what the tests prove, unresolved issues, and the interview lesson. Update `docs/BUILD-PROGRESS.md`, inspect the diff, and prepare a scoped checkpoint after verification. Do not push, deploy unrelated resources, or start another stage.

Learning checkpoint: read `learning/sections/08-ownership.md` before implementation. Fill `learning/checkpoints/19.md` with real code/test evidence, explain one path and test, ask two short questions, and stop. Use `./scripts/with-tools.sh` for terminal commands. Track learning separately from implementation.
