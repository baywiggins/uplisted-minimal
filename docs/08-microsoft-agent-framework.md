# Microsoft Agent Framework: required core runtime

MAF is the main application's required orchestration framework, beginning in Stage 01. The main app runs a Python MAF Agent with seven function tools on Azure Container Apps. Stage 18 compares that app with a managed Foundry Agent Service prompt agent. MAF, Azure model hosting, and Agent Service are distinct concepts.

## Ownership and interfaces

- MAF owns the model/tool iteration, tool-result messages, provider protocol continuation, and per-run AgentSession. There must be no second handwritten next_turn loop.
- `Coordinator.run(ctx, request) -> RunOutcome` is a thin application lifecycle adapter around the MAF agent execution API. It starts/finishes the durable run, maintains its lease, propagates cancellation, projects events and computes outcomes from committed artifacts.
- `build_agent(ctx, budget, client)` constructs a run-scoped MAF Agent with only the seven registered function tools and required middleware. Server actor/case/run/fence context is injected through runtime-only context, never model-visible parameters.
- `ScriptedChatClient` implements the installed MAF client contract and emits deterministic framework responses. Offline tests execute the real MAF loop, tool wrappers and middleware with this client; they must not stub Agent.run or substitute a handwritten loop.
- `build_live_client(settings)` constructs the MAF Responses client configured explicitly for Azure. MAF provider packages and core versions are locked together in Stage 01. Current Microsoft Python docs use `agent_framework.Agent`, `agent_framework.openai.OpenAIChatClient`, and `agent-framework-openai`; verify exact installed signatures rather than combining old ChatAgent/AzureOpenAIResponsesClient tutorials with new packages. Prefer stable compatible releases; if required functionality is prerelease, document that exact pinned release and limitation.
- `StructuredGenerator.generate_structured(purpose, input_data, schema, request_budget) -> GenerationAttempt` uses a tools-disabled MAF client path for floorplan/listing helper generation. Scripted and live implementations use the same accounting hook. Helper output is still validated by independent domain code.
- Domain services and PostgreSQL enforce authorization, strict validation, immutable versions, stale-write prevention and human approval. MAF sessions are ephemeral per-run protocol state, not the authoritative property store or approval record. Never share sessions across cases or helpers; a restart interrupts expired work rather than automatically resuming paid calls.

## Mandatory enforcement placement

1. Before each underlying model request, reserve from the shared 12-model-attempt budget, check cancellation/deadline/lease, and record known or unknown usage. This includes nested helper and repair requests. Disable provider retries and automatic framework retries.
2. Inspect every returned model tool proposal at a public client-response interception point before MAF tool lookup/argument parsing. Assign a server attempt ID from run/model-attempt/tool-slot and reserve a tool attempt, including unknown names, invalid JSON and repeated provider call IDs. Stop over-budget proposals before execution. For streaming, assemble a complete call before reserving once; start with non-streaming model responses and application progress events to keep this simple.
3. MAF function wrappers invoke only `dispatch_tool`. Dispatcher reservation uses the same server attempt ID, so it is idempotent, then enforces allowlist/schema/scope/provider budget/domain validation/commit gates. Invalid proposals rejected earlier still get a durable blocked event. Never rely exclusively on function middleware: unknown names and parser failures can occur before a function is invoked.
4. Configure serial function execution and bounded framework iterations. Framework limits are additional safeguards; the application ledger is authoritative and includes nested generation. Terminal budget/cancellation/lease exceptions must stop the MAF run, not become a recoverable tool error that causes more model requests.
5. Safe tool failures return typed redacted results. Raw SDK exceptions, credentials and private reasoning must not appear in model messages or UI. Only actual committed references establish successful effects.
6. Use a separate human endpoint to approve the exact review hash/version. Framework tool approval is not an application approval receipt. No publish/approve/shell/arbitrary URL tool is registered.

Stage 01 proves the installed public client/middleware extension points with one harmless offline tool call. Stage 09 implements policy wrappers; Stage 10 proves end-to-end enforcement. If the installed SDK cannot expose a required boundary, stop that dependent stage and document the concrete API gap; do not silently replace MAF or weaken the contract.

## Required evidence

- Stage 01: real MAF Agent + scripted client → one harmless function → result → final response, with no external sockets or credentials.
- Stage 09: exact seven tool schemas; server identities absent; wrappers cannot bypass dispatcher.
- Stage 10: real MAF loop tests for malformed/unknown proposals, repeated call IDs, shared helper budget exhaustion, serial calls, cancellation, stale writes, lease loss, session isolation and no hidden retries.
- Stage 12: include framework/provider package versions in reports; outcome graders remain independent of framework messages and self-reported success.
- Stage 13: switch only the client configuration to live Azure; verify actual tool-result round trip and the same policy hooks.
- Stage 19: explain a request through MAF and show a blocked action and measured failure analysis.

## Official references checked November 9, 2026

- [Pipeline](https://learn.microsoft.com/en-us/agent-framework/agents/agent-pipeline)
- [Function tools and runtime context](https://learn.microsoft.com/en-us/agent-framework/agents/tools/function-tools)
- [Python Responses client and explicit Azure routing](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/model-providers/openai)
- [Azure provider migration guidance](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/model-providers/azure-openai)
- [Framework source and samples](https://github.com/microsoft/agent-framework)

Read the Python sections and record installed versions. Provider/client names evolve; use current official examples compatible with the lockfile. This document specifies required behavior, not a claim that the SDK integration has already been implemented or tested.
