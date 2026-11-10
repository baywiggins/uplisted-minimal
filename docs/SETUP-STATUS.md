# Prepared folder: setup verification

Checked at 2026-11-10T03:26:03.913334+00:00.

These checks cover the prepared folder and local prerequisites, not the application or model performance.

| Check | Result | Observed detail |
|---|---|---|
| git | PASS | git version 2.50.1 (Apple Git-155) |
| uv | PASS | uv 0.12.23 (46b84fd0b 2026-10-03 aarch64-apple-darwin) |
| node | PASS | v24.22.2 |
| npm | PASS | 11.19.1 |
| python | PASS | Python 3.12.15 |
| docker | PASS | Docker version 29.1.3, build f52814d |
| Docker Compose | PASS | 2.40.3-desktop.1 |
| standalone Git repository | PASS | local repository; no remote required |
| COPILOT-START.md | PASS | file present |
| AGENTS.md | PASS | file present |
| .github/copilot-instructions.md | PASS | file present |
| .env.example | PASS | file present |
| docs/03-build-plan.md | PASS | file present |
| learning/stages.json | PASS | file present |
| evals/dev/scenarios.jsonl | PASS | file present |
| evals/cloud/scenarios.jsonl | PASS | file present |
| docs/06-azure-architecture.md | PASS | file present |
| docs/07-foundry-agent-lab.md | PASS | file present |
| docs/08-microsoft-agent-framework.md | PASS | file present |
| uplisted-interview.code-workspace | PASS | file present |
| learning map | PASS | 20 ordered stages (00–19) with existing sections/prompts/checkpoints |
| VS Code | PASS | installed |
| Copilot extension | FAIL | not detected |

## Scope

- Node 24 is installed under ignored `.tools/`; global Node settings are unchanged.
- Python 3.12 is linked to the existing uv-managed installation.
- Copilot account sign-in and VS Code workspace trust remain editor-controlled; no account or approval setting was changed.
- Application dependencies, source code, lockfiles, database/image setup and tests are left to Copilot Stage 01 onward.
- Docker/Compose version checks do not prove the daemon is running or a PostgreSQL image has been pulled.
- Azure CLI: available; account not checked.
- Azure tenant/subscription/model/permissions/budget/reviewer inputs are not configured; see AZURE-OWNER-SETUP.md.
- No Azure resource was created or deployed by this instruction update.
- No model/RentCast credentials were read or configured, and no paid provider was invoked.
- Stage 00 and all 19 implementation stages remain not started until Copilot implements and verifies them.

Rerun local checks: `./scripts/with-tools.sh python scripts/doctor.py`. Require Azure CLI too: add `--azure`.
