# Learn the implementation in six sections

You do not need to absorb the entire specification at once. Read the current section, let Copilot implement one stage, then inspect its learning checkpoint before moving on.

| Section | Stages | Main idea |
|---|---|---|
| [1. Foundations](sections/01-foundations.md) | 01–03 | Reproducible setup, typed data, and safe versioned state |
| [2. Evidence](sections/02-evidence.md) | 04–06 | One-screen inspection, source identity, freshness, and arithmetic |
| [3. Grounded artifacts](sections/03-grounding.md) | 07–08 | Schematics, photo references, and supported listing facts |
| [4. Agent authority](sections/04-agent-authority.md) | 09–11 | Tool choice, budgets, cancellation, and human approval |
| [5. Evaluations](sections/05-evaluations.md) | 12–14 | Independent graders, real-model trials, comparison, and failure analysis |
| [6. Ownership](sections/06-ownership.md) | 15 | Clean-checkout verification and your interview explanation |

## What Copilot does at every stage

1. Explain the purpose and inputs/outputs before editing.
2. Implement only the current numbered stage.
3. Run the relevant checks and show actual results.
4. Walk through one real code/data flow and one meaningful test.
5. Fill the matching checkpoint in `learning/checkpoints/` and ask two short questions.
6. Stop so you can understand, review, or request a correction.

Implementation and learning are separate statuses. A working feature does not mean you understand it yet; asking to continue does not mean you answered the teach-back questions. This tracking is for you, not a grading ceremony.

## Simple prompts you can use

- `Start Stage 01 using COPILOT-START.md.`
- `Explain the current stage more simply, using one concrete example from the code.`
- `Walk me through the request from the UI to the database and back.`
- `Show the test that catches the most important failure in this stage.`
- `Review the current stage against its contracts before we continue.`
- `Continue with only the next numbered stage.`
- `I want to skip the teach-back questions and continue one stage.`

The machine-readable stage-to-section/prompt/checkpoint mapping is [stages.json](stages.json). Technical requirements remain authoritative in [the contracts](../docs/02-contracts.md); learning pages explain them and do not introduce new behavior.
