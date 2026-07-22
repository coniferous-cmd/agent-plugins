import os
import sqlite3
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).parents[1]
SKILLS = REPO_ROOT / "plugins/todo-board/codex/skills"
SCRIPTS = SKILLS / "scripts"


def run_tool(*args, cwd, data_dir):
    env = os.environ.copy()
    env["CODEX_DATA_DIR"] = str(data_dir)
    return subprocess.run(
        [sys.executable, str(SCRIPTS / args[0]), *args[1:]],
        cwd=cwd,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )


def task_titles(data_dir):
    database = data_dir / "projects" / "todo-board.db"
    with sqlite3.connect(database) as connection:
        return [row[0] for row in connection.execute("SELECT title FROM task ORDER BY id")]


def test_todo_board_has_two_skills_and_two_self_contained_scripts():
    assert sorted(
        path.relative_to(SKILLS).as_posix()
        for path in SKILLS.rglob("*")
        if path.is_file()
    ) == ["next/SKILL.md", "push/SKILL.md", "scripts/next", "scripts/push"]

    assert "scripts/push" in (SKILLS / "push/SKILL.md").read_text()
    assert "scripts/next" in (SKILLS / "next/SKILL.md").read_text()


def test_push_writes_and_next_returns_then_removes_the_task(tmp_path):
    project = tmp_path / "opened-project"
    project.mkdir()
    data_dir = tmp_path / "system-data" / "Codex"

    pushed = run_tool(
        "push", "opened-project", "Implement database storage", "-d",
        "Use project-scoped SQLite", cwd=project, data_dir=data_dir,
    )
    assert pushed.stdout == ""
    assert task_titles(data_dir) == ["Implement database storage"]

    next_task = run_tool("next", "opened-project", cwd=project, data_dir=data_dir)
    assert next_task.stdout.splitlines() == [
        "Implement database storage", "Use project-scoped SQLite"
    ]
    assert task_titles(data_dir) == []


def test_next_does_not_consume_a_task_from_another_project(tmp_path):
    project_a = tmp_path / "project-a"
    project_b = tmp_path / "project-b"
    project_a.mkdir()
    project_b.mkdir()
    data_dir = tmp_path / "system-data" / "Codex"

    run_tool("push", "project-a", "Task A", cwd=project_a, data_dir=data_dir)
    run_tool("push", "project-b", "Task B", cwd=project_b, data_dir=data_dir)

    assert "Task A" in run_tool("next", "project-a", cwd=project_a, data_dir=data_dir).stdout
    assert "Task B" in run_tool("next", "project-b", cwd=project_b, data_dir=data_dir).stdout
