# Canonical implementation contracts

These are design targets for Copilot to implement. Code examples below are contract notation, not a delivered working library. All later stages use these names. Public JSON uses snake_case; TypeScript consumes generated OpenAPI types without renaming fields.

## 1. Repository and commands

```text
pyproject.toml, uv.lock, .python-version, .node-version, .env.example
src/uplisted/
  config.py, errors.py, contracts.py, cli.py
  api/app.py, api/routes.py, api/session.py
  state/db.py, state/repository.py, state/hashing.py
  domain/evidence.py, domain/pricing.py, domain/floorplan.py
  domain/photos.py, domain/listing.py, domain/review.py
  providers/base.py, providers/scripted.py, providers/rentcast.py
  providers/anthropic_gateway.py
  agent/tools.py, agent/dispatcher.py, agent/coordinator.py
  agent/budget.py, agent/prompts.py, agent/baseline.py
  telemetry/events.py, telemetry/redaction.py
  evals/__main__.py, evals/schema.py, evals/runner.py
  evals/graders.py, evals/report.py
tests/unit/, tests/integration/, tests/evals/, tests/conftest.py
web/src/api/, web/src/components/, web/src/views/, web/src/state/
web/tests/, web/e2e/, web/package.json, web/package-lock.json
fixtures/, evals/dev/, evals/regression/, docs/, prompts/
.github/copilot-instructions.md, .github/workflows/checks.yml
```

No code imports this handoff's original absolute filesystem location. Keep generated runtime data under ignored `.local/`; reports under ignored `reports/` unless a redacted report is intentionally selected for the project portfolio. Ignore `.env*` except `.env.example`, virtual environments, caches, `node_modules`, databases/WAL files, and unredacted traces.

Standard commands, from the new repository root:

```bash
uv sync --locked
npm --prefix web ci
uv run pytest -q
uv run ruff check .
uv run mypy src
npm --prefix web run check
npm --prefix web run test
npm --prefix web run build
uv run python -m uplisted.cli init-demo
uv run uvicorn uplisted.api.app:create_app --factory --host 127.0.0.1 --port 8000
npm --prefix web run dev -- --host 127.0.0.1 --port 5173
```

Use separate terminals for backend/frontend. `init-demo` is idempotent: creates missing synthetic cases and never overwrites an existing case. Stage 13 adds `init-case --input /absolute/path/to/property.json --confirm-non-synthetic` for a human-confirmed real property. It validates PropertyFacts, assigns a new case ID and actual-UTC provenance, marks it non-synthetic, and never overwrites an existing case. Select it using server configuration `CASE_ID`; restart the local app to bind a new human session to that case. Keep its input file under ignored local storage and never print private fields in normal logs. It is not a model tool. An explicit `reset-demo --confirm-local-reset` command is allowed only for local synthetic data, when no run is active. CI and evals use a temporary database, not `.local/demo.sqlite3`.

Stage 01 creates scripts `check` (TypeScript plus lint), `test` (Vitest non-watch), `build`, and later `test:e2e`. Playwright's configuration starts the local backend/frontend in fixture mode with a separate database. E2E browser network allowlist permits only loopback; backend tests block outbound sockets. Dependency installation can use the network; test execution cannot access external services.

## 2. Shared types and validation

Pydantic input models reject extra fields. Strict booleans/integers reject `"3"`, `true` as a bedroom count, NaN, infinity, negative money, and arbitrary attributes. Where JSON must convert strings into UUID/datetime/enum, validate the JSON boundary deliberately; don't add a permissive fallback to work around strict mode. Use integer USD cents internally and UTC timestamp strings externally. Decimal/provider conversion belongs only in provider adapters; reject amounts with more precision than the defined currency permits rather than relying on binary floats.

