# Copilot prompt: Stage 15 — Azure identity, persistent sessions and process ownership

Implement only Stage 15. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md`, the product brief, relevant canonical contracts/evaluation rules, and Azure architecture `docs/06-azure-architecture.md`. Inspect actual code and check results before editing. Use PostgreSQL and the Azure model/deployment architecture specified in the current documents.

Start by listing the contracts and files this stage touches. If a prerequisite is incomplete, report the exact missing interface/check and repair it before dependent implementation. Use the existing design. Do not create billable resources until the relevant cloud stage has the owner-supplied scope/limits; do not ask again for authorization already supplied for that scope.

The stage specification follows verbatim:

## Stage 15 — Azure identity, persistent sessions and process ownership

**Files:** implement `api/identity.py`, extend `api/session.py`, `state/run_ownership.py`, migrations for memberships/sessions/stored reports; `tests/integration/test_cloud_identity.py`, `test_run_ownership.py`, `test_persistent_sessions.py`; update frontend sign-in/expiry handling and configuration.

**Consumes:** PostgreSQL repository/lease contracts, local API, Entra/Container Apps boundary from `docs/06-azure-architecture.md`.

**Produces:** explicit local/cloud identity providers, cloud startup validation, persisted session/CSRF/actor bindings, per-case reviewer authorization, and tested correctness across overlapping process owners.

- [ ] Reject `APP_ENV=azure` with local_demo authentication, insecure database TLS, missing tenant/reviewer mapping, or invalid origin. Model and human identities are distinct. Test valid tenant/object-ID membership, another signed-in user, wrong tenant and absent/untrusted platform principal.
- [ ] Persist app session binding and require the current authenticated actor to match it on every human mutation. Test restart retention, CSRF/origin rejection and a body claiming another actor/role. Local tests use an explicit injected identity adapter, not generic spoofable headers.
- [ ] Complete owner/fence checks on every dispatch, budget reservation, artifact and review commit. Test two simulated process owners, lease renewal, healthy-owner protection, expired-owner interruption, and late result rejection. Never auto-replay an uncertain external call after loss of ownership.
- [ ] Store bounded redacted UI report projections in PostgreSQL instead of depending on container-local files. Keep telemetry/raw eval artifacts separate from authoritative state.
- [ ] Document the trusted ingress assumption and test it again after real deployment in Stage 17. A mocked principal unit test cannot establish that Azure strips/rejects forged identity headers.

**Gate:** `uv run pytest -q tests/integration/test_cloud_identity.py tests/integration/test_run_ownership.py tests/integration/test_persistent_sessions.py`; existing review/cancellation/scope tests still pass against PostgreSQL. Azure network behavior remains unverified until Stage 17.

**Interview focus:** Human authentication, application authorization, workload identity and model authority are four different concerns. Explain why one replica does not eliminate revision-overlap races.

At completion, report changed files, actual commands/results, unrun checks, what the tests prove, unresolved issues, and the interview lesson. Update `docs/BUILD-PROGRESS.md`, inspect the diff, and prepare a scoped checkpoint after verification. Do not push, deploy unrelated resources, or start another stage.

Learning checkpoint: read `learning/sections/06-azure-deployment.md` before implementation. Fill `learning/checkpoints/15.md` with real code/test evidence, explain one path and test, ask two short questions, and stop. Use `./scripts/with-tools.sh` for terminal commands. Track learning separately from implementation.
