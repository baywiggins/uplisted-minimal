# Copilot prompt: Stage 02 — Typed facts, provenance, and artifact contracts

Implement only Stage 02. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md`, the product brief, relevant canonical contracts/evaluation rules, and Azure architecture `docs/06-azure-architecture.md`. Inspect actual code and check results before editing. Use PostgreSQL and the Azure model/deployment architecture specified in the current documents.

Start by listing the contracts and files this stage touches. If a prerequisite is incomplete, report the exact missing interface/check and repair it before dependent implementation. Use the existing design. Do not create billable resources until the relevant cloud stage has the owner-supplied scope/limits; do not ask again for authorization already supplied for that scope.

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

At completion, report changed files, actual commands/results, unrun checks, what the tests prove, unresolved issues, and the interview lesson. Update `docs/BUILD-PROGRESS.md`, inspect the diff, and prepare a scoped checkpoint after verification. Do not push, deploy unrelated resources, or start another stage.

Learning checkpoint: read `learning/sections/01-foundations.md` before implementation. Fill `learning/checkpoints/02.md` with real code/test evidence, explain one path and test, ask two short questions, and stop. Use `./scripts/with-tools.sh` for terminal commands. Track learning separately from implementation.
