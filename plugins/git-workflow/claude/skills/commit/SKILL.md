---
name: commit
model: haiku
description: Guidance for writing clear, well-structured Git commit messages following the seven rules popularized by cbea.ms/git-commit (separate subject/body, 50-char subject, capitalize, no trailing period, imperative mood, wrap body at 72 chars, explain what/why not how). Use this skill whenever the user asks Claude to write, review, improve, or critique a git commit message, asks "how should I write this commit message", wants help summarizing a diff/staged changes into a commit, or is setting up commit message conventions/templates/hooks for a project.
disable-model-invocation: false
---
# Git Commit

Create Git commits safely and consistently. Start a dedicated sub-agent to
inspect staged changes, explain what and why changed, and propose a focused
message. Commit only when explicitly requested; never stage automatically,
amend, rebase, or force-push without explicit approval.
