# Start Uplisted with Microsoft Agent Framework

Read AGENTS.md, .github/copilot-instructions.md, docs/BUILD-PROGRESS.md and learning/stages.json. Begin the first incomplete stage. The reset project starts at **Stage 00**, orientation; Stage 01 begins implementation only after the learner continues.

Read docs/01-product-brief.md, docs/08-microsoft-agent-framework.md, the current stage from docs/03-build-plan.md, its prompt, learning section and checkpoint. Read applicable contracts/evaluation sections before coding; docs/06 covers Azure and docs/07 the managed-service lab.

The core runtime is Microsoft Agent Framework for both scripted tests and live Azure runs. Keep one MAF agent, seven tools, serial execution, one screen, typed validation, immutable state and human-only exact-version approval. Do not substitute a custom model/tool loop. The separate Foundry lab does not replace MAF.

## Teach before asking

Assume no prior agent/Azure knowledge. Explain each concept in plain language, show a concrete Uplisted example, then connect it to actual code when available. Ask one short optional question at a time, only after teaching the concept. If the learner does not know, explain and work through it; never demand independent study. Recommend defaults already specified instead of asking the learner to make unfamiliar architecture choices. Ask only for genuinely missing requirements, preferences or account values when needed.

## Execute one stage

Run commands through `./scripts/with-tools.sh`. Stage 00 runs the doctor and teaches the architecture without scaffolding. Stage 01 pins MAF dependencies and proves a real offline framework tool round trip. Subsequent stages implement the documented product. Azure account/model/spend choices are needed at Stage 13, not orientation. Do not create resources or make paid calls at startup.

After each stage run its gate, record actual evidence in docs/BUILD-PROGRESS.md and its learning checkpoint, explain one real code path/test if code exists, and stop. Record implementation, verification and learning separately. “Continue” permits only the next stage. Explanation questions never advance stages. Respect skipped teach-back and never infer understanding from silence.

Preserve instructions, fixtures, prepared tools and workspace settings while scaffolding. All stage completion records were reset; previous implementation evidence does not apply to this build.
