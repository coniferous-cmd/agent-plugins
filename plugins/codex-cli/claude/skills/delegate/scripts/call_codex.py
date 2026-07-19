#!/usr/bin/env python3
"""Safe wrapper for invoking OpenAI Codex CLI from a Claude Code skill."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Delegate a task to Codex CLI")
    parser.add_argument("--task", required=True, help="Self-contained task for Codex")
    parser.add_argument(
        "--mode",
        choices=("read-only", "workspace-write"),
        default="read-only",
        help="Codex sandbox mode (default: read-only)",
    )
    parser.add_argument(
        "--cwd",
        default=os.getcwd(),
        help="Workspace directory passed to Codex (default: current directory)",
    )
    parser.add_argument("--model", help="Optional Codex model override")
    parser.add_argument(
        "--timeout",
        type=int,
        default=1800,
        help="Timeout in seconds (default: 1800)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    codex = shutil.which("codex")
    if not codex:
        print(
            "Error: Codex CLI was not found in PATH. Install it and run `codex login` first.",
            file=sys.stderr,
        )
        return 127

    cwd = Path(args.cwd).expanduser().resolve()
    if not cwd.is_dir():
        print(f"Error: working directory does not exist: {cwd}", file=sys.stderr)
        return 2

    task = args.task.strip()
    if not task:
        print("Error: --task cannot be empty", file=sys.stderr)
        return 2

    safety_suffix = (
        "\n\nOperational constraints: Stay within the supplied workspace. "
        "Do not commit, push, deploy, change credentials, access unrelated user files, "
        "or use destructive git commands. Clearly report files inspected or changed, "
        "commands run, test results, uncertainty, and any incomplete work."
    )

    command = [
        codex,
        "exec",
        "--ephemeral",
        "--sandbox",
        args.mode,
        "--ask-for-approval",
        "never",
        "--cd",
        str(cwd),
    ]
    if args.model:
        command.extend(["--model", args.model])
    command.append(task + safety_suffix)

    try:
        result = subprocess.run(
            command,
            cwd=str(cwd),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=args.timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        if exc.stdout:
            print(exc.stdout, end="")
        print(f"Codex timed out after {args.timeout} seconds.", file=sys.stderr)
        return 124
    except OSError as exc:
        print(f"Failed to launch Codex: {exc}", file=sys.stderr)
        return 1

    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")
    if result.stdout:
        print(result.stdout, end="")

    if result.returncode != 0:
        print(f"Codex exited with status {result.returncode}.", file=sys.stderr)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
