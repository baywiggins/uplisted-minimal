# Copilot prompt: Stage 18 — Build and compare a managed Foundry agent

Implement only Stage 18. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md`, the product brief, relevant canonical contracts/evaluation rules, and Azure architecture `docs/06-azure-architecture.md`. Inspect actual code and check results before editing. Use PostgreSQL and the Azure model/deployment architecture specified in the current documents.

Start by listing the contracts and files this stage touches. If a prerequisite is incomplete, report the exact missing interface/check and repair it before dependent implementation. Use the existing design. Do not create billable resources until the relevant cloud stage has the owner-supplied scope/limits; do not ask again for authorization already supplied for that scope.

The stage specification follows verbatim:

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

At completion, report changed files, actual commands/results, unrun checks, what the tests prove, unresolved issues, and the interview lesson. Update `docs/BUILD-PROGRESS.md`, inspect the diff, and prepare a scoped checkpoint after verification. Do not push, deploy unrelated resources, or start another stage.

Learning checkpoint: read `learning/sections/07-managed-agents.md` before implementation. Fill `learning/checkpoints/18.md` with real code/test evidence, explain one path and test, ask two short questions, and stop. Use `./scripts/with-tools.sh` for terminal commands. Track learning separately from implementation.
