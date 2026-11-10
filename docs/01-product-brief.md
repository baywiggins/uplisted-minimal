# Uplisted: single-screen listing preparation agent

## Purpose and interview focus

Build a small application that turns a human's property-preparation request into useful, inspectable drafts. The user can ask for a whole rental package or any supported part. The assistant decides which tools are relevant, asks for missing information, and prepares a versioned review request. A human inspects and approves it in place.

The interview email emphasizes **agent design, system design, and evaluations that measure purpose and risk**. Prioritize these demonstrations:

1. **Purpose:** Does the requested outcome actually exist in storage, with the right facts and dependencies? A confident completion message is insufficient.
2. **Tool use:** Does the agent select the needed tools and avoid unrelated work? A photo request should not spend money fetching rent evidence.
3. **Risk:** Can untrusted text, invented facts, stale outputs, duplicate requests, or cancellation cause an unauthorized or misleading effect?
4. **Measurement:** Are graders independent, examples representative, failures retained, repeated trials reset, and uncertainty visible?
5. **Engineering:** Can you explain the transaction, versioning, retry, cache, budget, and UI choices without appealing to a framework's magic?

These are suggested priorities based on the recruiter email, not a claim about Microsoft's undisclosed interview rubric. There is no need to build a large production platform to explain these ideas well.

## Scope

One rental case in the normal UI, with authenticated access on Azure; two synthetic cases in tests to exercise scope isolation. Monthly USD rent only. Separate project, built from zero; no imports from the production Uplisted project. One backend process per Container Apps replica, PostgreSQL locally and in Azure, one model-controlled coordinator, and seven tools. The UI has one route.

| Capability | What it means here | What it does not establish |
|---|---|---|
| RentCast evidence | Fetch or replay subject rent estimate, provider range, comparable records, and dates | Correct future market rent or tenant willingness to pay |
| Pricing | Explain fixed illustrative scenarios derived from acceptable evidence | Optimization, appraisal, or guaranteed return |
| Floorplan | Generate typed room intent and compile a labeled schematic | A survey, measured reconstruction, structural design, or code compliance |
| Photos | Produce room-linked shot cards | Inspection of real uploaded photos |
| Listing copy | Select supported factual claims and render them with controlled templates | Open-ended legal review or unrestricted creative copy |
| Review | Freeze exact current artifacts for a human approval event | Publication, lease creation, or messages to third parties |

**Deliberate simplification:** for the initial implementation, the model selects and orders typed listing claims; deterministic templates render factual sentences. This narrows the risk of text saying more than its citation supports. Free-form marketing prose is an extension requiring broader semantic grading. The assistant's conversational summaries still need factual evaluation. This is a smaller implementation of the earlier grounded-copy proposal, chosen for explainability.

Require an Azure deployment with Microsoft Foundry model access, Container Apps, PostgreSQL, Entra sign-in, managed identity, Key Vault, and telemetry. A separate Foundry Agent Service lab adds managed-agent experience. Exclude brokerage administration, CRM, leases, signatures, offers, payments, calendar writes, email, MLS/public publishing, document uploads, arbitrary browsing, MCP servers, vector databases, multiple production agents, application job queues, and full CAD editing. Do not add a capability because a library makes it easy.

## Runtime and development tools

Use Python 3.12, FastAPI, Pydantic 2, PostgreSQL 16 with psycopg 3 and a bounded connection pool, and explicit repositories/services. Use a local Docker Compose database and Azure Database for PostgreSQL Flexible Server, avoiding a second SQL dialect. Use React, TypeScript in strict mode, and Vite for the frontend. Use `uv` and npm lockfiles, pytest/Ruff/mypy, Vitest/Testing Library, and Playwright. Resolve compatible library versions at bootstrap and commit exact lockfiles; this specification does not invent future patch numbers.

Use Microsoft Agent Framework as the core runtime. A run-scoped MAF Agent manages model/tool iteration with seven function tools and application policy middleware. ScriptedChatClient supports offline tests through the real framework; a MAF Responses client configured for Azure supplies live inference. Coordinator is only a lifecycle adapter. Domain services enforce validation, permissions, budgets and transactional acceptance. See [MAF contract](08-microsoft-agent-framework.md).

Azure is required. Stage 18 separately compares the main application-hosted MAF agent with a managed Foundry prompt agent using one read-only tool. See [Azure architecture](06-azure-architecture.md) and [managed-agent lab](07-foundry-agent-lab.md).

