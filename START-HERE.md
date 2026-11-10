# Uplisted interview project: Copilot handoff

Drafted November 7, 2026. This is a complete implementation specification and staged prompt pack, **not an implemented or tested application**. The prepared repository contains the handoff and tooling; application code is not yet implemented. Nothing depends on access to the original Uplisted repository, its credentials, or previous Codex chats.

## The project you will build

A single-screen rental-listing assistant: ask for a task, inspect its evidence and drafts, make corrections, and approve an exact review snapshot in the same workspace. It can use RentCast evidence, calculate illustrative rent options, create a schematic floorplan, make a photo shot list, draft grounded listing copy, and prepare a review bundle. Approval belongs to the human; external publication is absent.

**Interview thesis:** “I built a constrained agent and evaluated whether it accomplished the user's task without exceeding its authority. I separated model judgment from deterministic validation, recorded failures, and tested the controls that protect state and evidence.”

The required target is now Azure: Python/FastAPI/Pydantic with PostgreSQL locally and in Azure, React/TypeScript/Vite, a Microsoft Agent Framework agent with seven policy-wrapped tools, Azure OpenAI model access through Microsoft Foundry, and a real authenticated Container Apps deployment. Entra ID, managed identity, Key Vault, telemetry and cost/cleanup are part of the build. Stage 18 adds actual Foundry Agent Service experience separately from the main coordinator. Copilot remains the coding assistant, not the runtime agent.

## This folder is ready

The copy/setup step has already been done. Open `uplisted-interview.code-workspace` in VS Code and prompt Copilot: **Read COPILOT-START.md and begin Stage 00.** It should teach Stage 00, run its prerequisite check and stop at the learning checkpoint. Stage 01 starts implementation after you continue. You do not need to paste each document or copy the individual stage prompts.

Use [README.md](README.md) for the short entry point and [the eight-section learning map](learning/README.md) to understand the implementation. Later, “Continue” authorizes only the next numbered stage. The 20 stage prompts (00–19) remain available for detailed reference.


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
| [06-azure-architecture.md](docs/06-azure-architecture.md) | Required resource topology, identity, deployment, observability and cleanup |
| [07-foundry-agent-lab.md](docs/07-foundry-agent-lab.md) | Separate managed-agent experiment and comparison |
| [Azure owner setup](docs/AZURE-OWNER-SETUP.md) | Account, region, reviewer, budget and expiry inputs needed later |
| [fixtures](fixtures/property-case.json) | Explicitly synthetic examples; not live-provider evidence |
| [development scenarios](evals/dev/scenarios.jsonl) | Public development specifications; not an unseen holdout |

When documents appear inconsistent: product goals come from 01; names, limits, interfaces, and state semantics come from 02; evaluation definitions come from 04. Stop the affected stage, identify the conflict, and amend the documents together. Do not silently choose a new architecture. The previous Uplisted proposal is background; this pack contains the implementation decisions needed from zero.

## Build sequence

| Stage | Deliverable |
|---|---|
| [00](prompts/00-start.md) | Orientation and MAF mental model |
| [01](prompts/01-bootable-project-and-reproducible-commands.md) | Bootable project and reproducible commands |
| [02](prompts/02-typed-facts-provenance-and-artifact-contracts.md) | Typed facts, provenance, and artifact contracts |
| [03](prompts/03-versioned-state-concurrency-and-idempotency.md) | Versioned state, concurrency, and idempotency |
| [04](prompts/04-single-screen-shell-and-human-inspection.md) | Single-screen shell and human inspection |
| [05](prompts/05-rentcast-evidence-freshness-and-complete-cache-keys.md) | RentCast evidence, freshness, and complete cache keys |
| [06](prompts/06-deterministic-illustrative-pricing.md) | Deterministic illustrative pricing |
| [07](prompts/07-typed-floorplan-intent-and-safe-schematic-rendering.md) | Typed floorplan intent and safe schematic rendering |
| [08](prompts/08-photo-plan-and-controlled-grounded-listing.md) | Photo plan and controlled grounded listing |
| [09](prompts/09-closed-tool-registry-and-shared-policy-enforcement.md) | Closed tool registry and shared policy enforcement |
| [10](prompts/10-coordinator-budgets-cancellation-and-fixed-baseline.md) | Coordinator, budgets, cancellation, and fixed baseline |
| [11](prompts/11-human-review-api-and-complete-one-screen-flow.md) | Human review API and complete one-screen flow |
| [12](prompts/12-independent-evaluation-harness-and-grader-self-tests.md) | Independent evaluation harness and grader self-tests |
| [13](prompts/13-azure-openai-model-integration-and-model-resource-setup.md) | Azure OpenAI model integration and model-resource setup |
| [14](prompts/14-baseline-comparison-failure-analysis-and-frozen-holdout.md) | Baseline comparison, failure analysis, and frozen holdout |
| [15](prompts/15-azure-identity-persistent-sessions-and-process-ownership.md) | Azure identity, persistent sessions and process ownership |
| [16](prompts/16-azure-infrastructure-image-telemetry-and-deployment-runbook.md) | Azure infrastructure, image, telemetry and deployment runbook |
| [17](prompts/17-deploy-and-verify-the-azure-prototype.md) | Deploy and verify the Azure prototype |
| [18](prompts/18-build-and-compare-a-managed-foundry-agent.md) | Build and compare a managed Foundry agent |
| [19](prompts/19-clean-checkout-verification-and-rehearsal.md) | Clean-checkout verification and rehearsal |

There is no calendar deadline built into the plan. Advance by evidence, not by elapsed time. Stages 02–03 and 09–18 contain the main interview material, including the required Azure deployment and managed-agent comparison. The UI makes those decisions visible; spending extra time on visual polish should not displace the evaluation work.

## The rule for every Copilot stage

Ask it to summarize the relevant contracts, implement only the current stage, run the named checks, and provide changed files, actual commands/results, unresolved issues, and one interview lesson. Require a checkpoint commit only after reviewing passing output. Never let it turn a failing assertion into a passing one by weakening the requirement, hide a live-provider failure behind a fixture, or populate a benchmark table with invented values.

This pack reduces ambiguity. It does not guarantee correct generated code; the acceptance gates and your review remain necessary.

## Required Microsoft Agent Framework

The main agent uses MAF for model/tool orchestration from Stage 01, with a scripted framework client before Azure access. Application services enforce permissions, budgets, validation and approval. Begin with Stage 00 orientation. See [MAF runtime contract](docs/08-microsoft-agent-framework.md).
