# Uplisted interview project: Copilot handoff

Drafted November 7, 2026. This is a complete implementation specification and staged prompt pack, **not an implemented or tested application**. The prepared repository contains the handoff and tooling; application code is not yet implemented. Nothing depends on access to the original Uplisted repository, its credentials, or previous Codex chats.

## The project you will build

A single-screen rental-listing assistant: ask for a task, inspect its evidence and drafts, make corrections, and approve an exact review snapshot in the same workspace. It can use RentCast evidence, calculate illustrative rent options, create a schematic floorplan, make a photo shot list, draft grounded listing copy, and prepare a review bundle. Approval belongs to the human; external publication is absent.

**Interview thesis:** “I built a constrained agent and evaluated whether it accomplished the user's task without exceeding its authority. I separated model judgment from deterministic validation, recorded failures, and tested the controls that protect state and evidence.”

The chosen defaults in this draft are Python/FastAPI/Pydantic/SQLite, React/TypeScript/Vite, a small explicit tool loop, and fixture-first development. These are design recommendations made for this handoff. Copilot is your coding assistant, not the application's runtime model. The real-model adapter, required for the final model-evaluation milestone, uses the Anthropic Messages API behind an interface; replacing it with Azure-hosted inference is an extension, not a prerequisite for demonstrating engineering judgment at Microsoft.

## This folder is ready

The copy/setup step has already been done. Open `uplisted-interview.code-workspace` in VS Code and prompt Copilot: **Read COPILOT-START.md and begin Stage 01.** It should implement one stage, run checks, explain the result, and stop for your learning checkpoint. You do not need to paste each document or copy the individual stage prompts.

Use [README.md](README.md) for the short entry point and [the six-section learning map](learning/README.md) to understand the implementation. Later, “Continue” authorizes only the next numbered stage. The original 15 prompts remain available for detailed reference.


GitHub supports repository-wide guidance in `.github/copilot-instructions.md`, with availability varying by surface. Explicitly include the relevant stage and specification in context rather than assuming automatic discovery. [GitHub documentation](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions).

## Documents and authority

| File | Purpose |
|---|---|
| [01-product-brief.md](docs/01-product-brief.md) | Product, scope, single-screen experience, and interview emphasis |
| [02-contracts.md](docs/02-contracts.md) | Canonical types, tool contracts, state, security, budgets, APIs, and commands |
| [03-build-plan.md](docs/03-build-plan.md) | Ordered implementation stages, exact files/interfaces, tests, and acceptance gates |
| [04-evaluation-plan.md](docs/04-evaluation-plan.md) | Graders, scenarios, measurement, comparison, and reporting rules |
| [05-interview-playbook.md](docs/05-interview-playbook.md) | Talk outline, live demo script, follow-up questions, and evidence checklist |
| [.github/copilot-instructions.md](.github/copilot-instructions.md) | Short persistent instructions to the development agent |
| [fixtures](fixtures/property-case.json) | Explicitly synthetic examples; not live-provider evidence |
| [development scenarios](evals/dev/scenarios.jsonl) | Public development specifications; not an unseen holdout |

When documents appear inconsistent: product goals come from 01; names, limits, interfaces, and state semantics come from 02; evaluation definitions come from 04. Stop the affected stage, identify the conflict, and amend the documents together. Do not silently choose a new architecture. The previous Uplisted proposal is background; this pack contains the implementation decisions needed from zero.

## Build sequence

| Stage | Deliverable | What you should be able to explain |
|---|---|---|
| [01](prompts/01-bootable-project-and-reproducible-commands.md) | Bootable project and offline checks | Reproducibility and separation of fixture/live modes |
| [02](prompts/02-typed-facts-provenance-and-artifact-contracts.md) | Typed facts, artifacts, and synthetic fixtures | Provenance; unknown versus false; schemas versus truth |
| [03](prompts/03-versioned-state-concurrency-and-idempotency.md) | Versioned SQLite state and idempotency | Transactions, stale writes, duplicate requests |
| [04](prompts/04-single-screen-shell-and-human-inspection.md) | Single-screen UI shell | Human inspection and control without a wizard |
| [05](prompts/05-rentcast-evidence-freshness-and-complete-cache-keys.md) | RentCast evidence adapter and cache | Source matching, units, freshness, missing evidence |
| [06](prompts/06-deterministic-illustrative-pricing.md) | Deterministic pricing | Business rules versus model judgment |
| [07](prompts/07-typed-floorplan-intent-and-safe-schematic-rendering.md) | Floorplan generation and renderer | Semantic accuracy versus schematic validity |
| [08](prompts/08-photo-plan-and-controlled-grounded-listing.md) | Photos and grounded listing copy | Generated assumptions cannot become property facts |
| [09](prompts/09-closed-tool-registry-and-shared-policy-enforcement.md) | Tool dispatcher and execution policy | The model proposes; the server authorizes |
| [10](prompts/10-coordinator-budgets-cancellation-and-fixed-baseline.md) | Coordinator, budgets, cancellation | Agent behavior versus workflow; bounded recovery |
| [11](prompts/11-human-review-api-and-complete-one-screen-flow.md) | Human review API and browser integration | Exact-version approval; race conditions |
| [12](prompts/12-independent-evaluation-harness-and-grader-self-tests.md) | Independent evaluation harness | Outcome, trajectory, grader validity, reproducibility |
| [13](prompts/13-real-model-adapter-and-optional-live-rentcast.md) | Real-model adapter/evaluation and optional live RentCast | What simulation proves and what it cannot prove |
| [14](prompts/14-baseline-comparison-failure-analysis-and-frozen-holdout.md) | Comparison, failure analysis, and regression evidence | Measured improvement and remaining uncertainty |
| [15](prompts/15-clean-checkout-verification-and-rehearsal.md) | Clean-checkout verification and interview rehearsal | Demonstrable results and honest limitations |

There is no calendar deadline built into the plan. Advance by evidence, not by elapsed time. Stages 02–03 and 09–14 contain the main interview material. The UI makes those decisions visible; spending extra time on visual polish should not displace the evaluation work.

## The rule for every Copilot stage

Ask it to summarize the relevant contracts, implement only the current stage, run the named checks, and provide changed files, actual commands/results, unresolved issues, and one interview lesson. Require a checkpoint commit only after reviewing passing output. Never let it turn a failing assertion into a passing one by weakening the requirement, hide a live-provider failure behind a fixture, or populate a benchmark table with invented values.

This pack reduces ambiguity. It does not guarantee correct generated code; the acceptance gates and your review remain necessary.