```python
ArtifactKind = Literal['evidence', 'pricing', 'floorplan', 'photos', 'listing']
ProviderMode = Literal['fixture', 'live']
ModelMode = Literal['scripted', 'live']

class ResourceRef:
    kind: Literal['property', 'evidence', 'pricing', 'floorplan', 'photos', 'listing']
    resource_id: str
    revision: int                 # starts at 1
    content_hash: str             # SHA-256 of canonical immutable content

class ExecutionContext:           # constructed by server; absent from tool JSON
    actor_id: str
    case_id: str
    run_id: str | None           # non-null for tools; null for human commands
    permissions: frozenset[str]

class ToolResult[T]:
    status: Literal['ok', 'error']
    data: T | None
    error: ToolError | None
    artifact_ref: ResourceRef | None
    event_ids: list[str]

class ToolError:
    code: ErrorCode
    message: str                 # safe for user, no secrets/provider raw body
    retryable: bool
    details: dict                # allowlisted typed details by error code
```

Enforce exclusive `data`/`error` combinations. `ErrorCode` is one of `needs_clarification`, `input_stale`, `evidence_insufficient`, `provider_disabled`, `provider_unavailable`, `provider_outcome_unknown`, `validation_failed`, `forbidden`, `budget_exhausted`, `cancelled`, `idempotency_conflict`, `run_active`, `not_found`. A tool failure never creates a successful artifact.

Pure domain functions return their documented payload or raise `DomainError(error: ToolError)`; the dispatcher/API adapter converts that exception to the documented envelope. Do not alternate between bare dicts, exceptions, and nullable success values in different services. Provider/gateway methods that perform IO are async; hashing, arithmetic, compilation, and small repository transactions are synchronous. The coordinator awaits IO and keeps the event loop responsive to cancellation.

`PropertyFacts` contains `address` (street/city/state/postal_code/unit, where unit may be null), `property_type` (`single_family|townhouse|condo|apartment`), `bedrooms` (0–20), `full_bathrooms` (0–20), `half_bathrooms` (0–20), `square_feet` (positive int or null), `levels` (1–4), `has_garage` (bool or null), `asking_rent_cents` (positive int or null), and `layout_description` (string or null, max 4,000 chars), plus `room_measurements: list[RoomMeasurement]` (default empty, max 40). Missing versus known false is meaningful. Avoid a generic amenity dictionary in v1.

`RoomMeasurement` contains unique `measurement_id`, stable `room_key`, `room_kind`, `level_index`, and positive `width_ft`/`length_ft` Decimal strings (0–200 ft, exclusive zero). These are **user-confirmed measurements**, not externally verified measurements. The property form can confirm them explicitly. After a schematic exists, its `Confirm measurements` action proposes these fields in the inline property form; saving creates a new property revision and makes old artifacts stale. It does not silently mutate the plan. Regeneration uses the new revision. PublicFact IDs for these values use `room_measurements.{measurement_id}.width_ft` and `.length_ft`; they are eligible only for the matching room's dimensions, not a generic marketing amenity.

`PropertySnapshot` contains `case_id`, `revision`, `facts`, `confirmed_by`, `confirmed_at`, `content_hash`, `synthetic`. All non-null facts were explicitly confirmed in the local demo. Server-derived `PublicFact` entries have `fact_id = '{case_id}:r{revision}:{field_path}'`, typed value, subject scope, source ref, and confirmation status. Do not accept model-supplied fact objects. Provider subject facts are external observations and never silently overwrite this snapshot.

`ArtifactEnvelope[T]` has `artifact_id`, `case_id`, `kind`, `revision`, `created_at`, `run_id` (nullable for human edits), `dependencies: list[ResourceRef]`, `payload`, `content_hash`, and `origin` (`scripted|live_model|deterministic|human_edit`). The immutable hash covers identity, revision, dependencies, payload, origin, and creation metadata; excludes later operational status. Canonical JSON sorts object keys, preserves list order, uses stable UTF-8, prohibits NaN/floats in financial fields, and has documented timestamp normalization.

Artifact IDs identify a revision series of one kind in one case; revision advances monotonically. A case has at most one current head per kind. Historical revisions remain retrievable only within the bound case. Approval/staleness are derived projections, not mutable payload fields.

## 3. Storage, dependencies, and transactions

Use standard `sqlite3`, parameterized SQL, foreign keys enabled, WAL mode, and short transactions. Tables: `cases`, `property_revisions`, `artifact_revisions`, `artifact_heads`, `runs`, `run_events`, `review_bundles`, `approvals`, `idempotency_records`, `provider_attempts`, `conversation_messages`. Model JSON can be stored as validated JSON text; don't build an ORM or migration framework. Track a schema version and ship an explicit v1 initialization script/function. One process only; no distributed durability claims.

