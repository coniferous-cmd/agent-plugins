---
name: todo-board
description: Manage queued implementation work with the bundled todo board. Use when Codex is asked to retrieve and execute the next queued todo, continue queued work, or save a finalized implementation plan to the todo queue.
---

# Todo Board

Use the bundled command files in `scripts/`: `scripts/push`, `scripts/list`,
and `scripts/next`. Shared database operations live in `scripts/todo_board.py`.

The CLI stores every project's tasks in one SQLite database in the system user
data directory: `~/Library/Application Support/Codex/projects/todo-board.db`
on macOS, `$XDG_DATA_HOME/codex/projects/todo-board.db` on Linux (defaulting
to `~/.local/share`), and `%LOCALAPPDATA%/Codex/projects/todo-board.db` on
Windows.
Each command receives the project name as its first argument. The canonical
`pwd` path is retained in the `project` table for reference, and tasks are
associated with the named project in the `task` table.

## Rules:

 - Always use to English for plan.

## Route the request

- To inspect incomplete tasks for a project, read and follow [handbooks/list.md](handbooks/list.md).
- To retrieve and execute the next queued task, read and follow [handbooks/next.md](handbooks/next.md).
- To save a finalized implementation plan, read and follow [handbooks/push.md](handbooks/push.md).

Perform only the requested operation. Respect repository instructions, shell wrappers, environment requirements, approval boundaries, and verification rules.

## Command

 - Todo list: `scripts/list <project-name>`.
 - Push a task: `scripts/push <project-name> <task> -d <description>`.
 - Retrieve and remove the next task: `scripts/next <project-name>`.

The CLI is implemented in Python and must be run with the `agents` Mamba
environment. `push` associates a task with the canonical current directory;
`next` prints and removes the highest-priority incomplete task for that
project. All projects use the same database, while project paths keep their
task queues separate.
