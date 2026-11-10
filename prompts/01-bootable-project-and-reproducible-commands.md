# Copilot stage 01

Read COPILOT-START.md, AGENTS.md, docs/08-microsoft-agent-framework.md and the mapped learning section/checkpoint first. Execute only this stage. Teach concepts before asking one optional understanding question at a time. Record actual results and stop.

## Stage 01 — Bootable project and reproducible commands

**Files:** create root `pyproject.toml`, `uv.lock`, `.python-version`, `.node-version`, `.gitignore`, `.env.example`, `README.md`; `src/uplisted/__init__.py`, `config.py`, `api/app.py`; `tests/conftest.py`, `tests/unit/test_config.py`, `tests/integration/test_health.py tests/integration/test_maf_smoke.py`; `web/` Vite React TypeScript project and scripts; `docs/BUILD-PROGRESS.md`.

**Consumes:** the copied handoff documents and official installation documentation.

**Produces:** `create_app() -> FastAPI`, validated `Settings`, `/api/health`, the standard commands from contracts §1, and a frontend that renders one empty workspace route. No tool/provider functionality yet.

- [ ] Inspect the empty target and copied docs; initialize Git if absent. Verify Python 3.12, Node 24, uv/npm and Docker/Compose versions. The prepared runtime wrapper remains in use. If tools are missing, report the exact prerequisite instead of executing an unrelated installer.
- [ ] Resolve compatible stable dependency releases. Use FastAPI/Pydantic 2/httpx/uvicorn and the named test tools; prepare compose.yaml with a pinned PostgreSQL 16 image, loopback port 5433, health check and local-only credentials from the example; install Microsoft Agent Framework core and its compatible Responses provider package; avoid unrelated frameworks. Commit lockfiles and record exact installed versions. Use current official docs for syntax.
- [ ] Add `agent/runtime.py` and `providers/scripted_chat_client.py` with a real MAF Agent offline smoke using one harmless fixture tool. Verify the installed public client-response interception and function middleware boundaries needed by docs/08; record exact package versions and signatures in `docs/MAF-SDK-NOTES.md`. This smoke is not the seven-tool product agent. Add `tests/integration/test_maf_smoke.py`; assert model → tool → result → final, no network, and serial invocation configuration.
- [ ] Create fixture-safe configuration: `MODEL_MODE=scripted`, `RENTCAST_MODE=fixture`, loopback origin, local PostgreSQL connection, APP_ENV=local/AUTH_MODE=local_demo, empty Azure identifiers/live secrets, and no provider work during import/startup. Tests assert invalid mode rejection and safe defaults. Use a global test guard that blocks external sockets and allows only the configured loopback test database; HTTP adapters use injected mock transports. Container image/dependency downloads are setup, not test execution.
- [ ] Implement `create_app` with readiness route and minimal frontend scripts. Health test asserts HTTP 200 and no credentials/machine paths. Do not add chat mock interactions that pretend to be a real agent.
- [ ] Write start/install/check commands in README; run from a fresh environment using lockfiles. A separate terminal is required for each dev server.

**Gate:** `docker compose config --quiet`; start the database and verify its health without exposing it beyond loopback; `uv run pytest -q tests/unit/test_config.py tests/integration/test_health.py`; `uv run ruff check .`; `uv run mypy src`; `npm --prefix web run check`; `npm --prefix web run build`. All must exit 0; inspect the page on the one route. Do not claim other features exist.

**Interview focus:** Reproducible configuration and explicit simulation prevent a polished demo from hiding missing integrations.
