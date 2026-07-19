---
name: bug-fix
description: Systematically locate and fix bugs. Emphasizes reproduction, hypothesis verification, minimal fix, regression tests, and independent review. Used for errors, abnormal behavior, production issues, or test failures.
disable-model-invocation: false
---

# Bug Fix

Investigate and fix: $ARGUMENTS

## Process

1. Use `bug-investigator` to define actual versus expected behavior and find a reproduction path.
2. Collect logs, inputs, environment, version, and call chain.
3. Build at least two falsifiable hypotheses unless evidence points directly to the root cause.
4. Identify the root cause, trigger conditions, and impact scope.
5. Have `task-orchestrator` build a minimal-fix work package.
6. Prefer having `test-generator` or `coder` add regression tests that fail before the fix.
7. Use `coder` to apply a minimal, safe fix.
8. Run the target test, related module tests, and static checks.
9. Use `reviewer` to check for masking fixes, boundary issues, concurrency, and compatibility.
10. Summarize the root cause, changes, verification, and remaining risks.

## Prohibited

- Adding only null checks without explaining why the data is null.
- Swallowing exceptions, deleting assertions, or increasing retries to hide the problem.
- Writing guesses as confirmed root causes when the issue cannot be reproduced.
- Drive-by refactoring of unrelated code.