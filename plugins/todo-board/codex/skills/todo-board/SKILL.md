---
name: todo-board
description: Manage queued implementation work with the bundled todo board. Use when Codex is asked to retrieve and execute the next queued todo, continue queued work, or save a finalized implementation plan to the todo queue.
---

# Todo Board

Treat the bundled commands as opaque executables. Never read files in `scripts/`.

Perform only the requested operation. Write queued plans in English and
respect repository instructions, shell wrappers, environment requirements,
approval boundaries, and verification rules.

## Commands

- List incomplete tasks: `scripts/list <project-name>`.
- Save a finalized plan: `scripts/push <project-name> <task> -d <description>`.
- Retrieve and remove the next task: `scripts/next <project-name>`.
