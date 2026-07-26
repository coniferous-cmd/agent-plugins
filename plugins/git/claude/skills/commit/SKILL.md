---
name: commit
description: Generate Conventional Commit messages from git diff
parameters:
  - name: language
    type: string
    description: Language for commit message (e.g., en, zh, es, fr)
    default: en
---

# Git Commit Skill

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
 - Keep the first line under 72 characters
 - Avoid vague messages like "update code" or "fix bug"
 - Describe user value or behavior changes
 - Require an new `sub agent` to execution

Workflow:
 1. Analyze the code changes and their context
 2. Determine the change type
 3. Generate a commit message
 4. Output one recommended commit message

