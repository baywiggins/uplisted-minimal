# Human inspection and usable evidence

Stages 04, 05, 06. This section groups concepts for learning; implement **one numbered stage per turn**, not the whole section.

## What you are learning

The screen displays backend state and gives the human control. External evidence has its own identity, dates, units, and limitations. Pricing performs explainable arithmetic on acceptable evidence; it does not discover an optimal rent or silently change the confirmed asking price.

## How the stages build on each other

- 04: Build the one-screen shell without triggering provider calls from navigation.
- 05: Normalize identity, preserve source dates, and include all effective inputs in cache keys.
- 06: Calculate illustrative scenarios exactly; keep them separate from confirmed asking price.

| Stage | Copy-ready implementation prompt | Record your understanding |
|---|---|---|
| 04 | [Single-screen shell and human inspection](../../prompts/04-single-screen-shell-and-human-inspection.md) | [Learning checkpoint](../checkpoints/04.md) |
| 05 | [RentCast evidence, freshness, and complete cache keys](../../prompts/05-rentcast-evidence-freshness-and-complete-cache-keys.md) | [Learning checkpoint](../checkpoints/05.md) |
| 06 | [Deterministic illustrative pricing](../../prompts/06-deterministic-illustrative-pricing.md) | [Learning checkpoint](../checkpoints/06.md) |

## Trace this after implementation

Confirmed snapshot → build_rent_request → complete cache key → fixture/provider response → evaluate_evidence → accepted evidence → calculate_pricing → Pricing view with dates and monthly units.

Before code exists, this is the intended path. After implementation, Copilot should show the actual functions and state changes in your repository.

## Check your understanding

1. Why can a response fetched today still contain stale evidence?
2. What separates an illustrative pricing scenario from confirmed asking rent?

Ask Copilot to walk through the relevant example if either answer is unclear. You can skip the questions explicitly; passing tests alone must not be recorded as understanding.

## Interview takeaway

“Freshness, request identity, and units determine whether evidence is usable; deterministic code handles the arithmetic.”

Use this wording only when you can explain and demonstrate the implemented behavior.

[Back to the learning map](../README.md)
