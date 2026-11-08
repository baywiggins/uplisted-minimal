# Copilot prompt: Stage 06 — Deterministic illustrative pricing

Implement only Stage 06. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md` if it exists, the product brief, the relevant canonical contracts, and this stage's evaluation requirements. Inspect the actual current code and previous check results before editing. Do not assume a previous stage is complete because a chat said so.

Start by listing the contracts this change relies on and the files you will touch. If a prerequisite stage is incomplete, report the exact missing interface/check and repair that prerequisite before dependent implementation. Keep the chosen architecture.

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

At completion, report:
- Implemented behavior and changed files.
- Exact commands executed and observed results; explicitly identify unrun checks.
- Which failure cases the tests exercise and what they do not prove.
- Any deviations or unresolved issues.
- A short explanation I can use in the interview.

Update `docs/BUILD-PROGRESS.md`. Inspect the diff and whitespace checks. Prepare a scoped checkpoint commit after passing checks and review; do not push or deploy. Stop before the next stage. Do not fill benchmark fields with invented numbers.


Learning checkpoint: read `learning/sections/02-evidence.md` before implementation. After the stage gate, fill `learning/checkpoints/06.md` with actual code/test evidence, explain the change, ask two short teach-back questions, and stop. Track learning separately from implementation. Use `./scripts/with-tools.sh` for each terminal command.
