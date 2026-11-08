# Prepared folder: setup verification

Checked at 2026-11-08T03:10:30.847163+00:00.

These checks cover the prepared folder and local prerequisites, not the application or model performance.

| Check | Result | Observed detail |
|---|---|---|
| git | PASS | git version 2.50.1 (Apple Git-155) |
| uv | PASS | uv 0.12.23 (46b84fd0b 2026-10-03 aarch64-apple-darwin) |
| node | PASS | v24.22.2 |
| npm | PASS | 11.19.1 |
| python | PASS | Python 3.12.15 |
| standalone Git repository | PASS | local repository; no remote required |
| COPILOT-START.md | PASS | file present |
| AGENTS.md | PASS | file present |
| .github/copilot-instructions.md | PASS | file present |
| .env.example | PASS | file present |
| docs/03-build-plan.md | PASS | file present |
| learning/stages.json | PASS | file present |
| evals/dev/scenarios.jsonl | PASS | file present |
| uplisted-interview.code-workspace | PASS | file present |
| learning map | PASS | 15 ordered stages with existing sections/prompts/checkpoints |
| VS Code | PASS | installed |
| Copilot extension | PASS | installed; account sign-in not checked |

## Scope

- Node 24 is installed under ignored `.tools/`; global Node settings are unchanged.
- Python 3.12 is linked to the existing uv-managed installation.
- Copilot account sign-in and VS Code workspace trust remain editor-controlled; no account or approval setting was changed.
- Application dependencies, source code, lockfiles, and tests are intentionally left to Copilot Stage 01 onward.
- No model/RentCast credentials were read or configured, and no paid provider was invoked.
- All 15 application stages remain not started until Copilot implements and verifies them.

Rerun: `./scripts/with-tools.sh python scripts/doctor.py`.