## One contained screen

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Uplisted   Sample property · Draft   Scripted/Live · Fixture/Live    │
│ 3 beds · 2 full / 1 half bath · 1,600 sq ft          Edit property    │
├──────────────────────────┬───────────────────────────────────────────┤
│ Assistant                │ Evidence Pricing Floorplan Photos Listing │
│                          │ Review                                    │
│ Request                  ├───────────────────────────────────────────┤
│ Clarification            │ One selected artifact                     │
│ Progress                 │ Sources, assumptions, issues, edits       │
│ Result links             │                                           │
│                          │                                           │
│ Composer       Send/Stop │ Review: Approve this version              │
├──────────────────────────┴───────────────────────────────────────────┤
│ Run details ▸ tools · validation · blocks · attempts · time · cost    │
└──────────────────────────────────────────────────────────────────────┘
```

The views are selectable artifacts, not steps. Do not add a wizard, dashboard, landing page, or route per tool. Keep the assistant persistent on desktop. On narrow screens, an accessible Assistant/Workspace switch preserves the same route and state. Normal scrolling is allowed.

Preload a clearly synthetic property on first setup; refreshing the browser must not reseed or erase edits. `Edit property` opens an inline form. All authoritative changes require its explicit save action. Chat suggestions alone cannot modify facts. Loading the page, switching tabs, opening run details, or inspecting a saved report must not invoke a model or provider.

Maintain artifact-specific state: not requested, generating, draft, needs clarification, failed, stale, or included in an approved snapshot. These are view projections; immutable artifact content is not mutated to change status. Retain the last accepted artifact if regeneration fails. A newer draft can coexist with a historical approved snapshot.

The listing viewer lets users choose/order supported sentences and inspect the exact source facts. The floorplan viewer supports room label and known-dimension edits through validated revision requests, not free drawing. Dimensions remain unknown unless explicitly supplied and confirmed. A description is evidence of what the user said, not a measurement of the building.

Do not steal focus, selected views, or reading position when a result arrives. Preserve unsent chat input and unsaved edits. Show result indicators. Stop prevents future dispatch and requests cancellation; accurately explain when an external request may already have incurred cost. Structured artifacts appear only after validation and successful version checks.

Human approval is an explicit control in the Review view. It calls a separate backend authority path with the exact bundle hash. The model cannot activate that control. Approval produces only an internal snapshot in PostgreSQL; deploying the application does not publish property listings.

## Seven runtime tools

1. `read_property_case`: obtain the server-bound current facts, missing fields, and current artifact references.
2. `fetch_rentcast_evidence`: obtain rental evidence for the current confirmed subject; provider identity and URLs are configured server-side.
3. `calculate_pricing_options`: deterministic illustrative scenarios from acceptable evidence.
4. `draft_floor_plan`: produce semantic room intent, validate it, then compile a schematic.
5. `build_photo_shot_plan`: deterministic shot cards bound to a current plan.
6. `draft_listing_copy`: select grounded claims, validate values/citations, render controlled factual sentences.
7. `submit_for_review`: freeze requested current artifacts and their dependencies.

The model may select tools, propose their arguments, ask questions, and explain results. It cannot grant permissions, change confirmed facts, invent provider evidence, approve, publish, run shell commands, or choose arbitrary URLs.

## Completion definition

The project is interview-ready when the single-screen flow works from a clean checkout and an authenticated Azure HTTPS deployment; the critical deterministic tests pass; a real model has been evaluated on reproducible tasks in the harness, with all actual failures retained; a fixed-workflow comparison is recorded; and you can show one failure, mitigation, and independent regression (or a clearly labeled injected fault if no model failure was observed). A fixture-only application is a useful milestone but is not evidence of model reliability.

Required additional evidence includes Azure workload identity/model access, durable state across restart, revision-overlap ownership tests, a correlated trace, a cost/cleanup runbook, and the managed-agent lab. Local-only completion is an intermediate milestone. All benchmark values start as **not measured**. Original Uplisted test results and saved prompt-evaluation scores belong to the earlier project and cannot be reported as results for this one.

## Approaches and tradeoffs

- **Fixed workflow:** simplest control and best baseline; explicit intent routing handles narrow requests, but adaptation is limited.
- **Small tool-choosing coordinator:** chosen for this draft; enough model agency to study tool selection while keeping execution boundaries inspectable.
- **Broad autonomous/multi-agent platform:** additional authority, coordination, and evaluation burden with little benefit to this project's task. Outside scope.

The user selected the single-screen experience, a complete Copilot handoff, and now an Azure-hosted prototype with Azure agent learning. Stack, limits, controlled templates, and serial execution are explicit recommendations in this draft, not claims that the user previously selected every technical detail.

## Required Microsoft Agent Framework

The main agent uses MAF for model/tool orchestration from Stage 01, with a scripted framework client before Azure access. Application services enforce permissions, budgets, validation and approval. Begin with Stage 00 orientation. See [MAF runtime contract](08-microsoft-agent-framework.md).
