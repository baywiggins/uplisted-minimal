# Uplisted single-screen agent implementation plan

> **For agentic workers:** execute with GitHub Copilot, one numbered stage at a time, using the paired prompt in `prompts/`. If a compatible Superpowers environment is available, its executing-plans discipline can support this workflow; Copilot does not need that plugin. The user's selected execution method is Copilot. Do not scaffold or implement the whole plan in one response.

**Goal:** Build an inspectable rental-listing assistant and produce trustworthy evidence about task completion, tool use, and risk.

**Architecture:** One React workspace calls FastAPI locally and on Azure Container Apps. A small coordinator proposes actions through seven typed tools; deterministic services enforce scope, versions, budgets, validation, and human approval. PostgreSQL stores immutable state, run ownership, ordered events and approvals; Azure OpenAI supplies the model.

**Tech stack:** Python 3.12, FastAPI/Pydantic 2, PostgreSQL 16/psycopg 3, Docker Compose, React/TypeScript/Vite, uv/npm, pytest/Ruff/mypy, Vitest/Testing Library/Playwright, Azure CLI/Bicep, Container Apps, Foundry/Azure OpenAI and Entra ID. The real-model adapter is required for final model evaluation; live RentCast is optional. Both remain isolated and disabled until explicitly configured.

**Spec:** `docs/01-product-brief.md`, `docs/02-contracts.md`, and `docs/04-evaluation-plan.md`, `docs/06-azure-architecture.md` and `docs/07-foundry-agent-lab.md` travel with this plan.

## Global constraints

- Single route and current case; persistent assistant; no wizard or dashboard.
- Required Azure HTTPS deployment and managed-agent learning lab; local-only is an intermediate milestone.
- PostgreSQL locally/in Azure; Entra-protected cloud access; durable owner/lease/fence checks during revision overlap.
- One coordinator, seven tools, serial tools, one active run per case.
- Fixtures/scripted mode by default; live provider/model mode separately configured and labeled.
- Confirmed facts, external evidence, and generated assumptions stay separate.
- Immutable artifacts; exact dependency and target-head checks on acceptance.
- Human-only exact-version approval, no publication capability.
- 12 tool attempts, 12 shared model attempts, one repair per artifact, 90-second run deadline; no automatic HTTP/SDK retries in v1.
- Scoped unknown and cross-case resources return equivalent safe responses.
- Offline tests have no external network access; never read production Uplisted credentials.
- All benchmark results start as not measured; public development cases are not holdout.

## Review focus

1. **A slow generation finishes after a human edit:** the destination-head check must prevent overwriting that edit. Owned by Stages 03/11, test `test_late_generation_cannot_replace_human_revision`.
2. **Facts change and change back:** matching displayed values do not revive a review tied to older revisions. Owned by Stage 11, test `test_change_back_does_not_revive_review`.
3. **A provider timed out after dispatch:** local idempotency must not be advertised as exactly-once remote billing. Owned by Stages 05/10/13, test `test_dispatched_timeout_has_unknown_outcome_without_retry`.
4. **A valid citation accompanies the wrong sentence:** an independent grader must detect the false statement. Owned by Stages 08/12, test `test_grader_rejects_wrong_value_with_valid_citation`.
5. **A nested repair consumes the last allowance:** the helper cannot escape the shared budget. Owned by Stage 10, test `test_repair_uses_shared_model_attempt_budget`.

## Working rule for every stage

Read that stage's input documents, list its touched files/interfaces, then implement only it. For a behavior change, first write the named test/assertions and observe the intended failure, implement the smallest solution, and rerun. Do not add tests that merely repeat implementation branches. Configuration/docs-only work needs direct verification rather than artificial tests.

At the gate, run the stage's commands and inspect actual output. Keep `docs/BUILD-PROGRESS.md` with status, files, command results, unresolved limitations, and next stage. Inspect `git diff --check` and the diff; make a scoped checkpoint commit after passing checks. A failed check blocks only dependent work; repair it without weakening the spec. Never fabricate a test count. Commands and expected outcomes below are instructions for future execution, not claims they have already run.

---

## Stage 01 — Bootable project and reproducible commands

**Files:** create root `pyproject.toml`, `uv.lock`, `.python-version`, `.node-version`, `.gitignore`, `.env.example`, `README.md`; `src/uplisted/__init__.py`, `config.py`, `api/app.py`; `tests/conftest.py`, `tests/unit/test_config.py`, `tests/integration/test_health.py`; `web/` Vite React TypeScript project and scripts; `docs/BUILD-PROGRESS.md`.

**Consumes:** the copied handoff documents and official installation documentation.

**Produces:** `create_app() -> FastAPI`, validated `Settings`, `/api/health`, the standard commands from contracts §1, and a frontend that renders one empty workspace route. No tool/provider functionality yet.

- [ ] Inspect the empty target and copied docs; initialize Git if absent. Verify Python 3.12, Node 24, uv/npm and Docker/Compose versions. The prepared runtime wrapper remains in use. If tools are missing, report the exact prerequisite instead of executing an unrelated installer.
- [ ] Resolve compatible stable dependency releases. Use FastAPI/Pydantic 2/httpx/uvicorn and the named test tools; prepare compose.yaml with a pinned PostgreSQL 16 image, loopback port 5433, health check and local-only credentials from the example; avoid extra runtime frameworks. Commit lockfiles and record exact installed versions. Use current official docs for syntax.
- [ ] Create fixture-safe configuration: `MODEL_MODE=scripted`, `RENTCAST_MODE=fixture`, loopback origin, local PostgreSQL connection, APP_ENV=local/AUTH_MODE=local_demo, empty Azure identifiers/live secrets, and no provider work during import/startup. Tests assert invalid mode rejection and safe defaults. Use a global test guard that blocks external sockets and allows only the configured loopback test database; HTTP adapters use injected mock transports. Container image/dependency downloads are setup, not test execution.
- [ ] Implement `create_app` with readiness route and minimal frontend scripts. Health test asserts HTTP 200 and no credentials/machine paths. Do not add chat mock interactions that pretend to be a real agent.
- [ ] Write start/install/check commands in README; run from a fresh environment using lockfiles. A separate terminal is required for each dev server.

