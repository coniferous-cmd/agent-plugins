#!/usr/bin/env python3
"""
TODO Queue — FIFO-based TODO management system.

Usage:
    todo.py push <title> [<content>]
    todo.py approve <id>
    todo.py next
    todo.py finish <id>
    todo.py list [--status <status>]

Database: <project_root>/.plann/plann.db
"""

import argparse
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path


# ── Database ────────────────────────────────────────────────────────────────

def get_db_path() -> Path:
    """Return path to plann.db, creating .plann/ dir if needed."""
    project_root = Path.cwd().resolve()
    db_dir = project_root / ".plann"
    db_dir.mkdir(parents=True, exist_ok=True)
    return db_dir / "plann.db"


def get_connection() -> sqlite3.Connection:
    """Get a connection, creating the database and table if needed."""
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            title      TEXT    NOT NULL,
            content    TEXT,
            status     TEXT    NOT NULL DEFAULT 'REVIEWING',
            created_at TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
        )
    """)
    conn.commit()
    return conn


STATUSES = {"REVIEWING", "PENDING", "PROCESSING", "DONE"}


# ── Commands ────────────────────────────────────────────────────────────────

def cmd_push(args: argparse.Namespace) -> None:
    """Insert a new TODO with status REVIEWING."""
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO todos (title, content, status) VALUES (?, ?, 'REVIEWING')",
        (args.title, args.content or ""),
    )
    todo_id = cursor.lastrowid
    conn.commit()
    conn.close()
    print(f"Created TODO #{todo_id}: {args.title} (REVIEWING)")


def cmd_approve(args: argparse.Namespace) -> None:
    """Transition REVIEWING → PENDING."""
    conn = get_connection()
    row = conn.execute("SELECT id, title, status FROM todos WHERE id = ?", (args.id,)).fetchone()
    if row is None:
        sys.exit(f"TODO #{args.id} not found")
    if row["status"] != "REVIEWING":
        sys.exit(f"TODO #{args.id} is in {row['status']}, expected REVIEWING")
    conn.execute("UPDATE todos SET status = 'PENDING' WHERE id = ?", (args.id,))
    conn.commit()
    conn.close()
    print(f"Approved TODO #{args.id}: {row['title']} → PENDING")


def cmd_next(args: argparse.Namespace) -> None:
    """Pop the earliest PENDING TODO and set it to PROCESSING."""
    conn = get_connection()
    row = conn.execute(
        "SELECT id, title, content FROM todos WHERE status = 'PENDING' ORDER BY created_at ASC LIMIT 1",
    ).fetchone()
    if row is None:
        print("No PENDING todos. Everything is up to date.")
        conn.close()
        return
    conn.execute("UPDATE todos SET status = 'PROCESSING' WHERE id = ?", (row["id"],))
    conn.commit()
    conn.close()
    print(f"Now processing TODO #{row['id']}: {row['title']}")
    if row["content"]:
        print(f"  Content: {row['content']}")


def cmd_finish(args: argparse.Namespace) -> None:
    """Transition PROCESSING → DONE."""
    conn = get_connection()
    row = conn.execute("SELECT id, title, status FROM todos WHERE id = ?", (args.id,)).fetchone()
    if row is None:
        sys.exit(f"TODO #{args.id} not found")
    if row["status"] != "PROCESSING":
        sys.exit(f"TODO #{args.id} is in {row['status']}, expected PROCESSING")
    conn.execute("UPDATE todos SET status = 'DONE' WHERE id = ?", (args.id,))
    conn.commit()
    conn.close()
    print(f"Completed TODO #{args.id}: {row['title']} → DONE")


def cmd_list(args: argparse.Namespace) -> None:
    """List todos, optionally filtered by status."""
    conn = get_connection()
    if args.status:
        if args.status.upper() not in STATUSES:
            valid = ", ".join(sorted(STATUSES))
            sys.exit(f"Invalid status '{args.status}'. Valid: {valid}")
        rows = conn.execute(
            "SELECT id, title, content, status, created_at FROM todos WHERE status = ? ORDER BY created_at ASC",
            (args.status.upper(),),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, title, content, status, created_at FROM todos ORDER BY created_at ASC",
        ).fetchall()
    conn.close()

    if not rows:
        print("No todos found.")
        return

    # Calculate column widths
    id_width = max(len(str(r["id"])) for r in rows)
    title_width = max(len(r["title"]) for r in rows)
    status_width = max(len(r["status"]) for r in rows)

    header = (
        f"{'ID'.ljust(id_width)}  "
        f"{'Title'.ljust(title_width)}  "
        f"{'Status'.ljust(status_width)}  "
        f"Created At"
    )
    sep = "-" * len(header)
    print(sep)
    print(header)
    print(sep)
    for r in rows:
        print(
            f"{str(r['id']).ljust(id_width)}  "
            f"{r['title'].ljust(title_width)}  "
            f"{r['status'].ljust(status_width)}  "
            f"{r['created_at']}"
        )
    print(sep)
    print(f"Total: {len(rows)}")


# ── CLI ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="TODO Queue — FIFO-based TODO management")
    sub = parser.add_subparsers(dest="command", required=True)

    # push
    p_push = sub.add_parser("push", help="Add a new TODO (status: REVIEWING)")
    p_push.add_argument("title", help="TODO title")
    p_push.add_argument("content", nargs="?", default="", help="TODO content (optional)")

    # approve
    p_approve = sub.add_parser("approve", help="Approve a REVIEWING TODO → PENDING")
    p_approve.add_argument("id", type=int, help="TODO ID")

    # next
    p_next = sub.add_parser("next", help="Pop the earliest PENDING TODO → PROCESSING")

    # finish
    p_finish = sub.add_parser("finish", help="Mark a PROCESSING TODO → DONE")
    p_finish.add_argument("id", type=int, help="TODO ID")

    # list
    p_list = sub.add_parser("list", help="List todos (optional filter by status)")
    p_list.add_argument("--status", "-s", help=f"Filter by status: {', '.join(sorted(STATUSES))}")

    parsed = parser.parse_args()

    commands = {
        "push": cmd_push,
        "approve": cmd_approve,
        "next": cmd_next,
        "finish": cmd_finish,
        "list": cmd_list,
    }
    commands[parsed.command](parsed)


if __name__ == "__main__":
    main()
