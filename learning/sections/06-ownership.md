# Reproducibility and ownership

Stages 15. This section groups concepts for learning; implement **one numbered stage per turn**, not the whole section.

## What you are learning

The project is ready to demonstrate when a fresh checkout can run it and you can explain its critical decisions. A polished demo does not substitute for measured results. Connect a failure to its cause, mitigation, independent regression, and remaining limitation.

## How the stages build on each other

- 15: Reproduce the project from a clean checkout and rehearse using actual evidence.

| Stage | Copy-ready implementation prompt | Record your understanding |
|---|---|---|
| 15 | [Clean-checkout verification and rehearsal](../../prompts/15-clean-checkout-verification-and-rehearsal.md) | [Learning checkpoint](../checkpoints/15.md) |

## Trace this after implementation

Clean checkout → locked dependencies → synthetic initialization → browser flow → stored evaluation report → corresponding code/test → honest interview explanation.

Before code exists, this is the intended path. After implementation, Copilot should show the actual functions and state changes in your repository.

## Check your understanding

1. Which claims can a fixture demonstration support, and which require real-model trials?
2. For one failure, can you identify its cause, the changed behavior, and the independent evidence that detects recurrence?

Ask Copilot to walk through the relevant example if either answer is unclear. You can skip the questions explicitly; passing tests alone must not be recorded as understanding.

## Interview takeaway

“My ownership is demonstrated by the design, code paths, tests, and evidence I can explain, including where Copilot helped and what remains unverified.”

Use this wording only when you can explain and demonstrate the implemented behavior.

[Back to the learning map](../README.md)
