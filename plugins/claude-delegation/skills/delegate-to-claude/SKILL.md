---
name: delegate-to-claude
description: Delegate a well-scoped task from Codex to the local Claude Code CLI while keeping Claude in the exact same project directory and Git worktree. Use when the user explicitly asks Codex to have Claude inspect, implement, review, or explain something in the current project.
---

# Delegate to Claude

Use this skill only for explicit delegation to the local `claude` CLI. Claude must
operate on the same project that Codex is currently using.

## Required workflow

1. Identify the project root from the current directory:

   ```zsh
   project_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd -P)"
   ```

   A Git repository's top-level directory is the project root. Outside Git,
   use the current directory as the project root.

2. Run Claude from that exact directory. Prefer the bundled helper:

   ```zsh
   plugins/claude-delegation/skills/delegate-to-claude/scripts/delegate-to-claude "<task>"
   ```

   Or use the equivalent command directly:

   ```zsh
   cd "$project_root"
   rtk claude -p "$CLAUDE_TASK"
   ```

3. Tell Claude the absolute project root in the task and state what Codex
   expects back: findings, changed files, tests, and unresolved issues.

4. After Claude returns, inspect its output and the shared working tree. Report
   Claude's result to the user; do not claim changes or tests that were not
   verified in the current project.

## Commit workflow

When the user explicitly asks Claude to commit changes, use a commit subagent
or commit skill available in the current Claude environment or project. Keep
this workflow generic and do not assume a particular plugin or agent name.

The commit workflow must preserve the repository's rules, inspect status and
the staged diff, avoid staging files automatically unless explicitly requested,
and report clearly if no suitable commit subagent or skill is available. Do not
run `git commit` directly as a fallback. A commit request must be explicit;
implementation or review tasks alone must not create a commit.

## Same-project guardrails

- Never use Claude's `--worktree` option.
- Never `cd` to a temporary clone, copied directory, or another checkout.
- Do not use `--add-dir` as a substitute for running in the project root.
- Do not resume an unrelated Claude session. Use a new `claude -p` invocation
  unless the user explicitly identifies a session belonging to this project.
- If the project root cannot be determined or the current directory is not the
  project the user intended, stop and ask before delegating.
- Keep the delegation prompt focused. Claude is a collaborator in the same
  worktree, not an independent implementation target.

## Prompt template

Include all of the following in the delegated prompt:

```text
You are Claude Code working as a delegated collaborator.
Project root: <absolute project root>
Work only in this project and its current Git worktree. Do not create or use a
worktree, clone, temporary copy, or unrelated checkout.

Task: <specific task>
If a commit is explicitly requested, use the project's available commit
subagent or skill. Do not assume a particular plugin name.
Return: summary, files changed, validation performed, and remaining risks.
```
