# Start the prepared Uplisted project

The user has authorized you to start implementing this project's existing specification. The folder is prepared; do not ask the user to create a folder, copy files, choose the architecture again, or paste all the documents. Begin the first incomplete stage after checking actual progress; on a fresh checkout this is Stage 01.

## Read only what you need first

1. `AGENTS.md` and `.github/copilot-instructions.md`.
2. `docs/BUILD-PROGRESS.md` and `learning/stages.json`.
3. `docs/01-product-brief.md`; the relevant sections of `docs/02-contracts.md` and `docs/04-evaluation-plan.md`.
4. The current stage's prompt and learning section from the stage mapping.

The canonical stage text is in `docs/03-build-plan.md`; each matching file in `prompts/` contains the same instructions. Implementation decisions are already documented. Resolve routine details yourself within those contracts. Ask only when a concrete conflict cannot be resolved from them.

## Start work, do not stop at orientation

Briefly explain this stage's purpose, what currently exists, and what you will add. Run `./scripts/with-tools.sh python scripts/doctor.py`. The prepared Node/Python tools are local to this project; do not upgrade or replace global runtimes. Run stage commands through `./scripts/with-tools.sh` so each terminal call uses the correct PATH.

Implement Stage 01 now if nothing is implemented. Preserve the ready-folder README's learning links when adding actual run/build commands. Do not overwrite the prepared workspace/tooling or mark later features implemented. Install only dependencies needed for the current stage, then pin them in the planned lockfiles.

## Finish with a learning checkpoint

Run the current stage's actual acceptance checks and report their results. Fix scoped failures without weakening requirements. Update `docs/BUILD-PROGRESS.md` and the matching `learning/checkpoints/NN.md` with:

- What changed and why, in plain English.
- One real code/data flow with verified source paths and symbols.
- One meaningful test, its actual result, and the failure it detects.
- Two short questions that help me explain the implementation myself.
- One interview takeaway and one remaining limitation.

Record learning as explained, not automatically understood. Stop after this single stage so I can inspect the work. Answer my questions before advancing. “Continue” means only the next numbered stage. If I explicitly skip the questions, respect that and record it.

## Preserve the project boundaries

One contained screen, one coordinator, seven tools, typed/domain validation, immutable state, exact-version human approval, no external publication, and fixture/scripted providers initially. The real-model evaluation milestone requires separately configured runtime access later. A passing scripted demo cannot establish model reliability. All result tables remain unfilled until actually measured.