Repository methods:

```python
get_case(ctx: ExecutionContext) -> CaseView
confirm_property(ctx: HumanContext, expected_revision: int,
                 facts: PropertyFacts, command_key: str) -> PropertySnapshot
accept_artifact(ctx: ExecutionContext | HumanContext, expected_property: ResourceRef,
                expected_target: ResourceRef | None,
                dependencies: list[ResourceRef], kind: ArtifactKind,
                payload: BaseModel, origin: str, command_key: str) -> ArtifactEnvelope
create_review(ctx: ExecutionContext, refs: list[ResourceRef],
              command_key: str) -> ReviewBundle
approve_review(ctx: HumanContext, bundle_id: str,
               expected_hash: str, command_key: str) -> ApprovalReceipt
```

`HumanContext` comes only from the browser session adapter and contains actor/case permissions. It is not a model-tool argument. Domain helper interfaces use repository transactions; no tool writes SQL itself.

Every artifact acceptance transaction checks: case scope; current property revision; exact dependency heads and their transitive freshness; expected target head; active non-cancelled run for agent-origin writes (or explicit human edit permission for human-origin writes); and idempotency key. If anything changed during generation, reject `input_stale` or `cancelled`; retain diagnostic attempt metadata without installing the result. Do not hold a transaction across model/HTTP calls.

Any property revision makes all prior derived artifacts stale in v1, even if an unrelated field changed or was changed back. This conservative choice is easier to prove than field-level invalidation. Changing a floorplan invalidates dependent photos and reviews; an independent pricing artifact remains current if its dependencies remain current. Never automatically revive an old approval.

Idempotency key scope is `(case_id, operation, command_key)`, with a request hash including actor, operation, exact inputs and refs. Same key and same request returns the original logical result; same key and different request returns `idempotency_conflict`. Replaying a completed operation returns its original receipt, even if it is now stale, and labels current freshness separately; it does not create a new effect or revive approval. A pending key returns pending state. Store the result and state change in one transaction. Local idempotency does not establish exactly-once external billing.

Review membership must contain 1–5 refs, at most one of each artifact kind, with no property refs, duplicates, or cross-case refs. Approval means approval of exactly these displayed artifacts, not implicit completion of every item in the original natural-language request. The UI names all included artifacts and any unresolved requested work. Task-success graders independently compare membership with the scenario goal; a partial bundle cannot earn full-package success. `create_review` also checks the run is active and not cancelled in its commit transaction.

Review bundle payload: `bundle_id`, `case_id`, `property_ref`, `artifact_refs`, transitive `dependency_refs`, `created_by_run`, `created_at`, `bundle_hash`. Tool submission requires all requested artifacts present, current, validated, and free of blocking issues; otherwise a typed error, no bundle. Approval rechecks everything atomically and stores reviewer, exact bundle/hash, timestamp, and receipt ID. Review bundles are immutable. Human property edits and approval compete through transactions; one must observe the other's new revision.

## 4. Domain contracts

### Evidence

`RentEvidence` contains normalized request hash, confirmed subject ref, `subject_match` (`matched|unresolved|mismatch`), `estimate_cents`, nullable `range_low_cents`/`range_high_cents`, `currency='USD'`, `period='month'`, comparable IDs and typed records, `fetched_at`, nullable source observation dates, `provider_mode`, and `issues`. Preserve source dates: fetching today does not make old listings new.

Input bathroom value for RentCast is full + half × 0.5; physical bathroom-room count for the floorplan is full + half. Never interchange these. Request cache key includes provider/endpoint version, address including unit, property type, all supplied attributes, mode, and policy parameters. Cache TTL = 24 hours from fetch. A fresh cached response must still pass current subject, source-age, and dependency checks. Cached evidence cannot be relabeled live if it originated as a fixture.

Accept exact normalized unit-aware subject matches only in v1; unknown subject identity is unresolved. If apartment/condo unit is absent, ask before the provider request. Compare street/city/state/postal/unit separately using a documented conservative normalization, no fuzzy acceptance. Source subject conflicts are surfaced. Minimum usable comparables for pricing = 3 unique comparable IDs, known observation age ≤180 days, same monthly USD units; unknown dates are not fresh. These are **demo policies**, not validated market thresholds.

