# Copilot repair prompt

Stay within the current stage. Read its specification and the actual failing check output before changing code. First state the violated requirement and your evidence for the root cause. If the failure is unrelated, separate it without concealing it.

Reproduce the smallest meaningful failing case. Fix the responsible implementation; do not weaken expected values, remove an assertion, skip the test, disable strict typing, swallow an exception, increase permissions, silently use fixture data in live mode, or change the evaluator merely to make the result green.

If a contract genuinely needs revision, explain the concrete contradiction and propose a narrow documented change before changing dependent code. Routine implementation mistakes do not require redesigning the application.

Run the targeted test and relevant existing checks after the fix. Show actual commands, results, changed files, and remaining failures. Keep the original failing evaluation artifact and add an independent regression where appropriate. Update `docs/BUILD-PROGRESS.md`; do not start the next stage yet.
