# Foundations: a system that remembers safely

Stages 01, 02, 03. This section groups concepts for learning; implement **one numbered stage per turn**, not the whole section.

## What you are learning

The project needs a reproducible environment, clearly defined data, and a database that preserves history. A valid data shape does not establish truth or permission. Revisions identify exactly which facts an output used; transactions prevent a slow result from replacing a newer edit.

## How the stages build on each other

- 01: Get reproducible commands running; do not confuse readiness with a finished feature.
- 02: Represent unknown, false, confirmed, and assumed data distinctly.
- 03: Store revisions; make stale writes and duplicate commands behave predictably.

| Stage | Copy-ready implementation prompt | Record your understanding |
|---|---|---|
| 01 | [Bootable project and reproducible commands](../../prompts/01-bootable-project-and-reproducible-commands.md) | [Learning checkpoint](../checkpoints/01.md) |
| 02 | [Typed facts, provenance, and artifact contracts](../../prompts/02-typed-facts-provenance-and-artifact-contracts.md) | [Learning checkpoint](../checkpoints/02.md) |
| 03 | [Versioned state, concurrency, and idempotency](../../prompts/03-versioned-state-concurrency-and-idempotency.md) | [Learning checkpoint](../checkpoints/03.md) |

## Trace this after implementation

Synthetic property JSON → PropertyFacts → immutable property snapshot → artifact with source references and captured destination head → accept_artifact transaction → new head or stale-result rejection.

Before code exists, this is the intended path. After implementation, Copilot should show the actual functions and state changes in your repository.

## Check your understanding

1. Why does passing Pydantic validation not prove that a property fact is true?
2. If property facts stay unchanged, why must acceptance still check the destination artifact’s head?

Ask Copilot to walk through the relevant example if either answer is unclear. You can skip the questions explicitly; passing tests alone must not be recorded as understanding.

## Interview takeaway

“I use explicit data contracts and atomic version checks to protect state; hashes and idempotency keys each solve only part of that problem.”

Use this wording only when you can explain and demonstrate the implemented behavior.

[Back to the learning map](../README.md)
