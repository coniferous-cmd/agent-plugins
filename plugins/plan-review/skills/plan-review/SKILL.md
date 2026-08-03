---
name: plan-review
description: Draft an implementation plan, then ask Codex's rescue skill to audit it before proceeding.
argument-hint: "<task or objective>"
allowed-tools:
  - Read
  - Grep
  - Glob
context: fork
agent: Explore
model: haiku
---

# Plan Review

For the requested task, create a concise but actionable implementation plan. Do not make code changes before the plan has passed review.

## Workflow

1. Inspect the relevant repository context and write a draft plan that includes scope, affected files, implementation steps, validation, and risks.
2. Invoke the `codex:rescue` skill directly for an independent audit. Give it the draft plan and ask it to identify missing requirements, unsafe assumptions, regressions, and insufficient validation. Request prioritized, actionable findings only.

3. Incorporate valid findings into a revised plan. Resolve conflicting feedback using the repository evidence; do not blindly apply it.
4. Present the final plan with a short `Codex rescue audit` section that records either the material changes made or `No material findings`.
5. Ask for confirmation before implementing, unless the user already explicitly authorized implementation after planning.

## Rules

- If the `codex:rescue` skill is unavailable, say so clearly and provide the draft plan for manual review; do not claim it was audited.
- Provide `codex:rescue` only the task context and draft plan needed for a sound review.
- Treat Codex's output as review feedback, not implementation authority.