**Gate:** `docker compose config --quiet`; start the database and verify its health without exposing it beyond loopback; `uv run pytest -q tests/unit/test_config.py tests/integration/test_health.py`; `uv run ruff check .`; `uv run mypy src`; `npm --prefix web run check`; `npm --prefix web run build`. All must exit 0; inspect the page on the one route. Do not claim other features exist.

**Interview focus:** Reproducible configuration and explicit simulation prevent a polished demo from hiding missing integrations.

## Stage 02 — Typed facts, provenance, and artifact contracts

**Files:** create `src/uplisted/contracts.py`, `errors.py`, `state/hashing.py`; `tests/unit/test_contracts.py`, `test_hashing.py`; extend `fixtures/` with reviewed negative cases.

**Consumes:** contracts §2 and the three supplied synthetic JSON examples.

**Produces:** `PropertyFacts`, `PropertySnapshot`, `PublicFact`, `ResourceRef`, `ArtifactEnvelope`, `ToolResult`, `ToolError`, `ExecutionContext`, `HumanContext`; `canonical_hash(value: BaseModel | dict) -> str`; `build_public_facts(snapshot: PropertySnapshot) -> list[PublicFact]`.

- [ ] Define strict boundary models with explicit enum/range/string/collection constraints. Human/session identities are server-side types, never fields in model tool arguments.
- [ ] Add tests rejecting unknown fields, string/boolean room counts, negative rent, malformed timestamps, invalid levels, and both/neither ToolResult data/error. Assert false and null garage remain distinguishable.
- [ ] Test full/half bathrooms independently: physical room count 3 while RentCast request value is 2.5 for the supplied case. Use a dedicated conversion helper later in the adapter; never store 2.5 as bathroom-room count.
- [ ] Implement canonical hashing. Tests assert dictionary key order does not change a hash, changing a value/dependency does, and list order remains meaningful. Hashes do not establish user authorization.
- [ ] Convert seed input to a typed snapshot with generated immutable metadata. Build only public subject facts from confirmed typed fields. Test that comparable attributes and unknown fields cannot enter that fact set. Define RoomMeasurement and test exact room identity/level/value mapping, duplicate keys, and human confirmation provenance.

**Gate:** `uv run pytest -q tests/unit/test_contracts.py tests/unit/test_hashing.py`; backend lint/type checks. Positive fixtures parse; negative fixtures fail for the intended reason. Record these as schema checks, not proof that the facts are true.

**Interview focus:** Explain why schema validity, factual support, and authorization are distinct properties.

## Stage 03 — Versioned state, concurrency, and idempotency

**Files:** create `state/db.py`, `state/repository.py`, `state/run_ownership.py`, `state/migrations/001_initial.sql`, `cli.py`; `tests/integration/test_repository.py`, `test_idempotency.py`, `test_freshness.py`; define minimal run/event records needed by later stages.

**Consumes:** Stage 02 models and hashes. Use all repository signatures in contracts §3.

**Produces:** v1 PostgreSQL schema; repository methods; `is_current(ref, case_id, clock) -> FreshnessResult`; idempotent `init-demo`; immutable property/artifact storage and target-head acceptance gate.

- [ ] Build short parameterized PostgreSQL transactions and numbered migrations with foreign keys and scoped unique indexes. Use psycopg 3 AsyncConnectionPool and async runtime repository methods with a consistent lock order; keep arithmetic/hashing synchronous. Test against a disposable PostgreSQL database/schema, with cleanup restricted to test namespaces; use an injected clock. Add run owner/fence/lease fields and transactional single-active-run admission from contracts §10.
- [ ] Test and implement case-scoped retrieval; unknown/cross-case refs have equivalent safe results. Seed Case B with a unique private marker and assert it does not leak.
- [ ] Implement monotonic property revisions and per-kind artifact heads. A property edit invalidates all derived artifacts; artifact edits invalidate descendants through exact refs. Test dependency cycles are rejected or impossible by construction.
- [ ] Implement `accept_artifact` atomic checks for property/dependencies/target head and active, uncancelled run with current unexpired owner/fence. Human edits use a separately authorized path through the same validation/version checks; they do not need an active agent run. Test stale source, changed destination head, and cancellation using controlled transaction ordering.
- [ ] Implement operation records before dispatch and atomic local completion receipts. Same key/same hash returns original result, different input or actor conflicts, pending returns pending. Test at most one effect from concurrent duplicate requests.
- [ ] Implement `init-demo` without overwriting existing state, and explicit local reset. Recovery interrupts only expired leases, not every active row. Test that a second process cannot interrupt a healthy owner; it does not replay calls.

**Gate:** `uv run pytest -q tests/integration/test_repository.py tests/integration/test_idempotency.py tests/integration/test_freshness.py`; lint/type checks. Use two PostgreSQL repository connections for race tests, not only mocks. Keep fixture/model tests externally offline.

**Interview focus:** Be able to draw the transaction boundary and explain why an idempotency key alone does not solve stale writes or remote billing.

## Stage 04 — Single-screen shell and human inspection

