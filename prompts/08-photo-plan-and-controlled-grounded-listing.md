# Copilot prompt: Stage 08 — Photo plan and controlled grounded listing

Implement only Stage 08. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md`, the product brief, relevant canonical contracts/evaluation rules, and Azure architecture `docs/06-azure-architecture.md`. Inspect actual code and check results before editing. Use PostgreSQL and the Azure model/deployment architecture specified in the current documents.

Start by listing the contracts and files this stage touches. If a prerequisite is incomplete, report the exact missing interface/check and repair it before dependent implementation. Use the existing design. Do not create billable resources until the relevant cloud stage has the owner-supplied scope/limits; do not ask again for authorization already supplied for that scope.

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

At completion, report changed files, actual commands/results, unrun checks, what the tests prove, unresolved issues, and the interview lesson. Update `docs/BUILD-PROGRESS.md`, inspect the diff, and prepare a scoped checkpoint after verification. Do not push, deploy unrelated resources, or start another stage.

Learning checkpoint: read `learning/sections/03-grounding.md` before implementation. Fill `learning/checkpoints/08.md` with real code/test evidence, explain one path and test, ask two short questions, and stop. Use `./scripts/with-tools.sh` for terminal commands. Track learning separately from implementation.
