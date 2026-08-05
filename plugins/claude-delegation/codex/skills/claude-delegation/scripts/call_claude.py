#!/usr/bin/env python3
"""Call Claude Code CLI and emit a single structured JSON value."""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def emit(payload, exit_code=0):
    print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    raise SystemExit(exit_code)


def read_schema(value):
    candidate = Path(value)
    try:
        raw = candidate.read_text(encoding="utf-8") if candidate.is_file() else value
        schema = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        emit({"ok": False, "error": {"type": "invalid_schema", "message": str(exc)}}, 2)
    if not isinstance(schema, dict) or schema.get("type") != "object":
        emit({"ok": False, "error": {"type": "invalid_schema", "message": "Schema root must be an object with type 'object'."}}, 2)
    return schema


def parse_model_json(text):
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3 and lines[-1].strip().startswith("```"):
            text = "\n".join(lines[1:-1]).strip()
    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError("Claude output must be a JSON object.")
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", help="User prompt; read stdin when omitted.")
    parser.add_argument("--schema", required=True, help="JSON Schema file path or inline JSON.")
    parser.add_argument("--system", help="Optional Claude system prompt.")
    parser.add_argument("--model", help="Optional Claude CLI model alias or ID.")
    parser.add_argument("--max-turns", type=int, default=1, help="Maximum Claude CLI turns (default: 1).")
    args = parser.parse_args()

    prompt = args.prompt if args.prompt is not None else sys.stdin.read()
    if not prompt.strip():
        emit({"ok": False, "error": {"type": "invalid_prompt", "message": "Provide --prompt or stdin."}}, 2)
    schema = read_schema(args.schema)
    if not shutil.which("claude"):
        emit({"ok": False, "error": {"type": "claude_not_found", "message": "Install Claude Code and make 'claude' available on PATH."}}, 127)

    instruction = "Return only the structured result for this task:\n" + prompt
    command = [
        "claude", "-p", "--output-format", "json", "--json-schema",
        json.dumps(schema, ensure_ascii=False), "--tools", "", "--max-turns", str(args.max_turns),
    ]
    if args.model:
        command.extend(["--model", args.model])
    if args.system:
        command.extend(["--system-prompt", args.system])
    command.append(instruction)
    try:
        completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=600)
        try:
            outer = json.loads(completed.stdout)
        except json.JSONDecodeError:
            if completed.returncode:
                emit({"ok": False, "error": {"type": "claude_failed", "message": completed.stderr.strip() or completed.stdout.strip() or "Claude CLI failed."}}, completed.returncode)
            raise
        if not isinstance(outer, dict):
            raise ValueError("Claude CLI output must be a JSON object.")
        if completed.returncode != 0:
            message = outer.get("result") or completed.stderr.strip()
            emit({"ok": False, "error": {"type": "claude_failed", "message": message or "Claude CLI failed."}}, completed.returncode)
        structured = outer.get("structured_output", outer.get("result"))
        result = parse_model_json(structured) if isinstance(structured, str) else structured
        if not isinstance(result, dict):
            raise ValueError("Claude structured output must be a JSON object.")
    except subprocess.TimeoutExpired:
        emit({"ok": False, "error": {"type": "timeout", "message": "Claude CLI exceeded 600 seconds."}}, 124)
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        emit({"ok": False, "error": {"type": "invalid_claude_output", "message": str(exc)}}, 1)
    emit({"ok": True, "result": result, "metadata": {"model": outer.get("model"), "session_id": outer.get("session_id")}})


if __name__ == "__main__":
    main()