**Files:** create `web/src/components/Workspace.tsx`, `AssistantPanel.tsx`, `PropertyHeader.tsx`, `ArtifactTabs.tsx`, `RunDetails.tsx`; `web/src/views/` placeholders; `web/src/state/workspace.ts`; `web/src/api/types.ts`; `web/tests/workspace.test.tsx` and styles.

**Consumes:** product brief layout and representative validated fixture data. Until the API exists, use a clearly labeled view adapter with static data, not ad hoc types in every component.

**Produces:** one workspace route, persistent composer, in-place property form, artifact selection, responsive Assistant/Workspace switch, accessible states. No live generation.

- [ ] Keep property/mode summary above assistant plus one selected artifact. No numbered progression or routing library unless required by the existing scaffold; one route is enough.
- [ ] Implement tab/view state without unmounting and losing unsent input or unsaved forms. New-result indication must not switch focus or selected tab automatically.
- [ ] Build explicit empty/loading/draft/stale/failed displays. Every example carries `Scripted model / Fixture evidence` labeling. Read-only views never dispatch generation.
- [ ] Add tests for preserved input/selection and semantic labels; do not snapshot an entire huge DOM. Check keyboard focus and a narrow viewport manually.
- [ ] Use simple typography, spacing, and restrained colors; if original Uplisted assets are unavailable, use a text wordmark and system font. The empty-repo build must not depend on original brand files.

**Gate:** `npm --prefix web run test`; `check`; `build`. Inspect desktop and narrow layouts. Save a local screenshot if useful, marked as shell/fixture stage. No claim of working agent integration.

**Interview focus:** The interface lets a human inspect evidence and exercise authority; visual state must reflect actual backend state later.

## Stage 05 — RentCast evidence, freshness, and complete cache keys

**Files:** create `providers/base.py`, `providers/scripted.py`, `providers/rentcast.py`, `domain/evidence.py`; `tests/unit/test_evidence.py`; `tests/integration/test_rentcast_adapter.py`.

**Consumes:** PropertySnapshot, ResourceRef, repository acceptance, synthetic normalized evidence fixture, contracts §4 evidence policies.

**Produces:** `RentCastGateway.fetch(request: RentRequest) -> RentEvidence`; `build_rent_request(snapshot) -> RentRequest`; `evaluate_evidence(evidence, snapshot, clock) -> EvidenceAssessment`; fixture gateway; cache interface/key function. Live HTTP adapter stays disabled until Stage 13.

- [ ] Write request mapping tests: unit retained; 2 full + 1 half maps to 2.5; edited sqft changes cache key; provider mode/parameters affect key; no identity fields supplied by model.
- [ ] Implement conservative matching and missing-unit clarification. Wrong/unknown unit cannot yield accepted matched evidence. Preserve provider subject observations separately from confirmed facts.
- [ ] Implement age/unit/unique-comparable checks and 24-hour cache TTL. Test fresh fetch with old source dates, unknown dates, duplicate comp IDs, incompatible units, malformed money, and cached fixture/live distinction.
- [ ] Use injected HTTP/mock transport tests to define 429, 500, malformed body, and dispatched-timeout outcomes. No automatic retries in v1. Record unknown external outcome where dispatch may have been accepted.
- [ ] Ensure failures do not install an artifact or silently synthesize successful evidence. No provider call on startup/view selection. Tests assert actual adapter attempt counters.

**Gate:** `uv run pytest -q tests/unit/test_evidence.py tests/integration/test_rentcast_adapter.py`; lint/type checks. Tests use no real credentials or external sockets.

**Interview focus:** Explain estimate/range versus calibrated confidence, observed date versus fetch date, and why cache keys include all effective request inputs.

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

## Stage 07 — Typed floorplan intent and safe schematic rendering

**Files:** create `domain/floorplan.py`; add structured-generation protocol to `providers/base.py` and scripted implementation; `tests/unit/test_floorplan.py`, `tests/integration/test_floorplan_generation.py`; `web/src/views/FloorplanView.tsx`, `web/tests/floorplan.test.tsx`.

**Consumes:** PropertySnapshot and confirmed description, shared model-attempt interface, supplied FloorPlanIntent example.

**Produces:** `validate_intent(intent, snapshot) -> ValidatedIntent`; `compile_schematic(intent) -> Schematic`; `generate_floorplan(ctx, snapshot, gateway, budget) -> FloorPlanPayload`. Until Stage 10, use an injected test budget implementing the eventual reservation interface.

- [ ] Define semantic models and tests for exact bedrooms/full baths/half baths, duplicate IDs, invalid levels, too many rooms, false garage, unsupported dimensions, and conflicting description/counts.
- [ ] Implement deterministic per-level grid compiler and independent bounds/non-overlap/reference assertions. Physical feet and screen coordinates must be separate fields.
- [ ] Implement scripted helper generation, raw attempt capture, at most one repair, and typed failure. Do not silently add missing required rooms to turn a failed first response into a raw pass.
- [ ] Render only accepted compiled data via React/SVG elements. Escape labels; reject model markup as a geometry source. A label containing `<script>` must display harmlessly or fail validation, not execute.
- [ ] Add visible schematic/unknown-dimension labels and an in-place room-label edit form. Confirm measurements through the inline property form as typed RoomMeasurement entries, creating a new property revision before regeneration. Test a free-text description alone cannot create accepted dimensions, and matching user-confirmed dimensions survive regeneration. Unsaved changes cannot mark an artifact approved.

**Gate:** `uv run pytest -q tests/unit/test_floorplan.py tests/integration/test_floorplan_generation.py`; frontend tests/check/build. Inspect both levels and unknown dimension display.

**Interview focus:** Distinguish semantic intent accuracy, renderer validity, and actual physical fidelity. Show what each test can and cannot establish.

