# Grounded artifacts and constrained generation

Stages 07, 08. This section groups concepts for learning; implement **one numbered stage per turn**, not the whole section.

## What you are learning

The model proposes structured intent. Ordinary code validates and renders the result. Room semantics, screen geometry, and measured physical accuracy are different claims. Listing sentences can draw only from confirmed subject facts; nearby comparable properties cannot supply missing features.

## How the stages build on each other

- 07: Validate room intent, then compile safe schematic geometry; confirm measurements through property facts.
- 08: Bind photos to real room IDs and factual sentences to allowed subject facts.

| Stage | Copy-ready implementation prompt | Record your understanding |
|---|---|---|
| 07 | [Typed floorplan intent and safe schematic rendering](../../prompts/07-typed-floorplan-intent-and-safe-schematic-rendering.md) | [Learning checkpoint](../checkpoints/07.md) |
| 08 | [Photo plan and controlled grounded listing](../../prompts/08-photo-plan-and-controlled-grounded-listing.md) | [Learning checkpoint](../checkpoints/08.md) |

## Trace this after implementation

Confirmed facts → build_public_facts → model-selected template IDs/fact references → validate_listing_intent → render_listing → sentence selection → supporting fact and source revision.

Before code exists, this is the intended path. After implementation, Copilot should show the actual functions and state changes in your repository.

## Check your understanding

1. Why can a correctly drawn schematic still fail to match the building’s real dimensions?
2. How can a real citation accompany a false sentence, and which checks address that risk?

Ask Copilot to walk through the relevant example if either answer is unclear. You can skip the questions explicitly; passing tests alone must not be recorded as understanding.

## Interview takeaway

“Grounding depends on controlled data flow and validation. Restricted listing grammar makes the initial system easier to verify.”

Use this wording only when you can explain and demonstrate the implemented behavior.

[Back to the learning map](../README.md)
