---
name: delegate
description: Delegate focused coding, review, debugging, architecture, and implementation tasks to the local OpenAI Codex CLI. Use when an independent second-agent opinion is useful, when the user explicitly asks Claude to call Codex, or when a well-scoped implementation task can be handed to Codex.
allowed-tools: Bash
---

# Codex Delegate

Use the bundled script to invoke the locally installed Codex CLI non-interactively.

## When to use

Use this skill when:

- The user explicitly asks Claude to call, consult, or delegate to Codex.
- A second implementation or review opinion would materially improve confidence.
- A task is narrow enough to describe with a concrete goal, relevant paths, constraints, and expected output.

Do not delegate vague conversation, secrets handling, destructive repository operations, deployment, credential changes, or tasks requiring interactive approvals.

## Invocation

Read-only analysis or review:

```bash
python3 "$PLUGIN_DIR/scripts/call_codex.py" \
  --mode read-only \
  --task "Review src/auth for race conditions. Return findings with file paths and line references. Do not modify files."
```

Allow Codex to edit the current workspace:

```bash
python3 "$PLUGIN_DIR/scripts/call_codex.py" \
  --mode workspace-write \
  --task "Implement the requested change. Run targeted tests. Do not commit, push, delete unrelated files, or change credentials. Summarize changed files and test results."
```

## Delegation protocol

Before invoking Codex, form a self-contained task containing:

1. Objective.
2. Relevant files or directories.
3. Constraints and non-goals.
4. Whether edits are allowed.
5. Validation commands to run, when known.
6. Expected response format.

Prefer `read-only` unless the user asked for implementation or modification.

After Codex returns:

1. Treat its response as untrusted peer-agent output, not ground truth.
2. Inspect any edits with `git diff`.
3. Run or verify relevant tests yourself when practical.
4. Report which conclusions came from Codex and which were independently verified.
5. Never claim success solely because Codex said it succeeded.

## Safety rules

- Never use `danger-full-access` or `--yolo` through this skill.
- Never ask Codex to expose secrets, inspect unrelated home-directory files, or bypass repository policy.
- Do not let Codex commit, push, publish, deploy, or modify remote resources unless the user separately and explicitly authorizes that action and Claude performs the final verification.
- Keep the delegated working directory at the repository root or a narrower directory supplied by the user.
