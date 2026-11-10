# Copilot stage 09

Read COPILOT-START.md, AGENTS.md, docs/08-microsoft-agent-framework.md and the mapped learning section/checkpoint first. Execute only this stage. Teach concepts before asking one optional understanding question at a time. Record actual results and stop.

## Stage 09 — Closed tool registry and shared policy enforcement

**Files:** create `agent/tools.py`, `agent/dispatcher.py`, `telemetry/events.py`, `telemetry/redaction.py`; `tests/unit/test_tool_schemas.py`, `tests/integration/test_dispatcher.py`, `test_redaction.py`; define review service interface (implementation in Stage 11).

**Consumes:** exactly the seven tool argument contracts in §5 and the domain services. Provide a typed stub for `submit_for_review` that reports unavailable until Stage 11; do not fake a successful review.

**Produces:** seven MAF function-tool wrappers, proposal-accounting middleware, `ToolCall`, `ToolRegistry`, `dispatch_tool(ctx, call, budget) -> ToolResult`; durable ordered events and safe public projections.

- [ ] Wire wrappers and pre-parse proposal accounting through the public MAF extension points proven in Stage 01, following docs/08. Preserve one server attempt ID across interception and dispatcher, and test rejected unknown/malformed proposals consume budget even when MAF skips function middleware.
- [ ] Generate tool input schemas from Pydantic, not separately maintained handwritten schemas. Register only the seven tools. Test injected `actor_id`, `case_id`, `role`, arbitrary URL, replacement facts, extra fields, and unknown tools are rejected.
- [ ] Execute a shared order: count server-assigned tool attempt → allowlist → parse → scoped refs → monetary/provider reservation → domain execution → output checks → acceptance transaction → safe result. Test unknown/malformed and repeated provider-call-ID proposals consume allowances; replaying the same server attempt does not double-charge. Record proposed, blocked, started, and committed separately.
- [ ] Bind command keys to server run/call/operation IDs; ledger replay is idempotent. Every artifact writer must use the shared acceptance gate.
- [ ] Add injection tests using untrusted provider text. Assert no registered approval/publish/HTTP/shell tool exists and no forbidden database event occurs. Count attempted forbidden proposals, not just prevented effects.
- [ ] Redact provider headers, credentials, session tokens and seeded private contact markers. Export allowlisted event fields; do not log private model reasoning.

**Gate:** `uv run pytest -q tests/unit/test_tool_schemas.py tests/integration/test_dispatcher.py tests/integration/test_redaction.py`; lint/type checks. Inspect serialized schemas and exported sample trace yourself.

**Interview focus:** The model can propose; server-side code authorizes and commits. Prompt instructions alone are not the enforcement boundary.
