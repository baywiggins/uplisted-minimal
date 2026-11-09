# Copilot prompt: Stage 09 — Closed tool registry and shared policy enforcement

Implement only Stage 09. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md`, the product brief, relevant canonical contracts/evaluation rules, and Azure architecture `docs/06-azure-architecture.md`. Inspect actual code and check results before editing. Use PostgreSQL and the Azure model/deployment architecture specified in the current documents.

Start by listing the contracts and files this stage touches. If a prerequisite is incomplete, report the exact missing interface/check and repair it before dependent implementation. Use the existing design. Do not create billable resources until the relevant cloud stage has the owner-supplied scope/limits; do not ask again for authorization already supplied for that scope.

The stage specification follows verbatim:

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

At completion, report changed files, actual commands/results, unrun checks, what the tests prove, unresolved issues, and the interview lesson. Update `docs/BUILD-PROGRESS.md`, inspect the diff, and prepare a scoped checkpoint after verification. Do not push, deploy unrelated resources, or start another stage.

Learning checkpoint: read `learning/sections/04-agent-authority.md` before implementation. Fill `learning/checkpoints/09.md` with real code/test evidence, explain one path and test, ask two short questions, and stop. Use `./scripts/with-tools.sh` for terminal commands. Track learning separately from implementation.