Live RentCast uses a server-fixed HTTPS origin and `/v1/avm/rent/long-term`, with an API key only on the server; verify the current request/response schema when implementing. A range is retained as provider-reported, not represented as calibrated confidence in the agent's recommendation. No `high confidence` label based solely on count. RentCast documents estimates/ranges/comparables and single-unit rental valuation. [RentCast valuation reference](https://developers.rentcast.io/reference/property-valuation).

### Pricing

`calculate_pricing(evidence: RentEvidence) -> PricingPayload` requires matched subject, positive estimate, valid units, fresh evidence, and ≥3 usable unique comps. Otherwise `evidence_insufficient`, with safe diagnostics. No manual model-authored adjustment formula in v1. Render three scenarios with multipliers 97%, 100%, 103%; compute integer cents with Decimal/ROUND_HALF_UP to the nearest cent. With 300000 cents, outputs are 291000, 300000, 309000. These are illustrative scenarios, not a learned forecast or confidence interval. An asking price enters public listing copy only if `asking_rent_cents` was explicitly confirmed; selecting/generating a pricing scenario does not confirm it.

### Floorplan

`FloorPlanIntent` = `rooms`, `assumptions`, `warnings`. A room has unique `room_id`, `kind` (`bedroom|full_bathroom|half_bathroom|kitchen|living|hall|stairs|garage|other`), nonempty `label` ≤60 chars, `level_index` from 0 to levels−1, nullable `measurement_id`, nullable `width_ft`/`length_ft` positive Decimal strings, `dimension_source_fact_ids`, and `basis` (`confirmed_description|confirmed_count|assumed`). No model SVG/HTML/CSS/JavaScript. Dimensions require an exact current RoomMeasurement matching `room_id == room_key`, room kind, and level; both values must equal that measurement and cite its two fact IDs. Missing measurement_id means both dimension values are null. Description text alone is not a structured measurement source. Reject duplicate use of a measurement across rooms; unknown dimensions stay null. Reject unsafe markup as data or escape it; never interpolate model text as raw SVG markup.

Validate exact bedroom, full-bath, and half-bath counts independently; unique IDs; valid levels; known dimensions; no asserted garage if confirmed false; room cap 40. Description conflicts with counts cause clarification. Sparse layout can yield an assumed schematic, visibly labeled, without invented dimensions. Unknown physical adjacency is not a measured connection.

`compile_schematic(intent: FloorPlanIntent) -> Schematic` produces deterministic grid rectangles within a 1000×700 logical canvas **per level**, with margins and gutters, using room IDs sorted by level and input order. Layout pixel coordinates are distinct from physical feet. Validate finite positive rectangles, bounds, non-overlap, unique references. This demo does not promise true physical adjacency or spatial scale. `FloorPlanPayload` stores intent, compiled rectangles, validation summary, and visible `Schematic — measurements are user-provided where labeled, not independently verified` label.

### Photos

`build_shot_plan(plan: FloorPlanPayload) -> PhotoPlanPayload` produces two cards per non-hall/non-stairs room: wide/context and detail. Each card has stable shot ID, exact room ID, source plan ref, kind, and templated advice. A garage card requires a real plan garage room backed by confirmed subject information. Reject stale/invalid plan references. No uploaded-image analysis or photographic-quality score.

### Listing

`ListingIntent` is a list of `ClaimSelection(template_id, fact_ids)`; no arbitrary factual `text` field accepted. Initial templates are `bedrooms`, `bathrooms`, `square_feet`, `property_type`, `garage`, and `asking_rent`. Templates use these exact confirmed paths. `garage` is permitted only for true; unknown/false is omitted. `asking_rent` uses confirmed asking rent, never an unselected estimate. `bathrooms` preserves full/half counts and correct grammar. All public claims cite subject facts from the same current property revision. Comparable or plan assumption IDs cannot satisfy these references.

