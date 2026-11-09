# Copilot prompt: Stage 11 — Human review API and complete one-screen flow

Implement only Stage 11. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md`, the product brief, relevant canonical contracts/evaluation rules, and Azure architecture `docs/06-azure-architecture.md`. Inspect actual code and check results before editing. Use PostgreSQL and the Azure model/deployment architecture specified in the current documents.

Start by listing the contracts and files this stage touches. If a prerequisite is incomplete, report the exact missing interface/check and repair it before dependent implementation. Use the existing design. Do not create billable resources until the relevant cloud stage has the owner-supplied scope/limits; do not ask again for authorization already supplied for that scope.

The stage specification follows verbatim:

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

At completion, report changed files, actual commands/results, unrun checks, what the tests prove, unresolved issues, and the interview lesson. Update `docs/BUILD-PROGRESS.md`, inspect the diff, and prepare a scoped checkpoint after verification. Do not push, deploy unrelated resources, or start another stage.

Learning checkpoint: read `learning/sections/04-agent-authority.md` before implementation. Fill `learning/checkpoints/11.md` with real code/test evidence, explain one path and test, ask two short questions, and stop. Use `./scripts/with-tools.sh` for terminal commands. Track learning separately from implementation.
