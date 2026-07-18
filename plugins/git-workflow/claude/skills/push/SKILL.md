---
name: push
model: haiku
description: Push local commits to the remote repository.
disable-model-invocation: false
---
# Git Push

Start a dedicated sub-agent, inspect the current branch and push status, and
push only when explicitly requested. Never force-push or push another branch
without explicit approval.
