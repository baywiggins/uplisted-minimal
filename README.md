# Uplisted interview — ready to build with Copilot

This folder is prepared for an Azure-targeted prototype. The earlier plan was local-only; Azure hosting and agent learning are now required milestones. Open `uplisted-interview.code-workspace` in VS Code and use Copilot in a mode that can edit local files and run terminal commands. If VS Code requests workspace trust or GitHub sign-in, handle that in the editor; this setup does not alter those permissions or accounts.

Paste this one prompt:

> Read COPILOT-START.md and begin Stage 00. Teach me the architecture, run its prerequisite check, then explain the concepts and stop at its learning checkpoint.

Copilot should start implementing, not ask you to copy files or redesign the project. All application stages are still unimplemented. This folder provides the specification, tooling preparation, fixtures, and learning structure.

## Begin with orientation, then learn in eight sections

[Stage 00: Orientation](learning/sections/00-orientation.md) teaches the architecture before any code is written. [Microsoft Agent Framework](docs/08-microsoft-agent-framework.md) is the required core runtime from Stage 01.

| Section | Stages | What you will understand |
|---|---|---|
| [1. Foundations](learning/sections/01-foundations.md) | 01–03 | Setup, typed data, revisions, transactions, and duplicate requests |
| [2. Evidence](learning/sections/02-evidence.md) | 04–06 | Single-screen inspection, RentCast identity/freshness, and pricing |
| [3. Grounded artifacts](learning/sections/03-grounding.md) | 07–08 | Schematic floorplans, photo plans, and supported listing facts |
| [4. Agent authority](learning/sections/04-agent-authority.md) | 09–11 | Tool execution, shared budgets, cancellation, and human approval |
| [5. Evaluations](learning/sections/05-evaluations.md) | 12–14 | Independent graders, real-model trials, fair comparisons, and failures |
| [6. Azure deployment](learning/sections/06-azure-deployment.md) | 15–17 | Cloud identity, run ownership, infrastructure, deployment and observability |
| [7. Managed agents](learning/sections/07-managed-agents.md) | 18 | Build a real Foundry Agent Service prompt agent and compare execution |
| [8. Ownership](learning/sections/08-ownership.md) | 19 | Reproducibility, limitations, and the interview demonstration |

Each stage has a copy-ready implementation prompt and its own learning checkpoint. A section groups concepts; Copilot still implements one stage at a time. After a checkpoint, ask questions or say `Continue with only the next numbered stage.`

## Find what you need

- [Learning map](learning/README.md): how to understand and discuss each section.
- [Build progress](docs/BUILD-PROGRESS.md): actual implementation and verification status.
- [Project brief](docs/01-product-brief.md): the single-screen product and interview goals.
- [Contracts](docs/02-contracts.md): exact interfaces, authority, state, and limits.
- [Build plan](docs/03-build-plan.md): Stage 00 plus 19 implementation stages and their checks.
- [Evaluation plan](docs/04-evaluation-plan.md): 30 development scenarios plus 10 separate Azure checks, metrics, graders, and holdout rules.
- [Azure architecture](docs/06-azure-architecture.md): required cloud resources, deployment, identity, telemetry and cleanup.
- [Azure owner setup](docs/AZURE-OWNER-SETUP.md): inputs needed before provisioning or paid calls.
- [Managed-agent lab](docs/07-foundry-agent-lab.md): actual Foundry Agent Service practice.
- [Interview playbook](docs/05-interview-playbook.md): ten-minute talk, demonstrations, and likely questions.
- [Setup status](docs/SETUP-STATUS.md): verified local prerequisites and remaining future setup.

## Tooling already prepared

The existing Git/VS Code/Copilot/uv/Node 24/Python 3.12 setup remains prepared. Stage 01 verifies Docker/Compose for local PostgreSQL. Azure CLI, subscription access, model availability, tenant/reviewer and spend choices are checked before Stage 13; they are not assumed configured. Application dependencies/lockfiles remain Copilot work. No Azure resources or paid calls are needed to start Stage 00.

Use `./scripts/with-tools.sh COMMAND ...` for terminal commands. It selects the prepared runtimes without changing global Node/Python settings. Example: `./scripts/with-tools.sh python scripts/doctor.py`. VS Code terminals also have a project PATH hint, but the wrapper is reliable across separate agent terminal calls.

## Interview priorities

Emphasize real Azure deployment/identity boundaries alongside measured task completion, independent evaluation, bounded tool authority, provenance, stale-version rejection, and failure recovery. Show one concrete failure and the evidence behind its fix. Do not substitute framework names, a polished screen, or a high test count for an explanation of the system.

Copilot should append the application's verified install/run/test commands below during Stage 01 while preserving this navigation.

## Application commands

Not implemented yet. Stage 01 will add verified commands here.

## Required Microsoft Agent Framework

The main agent uses MAF for model/tool orchestration from Stage 01, with a scripted framework client before Azure access. Application services enforce permissions, budgets, validation and approval. Begin with Stage 00 orientation. See [MAF runtime contract](docs/08-microsoft-agent-framework.md).
