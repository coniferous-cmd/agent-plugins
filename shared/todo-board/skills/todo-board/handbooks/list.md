---
name: todo-list
description: List incomplete tasks for a project.
---

# List

Use the bundled Python command `scripts/list <project-name>` with the
`agents` Mamba environment. The command reads the shared system data
database and lists only incomplete, non-deleted tasks for the named project.

The project name must be supplied explicitly; it is not inferred from the
current directory.

## Workflow

1. Determine the project name.
2. Run `scripts/list "<project-name>"` with the `agents` Mamba environment.
3. Read the returned task titles and descriptions.
4. If no task is returned, report that the project queue is empty.

## Rules

- Preserve task order returned by the command.
- Do not modify task state while listing.
- Respect repository instructions, shell wrappers, environment requirements,
  and approval boundaries.