## Stage 08 — Photo plan and controlled grounded listing

**Files:** create `domain/photos.py`, `domain/listing.py`; `tests/unit/test_photos.py`, `test_listing.py`; `web/src/views/PhotosView.tsx`, `ListingView.tsx` with focused tests.

**Consumes:** current validated FloorPlanPayload; PublicFact set; structured generation interface; template IDs from contracts §4.

**Produces:** `build_shot_plan(plan) -> PhotoPlanPayload`; `validate_listing_intent(intent, public_facts) -> ValidatedListingIntent`; `render_listing(intent, public_facts) -> ListingPayload`; helper selecting typed claims/order.

- [ ] Implement two deterministic cards per eligible room, exact room IDs and source-plan revision. Assert no shots for nonexistent rooms, stale plans, halls/stairs, or unsupported garage.
- [ ] Implement the six controlled templates. Reject free-text fields, unknown template IDs, wrong fact paths, wrong-case/revision refs, comparable facts, and assumptions as citations. Handle zero/one/plural grammar and separate full/half baths.
- [ ] Add tests for no asking-rent claim unless confirmed; no garage if false/unknown; wrong selected fact cannot be rendered as a supported sentence. Preserve raw rejected helper output.
- [ ] Implement the listing editor as supported sentence selection/removal/reordering, not arbitrary prose entry. Clicking a sentence reveals supporting fact value, source revision, and provenance in place.
- [ ] Keep assistant summaries outside the artifact truth guarantee; create negative examples for later semantic grading. Do not add a “legally compliant” badge.

**Gate:** `uv run pytest -q tests/unit/test_photos.py tests/unit/test_listing.py`; frontend tests/check/build. The three-bed sample must not acquire the comparable's garage.

**Interview focus:** Grounding is a data-flow constraint. Explain the restricted grammar tradeoff and the evaluation needed before allowing broader prose.

## Stage 09 — Closed tool registry and shared policy enforcement

**Files:** create `agent/tools.py`, `agent/dispatcher.py`, `telemetry/events.py`, `telemetry/redaction.py`; `tests/unit/test_tool_schemas.py`, `tests/integration/test_dispatcher.py`, `test_redaction.py`; define review service interface (implementation in Stage 11).

**Consumes:** exactly the seven tool argument contracts in §5 and the domain services. Provide a typed stub for `submit_for_review` that reports unavailable until Stage 11; do not fake a successful review.

**Produces:** `ToolCall`, `ToolRegistry`, `dispatch_tool(ctx, call, budget) -> ToolResult`; durable ordered events and safe public projections.

- [ ] Generate tool input schemas from Pydantic, not separately maintained handwritten schemas. Register only the seven tools. Test injected `actor_id`, `case_id`, `role`, arbitrary URL, replacement facts, extra fields, and unknown tools are rejected.
- [ ] Execute a shared order: count server-assigned tool attempt → allowlist → parse → scoped refs → monetary/provider reservation → domain execution → output checks → acceptance transaction → safe result. Test unknown/malformed and repeated provider-call-ID proposals consume allowances; replaying the same server attempt does not double-charge. Record proposed, blocked, started, and committed separately.
- [ ] Bind command keys to server run/call/operation IDs; ledger replay is idempotent. Every artifact writer must use the shared acceptance gate.
- [ ] Add injection tests using untrusted provider text. Assert no registered approval/publish/HTTP/shell tool exists and no forbidden database event occurs. Count attempted forbidden proposals, not just prevented effects.
- [ ] Redact provider headers, credentials, session tokens and seeded private contact markers. Export allowlisted event fields; do not log private model reasoning.

**Gate:** `uv run pytest -q tests/unit/test_tool_schemas.py tests/integration/test_dispatcher.py tests/integration/test_redaction.py`; lint/type checks. Inspect serialized schemas and exported sample trace yourself.

**Interview focus:** The model can propose; server-side code authorizes and commits. Prompt instructions alone are not the enforcement boundary.

## Stage 10 — Coordinator, budgets, cancellation, and fixed baseline

**Files:** create `agent/coordinator.py`, `agent/budget.py`, `agent/prompts.py`, `agent/baseline.py`; extend scripted gateway; `tests/integration/test_coordinator.py`, `test_budget.py`, `test_cancellation.py`, `test_baseline.py`, `test_run_ownership.py`.

**Consumes:** dispatcher, repositories, model protocol, exact limits/run states in contracts §6.

**Produces:** `Coordinator.run(ctx, request) -> RunOutcome`; `RunBudget.reserve_model(...)`, `reserve_tool(...)`, `record_usage(...)`, `check_deadline()`; `FixedWorkflow.run(ctx, request)`. Model reservations include helper and repair calls.

- [ ] Use scripted model turns to test read → tool → observation → final flow and an appropriate clarification. A model final message cannot create completion artifacts. Handle malformed/unknown calls and tool failures explicitly.
- [ ] Enforce one active run per case, serial tool execution, call-ID correspondence, per-run opaque provider continuation state, max attempts, deadline, and at most one repair. Test a helper consumes the last model allowance; further repair/coordinator calls are blocked.
- [ ] Cancellation sets a durable flag, halts further dispatch, and blocks late acceptance. Barrier tests cover cancel before dispatch, while provider in flight, and after one artifact committed. Retain successful earlier artifacts.
- [ ] Renew the 30-second DB lease every 5 seconds during async model/tool work. Lease loss stops dispatch and commits; expired-run reconciliation marks only expired owners interrupted without automatic paid replay. Usage/cost may be unknown. Disable SDK retries later; gateway protocol makes attempts visible now.
- [ ] Implement a fair fixed baseline supporting narrow task categories. It shares tools, helper settings and guardrails; do not fetch RentCast for photos-only. Unknown intent asks a bounded clarification.
- [ ] Write system instructions describing tools, untrusted data, factual limits, progress honesty, and clarification. Keep them versioned and hashed. Do not put grading labels or scenario-specific answers in prompts.

