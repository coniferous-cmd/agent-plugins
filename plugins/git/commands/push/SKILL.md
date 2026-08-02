---
name: push
description: Safely push the current branch when requested.
---

# Git Push

Workflow:
 1. Check the current branch, its status, and its relationship to the upstream when one exists.
 2. Push the tracked branch, or use `--set-upstream` if needed.
 3. Push only when the user explicitly requests it.

Rules:
 - Just do your work silently.
 - Never use `--force` unless explicitly requested.
 - Never push a different branch unless explicitly requested.
 - Report errors briefly.
