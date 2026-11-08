# Copilot prompt: Stage 01 — Bootable project and reproducible commands

Implement only Stage 01. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md` if it exists, the product brief, the relevant canonical contracts, and this stage's evaluation requirements. Inspect the actual current code and previous check results before editing. Do not assume a previous stage is complete because a chat said so.

Start by listing the contracts this change relies on and the files you will touch. If a prerequisite stage is incomplete, report the exact missing interface/check and repair that prerequisite before dependent implementation. Keep the chosen architecture.

The stage specification follows verbatim:

## Stage 01 — Bootable project and reproducible commands

**Files:** create root `pyproject.toml`, `uv.lock`, `.python-version`, `.node-version`, `.gitignore`, `.env.example`, `README.md`; `src/uplisted/__init__.py`, `config.py`, `api/app.py`; `tests/conftest.py`, `tests/unit/test_config.py`, `tests/integration/test_health.py`; `web/` Vite React TypeScript project and scripts; `docs/BUILD-PROGRESS.md`.

**Consumes:** the copied handoff documents and official installation documentation.

**Produces:** `create_app() -> FastAPI`, validated `Settings`, `/api/health`, the standard commands from contracts §1, and a frontend that renders one empty workspace route. No tool/provider functionality yet.

- [ ] Inspect the empty target and copied docs; initialize Git if absent. Verify Python 3.12, Node 24, uv/npm versions. If tools are missing, report the exact prerequisite instead of executing an unrelated installer.
- [ ] Resolve compatible stable dependency releases. Use FastAPI/Pydantic 2/httpx/uvicorn and the named test tools; avoid extra runtime frameworks. Commit lockfiles and record exact installed versions. Use current official docs for syntax.
- [ ] Create fixture-safe configuration: `MODEL_MODE=scripted`, `RENTCAST_MODE=fixture`, loopback origin, ignored local database, empty live secrets, and no provider work during import/startup. Tests assert invalid mode rejection and safe defaults. Use a global test guard that blocks external sockets; HTTP adapters use injected mock transports.
- [ ] Implement `create_app` with readiness route and minimal frontend scripts. Health test asserts HTTP 200 and no credentials/machine paths. Do not add chat mock interactions that pretend to be a real agent.
- [ ] Write start/install/check commands in README; run from a fresh environment using lockfiles. A separate terminal is required for each dev server.

**Gate:** `uv run pytest -q tests/unit/test_config.py tests/integration/test_health.py`; `uv run ruff check .`; `uv run mypy src`; `npm --prefix web run check`; `npm --prefix web run build`. All must exit 0; inspect the page on the one route. Do not claim other features exist.

**Interview focus:** Reproducible configuration and explicit simulation prevent a polished demo from hiding missing integrations.

At completion, report:
- Implemented behavior and changed files.
- Exact commands executed and observed results; explicitly identify unrun checks.
- Which failure cases the tests exercise and what they do not prove.
- Any deviations or unresolved issues.
- A short explanation I can use in the interview.

Update `docs/BUILD-PROGRESS.md`. Inspect the diff and whitespace checks. Prepare a scoped checkpoint commit after passing checks and review; do not push or deploy. Stop before the next stage. Do not fill benchmark fields with invented numbers.


Learning checkpoint: read `learning/sections/01-foundations.md` before implementation. After the stage gate, fill `learning/checkpoints/01.md` with actual code/test evidence, explain the change, ask two short teach-back questions, and stop. Track learning separately from implementation. Use `./scripts/with-tools.sh` for each terminal command.
