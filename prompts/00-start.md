# Copilot stage 00

Read COPILOT-START.md, AGENTS.md, docs/08-microsoft-agent-framework.md and the mapped learning section/checkpoint first. Execute only this stage. Teach concepts before asking one optional understanding question at a time. Record actual results and stop.

## Stage 00 — Orientation and MAF mental model

**Files:** update only `docs/BUILD-PROGRESS.md` and `learning/checkpoints/00.md` after this stage is actually conducted.

**Consumes:** COPILOT-START, product brief, MAF runtime contract, learning/sections/00-orientation.md.

**Produces:** an explained architecture and prerequisite report, without application implementation.

- [ ] Explain agent versus model versus tool using an Uplisted example. Define MAF, Azure OpenAI, and Foundry Agent Service separately.
- [ ] Walk through user request → MAF agent → validated tool → evidence/artifact → human review. Explain why the framework does not prove factual correctness or grant permissions.
- [ ] Explain scripted mode and why it uses the actual MAF runtime with a fake model client.
- [ ] Run `./scripts/with-tools.sh python scripts/doctor.py`. Report missing prerequisites accurately. Azure account knowledge is not required now.
- [ ] Explain the upcoming stages and ask one optional understanding question only after teaching its answer through a concrete example. If the learner does not know, explain and practice; do not require outside study.

**Gate:** prerequisite command output inspected; orientation recorded as explained, never automatically understood. No product code, dependencies, migrations or cloud resources created.

**Interview focus:** Identify which responsibilities belong to the framework, model, application and human.
