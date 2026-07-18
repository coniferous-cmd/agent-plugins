---
name: todo-push
description: Push finalized plans.
---

# Push

Use the bundled Python command `scripts/push` in the `agents` Mamba
environment. The command writes to the shared system data database and uses
the first argument as the project name.

The project name must be supplied explicitly; it is not inferred from the
current directory.

## Workflow

1. Determine the project name for the current work.
2. Derive a short action title.
3. Write the completed implementation plan description.
4. Resolve the command relative to this skill directory.
5. Run `scripts/push "<project-name>" "<title>" -d "<plan>"` with the `agents` Mamba
   environment.
6. Keep the project name, title, and plan as separate safe arguments.
7. Report success and the resulting task.

## Rules

- Preserve the executable.
- Only push finalized plans.
- Do not create `trough/*.md` files.
- Do not modify or replace the executable.
