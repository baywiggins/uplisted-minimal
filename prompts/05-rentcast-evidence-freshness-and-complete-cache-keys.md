# Copilot stage 05

Read COPILOT-START.md, AGENTS.md, docs/08-microsoft-agent-framework.md and the mapped learning section/checkpoint first. Execute only this stage. Teach concepts before asking one optional understanding question at a time. Record actual results and stop.

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
