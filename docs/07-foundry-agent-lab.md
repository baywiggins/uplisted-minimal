# Foundry Agent Service learning lab

This required learning milestone is separate from the deployed application's coordinator. Its purpose is to give you actual managed-agent experience without replacing the validated product during the interview build.

## Three concepts to distinguish

1. **Azure model inference:** your application calls a model endpoint, owns the loop, and executes tools. This is the main Uplisted runtime.
2. **Microsoft Agent Framework:** a client-side framework can manage messages and tool orchestration. It can reduce boilerplate but does not automatically grant correct authorization or budget behavior.
3. **Microsoft Foundry Agent Service:** you create and invoke a versioned prompt-agent definition in a managed service. Client function tools still require your application/client to execute them and return results.

Current Python SDK families and endpoint types differ; do not mix classic project examples with new project APIs. [SDK guide](https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/sdk-overview), [Agent Service overview](https://learn.microsoft.com/en-us/azure/foundry/agents/overview).

## Required small experiment

Create `labs/foundry_agent/` with a separate optional dependency group, README, input fixture, runner and cleanup command. Pin a supported current `azure-ai-projects` 2.x version and `azure-identity` from the official prompt-agent quickstart. Use a Foundry project endpoint `https://<resource>.services.ai.azure.com/api/projects/<project>` with Entra credentials, not the direct `/openai/v1/` inference endpoint.

Create one named versioned prompt agent using `AIProjectClient`, `PromptAgentDefinition`, and the current `agents.create_version()` API. Use the selected deployed model and one client-executed read-only function: `read_property_case` returning a frozen public synthetic projection. Do not give the lab agent database write, approval, publication, shell, browsing, or generic HTTP tools. [Current prompt-agent quickstart](https://learn.microsoft.com/en-us/azure/foundry/agents/quickstarts/prompt-agent).

Implement the explicit client loop: receive a function call → validate name/arguments → execute the local read-only fixture function → send function-call output with the original call ID → obtain final response. Managed registration does not upload/host the Python function body. [Function-calling guide](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/function-calling).

Run three labeled cases:

- Ask for known bedroom/bathroom facts: answer supported by returned subject facts.
- Ask to approve or publish: no such effect or tool is available; report any attempted forbidden call separately.
- Return a malicious note inside the tool data: verify it does not create authority and assess the final answer for unsupported claims.

Limits: three tool dispatch attempts, six client model/response requests, a 90-second client deadline, and an owner-configured estimated lab spend cap. Disable automatic client retries. If the service performs internal work whose count/cost is not exposed, record it as unknown rather than claiming the MAF-backed runtime's exact accounting applies. Keep Azure/model/SDK/agent-version IDs and the trace, with sensitive content capture disabled.

Compare the same three tasks to the application-hosted MAF loop. The resulting table should identify who owns conversation state, tool execution, retries, iteration limits, identity, traces, lifecycle and cleanup. Do not treat a different runtime's successful reply as evidence that the original app's approval/lease invariants passed.

## Compare with the required main MAF agent

The main app already uses MAF from Stage 01. This lab compares application-hosted MAF orchestration with a managed Foundry prompt agent. Explain which service holds protocol state, where tools execute, how limits are observed and where authorization is enforced. MAF is required in the main app, not an optional extension here.

## Evidence and cleanup

Write `docs/FOUNDRY-LAB-RESULTS.md` with actual output, tool traces, known/unknown cost, one comparison table, and limitations. Save exact created agent/version/conversation IDs in an ignored local manifest. Cleanup removes only those lab-owned objects; no wildcard deletion or deleting a shared model deployment. Verify deletion or record why objects remain. Keep desired redacted results first.

Your interview statement after successful execution can be: “I deployed an application-owned agent on Azure and also built a small managed Foundry agent to compare execution boundaries. My tools and deterministic checks still decide what the system is allowed to do.” Do not make that claim before both experiments exist.
