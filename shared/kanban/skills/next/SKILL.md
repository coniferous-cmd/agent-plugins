---
name: todo-next
description: Retrieve and execute the next queued implementation task.
---

# Todo Next

Use `../scripts/next <project-name>` with the `agents` Mamba environment. It
prints and removes the highest-priority pending task for that project.

If it returns no task, report that the queue is empty. Otherwise, read the
repository instructions, implement only the returned task, and verify it.
