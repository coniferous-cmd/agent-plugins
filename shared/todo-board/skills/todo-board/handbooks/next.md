---
name: next
description: Retrieve and execute the next queued task.
---

# Next

Use the bundled Python command `scripts/next <project-name>` with the `agents`
Mamba environment. The command opens the shared system data database, prints,
and removes only a task belonging to the named project.

The project name must be supplied explicitly; it is not inferred from the
current directory.

## Workflow

1. Run `scripts/next "<project-name>"` with the `agents` Mamba environment and capture its output.
2. Read the returned title, description, and task spec.
3. If no task is returned, report that the queue is empty.
4. Read the repository instructions and inspect the relevant code or docs.
5. Follow the plan constraints, tests, and acceptance criteria.
6. Execute only the returned task, then verify the result.

## Rules

- If retrieval fails, report the failure and stop.
- Respect repository instructions, shell wrappers, environment requirements, and approval boundaries.
