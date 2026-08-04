---
name: push
description: Safely push the current branch when requested.
agent: Git Worker
---

# Git Push

1. Check the current branch, status, and its relationship to the upstream when one exists.
2. Push the tracked branch, or use `--set-upstream` if needed.
3. Push only when the user explicitly requests it.

## Rules

- Never use `--force` unless explicitly requested.
- Never push a different branch unless explicitly requested.
- Report errors briefly.