**Gate:** `uv run pytest -q tests/integration/test_coordinator.py tests/integration/test_budget.py tests/integration/test_cancellation.py tests/integration/test_baseline.py tests/integration/test_run_ownership.py`; all prior backend tests. Use fake clocks and event barriers, no long sleeps.

**Interview focus:** Explain where the agent has discretion, why serial execution is sufficient, how nested costs accumulate, and when a fixed workflow is preferable.

## Stage 11 — Human review API and complete one-screen flow

**Files:** create `domain/review.py`, `api/routes.py`, `api/session.py`; extend app/CLI; `tests/integration/test_api.py`, `test_review.py`, `test_human_edits.py`; `web/src/api/client.ts`, generated `types.ts`, integrated workspace views including `ReviewView.tsx`; `web/e2e/workspace.spec.ts`, Playwright config.

**Consumes:** all prior contracts; API table and environment-specific security boundary in §7/§10. Implement a LocalIdentityProvider now and a typed Azure identity seam; the cloud adapter is Stage 15. Replace shell fixtures with the real local API; keep provider modes scripted/fixture.

**Produces:** API endpoints, separate human mutation context, exact-version approval, polling events, persisted case conversation/reconnect, active run/Stop control, real artifact views/edits, and completed local browser journey.

- [ ] Implement the environment-aware session contract using the local identity adapter now, plus CSRF/origin checks and scoped API projections; preserve the same session response shape for Stage 15 Entra integration. Never accept body-supplied actor/permissions. Test agent-context approval and fact mutation denial, missing CSRF, cross-case lookup, and safe error responses.
- [ ] Implement review creation and approval transactions with nonempty unique membership and an active/non-cancelled run at creation. Show exact included artifacts; a subset approval does not mean the original full task succeeded. Tests cover missing artifact, stale transitive dependency, expired evidence, wrong hash, repeated approval, edit/approve race, and facts changed then changed back. A success receipt does not publish.
- [ ] Implement human artifact revisions through the same domain validators and destination-head checks, with explicit human permission. An active run is not required for a human edit. A late generator must not overwrite that revision.
- [ ] Integrate API client with 500ms ordered-event polling while active; deduplicate by run/sequence/message ID. Persist final/clarifying text and reconnect on reload using active_run_id and conversation history. Stop polling at terminal. Refetch current heads after accepted changes; avoid optimistic approval before server receipt.
- [ ] Wire conversation, property form, supported listing edits, plan edits, partial failures, retry as new run, Stop, source inspection, review, and redacted Run details. Preserve unsaved input and focus when results arrive.
- [ ] Add Playwright flow for same-route request → inspect → edit → regenerate → review → approve. Add stale approval, cancellation, partial failure, no side effects on tab changes, keyboard-only and narrow-view flows. Test no unknown network domains.

**Gate:** `uv run pytest -q tests/integration/test_api.py tests/integration/test_review.py tests/integration/test_human_edits.py`; frontend check/test/build; `npm --prefix web run test:e2e`. Review actual UI behavior, not just screenshots.

**Interview focus:** Show approval as a transaction over an exact snapshot, and show the UI truthfully representing it.

## Stage 12 — Independent evaluation harness and grader self-tests

**Files:** create `evals/__main__.py`, `schema.py`, `runner.py`, `graders.py`, `report.py`; `tests/evals/test_scenarios.py`, `test_harness.py`, `test_graders.py`; scenario builder/driver modules under `src/uplisted/evals/cases/`; `docs/GRADER-CALIBRATION.md`.

**Consumes:** all 30 public scenario specifications, the fixed baseline, scripted coordinator, outcome snapshots, and the complete evaluation plan.

**Produces:** validated CASE_REGISTRY, typed executable cases, CLI commands, resettable isolated trials, independent deterministic graders, redacted reports, and optional human scoring forms.

- [ ] Validate JSONL IDs/families/drivers and implement a reviewed builder for every ID. Service, agent and browser cases remain separately counted. Browser cases link actual Playwright output; missing output is not a pass.
- [ ] Build each trial in a new disposable PostgreSQL test database/schema with fixed clock/fixtures, clean budgets/cache, and hidden evaluator labels. Use barriers for the specified races and injected transports for failures. The agent receives no `expected`, `grading`, or scenario ID shortcuts.
- [ ] Grade persisted outcomes and trace independently. Implement separate arithmetic/template/ref/approval assertions; do not call production validation to decide success.
- [ ] Mutation-test graders: valid counterpart passes; corrupt price/unit/room ref/citation value/dependency/approval fails. Include missing-output, grader-exception, unknown-ID, duplicate-ID, zero-selection, missing-family and offline-network failures. Use defined nonzero exit codes.
- [ ] Implement coverage manifest, trusted external case-registry loading, browser-result import, human score import, and finalize protocol from evaluation plan. Pending required semantic scores are incomplete, never passing. Write manifests/trials/summaries/reports with real counts, raw-versus-repaired outputs, exception records, mode labels, and unknown costs. A scripted run is labeled application testing, not model performance.
- [ ] Add human semantic scoring form and 24-output calibration specification. A judge model is optional; if added later it cannot override deterministic failures and its spend is separate.

