# Copilot stage 07

Read COPILOT-START.md, AGENTS.md, docs/08-microsoft-agent-framework.md and the mapped learning section/checkpoint first. Execute only this stage. Teach concepts before asking one optional understanding question at a time. Record actual results and stop.

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