`render_listing(intent, public_facts) -> ListingPayload` returns ordered sentence IDs, rendered text, citations, and warnings. Example: `3 bedrooms. 2 full bathrooms and 1 half bathroom.` Short factual copy is sufficient. Include a deterministic plain title using confirmed property type; no invented neighborhood amenities, superlatives, eligibility preferences, or proximity claims. The model can choose/order these claims but cannot invent the sentence body. The single-screen editor selects/removes/reorders supported sentences and saves a new validated revision. Do not add an unrestricted textarea in v1.

Inspect conversational responses separately for unsupported facts. A restricted artifact grammar does not make the assistant's free-text explanations automatically trustworthy. Broader marketing generation, housing-language classifiers, and measured-layout reconstruction remain documented extensions rather than fake implemented capabilities.

## 5. Tool schemas and dispatcher

All tool inputs forbid extra keys. References use the shared `ResourceRef`. In each row, `ctx` is injected, never exposed in the model schema. `command_key` for writes is derived server-side from run ID, model tool-call ID, and operation, never trusted to confer scope.

| Tool | Model arguments | Success data / persisted effect |
|---|---|---|
| `read_property_case` | `{}` | CaseView: public facts, missing information, heads, freshness, modes |
| `fetch_rentcast_evidence` | `{property_ref}` | Evidence artifact; request built from stored facts |
| `calculate_pricing_options` | `{evidence_ref}` | Pricing artifact with evidence/property dependencies |
| `draft_floor_plan` | `{property_ref}` | Floorplan artifact; stored layout description used as input |
| `build_photo_shot_plan` | `{floorplan_ref}` | Photos artifact with plan dependency |
| `draft_listing_copy` | `{property_ref}` | Listing artifact; helper chooses typed claims |
| `submit_for_review` | `{artifact_refs: ResourceRef[]}` | Immutable ReviewBundle; does not approve |

`ToolRegistry` holds name, Pydantic input type, description, required permission, effect type, and handler. `dispatch_tool(ctx, call: ToolCall, budget: RunBudget) -> ToolResult` performs allowlist lookup, strict parse, scope/reference checks, budget reservation, handler, output validation, atomic acceptance, and event emission. No generic URL/file/SQL/shell capability. All exposed output is a minimal projection. Unknown/cross-case refs return the same safe denial without revealing another case's existence/content.

Never trust a model's `is_admin`, claimed human approval, input URL, replacement facts, cached payload, or success boolean. These fields are absent from schemas. Provider text is data and cannot register tools or change the system policy.

## 6. Coordinator, progress, and budgets

`ModelGateway.next_turn(messages, tool_specs, request_budget) -> ModelTurn` returns ordered visible text blocks, tool calls with IDs/names/JSON args, finish reason, and nullable usage. `ModelGateway.generate_structured(purpose, input_data, schema, request_budget) -> GenerationAttempt` supports `floorplan_intent` and `listing_intent`. `GenerationAttempt` preserves raw payload and parse/semantic outcomes. Implement scripted and live providers behind the same interface.

`Coordinator.run(ctx, request: RunRequest) -> RunOutcome` is application-owned. `RunRequest` has user message ≤4,000 chars and expected property revision. One active run per case; a second start returns `run_active`. Tools execute serially, even if the model proposes multiple calls. Capture a tool's current target head before starting it. Do not let a model-emitted final text prove completion; run outcome contains actual committed refs and unresolved issues.

Use `RunRequest = {message, expected_property_revision}`. `RunOutcome` contains `run_id`, `status`, `accepted_artifact_refs`, `review_bundle_ids`, `unresolved_issues: list[ToolError]`, `final_message_id`, and `usage_summary` (counts, elapsed_ms, nullable known_cost_usd, unknown_cost_attempt_count). `CaseView` contains `property`, `public_facts`, `heads` keyed by ArtifactKind with ref/freshness/issues, `missing_fields`, `model_mode`, `rentcast_mode`, `domain_as_of`, recent `conversation`, `active_run_id`, and `latest_review_id`. Define these models once in contracts; generate frontend types from the implemented OpenAPI schema.