**Gate:** `uv run pytest -q tests/evals`; run `evals validate`, service/scripted CLI runs from evaluation plan. Import required human scores before finalizing agent trials. Inspect one deliberately failing report and one pending-score report and verify they are nonzero/incomplete rather than green. All expected public registry cases must be implemented; do not silently skip hard ones.

**Interview focus:** A valid evaluator is itself a tested system. Explain why final database state, trajectory, and semantic quality need different graders.

## Stage 13 — Azure OpenAI model integration and model-resource setup

**Files:** implement `providers/azure_openai_gateway.py`; finish optional live `providers/rentcast.py`; extend config; `tests/integration/test_model_adapter.py`, `test_live_mode_guards.py`; `infra/model.bicep`, model parameter example; `scripts/azure/model-preflight.sh`; `docs/LIVE-SETUP.md`.

**Consumes:** ModelGateway/structured helper protocols, current Microsoft v1 SDK docs, owner Azure choices, a supported deployed model and the existing shared budget/attempt ledger. Read `docs/06-azure-architecture.md` before touching cloud access.

**Produces:** AzureOpenAIModelGateway using `openai`/`azure-identity`, original call-ID tool round trips, schema-validated structured output, actual Azure-model evidence with fixture property data. Live RentCast remains a separately optional adapter.

- [ ] Resolve and pin compatible SDK versions. Use Azure's `/openai/v1/` endpoint, the actual deployment name, Entra credentials and current documented token audience. Keep opaque protocol continuation items if required; do not expose reasoning. Disable retries. Validate truncation, errors, nullable usage, function-call IDs and function-call outputs with synthetic SDK-shaped adapter tests.
- [ ] Prepare `infra/model.bicep` for the Foundry resource/project and chosen model deployment, or reference explicitly approved existing resources. Verify region/model/quota and dated rates. Prepare the cost/scope/what-if plan before collecting any missing owner choices; never assume the CLI default subscription is approved. Do not hard-code a catalog model name as a deployment name.
- [ ] When the owner has authorized this stage with required account/scope/spend values, provision only its model resources or reuse the specified deployment. Use resource-scoped inference permission for local developer identity; provisioning roles are distinct. Store identifiers, not keys, in local configuration. If access/permission is missing, report the exact blocker and leave live evidence incomplete.
- [ ] Test one actual response, a client-tool request/result loop, one structured helper output, and a forced budget stop against Azure. Then run the existing agent evaluation with frozen evidence, real execution clocks, and fixed fixture-domain time. Record actual model/deployment/version/region and unknown telemetry.
- [ ] Keep the human-operated real-property init CLI for optional live RentCast. Synthetic addresses are never sent to that property-data provider. No live model/provider call occurs on page load, install or offline tests.

**Gate:** `uv run pytest -q tests/integration/test_model_adapter.py tests/integration/test_live_mode_guards.py`; Bicep validates; actual Azure capability smoke and model trials are linked in the report. Mocked adapter success does not complete the Azure-model milestone. The full web deployment occurs in Stage 17.

**Interview focus:** Explain a model deployment versus an agent runtime, how Entra access reaches Azure inference, and which tool effects remain controlled by your code.

## Stage 14 — Baseline comparison, failure analysis, and frozen holdout

**Files:** add reviewed regression cases under `evals/regression/`; create `docs/RESULTS.md`, `docs/FAILURE-ANALYSIS.md`; select redacted report artifacts. Holdout inputs/labels live in a separate evaluator workspace outside Copilot's tuning context.

**Consumes:** validated harness, real model, fixed evidence, fixed baseline, calibrated human/optional model judgments, and explicit evaluation-batch budget.

**Produces:** measured comparison, honest limitations, one reproducible failure → mitigation → independent regression chain, and clearly labeled holdout status.

- [ ] Freeze code/prompt/model/fixtures and budgets. Run baseline and agent on the same eligible tasks; include narrow requests and failures. Repeat stochastic cases five times from reset state if budget allows; if fewer, report the actual count.
- [ ] Populate metric numerators/denominators, unique scenarios/trials, outcome-specific latency, known/unknown cost, and harmful proposals/blocks/effects. Do not omit unsuccessful trials or overwrite their report with the rerun.
- [ ] Select an observed failure, reproduce it, explain its cause, change one responsible part, and add an independent regression. If no model failure was observed in the small sample, demonstrate an intentionally injected software fault labeled as such; do not invent an incident.
- [ ] Freeze improved configuration, run genuinely fresh owner/evaluator-held cases, and record their handling. Once inspected for tuning, those cases become regression; create replacement holdout. Report absence of holdout if it has not been created.
- [ ] Review critical deterministic failures separately from aggregate quality. Set any model-quality release threshold from a documented product requirement/baseline before the final evaluation; do not manufacture a favorable threshold afterward.

**Gate:** results files link real manifests and failed/passing trial IDs; denominators reconcile to selected cases; critical state/authority tests pass; rubric disagreements/unknown telemetry visible. A report of limitations is preferable to claiming broad reliability from a small suite.

**Interview focus:** The strongest story is why a particular metric caught a meaningful failure and how the fix changed measured behavior.

## Stage 15 — Azure identity, persistent sessions and process ownership

**Files:** implement `api/identity.py`, extend `api/session.py`, `state/run_ownership.py`, migrations for memberships/sessions/stored reports; `tests/integration/test_cloud_identity.py`, `test_run_ownership.py`, `test_persistent_sessions.py`; update frontend sign-in/expiry handling and configuration.

**Consumes:** PostgreSQL repository/lease contracts, local API, Entra/Container Apps boundary from `docs/06-azure-architecture.md`.

**Produces:** explicit local/cloud identity providers, cloud startup validation, persisted session/CSRF/actor bindings, per-case reviewer authorization, and tested correctness across overlapping process owners.

