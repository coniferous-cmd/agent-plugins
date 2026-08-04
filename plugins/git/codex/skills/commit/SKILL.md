---
name: commit
description: Use Git Worker to create a focused Git commit from staged changes with a clear Conventional Commit message. Use when the user asks to commit staged work or needs a commit message reviewed.
---

# Git Commit

> Generate Git commit messages that follow the Conventional Commits specification based on git diff.

## Format

`<type>(scope): description`

## Types

- `feat`: new feature
- `fix`: bug fix
- `docs`: documentation
- `refactor`: code restructuring
- `test`: testing changes
- `chore`: maintenance tasks

## Rules

- Use imperative mood.
- Work silently.
- Describe user value or behavior changes.
- Keep the first line under 72 characters.
- Avoid vague messages such as `update code` or `fix bug`.
- If changes contain modifications with clearly different logic, split them into separate commits.

## Workflow

1. Analyze the code changes and their context.
2. Determine the change type.
3. Generate a commit message.
4. Execute the commit directly.
