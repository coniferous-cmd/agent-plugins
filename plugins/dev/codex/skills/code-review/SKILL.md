---
name: code-review
description: Perform an independent review of code changes, focusing on correctness, security, regressions, performance, tests, and maintainability. Output actionable issues with severity.
disable-model-invocation: false
---

# Code Review

Review scope: $ARGUMENTS

Use `reviewer` to perform an independent check.

## Mandatory checks

- Whether the change meets requirements and acceptance criteria.
- Boundaries, nulls, exceptions, state transitions, concurrency, transactions, and idempotency.
- Authentication, authorization, input validation, and sensitive data.
- API, database, configuration, and caller compatibility.
- Query count, loops, memory, and resource release.
- Whether tests cover happy, failure, and boundary scenarios.
- Whether assertions have been weakened, exceptions swallowed, or temporary workarounds introduced.
- Whether the change scope was expanded.
- Whether the code matches existing project patterns.

## Output

Lead with the verdict: `approve`, `approve-with-notes`, or `request-changes`.

Every issue must include severity, location, evidence, impact, trigger condition, and a minimal fix recommendation. Even when no blocking issues exist, state which key areas were checked.