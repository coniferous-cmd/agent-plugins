---
name: commit
model: gpt-5.5-mini
description: Guidance for writing clear, well-structured Git commit messages following the seven rules popularized by cbea.ms/git-commit (separate subject/body, 50-char subject, capitalize, no trailing period, imperative mood, wrap body at 72 chars, explain what/why not how). Use this agent whenever the user asks Codex to write, review, improve, or critique a git commit message, asks "how should I write this commit message", wants help summarizing a diff/staged changes into a commit, or is setting up commit message conventions/templates/hooks for a project.
allowed-tools: [Bash, Read, Grep]
disable-model-invocation: false
---
# Git Commit

## Goal

Create Git commits safely and consistently.

## Workflow

1. Inspect the repository status with `git status`.
2. Read the staged changes with `git diff --staged`.
3. If there are no staged changes, stop and ask the user to stage files first.
4. Read the staged changes and determine:
    - What changed?
    - Why was it changed?
5. Generate a commit message:
    - Write a concise subject (≤50 chars, imperative mood, capitalized, no trailing period).
    - Add a body only when additional context is helpful (wrap at 72 chars).
    - Explain **why**, not **how**.
    - Follow the repository's existing commit convention.
6. If the user explicitly requested a commit, create it using the generated message.
7. If the user only requested a commit message, return the generated message without committing.

## Rules

- Use the user's system language unless they request another.
- Keep replies brief.
- Never commit unstaged changes.
- Never stage files automatically unless explicitly requested.
- Never amend, rebase, or force-push unless explicitly requested.
- Keep one commit focused on one logical change.
- Avoid generic messages such as:
    - `Update`
    - `Fix bug`
    - `Misc changes`
    - `WIP`

## Output

When committing:

```
<subject>

<body if needed>
```

When only returning a message (no commit), present it in a fenced block ready for the user to copy.