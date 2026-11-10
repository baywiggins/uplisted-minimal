# Agent decisions, bounded execution, and human approval

Stages 09, 10, 11. This section groups concepts for learning; implement **one numbered stage per turn**, not the whole section.

## What you are learning

The model chooses among seven tools; the server controls their effects. Coordinator, helper, and repair calls share limits. Stop blocks future dispatch and late acceptance but cannot promise to undo an external request. Human approval uses a separate authority path over an exact snapshot.

## How the stages build on each other

- 09: Centralize the allowlist, permissions, validation, and event recording.
- 10: Integrate the MAF decision loop, shared budgets, cancellation, and fair workflow baseline.
- 11: Connect the screen to real backend state and keep human approval separate.

| Stage | Copy-ready implementation prompt | Record your understanding |
|---|---|---|
| 09 | [Closed tool registry and shared policy enforcement](../../prompts/09-closed-tool-registry-and-shared-policy-enforcement.md) | [Learning checkpoint](../checkpoints/09.md) |
| 10 | [Coordinator, budgets, cancellation, and fixed baseline](../../prompts/10-coordinator-budgets-cancellation-and-fixed-baseline.md) | [Learning checkpoint](../checkpoints/10.md) |
| 11 | [Human review API and complete one-screen flow](../../prompts/11-human-review-api-and-complete-one-screen-flow.md) | [Learning checkpoint](../checkpoints/11.md) |

## Trace this after implementation

User request → coordinator proposal → dispatcher allowlist/schema/scope checks → shared budget → domain operation → version-checked acceptance → observation → review bundle → human endpoint → atomic approval receipt.

Before code exists, this is the intended path. After implementation, Copilot should show the actual functions and state changes in your repository.

## Check your understanding

1. If provider text tells the model to approve and publish, where does the system prevent those effects?
2. What happens when Stop is pressed after one artifact is saved and another provider call is in flight?

Ask Copilot to walk through the relevant example if either answer is unclear. You can skip the questions explicitly; passing tests alone must not be recorded as understanding.

## Interview takeaway

“Model discretion is bounded by server authority, shared budgets, and transactions. Approval is a human action over an exact version.”

Use this wording only when you can explain and demonstrate the implemented behavior.

[Back to the learning map](../README.md)
