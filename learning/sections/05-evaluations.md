# Testing the agent and the evaluator

Stages 12, 13, 14. This section groups concepts for learning; implement **one numbered stage per turn**, not the whole section.

## What you are learning

Application tests establish specified software behavior. Real-model trials measure decisions under a recorded configuration. The evaluator inspects persisted outcomes independently and needs its own failure tests. Comparisons use the same tasks and account for failures, repeated trials, and unknown costs.

## How the stages build on each other

- 12: Build isolated trials, independent graders, and failure-detecting harness tests.
- 13: Add the real model; distinguish frozen evidence from optional live RentCast.
- 14: Compare fairly, investigate failures, and evaluate fresh holdout cases separately.

| Stage | Copy-ready implementation prompt | Record your understanding |
|---|---|---|
| 12 | [Independent evaluation harness and grader self-tests](../../prompts/12-independent-evaluation-harness-and-grader-self-tests.md) | [Learning checkpoint](../checkpoints/12.md) |
| 13 | [Real model adapter and optional live RentCast](../../prompts/13-real-model-adapter-and-optional-live-rentcast.md) | [Learning checkpoint](../checkpoints/13.md) |
| 14 | [Baseline comparison, failure analysis, and frozen holdout](../../prompts/14-baseline-comparison-failure-analysis-and-frozen-holdout.md) | [Learning checkpoint](../checkpoints/14.md) |

## Trace this after implementation

Development case → fresh trial database/budget/cache → agent or baseline → stored outputs/trace → independent graders → semantic review → finalized report → comparison and retained failure analysis.

Before code exists, this is the intended path. After implementation, Copilot should show the actual functions and state changes in your repository.

## Check your understanding

1. Why does a passing scripted run not establish real-model reliability?
2. How would you prove that a grader detects a wrong bedroom count even when the citation exists?

Ask Copilot to walk through the relevant example if either answer is unclear. You can skip the questions explicitly; passing tests alone must not be recorded as understanding.

## Interview takeaway

“I evaluate outcomes and tool behavior, test the graders, preserve unsuccessful trials, and report exactly what the evidence supports.”

Use this wording only when you can explain and demonstrate the implemented behavior.

[Back to the learning map](../README.md)
