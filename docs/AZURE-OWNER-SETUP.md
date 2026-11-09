# Azure choices needed before cloud execution

Local Stages 01–12 do not require an Azure account or paid model calls. Docker with Compose is required for the local PostgreSQL service from Stage 03. Stage 13 requires an authorized Azure account/model deployment. Stage 17 deploys the application; Stage 18 exercises Foundry Agent Service.

Copilot should collect missing values together when they become necessary, after preparing the concrete stage artifacts. Do not guess an account, charge a subscription merely because it is the CLI default, or weaken authentication to bypass missing directory permissions. Do not ask again for choices already supplied.

| Choice | Owner value / status |
|---|---|
| Subscription ID and tenant ID | Not supplied |
| Dedicated development resource group/name prefix | Not supplied |
| Permitted region(s) / data location preference | Not supplied |
| Azure OpenAI deployment name/model version, supported tools/structured output, quota | Verify with owner and subscription |
| Monthly environment alert amount and currency | Not supplied; alert is not a spending cap |
| Maximum estimated application run spend | Not supplied |
| Maximum model-evaluation batch spend | Not supplied |
| Maximum managed-agent lab spend | Not supplied |
| Resource expiry date and owner tag | Not supplied |
| Allowed reviewer tenant/object ID | Not supplied |
| Entra app registration available, or directory permission to create one | Not verified |
| Private-network database migration/bootstrap identity | Not selected until infrastructure plan |
| Shared/pre-existing resources that must not be deleted | None declared; verify before provisioning |

Identifiers are configuration, not secret credentials. Keep passwords, tokens, API keys, and client secrets out of this file. Use `az login` interactively when required; do not paste tokens into chat. Workload access uses managed identity. Live RentCast is optional and its key belongs in Key Vault.

The implementation must create a short dated deployment plan with selected resources, cost assumptions, permissions, what-if output, and cleanup scope. If the owner has already authorized that concrete stage within these choices, proceed within the scope. Creating resources is not authorized by merely reading or updating these instructions.
