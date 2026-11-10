# Copilot stage 15

Read COPILOT-START.md, AGENTS.md, docs/08-microsoft-agent-framework.md and the mapped learning section/checkpoint first. Execute only this stage. Teach concepts before asking one optional understanding question at a time. Record actual results and stop.

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
