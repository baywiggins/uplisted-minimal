# Azure deployment, identity and operations

Stages 15, 16, 17. Implement only one stage per turn; this section groups concepts.

## What you are learning

A working cloud prototype needs more than changing a model URL. Entra establishes the human identity; managed identity establishes the application identity. PostgreSQL preserves state across container changes. An old and new revision can overlap, so database ownership and fencing still decide which process may commit.

| Stage | Implementation prompt | Your record |
|---|---|---|
| 15 | [Azure identity, persistent sessions and process ownership](../../prompts/15-azure-identity-persistent-sessions-and-process-ownership.md) | [Checkpoint](../checkpoints/15.md) |
| 16 | [Azure infrastructure, image, telemetry and deployment runbook](../../prompts/16-azure-infrastructure-image-telemetry-and-deployment-runbook.md) | [Checkpoint](../checkpoints/16.md) |
| 17 | [Deploy and verify the Azure prototype](../../prompts/17-deploy-and-verify-the-azure-prototype.md) | [Checkpoint](../checkpoints/17.md) |

## Trace this after implementation

Browser → Entra-protected ingress → application membership → run claim/fence → tool/model call → PostgreSQL commit → correlated Azure telemetry.

## Check your understanding

1. Why does setting maxReplicas to one not prove that only one process can write during deployment?
2. Why can a signed-in user or a managed identity still lack permission to approve a listing?

## Interview takeaway

“I deployed an Azure prototype with explicit identity and transaction boundaries, then tested persistence and revision-overlap failures instead of assuming the platform made them safe.”

Use the claim only after actual implementation and verification.

[Back to learning map](../README.md)
