# Copilot prompt: Stage 01 — Bootable project and reproducible commands

Implement only Stage 01. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md`, the product brief, relevant canonical contracts/evaluation rules, and Azure architecture `docs/06-azure-architecture.md`. Inspect actual code and check results before editing. Use PostgreSQL and the Azure model/deployment architecture specified in the current documents.

Start by listing the contracts and files this stage touches. If a prerequisite is incomplete, report the exact missing interface/check and repair it before dependent implementation. Use the existing design. Do not create billable resources until the relevant cloud stage has the owner-supplied scope/limits; do not ask again for authorization already supplied for that scope.

The stage specification follows verbatim:

## Stage 01 — Bootable project and reproducible commands

**Files:** create root `pyproject.toml`, `uv.lock`, `.python-version`, `.node-version`, `.gitignore`, `.env.example`, `README.md`; `src/uplisted/__init__.py`, `config.py`, `api/app.py`; `tests/conftest.py`, `tests/unit/test_config.py`, `tests/integration/test_health.py`; `web/` Vite React TypeScript project and scripts; `docs/BUILD-PROGRESS.md`.

**Consumes:** the copied handoff documents and official installation documentation.

**Produces:** `create_app() -> FastAPI`, validated `Settings`, `/api/health`, the standard commands from contracts §1, and a frontend that renders one empty workspace route. No tool/provider functionality yet.

- [ ] Inspect the empty target and copied docs; initialize Git if absent. Verify Python 3.12, Node 24, uv/npm and Docker/Compose versions. The prepared runtime wrapper remains in use. If tools are missing, report the exact prerequisite instead of executing an unrelated installer.
- [ ] Resolve compatible stable dependency releases. Use FastAPI/Pydantic 2/httpx/uvicorn and the named test tools; prepare compose.yaml with a pinned PostgreSQL 16 image, loopback port 5433, health check and local-only credentials from the example; avoid extra runtime frameworks. Commit lockfiles and record exact installed versions. Use current official docs for syntax.
- [ ] Create fixture-safe configuration: `MODEL_MODE=scripted`, `RENTCAST_MODE=fixture`, loopback origin, local PostgreSQL connection, APP_ENV=local/AUTH_MODE=local_demo, empty Azure identifiers/live secrets, and no provider work during import/startup. Tests assert invalid mode rejection and safe defaults. Use a global test guard that blocks external sockets and allows only the configured loopback test database; HTTP adapters use injected mock transports. Container image/dependency downloads are setup, not test execution.
- [ ] Implement `create_app` with readiness route and minimal frontend scripts. Health test asserts HTTP 200 and no credentials/machine paths. Do not add chat mock interactions that pretend to be a real agent.
- [ ] Write start/install/check commands in README; run from a fresh environment using lockfiles. A separate terminal is required for each dev server.

**Gate:** `docker compose config --quiet`; start the database and verify its health without exposing it beyond loopback; `uv run pytest -q tests/unit/test_config.py tests/integration/test_health.py`; `uv run ruff check .`; `uv run mypy src`; `npm --prefix web run check`; `npm --prefix web run build`. All must exit 0; inspect the page on the one route. Do not claim other features exist.

**Interview focus:** Reproducible configuration and explicit simulation prevent a polished demo from hiding missing integrations.

At completion, report changed files, actual commands/results, unrun checks, what the tests prove, unresolved issues, and the interview lesson. Update `docs/BUILD-PROGRESS.md`, inspect the diff, and prepare a scoped checkpoint after verification. Do not push, deploy unrelated resources, or start another stage.

Learning checkpoint: read `learning/sections/01-foundations.md` before implementation. Fill `learning/checkpoints/01.md` with real code/test evidence, explain one path and test, ask two short questions, and stop. Use `./scripts/with-tools.sh` for terminal commands. Track learning separately from implementation.
