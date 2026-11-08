# Copilot prompt: Stage 02 — Typed facts, provenance, and artifact contracts

Implement only Stage 02. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md` if it exists, the product brief, the relevant canonical contracts, and this stage's evaluation requirements. Inspect the actual current code and previous check results before editing. Do not assume a previous stage is complete because a chat said so.

Start by listing the contracts this change relies on and the files you will touch. If a prerequisite stage is incomplete, report the exact missing interface/check and repair that prerequisite before dependent implementation. Keep the chosen architecture.

The stage specification follows verbatim:

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

At completion, report:
- Implemented behavior and changed files.
- Exact commands executed and observed results; explicitly identify unrun checks.
- Which failure cases the tests exercise and what they do not prove.
- Any deviations or unresolved issues.
- A short explanation I can use in the interview.

Update `docs/BUILD-PROGRESS.md`. Inspect the diff and whitespace checks. Prepare a scoped checkpoint commit after passing checks and review; do not push or deploy. Stop before the next stage. Do not fill benchmark fields with invented numbers.


Learning checkpoint: read `learning/sections/01-foundations.md` before implementation. After the stage gate, fill `learning/checkpoints/02.md` with actual code/test evidence, explain the change, ask two short teach-back questions, and stop. Track learning separately from implementation. Use `./scripts/with-tools.sh` for each terminal command.
