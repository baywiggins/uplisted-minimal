# Copilot prompt: Stage 11 — Human review API and complete one-screen flow

Implement only Stage 11. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md` if it exists, the product brief, the relevant canonical contracts, and this stage's evaluation requirements. Inspect the actual current code and previous check results before editing. Do not assume a previous stage is complete because a chat said so.

Start by listing the contracts this change relies on and the files you will touch. If a prerequisite stage is incomplete, report the exact missing interface/check and repair that prerequisite before dependent implementation. Keep the chosen architecture.

The stage specification follows verbatim:

## Stage 11 — Human review API and complete one-screen flow

**Files:** create `domain/review.py`, `api/routes.py`, `api/session.py`; extend app/CLI; `tests/integration/test_api.py`, `test_review.py`, `test_human_edits.py`; `web/src/api/client.ts`, generated `types.ts`, integrated workspace views including `ReviewView.tsx`; `web/e2e/workspace.spec.ts`, Playwright config.

**Consumes:** all prior contracts; API table and local security boundary in §7. Replace shell fixtures with the real local API; keep provider modes scripted/fixture.

**Produces:** API endpoints, separate human mutation context, exact-version approval, polling events, persisted case conversation/reconnect, active run/Stop control, real artifact views/edits, and completed local browser journey.

- [ ] Implement local session/CSRF/origin checks and scoped API projections. Never accept body-supplied actor/permissions. Test agent-context approval and fact mutation denial, missing CSRF, cross-case lookup, and safe error responses.
- [ ] Implement review creation and approval transactions with nonempty unique membership and an active/non-cancelled run at creation. Show exact included artifacts; a subset approval does not mean the original full task succeeded. Tests cover missing artifact, stale transitive dependency, expired evidence, wrong hash, repeated approval, edit/approve race, and facts changed then changed back. A success receipt does not publish.
- [ ] Implement human artifact revisions through the same domain validators and destination-head checks, with explicit human permission. An active run is not required for a human edit. A late generator must not overwrite that revision.
- [ ] Integrate API client with 500ms ordered-event polling while active; deduplicate by run/sequence/message ID. Persist final/clarifying text and reconnect on reload using active_run_id and conversation history. Stop polling at terminal. Refetch current heads after accepted changes; avoid optimistic approval before server receipt.
- [ ] Wire conversation, property form, supported listing edits, plan edits, partial failures, retry as new run, Stop, source inspection, review, and redacted Run details. Preserve unsaved input and focus when results arrive.
- [ ] Add Playwright flow for same-route request → inspect → edit → regenerate → review → approve. Add stale approval, cancellation, partial failure, no side effects on tab changes, keyboard-only and narrow-view flows. Test no unknown network domains.

**Gate:** `uv run pytest -q tests/integration/test_api.py tests/integration/test_review.py tests/integration/test_human_edits.py`; frontend check/test/build; `npm --prefix web run test:e2e`. Review actual UI behavior, not just screenshots.

**Interview focus:** Show approval as a transaction over an exact snapshot, and show the UI truthfully representing it.

At completion, report:
- Implemented behavior and changed files.
- Exact commands executed and observed results; explicitly identify unrun checks.
- Which failure cases the tests exercise and what they do not prove.
- Any deviations or unresolved issues.
- A short explanation I can use in the interview.

Update `docs/BUILD-PROGRESS.md`. Inspect the diff and whitespace checks. Prepare a scoped checkpoint commit after passing checks and review; do not push or deploy. Stop before the next stage. Do not fill benchmark fields with invented numbers.


Learning checkpoint: read `learning/sections/04-agent-authority.md` before implementation. After the stage gate, fill `learning/checkpoints/11.md` with actual code/test evidence, explain the change, ask two short teach-back questions, and stop. Track learning separately from implementation. Use `./scripts/with-tools.sh` for each terminal command.
