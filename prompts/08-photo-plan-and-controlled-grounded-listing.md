# Copilot prompt: Stage 08 — Photo plan and controlled grounded listing

Implement only Stage 08. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md` if it exists, the product brief, the relevant canonical contracts, and this stage's evaluation requirements. Inspect the actual current code and previous check results before editing. Do not assume a previous stage is complete because a chat said so.

Start by listing the contracts this change relies on and the files you will touch. If a prerequisite stage is incomplete, report the exact missing interface/check and repair that prerequisite before dependent implementation. Keep the chosen architecture.

The stage specification follows verbatim:

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

At completion, report:
- Implemented behavior and changed files.
- Exact commands executed and observed results; explicitly identify unrun checks.
- Which failure cases the tests exercise and what they do not prove.
- Any deviations or unresolved issues.
- A short explanation I can use in the interview.

Update `docs/BUILD-PROGRESS.md`. Inspect the diff and whitespace checks. Prepare a scoped checkpoint commit after passing checks and review; do not push or deploy. Stop before the next stage. Do not fill benchmark fields with invented numbers.


Learning checkpoint: read `learning/sections/03-grounding.md` before implementation. After the stage gate, fill `learning/checkpoints/08.md` with actual code/test evidence, explain the change, ask two short teach-back questions, and stop. Track learning separately from implementation. Use `./scripts/with-tools.sh` for each terminal command.
