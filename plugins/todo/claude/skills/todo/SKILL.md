---
name: todo
description: Manage a FIFO TODO queue with push/approve/next/finish lifecycle
---

# TODO Queue Skill

A FIFO-based TODO management system. Todos flow through a lifecycle:
`REVIEWING → PENDING → PROCESSING → DONE`

Each status transition requires a specific command — no skipping states.

## Database

The database is stored at `<project_root>/.plann/plann.db` (SQLite) and is
auto-created on first use.

## Commands

All commands are run via the `agents` mamba environment:

```bash
mamba run -n agents python3 <plugin_path>/todo.py <command> [args...]
```

Replace `<plugin_path>` with the absolute path to this plugin's directory.

### push — Add a new TODO

```bash
todo.py push "<title>" ["<content>"]
```

- Status is set to `REVIEWING`
- `title` is required, `content` is optional

### approve — Review and approve

```bash
todo.py approve <id>
```

- Transitions `REVIEWING` → `PENDING`
- Fails if the TODO is not in `REVIEWING`

### next — Pop the next pending item

```bash
todo.py next
```

- Takes the earliest (FIFO) `PENDING` item and sets it to `PROCESSING`
- `REVIEWING` items are **not** eligible — they must be approved first

### finish — Mark as done

```bash
todo.py finish <id>
```

- Transitions `PROCESSING` → `DONE`
- Fails if the TODO is not in `PROCESSING`

### list — View the queue

```bash
todo.py list [--status <status>]
```

- Shows all todos ordered by creation time
- Optionally filter by status: `REVIEWING`, `PENDING`, `PROCESSING`, `DONE`

## Rules

1. **Never modify the database directly** — always use `todo.py`
2. Status transitions are enforced — no skipping or jumping
3. `next` follows FIFO order (oldest `PENDING` first)
4. Always use the `mamba run -n agents` environment for execution

## Example Workflow

```bash
# Add a task
todo.py push "Write weekly report" "Summarize progress and blockers"

# Review and approve
todo.py approve 1

# Start working on it
todo.py next

# Mark complete
todo.py finish 1

# Check queue
todo.py list
```