- [ ] Reject `APP_ENV=azure` with local_demo authentication, insecure database TLS, missing tenant/reviewer mapping, or invalid origin. Model and human identities are distinct. Test valid tenant/object-ID membership, another signed-in user, wrong tenant and absent/untrusted platform principal.
- [ ] Persist app session binding and require the current authenticated actor to match it on every human mutation. Test restart retention, CSRF/origin rejection and a body claiming another actor/role. Local tests use an explicit injected identity adapter, not generic spoofable headers.
- [ ] Complete owner/fence checks on every dispatch, budget reservation, artifact and review commit. Test two simulated process owners, lease renewal, healthy-owner protection, expired-owner interruption, and late result rejection. Never auto-replay an uncertain external call after loss of ownership.
- [ ] Store bounded redacted UI report projections in PostgreSQL instead of depending on container-local files. Keep telemetry/raw eval artifacts separate from authoritative state.
- [ ] Document the trusted ingress assumption and test it again after real deployment in Stage 17. A mocked principal unit test cannot establish that Azure strips/rejects forged identity headers.

**Gate:** `uv run pytest -q tests/integration/test_cloud_identity.py tests/integration/test_run_ownership.py tests/integration/test_persistent_sessions.py`; existing review/cancellation/scope tests still pass against PostgreSQL. Azure network behavior remains unverified until Stage 17.

**Interview focus:** Human authentication, application authorization, workload identity and model authority are four different concerns. Explain why one replica does not eliminate revision-overlap races.

## Stage 16 — Azure infrastructure, image, telemetry and deployment runbook

**Files:** `Dockerfile`, `.dockerignore`, `infra/main.bicep`, modules/parameter example from the Azure architecture; `scripts/azure/preflight.sh`, `what-if.sh`, `deploy.sh`, `smoke.sh`, `teardown.sh`; `telemetry/azure_monitor.py`; `docs/AZURE-DEPLOYMENT.md`; tests for cloud configuration, image health and redaction.

**Consumes:** tested application, Stage 13 resource identities, Stage 15 authority/ownership boundaries, owner account/region/budget choices.

**Produces:** buildable single frontend/API image, validated infrastructure definitions, explicit auth/database migration bootstrap, telemetry integration and reviewable deployment/cleanup commands. This stage prepares the full deployment; it does not count as a running Azure prototype.

- [ ] Build a multistage Linux image with locked dependencies and built Vite assets, non-root runtime, one Uvicorn worker on port 8000, liveness/readiness, graceful shutdown and no secrets/local tools/reports in context. Verify the target platform instead of assuming the Mac architecture works in Azure.
- [ ] Define Container Apps/ACR, user-assigned identity, VNet/private DNS/PostgreSQL with public DB access disabled, Key Vault, monitoring and budget alerts. Reuse/reconcile the model module explicitly. Parameterize model, region, SKUs, identity mappings and owner/expiry; do not invent bill estimates or quota.
- [ ] Define single-tenant Entra authentication and the application reviewer/case allowlist, with no public bypass route to the backend. Document directory permissions/app-registration bootstrap separately. Prepare Key Vault secret injection without exposing secret values in outputs.
- [ ] Define managed-identity access to Azure inference, ACR and Key Vault plus a narrowly privileged PostgreSQL runtime identity. Define a separate migration identity and manually triggered one-shot private-network migration Job. App containers do not perform schema administration.
- [ ] Instrument redacted OpenTelemetry spans to Application Insights using current supported packages. Preserve durable audit events independently. Test a seeded secret/contact marker is absent from spans and output bundles; content capture stays disabled by default.
- [ ] Generate a concrete dated deployment plan/cost estimate, Bicep validation and what-if when authorized Azure access exists. Teardown defaults to inventory/dry run and names the exact dedicated group and separately tracked lab/directory objects. Do not auto-deploy on PRs.

**Gate:** `docker build` and local container health work; `az bicep build --file infra/main.bicep` succeeds; cloud config/redaction tests pass; deployment plan names actual parameters and permissions or explicitly identifies missing inputs. Owner review is of concrete resources/commands; no new permission question is needed when that scope is already authorized.

**Interview focus:** Show what infrastructure owns, what your runtime owns, and how identity/telemetry/cost choices preserve the existing safety boundaries.

## Stage 17 — Deploy and verify the Azure prototype

**Files:** execute prepared scripts within the authorized scope; fill `docs/AZURE-DEPLOYMENT-RESULTS.md`; add `evals/cloud/scenarios.jsonl` and executable cloud smoke drivers; preserve sanitized deployment/test artifacts.

**Consumes:** reviewed Stage 16 plan, exact owner subscription/region/identity/spend configuration, valid credentials/permissions, and the built image digest.

**Produces:** a working authenticated Azure HTTPS prototype, actual cloud acceptance evidence, known limitations, and a verified cleanup inventory. Provisioning is a real billable action in this stage; this instruction-editing task has not executed it.

