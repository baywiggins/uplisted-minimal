# Uplisted interview project

This is a prepared standalone project, currently containing specifications, development fixtures, project-local tooling, and learning sections. It is ready for staged implementation; the application has not been built yet.

For implementation requests, read `COPILOT-START.md`, `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md`, and `learning/stages.json`. Follow the canonical product/contracts/evaluation documents. Folder preparation, documentation maintenance, and verification do not authorize implementing application stages.

Implement exactly one numbered stage at a time. The eight learning sections are navigation groups, not permission to implement several stages. Stage 00 is orientation only; Stage 01 begins implementation. Before editing, explain the stage in plain language. After implementation, run its gate, show actual evidence, explain one real code path and test, fill its learning checkpoint, and stop. “Continue” permits only the next numbered stage. Answer explanation/status questions without advancing stages. If the user explicitly skips teach-back, record that and respect it.

Use project runtimes with `./scripts/with-tools.sh COMMAND ...`; terminal shells may otherwise select system Node 25. Do not replace or delete prepared documentation, fixtures, tool wrappers, workspace settings, or Git history while scaffolding. No application lockfiles currently exist; Copilot Stage 01 resolves them.

Maintain separate implementation/verification/learning statuses. Do not claim a passed check, user understanding, live integration, or benchmark result without evidence. Do not add live credentials, make paid calls, publish, deploy, or edit the original Uplisted repository as part of initial setup. Azure deployment is now a required later milestone, governed by docs/06-azure-architecture.md and the owner-supplied account/scope/budget choices. This instruction revision itself does not authorize provisioning. The main agent is application-owned on Azure; the managed Foundry lab is a separate learning exercise.

## Required MAF and beginner teaching

Read docs/08-microsoft-agent-framework.md. MAF is the core runtime from Stage 01, including offline scripted tests; no custom next_turn orchestration loop. Start a fresh project at Stage 00 and stop after orientation. Teach before questioning; explain unknown concepts and recommend documented implementation defaults. Do not require independent study.
