# Copilot stage 17

Read COPILOT-START.md, AGENTS.md, docs/08-microsoft-agent-framework.md and the mapped learning section/checkpoint first. Execute only this stage. Teach concepts before asking one optional understanding question at a time. Record actual results and stop.

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
