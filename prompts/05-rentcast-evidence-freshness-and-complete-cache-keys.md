# Copilot prompt: Stage 05 — RentCast evidence, freshness, and complete cache keys

Implement only Stage 05. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md`, the product brief, relevant canonical contracts/evaluation rules, and Azure architecture `docs/06-azure-architecture.md`. Inspect actual code and check results before editing. Use PostgreSQL and the Azure model/deployment architecture specified in the current documents.

Start by listing the contracts and files this stage touches. If a prerequisite is incomplete, report the exact missing interface/check and repair it before dependent implementation. Use the existing design. Do not create billable resources until the relevant cloud stage has the owner-supplied scope/limits; do not ask again for authorization already supplied for that scope.

The stage specification follows verbatim:

## Stage 05 — RentCast evidence, freshness, and complete cache keys

**Files:** create `providers/base.py`, `providers/scripted.py`, `providers/rentcast.py`, `domain/evidence.py`; `tests/unit/test_evidence.py`; `tests/integration/test_rentcast_adapter.py`.

**Consumes:** PropertySnapshot, ResourceRef, repository acceptance, synthetic normalized evidence fixture, contracts §4 evidence policies.

**Produces:** `RentCastGateway.fetch(request: RentRequest) -> RentEvidence`; `build_rent_request(snapshot) -> RentRequest`; `evaluate_evidence(evidence, snapshot, clock) -> EvidenceAssessment`; fixture gateway; cache interface/key function. Live HTTP adapter stays disabled until Stage 13.

- [ ] Write request mapping tests: unit retained; 2 full + 1 half maps to 2.5; edited sqft changes cache key; provider mode/parameters affect key; no identity fields supplied by model.
- [ ] Implement conservative matching and missing-unit clarification. Wrong/unknown unit cannot yield accepted matched evidence. Preserve provider subject observations separately from confirmed facts.
- [ ] Implement age/unit/unique-comparable checks and 24-hour cache TTL. Test fresh fetch with old source dates, unknown dates, duplicate comp IDs, incompatible units, malformed money, and cached fixture/live distinction.
- [ ] Use injected HTTP/mock transport tests to define 429, 500, malformed body, and dispatched-timeout outcomes. No automatic retries in v1. Record unknown external outcome where dispatch may have been accepted.
- [ ] Ensure failures do not install an artifact or silently synthesize successful evidence. No provider call on startup/view selection. Tests assert actual adapter attempt counters.

**Gate:** `uv run pytest -q tests/unit/test_evidence.py tests/integration/test_rentcast_adapter.py`; lint/type checks. Tests use no real credentials or external sockets.

**Interview focus:** Explain estimate/range versus calibrated confidence, observed date versus fetch date, and why cache keys include all effective request inputs.

At completion, report changed files, actual commands/results, unrun checks, what the tests prove, unresolved issues, and the interview lesson. Update `docs/BUILD-PROGRESS.md`, inspect the diff, and prepare a scoped checkpoint after verification. Do not push, deploy unrelated resources, or start another stage.

Learning checkpoint: read `learning/sections/02-evidence.md` before implementation. Fill `learning/checkpoints/05.md` with real code/test evidence, explain one path and test, ask two short questions, and stop. Use `./scripts/with-tools.sh` for terminal commands. Track learning separately from implementation.
