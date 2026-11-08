# Copilot prompt: Stage 09 — Closed tool registry and shared policy enforcement

Implement only Stage 09. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md` if it exists, the product brief, the relevant canonical contracts, and this stage's evaluation requirements. Inspect the actual current code and previous check results before editing. Do not assume a previous stage is complete because a chat said so.

Start by listing the contracts this change relies on and the files you will touch. If a prerequisite stage is incomplete, report the exact missing interface/check and repair that prerequisite before dependent implementation. Keep the chosen architecture.

The stage specification follows verbatim:

## Stage 09 — Closed tool registry and shared policy enforcement

**Files:** create `agent/tools.py`, `agent/dispatcher.py`, `telemetry/events.py`, `telemetry/redaction.py`; `tests/unit/test_tool_schemas.py`, `tests/integration/test_dispatcher.py`, `test_redaction.py`; define review service interface (implementation in Stage 11).

**Consumes:** exactly the seven tool argument contracts in §5 and the domain services. Provide a typed stub for `submit_for_review` that reports unavailable until Stage 11; do not fake a successful review.

**Produces:** `ToolCall`, `ToolRegistry`, `dispatch_tool(ctx, call, budget) -> ToolResult`; durable ordered events and safe public projections.

- [ ] Generate tool input schemas from Pydantic, not separately maintained handwritten schemas. Register only the seven tools. Test injected `actor_id`, `case_id`, `role`, arbitrary URL, replacement facts, extra fields, and unknown tools are rejected.
- [ ] Execute a shared order: allowlist → parse → scoped refs → budget reservation → domain execution → output checks → acceptance transaction → safe result. Record proposed, blocked, started, and committed separately.
- [ ] Bind command keys to server run/call/operation IDs; ledger replay is idempotent. Every artifact writer must use the shared acceptance gate.
- [ ] Add injection tests using untrusted provider text. Assert no registered approval/publish/HTTP/shell tool exists and no forbidden database event occurs. Count attempted forbidden proposals, not just prevented effects.
- [ ] Redact provider headers, credentials, session tokens and seeded private contact markers. Export allowlisted event fields; do not log private model reasoning.

**Gate:** `uv run pytest -q tests/unit/test_tool_schemas.py tests/integration/test_dispatcher.py tests/integration/test_redaction.py`; lint/type checks. Inspect serialized schemas and exported sample trace yourself.

**Interview focus:** The model can propose; server-side code authorizes and commits. Prompt instructions alone are not the enforcement boundary.

At completion, report:
- Implemented behavior and changed files.
- Exact commands executed and observed results; explicitly identify unrun checks.
- Which failure cases the tests exercise and what they do not prove.
- Any deviations or unresolved issues.
- A short explanation I can use in the interview.

Update `docs/BUILD-PROGRESS.md`. Inspect the diff and whitespace checks. Prepare a scoped checkpoint commit after passing checks and review; do not push or deploy. Stop before the next stage. Do not fill benchmark fields with invented numbers.


Learning checkpoint: read `learning/sections/04-agent-authority.md` before implementation. After the stage gate, fill `learning/checkpoints/09.md` with actual code/test evidence, explain the change, ask two short teach-back questions, and stop. Track learning separately from implementation. Use `./scripts/with-tools.sh` for each terminal command.
