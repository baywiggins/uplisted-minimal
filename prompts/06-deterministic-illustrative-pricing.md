# Copilot stage 06

Read COPILOT-START.md, AGENTS.md, docs/08-microsoft-agent-framework.md and the mapped learning section/checkpoint first. Execute only this stage. Teach concepts before asking one optional understanding question at a time. Record actual results and stop.

## Stage 06 — Deterministic illustrative pricing

**Files:** create `domain/pricing.py`; `tests/unit/test_pricing.py`; implement `web/src/views/PricingView.tsx` and its focused test.

**Consumes:** current RentEvidence, EvidenceAssessment, contracts §4 pricing.

**Produces:** `calculate_pricing(evidence: RentEvidence) -> PricingPayload` with three named illustrative scenarios and calculation provenance. Domain function raises/returns the shared typed domain error; dispatcher converts it to ToolResult later.

- [ ] Assert 300000 cents gives exactly 291000/300000/309000 cents. Add an odd-cent rounding case calculated independently with Decimal ROUND_HALF_UP.
- [ ] Reject insufficient usable comps, stale source/fetch, unknown/mismatched subject, missing estimate, invalid range order, and wrong units. A provider range is displayed separately from scenario multipliers.
- [ ] Render monthly USD units, evidence dates, scenario calculation, and limitations. Never label a count-based score `confidence`.
- [ ] Test that generating/selecting scenarios does not mutate confirmed `asking_rent_cents`. Human confirmation occurs through the property form later.

**Gate:** `uv run pytest -q tests/unit/test_pricing.py`; frontend focused tests/check/build. No model is needed to do this arithmetic.

**Interview focus:** A model is useful for deciding whether pricing is needed; deterministic code is easier to verify for the calculation itself.
