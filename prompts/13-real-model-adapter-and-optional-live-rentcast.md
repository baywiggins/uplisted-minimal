# Copilot prompt: Stage 13 — Real model adapter and optional live RentCast

Implement only Stage 13. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md` if it exists, the product brief, the relevant canonical contracts, and this stage's evaluation requirements. Inspect the actual current code and previous check results before editing. Do not assume a previous stage is complete because a chat said so.

Start by listing the contracts this change relies on and the files you will touch. If a prerequisite stage is incomplete, report the exact missing interface/check and repair that prerequisite before dependent implementation. Keep the chosen architecture.

The stage specification follows verbatim:

## Stage 13 — Real model adapter and optional live RentCast

**Files:** implement `providers/anthropic_gateway.py`; finish live `providers/rentcast.py`; extend config; `tests/integration/test_model_adapter.py`, `test_live_mode_guards.py`; `docs/LIVE-SETUP.md`; separately marked integration-smoke commands.

**Consumes:** official current provider docs, installed SDK version, existing interfaces, budget/attempt ledger, explicit owner-provided runtime credentials and limits.

**Produces:** real `ModelGateway`, protocol-correct client tool round trips and structured helper calls; optional live RentCast adapter; mode labels and live-mode guards. No cloud deployment.

- [ ] Read current official SDK docs; implement against the installed version and record version/model ID. Model ID is configuration, not a guessed constant. Support real tool call IDs, error tool results, usage, output limits, timeouts, truncation, and malformed response handling. Disable SDK retries.
- [ ] Adapter tests use recorded/provider-shaped synthetic responses via injected transport. Check exact mapping and call-ID round trips; do not require a key to run unit tests. Keep normalized fixture evidence distinct from raw RentCast response fixtures.
- [ ] Add explicit live-mode config validation: keys present only server-side, model/rate limits set, actual UTC domain clock and authorized non-synthetic property required for live RentCast. A real model with fixture evidence may use frozen domain time; real monotonic deadlines and UTC audit timestamps remain active. A synthetic replay address cannot be sent to a real provider.
- [ ] Implement the human-operated `init-case --input ... --confirm-non-synthetic` CLI and `CASE_ID` selection from contracts §1 so optional live RentCast has a real, explicitly confirmed subject. Test synthetic-case rejection. Write setup instructions with empty environment examples and official links. Explain runtime API billing separately from Copilot subscription. Missing credentials are a documented blocked live check, never a reason to fabricate successful runs.
- [ ] After the owner explicitly enables live model access and spend limits, run a small live-model/frozen-evidence smoke, then real-model evaluation. Record raw/accepted results and failures. Live RentCast is a separately enabled smoke on an authorized real address; if omitted, disclose that integration is unverified.

**Gate:** adapter/guard tests pass offline; real-model evidence exists before claiming model behavior. No live request is made by CI, install, page load, or ordinary test commands. If credentials are absent, mark this stage's live checks incomplete and continue preparing nondependent documentation; do not label the final project fully evaluated.

**Interview focus:** Explain precisely which component is real, replayed, or simulated, and what each configuration proves.

At completion, report:
- Implemented behavior and changed files.
- Exact commands executed and observed results; explicitly identify unrun checks.
- Which failure cases the tests exercise and what they do not prove.
- Any deviations or unresolved issues.
- A short explanation I can use in the interview.

Update `docs/BUILD-PROGRESS.md`. Inspect the diff and whitespace checks. Prepare a scoped checkpoint commit after passing checks and review; do not push or deploy. Stop before the next stage. Do not fill benchmark fields with invented numbers.


Learning checkpoint: read `learning/sections/05-evaluations.md` before implementation. After the stage gate, fill `learning/checkpoints/13.md` with actual code/test evidence, explain the change, ask two short teach-back questions, and stop. Track learning separately from implementation. Use `./scripts/with-tools.sh` for each terminal command.
