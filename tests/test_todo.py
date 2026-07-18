import importlib.util
from importlib.machinery import SourceFileLoader
import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).parents[1]
SCRIPTS = (REPO_ROOT / "plugins/todo-board/skills/todo-board/scripts").resolve()
COMMON = SCRIPTS / "todo_board.py"


def load_todo_module():
    loader = SourceFileLoader("todo_board", str(COMMON))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_tool(*args, cwd, data_dir):
    env = os.environ.copy()
    env["CLAUDE_DATA_DIR"] = str(data_dir)
    command = SCRIPTS / args[0]
    return subprocess.run(
        [sys.executable, str(command), *args[1:]],
        cwd=cwd,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )


def test_all_projects_share_one_database_under_system_data_directory(tmp_path):
    assert {path.name for path in SCRIPTS.iterdir()} >= {"push", "list", "next", "todo_board.py"}
    assert not (REPO_ROOT / "plugins/todo-board/skills/todo-board/tools").exists()
    module = load_todo_module()
    project_a = tmp_path / "opened-project-a"
    project_b = tmp_path / "opened-project-b"
    project_a.mkdir()
    project_b.mkdir()
    data_dir = tmp_path / "system-data" / "Claude"

    path_a = module.database_path(project_a, data_dir)
    path_b = module.database_path(project_b, data_dir)

    assert path_a == data_dir / "projects" / "todo-board.db"
    assert path_b == path_a
    assert path_a.name == "todo-board.db"
    assert path_a.parent == data_dir / "projects"


def test_push_writes_current_project_database_and_next_removes_task(tmp_path):
    project = tmp_path / "opened-project"
    project.mkdir()
    data_dir = tmp_path / "system-data" / "Claude"

    pushed = run_tool(
        "push",
        "opened-project",
        "Implement database storage",
        "-d",
        "Use project-scoped SQLite",
        cwd=project,
        data_dir=data_dir,
    )
    assert pushed.stdout == ""

    module = load_todo_module()
    db_path = module.database_path(project, data_dir)
    assert db_path.is_file()
    assert db_path == data_dir / "projects" / "todo-board.db"

    with module.connect_database(db_path) as connection:
        projects = [
            tuple(row)
            for row in connection.execute("SELECT name, path FROM project").fetchall()
        ]
        tasks = [
            tuple(row)
            for row in connection.execute("SELECT title FROM task").fetchall()
        ]
    assert projects == [(project.name, str(project.resolve()))]
    assert tasks == [("Implement database storage",)]

    listed = run_tool("list", "opened-project", cwd=project, data_dir=data_dir)
    assert "Implement database storage" in listed.stdout
    assert "Use project-scoped SQLite" in listed.stdout

    next_task = run_tool("next", "opened-project", cwd=project, data_dir=data_dir)
    assert "Implement database storage" in next_task.stdout
    assert "Use project-scoped SQLite" in next_task.stdout

    assert "Implement database storage" not in run_tool(
        "list", "opened-project", cwd=project, data_dir=data_dir
    ).stdout

    with module.connect_database(db_path) as connection:
        remaining_tasks = connection.execute("SELECT title FROM task").fetchall()
    assert remaining_tasks == []


def test_next_does_not_consume_task_from_another_opened_project(tmp_path):
    project_a = tmp_path / "project-a"
    project_b = tmp_path / "project-b"
    project_a.mkdir()
    project_b.mkdir()
    data_dir = tmp_path / "system-data" / "Claude"

    run_tool("push", "project-a", "Task A", cwd=project_a, data_dir=data_dir)
    run_tool("push", "project-b", "Task B", cwd=project_b, data_dir=data_dir)

    next_a = run_tool("next", "project-a", cwd=project_a, data_dir=data_dir)
    assert "Task A" in next_a.stdout
    assert "Task B" not in next_a.stdout

    next_b = run_tool("next", "project-b", cwd=project_b, data_dir=data_dir)
    assert "Task B" in next_b.stdout

    module = load_todo_module()
    with module.connect_database(module.database_path(project_a, data_dir)) as connection:
        remaining_tasks = connection.execute(
            "SELECT title FROM task ORDER BY title"
        ).fetchall()
    assert remaining_tasks == []
