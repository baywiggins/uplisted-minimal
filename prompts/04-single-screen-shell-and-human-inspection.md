# Copilot prompt: Stage 04 — Single-screen shell and human inspection

Implement only Stage 04. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md`, the product brief, relevant canonical contracts/evaluation rules, and Azure architecture `docs/06-azure-architecture.md`. Inspect actual code and check results before editing. Use PostgreSQL and the Azure model/deployment architecture specified in the current documents.

Start by listing the contracts and files this stage touches. If a prerequisite is incomplete, report the exact missing interface/check and repair it before dependent implementation. Use the existing design. Do not create billable resources until the relevant cloud stage has the owner-supplied scope/limits; do not ask again for authorization already supplied for that scope.

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

At completion, report changed files, actual commands/results, unrun checks, what the tests prove, unresolved issues, and the interview lesson. Update `docs/BUILD-PROGRESS.md`, inspect the diff, and prepare a scoped checkpoint after verification. Do not push, deploy unrelated resources, or start another stage.

Learning checkpoint: read `learning/sections/02-evidence.md` before implementation. Fill `learning/checkpoints/04.md` with real code/test evidence, explain one path and test, ask two short questions, and stop. Use `./scripts/with-tools.sh` for terminal commands. Track learning separately from implementation.
