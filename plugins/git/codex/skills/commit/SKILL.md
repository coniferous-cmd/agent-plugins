---
name: commit
description: Write or review a clear Git commit message from staged changes.
agent: Git Worker
---

# Git Commit

Write or review a focused Conventional Commit message from the staged changes.

## Workflow

1. Inspect the repository status and staged diff.
2. Follow the repository's commit convention when one exists.
3. Use an imperative subject of no more than 72 characters and add a body only when useful.
4. Return the commit message without extra commentary unless the user asks for an explanation.

## Rules

- Do not commit unless the user explicitly requests it.
- Do not stage files automatically.
- Do not include unstaged changes in the message unless the user explicitly asks for them.
- Do not amend, rebase, or force-push unless explicitly requested.
- Keep one commit focused and avoid generic subjects such as `update code` or `fix bug`.
