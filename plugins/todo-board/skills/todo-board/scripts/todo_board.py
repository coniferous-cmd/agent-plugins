"""Shared project and SQLite operations for the todo-board commands."""
from __future__ import annotations

import os
import sqlite3
import sys
import time
from pathlib import Path

DATABASE_NAME = "todo-board.db"

def project_path(directory=None):
    return Path(directory or os.getcwd()).resolve()

def project_name(directory=None):
    path = project_path(directory)
    return path.name or str(path)

def database_path(directory=None, data_dir=None):
    if data_dir is None:
        override = os.environ.get("CODEX_DATA_DIR")
        if override:
            root = Path(override).expanduser()
        elif sys.platform == "darwin":
            root = Path.home() / "Library" / "Application Support" / "Codex"
        elif os.name == "nt":
            root = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData/Local")) / "Codex"
        else:
            root = Path(os.environ.get("XDG_DATA_HOME", "~/.local/share")).expanduser() / "codex"
    else:
        root = Path(data_dir).expanduser()
    projects = root / "projects"
    projects.mkdir(parents=True, exist_ok=True)
    return projects / DATABASE_NAME

def connect_database(path):
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript("""
        CREATE TABLE IF NOT EXISTS project (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE,
            path TEXT NOT NULL UNIQUE, created_at INTEGER NOT NULL, updated_at INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS task (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL REFERENCES project(id), title TEXT NOT NULL,
            detail TEXT NOT NULL DEFAULT '', done INTEGER NOT NULL DEFAULT 0,
            priority INTEGER NOT NULL DEFAULT 0, created_at INTEGER NOT NULL,
            updated_at INTEGER NOT NULL, deleted_at INTEGER
        );
        CREATE INDEX IF NOT EXISTS task_project_id_idx ON task(project_id);
        CREATE UNIQUE INDEX IF NOT EXISTS project_name_idx ON project(name);
    """)
    return connection

def ensure_project(connection, name, directory):
    now = int(time.time())
    path = str(project_path(directory))
    connection.execute("""
        INSERT INTO project (name, path, created_at, updated_at) VALUES (?, ?, ?, ?)
        ON CONFLICT(name) DO UPDATE SET path = excluded.path, updated_at = excluded.updated_at
    """, (name, path, now, now))
    return connection.execute("SELECT id FROM project WHERE name = ?", (name,)).fetchone()["id"]

def push(connection, name, directory, title, detail="", priority=0):
    now = int(time.time())
    project_id = ensure_project(connection, name, directory)
    connection.execute("""
        INSERT INTO task (project_id, title, detail, priority, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (project_id, title, detail, priority, now, now))
    connection.commit()

def list_tasks(connection, name):
    return connection.execute("""
        SELECT task.* FROM task JOIN project ON project.id = task.project_id
        WHERE project.name = ? AND task.deleted_at IS NULL AND task.done = 0
        ORDER BY task.priority DESC, task.created_at ASC, task.id ASC
    """, (name,)).fetchall()

def next_task(connection, name):
    tasks = list_tasks(connection, name)
    if not tasks:
        return None
    task = tasks[0]
    connection.execute("DELETE FROM task WHERE id = ?", (task["id"],))
    connection.commit()
    return task

def print_task(task):
    print(task["title"])
    if task["detail"]:
        print(task["detail"])
