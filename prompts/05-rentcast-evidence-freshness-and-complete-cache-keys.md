# Copilot prompt: Stage 05 — RentCast evidence, freshness, and complete cache keys

Implement only Stage 05. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md` if it exists, the product brief, the relevant canonical contracts, and this stage's evaluation requirements. Inspect the actual current code and previous check results before editing. Do not assume a previous stage is complete because a chat said so.

Start by listing the contracts this change relies on and the files you will touch. If a prerequisite stage is incomplete, report the exact missing interface/check and repair that prerequisite before dependent implementation. Keep the chosen architecture.

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

At completion, report:
- Implemented behavior and changed files.
- Exact commands executed and observed results; explicitly identify unrun checks.
- Which failure cases the tests exercise and what they do not prove.
- Any deviations or unresolved issues.
- A short explanation I can use in the interview.

Update `docs/BUILD-PROGRESS.md`. Inspect the diff and whitespace checks. Prepare a scoped checkpoint commit after passing checks and review; do not push or deploy. Stop before the next stage. Do not fill benchmark fields with invented numbers.


Learning checkpoint: read `learning/sections/02-evidence.md` before implementation. After the stage gate, fill `learning/checkpoints/05.md` with actual code/test evidence, explain the change, ask two short teach-back questions, and stop. Track learning separately from implementation. Use `./scripts/with-tools.sh` for each terminal command.
