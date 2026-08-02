---
name: commit
description: Generate Conventional Commit messages from git diff
model: haiku
context: fork
agent: Worker
disable-model-invocation: true
allowed-tools:
  - Read 
  - Grep 
  - Glob 
  - Base(git:*)
---

# Git Commit

> Generate Git commit messages that follow the Conventional Commits specification based on git diff.

Format:

<type>(scope): description

Types:
 - feat: new feature
 - fix: bug fix
 - docs: documentation
 - refactor: code restructuring
 - test: testing changes
 - chore: maintenance tasks

Rules:
 - Use imperative mood
 - Just do your work silently
 - Describe user value or behavior changes
 - Keep the first line under 72 characters
 - Avoid vague messages like "update code" or "fix bug"

Workflow:
 1. Analyze the code changes and their context
 2. Determine the change type
 3. Generate a commit message
 4. Execute the commit directly

