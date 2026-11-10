# Copilot stage 18

Read COPILOT-START.md, AGENTS.md, docs/08-microsoft-agent-framework.md and the mapped learning section/checkpoint first. Execute only this stage. Teach concepts before asking one optional understanding question at a time. Record actual results and stop.

## Stage 18 — Build and compare a managed Foundry agent

**Files:** `labs/foundry_agent/README.md`, runner/fixture/cleanup code and optional dependency group; `docs/FOUNDRY-LAB-RESULTS.md`; `tests/labs/test_foundry_function_boundary.py`.

**Consumes:** `docs/07-foundry-agent-lab.md`, actual Foundry project/model access and an owner-configured lab spend cap. This is separate from the deployed application coordinator.

**Produces:** one actual versioned Foundry Agent Service prompt agent, one client-executed read-only property function, three measured test cases and a lifecycle/authority comparison.

- [ ] Use the current supported new-project SDK/API and the project endpoint, not the direct model endpoint. Pin versions and verify role scope before creating the lab agent. Keep all production write/approval tools absent.
- [ ] Create the versioned prompt agent and implement the bounded function-call/output client loop. Test names/arguments/call IDs and disallowed function handling offline before live execution.
- [ ] Run the known-facts, forbidden-approval, and injected-tool-text scenarios. Record actual output/trace and limits, including unknown internal service work/cost. Compare with the main MAF-backed runtime on the same inputs, identifying framework versus hosted-service responsibilities.
- [ ] Write who owns conversation, tools, retries, iteration limits, identity, tracing and cleanup in each design. The main product already uses MAF; compare that framework-hosted runtime with the managed service using actual traces.
- [ ] Delete only the exact lab-owned agent/version/conversations captured in its manifest once results are saved; verify cleanup or state what remains. Retain the application/model resources needed for the interview.

**Gate:** offline boundary tests pass; actual Agent Service resource/invocation evidence and the three-case comparison exist; lab lifecycle/cleanup is recorded. A direct model response does not satisfy this managed-agent milestone.

**Interview focus:** Explain Azure-hosted model inference versus managed agent service versus client framework orchestration, using code and traces from both systems.