- [ ] Apply the reviewed infrastructure to its dedicated resource group. Configure Entra before enabling usable external ingress, initialize schema/seed through the private migration path, and deploy the immutable image digest. Start with scripted model/fixture evidence so infrastructure tests do not accidentally spend on models.
- [ ] Verify anonymous denial, authorized reviewer success, unlisted tenant-user denial, CSRF/origin enforcement and forged-principal resistance. Load/inspect/edit/review in the same HTTPS workspace. The Azure UI must visibly report its deployment/model/evidence mode without displaying secrets.
- [ ] Test accepted-state persistence through restart, healthy run ownership during revision overlap, expiration of an orphaned lease, concurrent start rejection, stale approval and late/cancelled result rejection. No duplicate billable retry or automatic provider replay.
- [ ] Explicitly enable Azure-model inference within the run/batch cap and complete a task with frozen evidence. Verify managed identity refresh, current data/approval state and correlated request/run/tool/model traces. Live RentCast remains optional and separately labeled.
- [ ] Record group/region/resource IDs, revision/image digest, SDK/model versions, auth/DB configuration fingerprints, timestamps, check results, cost assumptions/observed spend and limitations. Do not store tokens or private contact/property content in the shareable report.
- [ ] Exercise rollback to a compatible prior image if available; verify cleanup dry-run targets only owned resources. Keep the deployed demo until the owner elects teardown; documenting cleanup is not permission to delete the working demo immediately.

**Gate:** all required cloud acceptance checks in docs06 are backed by actual Azure observations; cloud failures stay distinct from offline/model-quality failures. An absent Azure account/permission leaves this stage incomplete rather than changing the target back to local.

**Interview focus:** Demonstrate a real deployment, an actual identity boundary, state surviving infrastructure changes, and evidence of behavior under failure.

## Stage 18 — Build and compare a managed Foundry agent

**Files:** `labs/foundry_agent/README.md`, runner/fixture/cleanup code and optional dependency group; `docs/FOUNDRY-LAB-RESULTS.md`; `tests/labs/test_foundry_function_boundary.py`.

**Consumes:** `docs/07-foundry-agent-lab.md`, actual Foundry project/model access and an owner-configured lab spend cap. This is separate from the deployed application coordinator.

**Produces:** one actual versioned Foundry Agent Service prompt agent, one client-executed read-only property function, three measured test cases and a lifecycle/authority comparison.

- [ ] Use the current supported new-project SDK/API and the project endpoint, not the direct model endpoint. Pin versions and verify role scope before creating the lab agent. Keep all production write/approval tools absent.
- [ ] Create the versioned prompt agent and implement the bounded function-call/output client loop. Test names/arguments/call IDs and disallowed function handling offline before live execution.
- [ ] Run the known-facts, forbidden-approval, and injected-tool-text scenarios. Record actual output/trace and limits, including unknown internal service work/cost. Compare with the custom coordinator on the same inputs.
- [ ] Write who owns conversation, tools, retries, iteration limits, identity, tracing and cleanup in each design. An optional Agent Framework version may follow, but it must not silently replace the production loop or its budgets.
- [ ] Delete only the exact lab-owned agent/version/conversations captured in its manifest once results are saved; verify cleanup or state what remains. Retain the application/model resources needed for the interview.

**Gate:** offline boundary tests pass; actual Agent Service resource/invocation evidence and the three-case comparison exist; lab lifecycle/cleanup is recorded. A direct model response does not satisfy this managed-agent milestone.

**Interview focus:** Explain Azure-hosted model inference versus managed agent service versus client framework orchestration, using code and traces from both systems.

## Stage 19 — Clean-checkout verification and rehearsal

**Files:** finalize README, `docs/BUILD-PROGRESS.md`, `docs/DEMO-SCRIPT.md`, `docs/RESULTS.md`, `docs/LIMITATIONS.md`, `.github/workflows/checks.yml`; optional local demo recording with synthetic data only.

**Consumes:** completed project, actual Azure deployment/managed-agent lab reports, plus the supplied interview playbook.

**Produces:** reproducible local and Azure project, offline CI, an authenticated cloud demo plus backup fixture replay, a concise technical talk, and accurate evidence claims.

- [ ] In a new temporary checkout/environment, install from lockfiles, initialize synthetic data, and start backend/frontend using README only. Confirm no original Uplisted file or secret is required.
- [ ] Run complete backend, frontend, browser, and harness self-tests. CI runs scripted/fixture only with external network blocked during tests; dependency installation/browser installation are separate setup steps. Do not run paid evals on pull requests.
- [ ] Freeze the final runtime/dependency/prompt/schema bundle fingerprint. Re-run affected model, browser and cloud checks after Stages 15–18, and rerun the full required suite for the final snapshot if its runtime bundle changed. Earlier Stage 14 comparisons remain historical evidence. Use the compatibility rules in the evaluation plan; do not combine mismatched runtime evidence into a release claim.
- [ ] Execute `finalize --profile azure` with the model/service/browser/cloud reports and actual Foundry lab receipt, using the command in docs04. Resolve missing grades/results and distinguish quality failures from critical-control failures. Save the final status/limitations; a generated report is not a passing release.
- [ ] Recheck the Azure URL, allowed reviewer, resource expiry and cost/cleanup notes. Walk the live demo: useful request, source-linked sentence, schematic caveat, photos-only restraint, injection/failure handling, stale approval rejection, and measured report. Keep a fixture replay and screenshots/recording as a clearly labeled backup.
- [ ] Fill talk placeholders only with actual implementation details/results. Explain Copilot's role honestly and identify the contracts, reviews, tests, and fixes you personally understood and directed.
- [ ] Record limitations: local-development versus Entra cloud auth, lease-expiry interruption, synthetic tasks, restricted listing grammar, unmeasured physical/market accuracy, incomplete live integrations and managed-service accounting limits, and any remaining failures. Remove unfinished UI claims or label them clearly.

**Gate:** clean-checkout commands reproduce the documented outcome, critical checks pass, and the ten-minute talk can be delivered without relying on Copilot to explain the code. Azure deployment and the managed-agent lab must have actual evidence; neither is replaced by the offline backup. Code exists only after implementation; this handoff itself does not satisfy the gate.

**Interview focus:** Show ownership of the design and evidence, including limitations. Framework names and code volume are secondary.
