---
name: commit
model: gpt-5.5-mini
description: Guidance for writing clear, well-structured Git commit messages following the seven rules popularized by cbea.ms/git-commit (separate subject/body, 50-char subject, capitalize, no trailing period, imperative mood, wrap body at 72 chars, explain what/why not how). Use this skill whenever the user asks Codex to write, review, improve, or critique a git commit message, asks "how should I write this commit message", wants help summarizing a diff/staged changes into a commit, or is setting up commit message conventions/templates/hooks for a project.
disable-model-invocation: false
---
# Git Commit

## Goal

Create Git commits safely and consistently.

## Workflow

1. Always start a dedicated sub-agent for the commit task.
2. The sub-agent should:
    - Check the repository status.
    - Inspect the staged changes.
    - If there are no staged changes, stop and ask the user to stage files first.
    - Read the staged changes and determine:
        - What changed?
        - Why was it changed?
    - Generate a commit message:
        - Write a concise subject.
        - Add a body only when additional context is helpful.
        - Explain **why**, not **how**.
        - Follow the repository's existing commit convention.
3. Review the sub-agent's result.
4. If the user explicitly requested a commit, create it using the generated message.
5. If the user only requested a commit message, return the generated message without committing.

## Rules

- Use the user's system language unless they request another.
- Keep replies brief.
- Always use a dedicated sub-agent for commit analysis and message generation.
- Never skip the sub-agent, even for small changes.
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

```
<subject>

<body if needed>
```