`RunBudget.reserve_tool(tool_name, call_id) -> Reservation`; `reserve_model(purpose, input_token_estimate, max_output_tokens, estimated_cost_usd) -> Reservation`; `record_usage(reservation_id, usage: UsageRecord) -> None`; `check_deadline() -> None`. Reservations are counted before dispatch and are idempotent by call/attempt ID. A pre-dispatch cancellation releases unspent monetary reservation while preserving attempted-counter history; dispatched requests reconcile to known or unknown cost, never silently refund. `UsageRecord` separates estimated input tokens, provider-reported tokens, actual known cost, and missing usage. No integer or monetary budget can be reset by a nested helper.

Loop: load scoped context → call model → dispatch allowed tools → append typed results → call model again → stop on final response, clarification, cancellation, exhaustion, or error. Provider protocol errors become failures, not fabricated observations. The live adapter must return tool results using the provider's original call IDs. If one call fails, other independent proposed calls may proceed only when still authorized/current and within budget; never report the batch as entirely successful.

Conversation is persisted per case in `conversation_messages`: `message_id`, case ID, nullable run ID, monotonic case sequence, `role=user|assistant`, visible text, referenced artifacts/reviews, and created_at. Persist the user's message atomically with run creation; persist final/clarifying assistant text once, then emit `assistant_message` with the message ID. Model-internal reasoning is not stored as a conversation message. `GET /case` includes the last 50 visible messages, active_run_id, and latest_review_id; `GET /conversation?before_seq=N` pages older messages. Reload reconnects to the active run/event cursor. The coordinator receives the last 12 visible messages within the configured input cap, current case snapshot, and current refs; prior conversational assertions never replace authoritative current facts. Provider-protocol tool turns remain per-run records. If history exceeds the cap, omit oldest messages with a visible context-trim event; do not invent a summary.

Clarification ends the run with `needs_clarification`; no suspended worker is held. The user confirms required property changes inline and sends a new request. Conversation remains visible. Server-rendered concise progress messages are enough for v1; token-level streaming is optional. Use polling for durable events, not a WebSocket service.

Run states: `queued → running → completed|needs_clarification|failed|cancelled|budget_exhausted|interrupted`. Cancellation flag can be set during running. `completed` means the coordinator ended normally; separate task evaluation determines correctness. A partial run reports completed refs plus unresolved requests. On process restart, previously active runs become `interrupted`; no automatic paid-call replay.

Keep three clocks distinct: domain as-of time for fixture freshness, actual UTC for audit/provider events, and monotonic elapsed time for deadlines. Deterministic tests can inject all three; real-model evaluations with frozen RentCast fixtures may freeze the domain clock while recording real latency/time. Live RentCast always uses actual UTC for freshness and a non-synthetic subject. `MODEL_MODE=live` alone does not prohibit fixture replay.

Default demo limits: 12 attempted tool dispatches; 12 total model attempts shared by coordinator, helpers, and repairs; one repair maximum per generated artifact; 90 seconds elapsed deadline; 30 seconds maximum per model request; 10 seconds maximum per RentCast request; one RentCast HTTP attempt per run. Do not automatically retry HTTP or SDK calls in v1: disable SDK retries. A later explicit user retry starts a new run and may incur a new charge. Valid cache hits do not spend a provider attempt but count as tool dispatches. Empty/invalid model proposals still count toward loop/attempt limits.

Live mode additionally requires configured maximum estimated run spend, model input/output limits, current dated model prices, and an eval-batch spend limit. The budget service reserves projected spend before every nested request, reconciles known usage, and marks unknown usage/cost explicitly. Request/count limits and deadlines are enforced locally; a price/token estimate is **not a provider-guaranteed hard billing cap**. Use account-level controls separately where available. Reject live requests if rate configuration is missing. Never convert missing usage to zero or omit repair cost. Judge-model costs are separate from application costs.

Stop sets cancellation before returning to the UI; subsequent dispatch and artifact acceptance check it. Ask the SDK to cancel in-flight work if possible. Record an already-dispatched result/unknown outcome, but do not install a late artifact after cancellation. Already accepted artifacts remain. Do not claim that Stop refunds a request.

## 7. API and local authority boundary

All routes under `/api`. Vite proxies these to loopback backend so browser requests are same-origin. Backend binds loopback and validates allowed hosts/origins. Demo session is a random opaque, HttpOnly, SameSite=Strict cookie bound server-side to a seeded actor and case; mutating human APIs require a session-bound CSRF token and expected origin. Session bootstrap has no paid work. UI never submits trusted role claims. This is a **local single-user demonstration**, not production authentication or tenant isolation certification.

