---
name: unit-testing
description: Design high-signal unit and regression tests for existing or new code, covering behavior, boundaries, and failure paths. Avoid brittle tests against private implementation details.
disable-model-invocation: false
---

# Unit Testing

Test target: $ARGUMENTS

## Steps

1. Identify public behaviors, acceptance criteria, and the highest-risk branches.
2. Read the project's test framework, naming, fixture, and mock conventions.
3. Build a test matrix.
4. Prefer tests that fail before the fix or that fail when new functionality is missing.
5. Execute and verify that failure reasons match the target.
6. After implementation, run again to ensure tests do not pass for the wrong reasons.

## Principles

- Keep Arrange / Act / Assert clear.
- One test expresses one behavior, but may include multiple related assertions.
- Test output, not private implementation steps.
- Mock external dependencies; do not mock the core unit under test.
- Avoid global state, real network calls, and fixed sleeps.
- Use controllable sources for time, randomness, and UUIDs.
- Parameterize tests to cover representative boundaries.
- Exception tests verify type and stable business messages.
- Do not chase meaningless 100% coverage.

Call `test-generator` to implement the tests when needed, and have `reviewer` verify the tests can actually prevent regressions.