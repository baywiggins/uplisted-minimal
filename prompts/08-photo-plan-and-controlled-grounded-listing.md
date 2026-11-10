# Copilot stage 08

Read COPILOT-START.md, AGENTS.md, docs/08-microsoft-agent-framework.md and the mapped learning section/checkpoint first. Execute only this stage. Teach concepts before asking one optional understanding question at a time. Record actual results and stop.

## Stage 08 — Photo plan and controlled grounded listing

**Files:** create `domain/photos.py`, `domain/listing.py`; `tests/unit/test_photos.py`, `test_listing.py`; `web/src/views/PhotosView.tsx`, `ListingView.tsx` with focused tests.

**Consumes:** current validated FloorPlanPayload; PublicFact set; structured generation interface; template IDs from contracts §4.

**Produces:** `build_shot_plan(plan) -> PhotoPlanPayload`; `validate_listing_intent(intent, public_facts) -> ValidatedListingIntent`; `render_listing(intent, public_facts) -> ListingPayload`; helper selecting typed claims/order.

- [ ] Implement two deterministic cards per eligible room, exact room IDs and source-plan revision. Assert no shots for nonexistent rooms, stale plans, halls/stairs, or unsupported garage.
- [ ] Implement the six controlled templates. Reject free-text fields, unknown template IDs, wrong fact paths, wrong-case/revision refs, comparable facts, and assumptions as citations. Handle zero/one/plural grammar and separate full/half baths.
- [ ] Add tests for no asking-rent claim unless confirmed; no garage if false/unknown; wrong selected fact cannot be rendered as a supported sentence. Preserve raw rejected helper output.
- [ ] Implement the listing editor as supported sentence selection/removal/reordering, not arbitrary prose entry. Clicking a sentence reveals supporting fact value, source revision, and provenance in place.
- [ ] Keep assistant summaries outside the artifact truth guarantee; create negative examples for later semantic grading. Do not add a “legally compliant” badge.

**Gate:** `uv run pytest -q tests/unit/test_photos.py tests/unit/test_listing.py`; frontend tests/check/build. The three-bed sample must not acquire the comparable's garage.

**Interview focus:** Grounding is a data-flow constraint. Explain the restricted grammar tradeoff and the evaluation needed before allowing broader prose.
