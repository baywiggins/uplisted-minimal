# Copilot prompt: Stage 07 — Typed floorplan intent and safe schematic rendering

Implement only Stage 07. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md`, the product brief, relevant canonical contracts/evaluation rules, and Azure architecture `docs/06-azure-architecture.md`. Inspect actual code and check results before editing. Use PostgreSQL and the Azure model/deployment architecture specified in the current documents.

Start by listing the contracts and files this stage touches. If a prerequisite is incomplete, report the exact missing interface/check and repair it before dependent implementation. Use the existing design. Do not create billable resources until the relevant cloud stage has the owner-supplied scope/limits; do not ask again for authorization already supplied for that scope.

The stage specification follows verbatim:

## Stage 07 — Typed floorplan intent and safe schematic rendering

**Files:** create `domain/floorplan.py`; add structured-generation protocol to `providers/base.py` and scripted implementation; `tests/unit/test_floorplan.py`, `tests/integration/test_floorplan_generation.py`; `web/src/views/FloorplanView.tsx`, `web/tests/floorplan.test.tsx`.

**Consumes:** PropertySnapshot and confirmed description, shared model-attempt interface, supplied FloorPlanIntent example.

**Produces:** `validate_intent(intent, snapshot) -> ValidatedIntent`; `compile_schematic(intent) -> Schematic`; `generate_floorplan(ctx, snapshot, gateway, budget) -> FloorPlanPayload`. Until Stage 10, use an injected test budget implementing the eventual reservation interface.

- [ ] Define semantic models and tests for exact bedrooms/full baths/half baths, duplicate IDs, invalid levels, too many rooms, false garage, unsupported dimensions, and conflicting description/counts.
- [ ] Implement deterministic per-level grid compiler and independent bounds/non-overlap/reference assertions. Physical feet and screen coordinates must be separate fields.
- [ ] Implement scripted helper generation, raw attempt capture, at most one repair, and typed failure. Do not silently add missing required rooms to turn a failed first response into a raw pass.
- [ ] Render only accepted compiled data via React/SVG elements. Escape labels; reject model markup as a geometry source. A label containing `<script>` must display harmlessly or fail validation, not execute.
- [ ] Add visible schematic/unknown-dimension labels and an in-place room-label edit form. Confirm measurements through the inline property form as typed RoomMeasurement entries, creating a new property revision before regeneration. Test a free-text description alone cannot create accepted dimensions, and matching user-confirmed dimensions survive regeneration. Unsaved changes cannot mark an artifact approved.

**Gate:** `uv run pytest -q tests/unit/test_floorplan.py tests/integration/test_floorplan_generation.py`; frontend tests/check/build. Inspect both levels and unknown dimension display.

**Interview focus:** Distinguish semantic intent accuracy, renderer validity, and actual physical fidelity. Show what each test can and cannot establish.

At completion, report changed files, actual commands/results, unrun checks, what the tests prove, unresolved issues, and the interview lesson. Update `docs/BUILD-PROGRESS.md`, inspect the diff, and prepare a scoped checkpoint after verification. Do not push, deploy unrelated resources, or start another stage.

Learning checkpoint: read `learning/sections/03-grounding.md` before implementation. Fill `learning/checkpoints/07.md` with real code/test evidence, explain one path and test, ask two short questions, and stop. Use `./scripts/with-tools.sh` for terminal commands. Track learning separately from implementation.
