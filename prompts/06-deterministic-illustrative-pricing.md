# Copilot prompt: Stage 06 — Deterministic illustrative pricing

Implement only Stage 06. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md`, the product brief, relevant canonical contracts/evaluation rules, and Azure architecture `docs/06-azure-architecture.md`. Inspect actual code and check results before editing. Use PostgreSQL and the Azure model/deployment architecture specified in the current documents.

Start by listing the contracts and files this stage touches. If a prerequisite is incomplete, report the exact missing interface/check and repair it before dependent implementation. Use the existing design. Do not create billable resources until the relevant cloud stage has the owner-supplied scope/limits; do not ask again for authorization already supplied for that scope.

The stage specification follows verbatim:

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

At completion, report changed files, actual commands/results, unrun checks, what the tests prove, unresolved issues, and the interview lesson. Update `docs/BUILD-PROGRESS.md`, inspect the diff, and prepare a scoped checkpoint after verification. Do not push, deploy unrelated resources, or start another stage.

Learning checkpoint: read `learning/sections/02-evidence.md` before implementation. Fill `learning/checkpoints/06.md` with real code/test evidence, explain one path and test, ask two short questions, and stop. Use `./scripts/with-tools.sh` for terminal commands. Track learning separately from implementation.
