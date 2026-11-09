# Copilot prompt: Stage 13 — Azure OpenAI model integration and model-resource setup

Implement only Stage 13. Read `.github/copilot-instructions.md`, `docs/BUILD-PROGRESS.md`, the product brief, relevant canonical contracts/evaluation rules, and Azure architecture `docs/06-azure-architecture.md`. Inspect actual code and check results before editing. Use PostgreSQL and the Azure model/deployment architecture specified in the current documents.

Start by listing the contracts and files this stage touches. If a prerequisite is incomplete, report the exact missing interface/check and repair it before dependent implementation. Use the existing design. Do not create billable resources until the relevant cloud stage has the owner-supplied scope/limits; do not ask again for authorization already supplied for that scope.

The stage specification follows verbatim:

## Stage 13 — Azure OpenAI model integration and model-resource setup

**Files:** implement `providers/azure_openai_gateway.py`; finish optional live `providers/rentcast.py`; extend config; `tests/integration/test_model_adapter.py`, `test_live_mode_guards.py`; `infra/model.bicep`, model parameter example; `scripts/azure/model-preflight.sh`; `docs/LIVE-SETUP.md`.

**Consumes:** ModelGateway/structured helper protocols, current Microsoft v1 SDK docs, owner Azure choices, a supported deployed model and the existing shared budget/attempt ledger. Read `docs/06-azure-architecture.md` before touching cloud access.

**Produces:** AzureOpenAIModelGateway using `openai`/`azure-identity`, original call-ID tool round trips, schema-validated structured output, actual Azure-model evidence with fixture property data. Live RentCast remains a separately optional adapter.

- [ ] Resolve and pin compatible SDK versions. Use Azure's `/openai/v1/` endpoint, the actual deployment name, Entra credentials and current documented token audience. Keep opaque protocol continuation items if required; do not expose reasoning. Disable retries. Validate truncation, errors, nullable usage, function-call IDs and function-call outputs with synthetic SDK-shaped adapter tests.
- [ ] Prepare `infra/model.bicep` for the Foundry resource/project and chosen model deployment, or reference explicitly approved existing resources. Verify region/model/quota and dated rates. Prepare the cost/scope/what-if plan before collecting any missing owner choices; never assume the CLI default subscription is approved. Do not hard-code a catalog model name as a deployment name.
- [ ] When the owner has authorized this stage with required account/scope/spend values, provision only its model resources or reuse the specified deployment. Use resource-scoped inference permission for local developer identity; provisioning roles are distinct. Store identifiers, not keys, in local configuration. If access/permission is missing, report the exact blocker and leave live evidence incomplete.
- [ ] Test one actual response, a client-tool request/result loop, one structured helper output, and a forced budget stop against Azure. Then run the existing agent evaluation with frozen evidence, real execution clocks, and fixed fixture-domain time. Record actual model/deployment/version/region and unknown telemetry.
- [ ] Keep the human-operated real-property init CLI for optional live RentCast. Synthetic addresses are never sent to that property-data provider. No live model/provider call occurs on page load, install or offline tests.

**Gate:** `uv run pytest -q tests/integration/test_model_adapter.py tests/integration/test_live_mode_guards.py`; Bicep validates; actual Azure capability smoke and model trials are linked in the report. Mocked adapter success does not complete the Azure-model milestone. The full web deployment occurs in Stage 17.

**Interview focus:** Explain a model deployment versus an agent runtime, how Entra access reaches Azure inference, and which tool effects remain controlled by your code.

At completion, report changed files, actual commands/results, unrun checks, what the tests prove, unresolved issues, and the interview lesson. Update `docs/BUILD-PROGRESS.md`, inspect the diff, and prepare a scoped checkpoint after verification. Do not push, deploy unrelated resources, or start another stage.

Learning checkpoint: read `learning/sections/05-evaluations.md` before implementation. Fill `learning/checkpoints/13.md` with real code/test evidence, explain one path and test, ask two short questions, and stop. Use `./scripts/with-tools.sh` for terminal commands. Track learning separately from implementation.