The runtime model gets no browser cookies, CSRF token, HTTP client, or generic API tool. Its `ExecutionContext` lacks `approve` and `confirm_property` permissions. Tests call the approval service with an agent context and assert denial; merely hiding the button is insufficient. The separate endpoint is an authority boundary inside the same screen.

| Method/path | Contract |
|---|---|
| `GET /health` | Readiness and version only; no secrets |
| `POST /session` | Local session bootstrap; returns CSRF token, case ID, modes |
| `GET /case` | Bound CaseView, current refs/freshness, recent conversation, active run and latest review |
| `GET /conversation?before_seq=N` | Earlier case-bound visible messages, ordered/paginated |
| `PATCH /case` | Human PropertyFacts + expected_revision + idempotency header |
| `GET /artifacts/{id}/revisions/{revision}` | Scoped immutable artifact; safe not-found/denial |
| `POST /artifacts/{id}/revisions` | Human edit of floorplan intent or listing intent, exact source/target refs; validates through same domain rules |
| `POST /runs` | RunRequest + idempotency header; returns run_id, status (202) |
| `GET /runs/{id}` | Scoped status, accepted refs, terminal reason, usage/cost summaries |
| `GET /runs/{id}/events?after_seq=N` | Durable ordered events, next_seq; poll every 500ms while active, stop at terminal |
| `POST /runs/{id}/cancel` | Human command, idempotent; cancellation requested/actual state |
| `GET /reviews/{id}` | Bundle, dependencies, current freshness and approvability |
| `POST /reviews/{id}/approve` | Human-only expected_hash + idempotency header; atomic receipt |
| `GET /reports/{id}` | Only allowlisted redacted stored reports; no arbitrary paths/no eval execution |

Validation failures map to 422; stale/idempotency/run-active conflicts to 409; scoped hidden resources to 404; insufficient permission to 403; provider failures are recorded in run/tool outcomes, not disguised as HTTP success artifacts. Error envelope: `{error:{code,message,details},request_id}`. Generation runs must be cancellable while the server serves other requests; use async IO and move brief blocking SQLite operations off the event loop if needed. A process-local async task supervisor is sufficient; explicitly document loss of in-flight execution on restart.

## 8. Events and data handling

Persist ordered events with `(run_id, seq)`, event ID, timestamp, type, actor class, tool/call/attempt IDs, source refs, outcome code, elapsed milliseconds, mode, nullable token counts and cost. Types: `run_started`, `model_attempted`, `tool_proposed`, `tool_blocked`, `tool_started`, `provider_attempted`, `provider_finished`, `validation_failed`, `artifact_committed`, `review_created`, `assistant_message`, `context_trimmed`, `cancel_requested`, `run_finished`. Human approvals have separate authoritative records/events; never infer them from assistant text.

Record diagnostic facts, not private chain-of-thought. Retain raw synthetic model outputs in eval artifacts for first-pass grading. Production-like public exports contain pseudonymous case IDs, allowlisted fields, and redacted text; secrets/API headers/session tokens/private contact fields never enter model context or exports. Unknown provider outcome and missing telemetry remain explicit.

Run details shows concise actions, versions, validation, blocked attempts, elapsed time, and known/unknown cost. A stored evaluation report is read-only. An API route to start evals or access arbitrary report paths is outside scope.

## 9. Critical invariants to test independently

- No cross-case reads/writes or raw secret leakage through tools, artifacts, final answers, or exported traces.
- No model approval, human impersonation, authoritative fact mutation, or publication path.
- No stale/cancelled result acceptance; no revival when values change back.
- Same logical idempotent command has at most one committed effect.
- Every public listing sentence derives from current confirmed subject facts; generated assumptions/comparable facts are ineligible.
- Price arithmetic and bathroom counts preserve their defined units/semantics.
- Every nested attempt consumes the shared limits, and exhaustion prevents further dispatch.
- Fixture/scripted labels are retained; live errors never become simulated success.
- A zero-case or broken-grader evaluation cannot produce a passing report.

See 04 for independent grading. These invariants are targets to implement and measure, not claims that this document has proven them.
