---
name: push
model: haiku
description: Push local commits to the remote repository.
disable-model-invocation: false
---
# Git Push

## Goal

Push local commits to the appropriate remote branch safely.

## Workflow

1. Always start a dedicated sub-agent.
2. Check the current branch and its push status.
3. If the branch is ready, push it to the tracked remote.
4. If no upstream exists, push with `--set-upstream`.
5. Push only when the user explicitly requests it.

## Rules

- Never use `--force` unless explicitly requested.
- Never push a different branch unless explicitly requested.
- Stop and report any errors.
- Keep replies brief.

## Output

```sh
Pushed <branch> to <remote>
```
