# Copilot stage 16

Read COPILOT-START.md, AGENTS.md, docs/08-microsoft-agent-framework.md and the mapped learning section/checkpoint first. Execute only this stage. Teach concepts before asking one optional understanding question at a time. Record actual results and stop.

## Stage 16 — Azure infrastructure, image, telemetry and deployment runbook

**Files:** `Dockerfile`, `.dockerignore`, `infra/main.bicep`, modules/parameter example from the Azure architecture; `scripts/azure/preflight.sh`, `what-if.sh`, `deploy.sh`, `smoke.sh`, `teardown.sh`; `telemetry/azure_monitor.py`; `docs/AZURE-DEPLOYMENT.md`; tests for cloud configuration, image health and redaction.

**Consumes:** tested application, Stage 13 resource identities, Stage 15 authority/ownership boundaries, owner account/region/budget choices.

**Produces:** buildable single frontend/API image, validated infrastructure definitions, explicit auth/database migration bootstrap, telemetry integration and reviewable deployment/cleanup commands. This stage prepares the full deployment; it does not count as a running Azure prototype.

- [ ] Build a multistage Linux image with locked dependencies and built Vite assets, non-root runtime, one Uvicorn worker on port 8000, liveness/readiness, graceful shutdown and no secrets/local tools/reports in context. Verify the target platform instead of assuming the Mac architecture works in Azure.
- [ ] Define Container Apps/ACR, user-assigned identity, VNet/private DNS/PostgreSQL with public DB access disabled, Key Vault, monitoring and budget alerts. Reuse/reconcile the model module explicitly. Parameterize model, region, SKUs, identity mappings and owner/expiry; do not invent bill estimates or quota.
- [ ] Define single-tenant Entra authentication and the application reviewer/case allowlist, with no public bypass route to the backend. Document directory permissions/app-registration bootstrap separately. Prepare Key Vault secret injection without exposing secret values in outputs.
- [ ] Define managed-identity access to Azure inference, ACR and Key Vault plus a narrowly privileged PostgreSQL runtime identity. Define a separate migration identity and manually triggered one-shot private-network migration Job. App containers do not perform schema administration.
- [ ] Instrument redacted OpenTelemetry spans to Application Insights using current supported packages. Preserve durable audit events independently. Test a seeded secret/contact marker is absent from spans and output bundles; content capture stays disabled by default.
- [ ] Generate a concrete dated deployment plan/cost estimate, Bicep validation and what-if when authorized Azure access exists. Teardown defaults to inventory/dry run and names the exact dedicated group and separately tracked lab/directory objects. Do not auto-deploy on PRs.

**Gate:** `docker build` and local container health work; `az bicep build --file infra/main.bicep` succeeds; cloud config/redaction tests pass; deployment plan names actual parameters and permissions or explicitly identifies missing inputs. Owner review is of concrete resources/commands; no new permission question is needed when that scope is already authorized.

**Interview focus:** Show what infrastructure owns, what your runtime owns, and how identity/telemetry/cost choices preserve the existing safety boundaries.
