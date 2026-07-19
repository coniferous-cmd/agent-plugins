---
name: feature-development
description: End-to-end development of a new feature, including codebase analysis, design, work-package splitting, implementation, tests, review, and documentation. Used when the user requests a new feature or extending an existing capability.
disable-model-invocation: false
---

# Feature Development

Handle feature request: $ARGUMENTS

## Execution flow

1. Use `task-orchestrator` to establish goals, scope, non-goals, and acceptance criteria.
2. Use `analyst` to investigate existing entry points, call chains, data models, permissions, and tests.
3. For cross-module or high-risk requirements, use `architect` to produce a minimum evolvable design.
4. Split the plan into work packages with dependencies, allowed paths, and validation commands.
5. Independent work packages without file conflicts can be dispatched in parallel via `subagent-orchestrator`.
6. Use `coder` to implement each work package.
7. Use `test-generator` to supplement key failure paths and boundary tests.
8. Use `reviewer` for an independent review.
9. critical/high issues must be fixed and re-reviewed.
10. Use `documenter` to update documentation when needed.

## Completion criteria

- Every acceptance criterion has evidence.
- Relevant tests, type checks, and builds pass, or environment limits are explicitly recorded.
- No open critical/high issues remain.
- The change does not exceed the planned scope.
- The final report includes changes, validation, risks, and incomplete items.