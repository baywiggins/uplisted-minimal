# Copilot prompt: Stage 07 — Typed floorplan intent and safe schematic rendering

Implement only Stage 07. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md` if it exists, the product brief, the relevant canonical contracts, and this stage's evaluation requirements. Inspect the actual current code and previous check results before editing. Do not assume a previous stage is complete because a chat said so.

Start by listing the contracts this change relies on and the files you will touch. If a prerequisite stage is incomplete, report the exact missing interface/check and repair that prerequisite before dependent implementation. Keep the chosen architecture.

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

At completion, report:
- Implemented behavior and changed files.
- Exact commands executed and observed results; explicitly identify unrun checks.
- Which failure cases the tests exercise and what they do not prove.
- Any deviations or unresolved issues.
- A short explanation I can use in the interview.

Update `docs/BUILD-PROGRESS.md`. Inspect the diff and whitespace checks. Prepare a scoped checkpoint commit after passing checks and review; do not push or deploy. Stop before the next stage. Do not fill benchmark fields with invented numbers.


Learning checkpoint: read `learning/sections/03-grounding.md` before implementation. After the stage gate, fill `learning/checkpoints/07.md` with actual code/test evidence, explain the change, ask two short teach-back questions, and stop. Track learning separately from implementation. Use `./scripts/with-tools.sh` for each terminal command.
