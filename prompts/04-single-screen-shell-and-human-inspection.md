# Copilot prompt: Stage 04 — Single-screen shell and human inspection

Implement only Stage 04. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md` if it exists, the product brief, the relevant canonical contracts, and this stage's evaluation requirements. Inspect the actual current code and previous check results before editing. Do not assume a previous stage is complete because a chat said so.

Start by listing the contracts this change relies on and the files you will touch. If a prerequisite stage is incomplete, report the exact missing interface/check and repair that prerequisite before dependent implementation. Keep the chosen architecture.

The stage specification follows verbatim:

## Stage 04 — Single-screen shell and human inspection

**Files:** create `web/src/components/Workspace.tsx`, `AssistantPanel.tsx`, `PropertyHeader.tsx`, `ArtifactTabs.tsx`, `RunDetails.tsx`; `web/src/views/` placeholders; `web/src/state/workspace.ts`; `web/src/api/types.ts`; `web/tests/workspace.test.tsx` and styles.

**Consumes:** product brief layout and representative validated fixture data. Until the API exists, use a clearly labeled view adapter with static data, not ad hoc types in every component.

**Produces:** one workspace route, persistent composer, in-place property form, artifact selection, responsive Assistant/Workspace switch, accessible states. No live generation.

- [ ] Keep property/mode summary above assistant plus one selected artifact. No numbered progression or routing library unless required by the existing scaffold; one route is enough.
- [ ] Implement tab/view state without unmounting and losing unsent input or unsaved forms. New-result indication must not switch focus or selected tab automatically.
- [ ] Build explicit empty/loading/draft/stale/failed displays. Every example carries `Scripted model / Fixture evidence` labeling. Read-only views never dispatch generation.
- [ ] Add tests for preserved input/selection and semantic labels; do not snapshot an entire huge DOM. Check keyboard focus and a narrow viewport manually.
- [ ] Use simple typography, spacing, and restrained colors; if original Uplisted assets are unavailable, use a text wordmark and system font. The empty-repo build must not depend on original brand files.

**Gate:** `npm --prefix web run test`; `check`; `build`. Inspect desktop and narrow layouts. Save a local screenshot if useful, marked as shell/fixture stage. No claim of working agent integration.

**Interview focus:** The interface lets a human inspect evidence and exercise authority; visual state must reflect actual backend state later.

At completion, report:
- Implemented behavior and changed files.
- Exact commands executed and observed results; explicitly identify unrun checks.
- Which failure cases the tests exercise and what they do not prove.
- Any deviations or unresolved issues.
- A short explanation I can use in the interview.

Update `docs/BUILD-PROGRESS.md`. Inspect the diff and whitespace checks. Prepare a scoped checkpoint commit after passing checks and review; do not push or deploy. Stop before the next stage. Do not fill benchmark fields with invented numbers.


Learning checkpoint: read `learning/sections/02-evidence.md` before implementation. After the stage gate, fill `learning/checkpoints/04.md` with actual code/test evidence, explain the change, ask two short teach-back questions, and stop. Track learning separately from implementation. Use `./scripts/with-tools.sh` for each terminal command.
