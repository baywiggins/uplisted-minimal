# Managed Foundry agents versus your own coordinator

Stages 18. Implement only one stage per turn; this section groups concepts.

## What you are learning

A model API provides inference. Agent Framework can orchestrate a client loop. Foundry Agent Service stores and runs agent definitions, but client function tools still execute in your client. Learn these distinctions using one read-only tool and the same small task set.

| Stage | Implementation prompt | Your record |
|---|---|---|
| 18 | [Build and compare a managed Foundry agent](../../prompts/18-build-and-compare-a-managed-foundry-agent.md) | [Checkpoint](../checkpoints/18.md) |

## Trace this after implementation

Versioned Foundry prompt agent → function_call → bounded client dispatcher → frozen property result → function_call_output → managed response → trace/evaluation → exact-ID cleanup.

## Check your understanding

1. Which parts of your MAF-backed runtime are now handled by the service, and which still belong to your client?
2. Why does a managed agent definition not grant a function permission to approve or publish?

## Interview takeaway

“I compared Azure-hosted inference and a real managed agent using the same read-only tasks, recording the differences in tool execution, lifecycle and observable cost.”

Use the claim only after actual implementation and verification.

[Back to learning map](../README.md)
