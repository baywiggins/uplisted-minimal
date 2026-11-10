# Uplisted interview demo: repository instructions

For a start request, read `COPILOT-START.md` and begin the first incomplete stage; do not stop after orientation. Read `docs/01-product-brief.md`, the applicable sections of `docs/02-contracts.md`, and the current stage of `docs/03-build-plan.md` before edits. Evaluation rules are in `docs/04-evaluation-plan.md`. Work on one stage only. Record progress in `docs/BUILD-PROGRESS.md`; never mark work verified without running its checks.

Build a single-screen rental-listing assistant. Python 3.12/FastAPI/Pydantic 2/PostgreSQL 16 backend; React/TypeScript/Vite frontend. One MAF agent, seven allowlisted tools, serial execution, one active run per case. Azure deployment is required: Microsoft Foundry/Azure OpenAI, Container Apps, PostgreSQL Flexible Server, Entra ID, managed identity, Key Vault and telemetry. See docs/06-azure-architecture.md. A separate Stage 18 managed Foundry agent lab is required for learning; it does not replace the product loop. Do not add unrelated agents, runtime queues, generic HTTP/shell tools, listing publishing, email, lease, payment or calendar workflows.

Provider modes are separate: `MODEL_MODE=scripted|live`, `RENTCAST_MODE=fixture|live`. Defaults are scripted/fixture. Never silently fall back from live to simulated. No credentials in browser code, fixtures, screenshots, logs, or Git. Do not read any original Uplisted environment files. Do not make billable requests as part of install, page load, unit tests, CI, or an ordinary build.

Confirmed facts, external comparable facts, and generated assumptions are separate. Missing values remain unknown. Every accepted artifact is immutable and carries source dependencies. Compare-and-swap commits reject stale input, stale target heads, cancellation, expired ownership/fences and cross-case references. Model tool arguments never supply actor identity, permissions, endpoints, or authoritative property replacements.

The runtime model can prepare review; it cannot approve. Approval is a separate human API action bound to the current exact bundle hash. Chat text, model outputs, and provider data cannot confer approval authority. Approval creates an internal snapshot only.

Use shared typed validators in application code; evaluation graders independently inspect persisted outcomes. Judge models cannot decide authorization, numeric correctness, or whether a database effect occurred. Log attempted, blocked, and committed actions separately. Do not expose hidden expected answers to runtime models. The supplied development cases are public; do not call them a holdout.

Create the root commands in Stage 01 and keep them stable:
- `uv sync --locked` installs Python dependencies after the lock exists.
- `uv run pytest -q` runs backend tests with external network blocked and only local test PostgreSQL permitted.
- `uv run ruff check .` and `uv run mypy src` check backend code.
- `npm --prefix web ci` installs locked frontend dependencies.
- `npm --prefix web run check`, `test`, and `build` validate the frontend.
- `npm --prefix web run test:e2e` runs local Playwright flows once implemented.
- `uv run python -m uplisted.evals validate --suite evals/dev/scenarios.jsonl` validates scenarios once Stage 12 exists.

Use official documentation for the installed SDK versions. Pin resolved dependencies in `uv.lock` and `web/package-lock.json`; do not invent patch versions or nonexistent SDK methods. Tests may use injected transports and clocks. Keep live adapters behind explicit configuration and separate tests. Cloud deployment and the managed-agent lab require actual Azure evidence; do not report them complete from mocked tests. Use Bicep/what-if and the owner choices in docs/AZURE-OWNER-SETUP.md before billable stages; do not silently select the CLI default subscription.

For risky behavior changes, write a meaningful failing test, implement the smallest correction, and show it passing. Do not mirror implementation details in tests, swallow exceptions, disable type checks, skip critical assertions, widen permissions, or alter expected results merely to pass. Preserve user edits and partial successes. Invalid model output produces a typed error or a bounded, recorded repair.

At stage completion report changed files, exact commands and observed results, incomplete checks, contract changes if any, and the relevant interview lesson. Stop before the next stage. Do not claim production readiness, legal compliance, calibrated market accuracy, verified physical dimensions, or benchmark performance without the appropriate evidence.

## Learning workflow

Use `learning/stages.json` to locate the current section, stage prompt, and checkpoint. Implement only one numbered stage; a learning section does not authorize several stages. Explain its purpose before editing. After passing or accurately reporting its gate, show one real code/data flow and one meaningful test, fill `learning/checkpoints/NN.md`, teach the concepts with a concrete example, then ask one optional question at a time, and stop. Record learning separately from implementation; never infer understanding from silence or passing tests. “Continue” permits only the next numbered stage; explanation requests do not advance it. Respect an explicit request to skip teach-back.

Run commands through `./scripts/with-tools.sh COMMAND ...` to select prepared project runtimes. Stage 01 must preserve the existing README learning map, workspace settings, scripts, fixtures, and documentation while adding product code and dependency lockfiles.

## Required MAF and beginner teaching

Read docs/08-microsoft-agent-framework.md. MAF is the core runtime from Stage 01, including offline scripted tests; no custom next_turn orchestration loop. Start a fresh project at Stage 00 and stop after orientation. Teach before questioning; explain unknown concepts and recommend documented implementation defaults. Do not require independent study.
