# Build progress

The folder and existing project-local runtimes are prepared. The target is now Azure; Docker and Azure CLI/account readiness are tracked separately in SETUP-STATUS and AZURE-OWNER-SETUP. No application stages have been implemented or checked by the handoff author. Copilot updates it using observed results, never assumptions.

| Stage | Status | Actual verification | Remaining issue |
|---|---|---|---|
| 01 | Not started | Not run | — |
| 02 | Not started | Not run | — |
| 03 | Not started | Not run | — |
| 04 | Not started | Not run | — |
| 05 | Not started | Not run | — |
| 06 | Not started | Not run | — |
| 07 | Not started | Not run | — |
| 08 | Not started | Not run | — |
| 09 | Not started | Not run | — |
| 10 | Not started | Not run | — |
| 11 | Not started | Not run | — |
| 12 | Not started | Not run | — |
| 13 | Not started | Not run | Azure account/model deployment and explicit spend inputs needed |
| 14 | Not started | Not run | Real comparison and fresh holdout not yet measured |
| 15 | Not started | Not run | Cloud identity and ownership checks not implemented |
| 16 | Not started | Not run | Infrastructure/cost/permission plan not implemented |
| 17 | Not started | Not run | No Azure application deployed |
| 18 | Not started | Not run | No managed Foundry agent created |
| 19 | Not started | Not run | Final local/cloud rehearsal pending |

For each completed stage append: date, commit, files changed, exact commands, actual results, limits/unrun checks, decision changes, and the interview lesson. If only offline checks passed, do not mark live checks passed. Keep failed evaluation artifacts and explain their disposition.

## Separate learning progress

Each stage has a record under `learning/checkpoints/`. All start as not reviewed. Copilot records explained / teach-back reviewed / skipped by user separately from whether implementation checks passed.
