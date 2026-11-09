# Copilot prompt: Stage 17 — Deploy and verify the Azure prototype

Implement only Stage 17. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md`, the product brief, relevant canonical contracts/evaluation rules, and Azure architecture `docs/06-azure-architecture.md`. Inspect actual code and check results before editing. Use PostgreSQL and the Azure model/deployment architecture specified in the current documents.

Start by listing the contracts and files this stage touches. If a prerequisite is incomplete, report the exact missing interface/check and repair it before dependent implementation. Use the existing design. Do not create billable resources until the relevant cloud stage has the owner-supplied scope/limits; do not ask again for authorization already supplied for that scope.

The stage specification follows verbatim:

## Stage 17 — Deploy and verify the Azure prototype

**Files:** execute prepared scripts within the authorized scope; fill `docs/AZURE-DEPLOYMENT-RESULTS.md`; add `evals/cloud/scenarios.jsonl` and executable cloud smoke drivers; preserve sanitized deployment/test artifacts.

**Consumes:** reviewed Stage 16 plan, exact owner subscription/region/identity/spend configuration, valid credentials/permissions, and the built image digest.

**Produces:** a working authenticated Azure HTTPS prototype, actual cloud acceptance evidence, known limitations, and a verified cleanup inventory. Provisioning is a real billable action in this stage; this instruction-editing task has not executed it.

- [ ] Apply the reviewed infrastructure to its dedicated resource group. Configure Entra before enabling usable external ingress, initialize schema/seed through the private migration path, and deploy the immutable image digest. Start with scripted model/fixture evidence so infrastructure tests do not accidentally spend on models.
- [ ] Verify anonymous denial, authorized reviewer success, unlisted tenant-user denial, CSRF/origin enforcement and forged-principal resistance. Load/inspect/edit/review in the same HTTPS workspace. The Azure UI must visibly report its deployment/model/evidence mode without displaying secrets.
- [ ] Test accepted-state persistence through restart, healthy run ownership during revision overlap, expiration of an orphaned lease, concurrent start rejection, stale approval and late/cancelled result rejection. No duplicate billable retry or automatic provider replay.
- [ ] Explicitly enable Azure-model inference within the run/batch cap and complete a task with frozen evidence. Verify managed identity refresh, current data/approval state and correlated request/run/tool/model traces. Live RentCast remains optional and separately labeled.
- [ ] Record group/region/resource IDs, revision/image digest, SDK/model versions, auth/DB configuration fingerprints, timestamps, check results, cost assumptions/observed spend and limitations. Do not store tokens or private contact/property content in the shareable report.
- [ ] Exercise rollback to a compatible prior image if available; verify cleanup dry-run targets only owned resources. Keep the deployed demo until the owner elects teardown; documenting cleanup is not permission to delete the working demo immediately.

**Gate:** all required cloud acceptance checks in docs06 are backed by actual Azure observations; cloud failures stay distinct from offline/model-quality failures. An absent Azure account/permission leaves this stage incomplete rather than changing the target back to local.

**Interview focus:** Demonstrate a real deployment, an actual identity boundary, state surviving infrastructure changes, and evidence of behavior under failure.

At completion, report changed files, actual commands/results, unrun checks, what the tests prove, unresolved issues, and the interview lesson. Update `docs/BUILD-PROGRESS.md`, inspect the diff, and prepare a scoped checkpoint after verification. Do not push, deploy unrelated resources, or start another stage.

Learning checkpoint: read `learning/sections/06-azure-deployment.md` before implementation. Fill `learning/checkpoints/17.md` with real code/test evidence, explain one path and test, ask two short questions, and stop. Use `./scripts/with-tools.sh` for terminal commands. Track learning separately from implementation.
