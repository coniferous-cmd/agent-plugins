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
    parser = argparse.ArgumentParser(
        description=__doc__,
        usage=(
            "%(prog)s --schema <file> [--prompt <text>|--stdin] [options]\n"
            "       %(prog)s model <alias> --schema <file> <prompt text>   (short form)"
        ),
    )
    parser.add_argument(
        "positional",
        nargs="*",
        help=(
            "Short form: `model <alias> <prompt text>` — first token must be the literal "
            "`model`; second is the CLI model alias; remaining tokens join into the prompt."
        ),
    )
    parser.add_argument("--prompt", help="User prompt; read stdin when omitted.")
    parser.add_argument("--schema", required=True, help="JSON Schema file path or inline JSON.")
    parser.add_argument("--system", help="Optional Claude system prompt.")
    parser.add_argument(
        "--model",
        help=(
            "Optional Claude CLI model alias (fast, balanced, or most capable). "
            "Pass any alias accepted by `claude`; omit to use the Claude CLI default."
        ),
    )
    parser.add_argument("--max-turns", type=int, default=3, help="Maximum Claude CLI turns (default: 3). Two turns cover Claude's occasional tool-probing even with --tools ''; raise if your prompt needs more.")
    args = parser.parse_args()

    # Short form: `model <alias> <prompt text>`
    if args.positional:
        if args.positional[0] != "model":
            emit({"ok": False, "error": {"type": "invalid_usage", "message": "First positional token must be `model` when using short form."}}, 2)
        if len(args.positional) < 3:
            emit({"ok": False, "error": {"type": "invalid_usage", "message": "Short form needs `model <alias> <prompt text>`."}}, 2)
        if args.model:
            emit({"ok": False, "error": {"type": "invalid_usage", "message": "`--model` and short form are mutually exclusive."}}, 2)
        if args.prompt:
            emit({"ok": False, "error": {"type": "invalid_usage", "message": "`--prompt` and short form are mutually exclusive."}}, 2)
        args.model = args.positional[1]
        args.prompt = " ".join(args.positional[2:])

    prompt = args.prompt if args.prompt is not None else sys.stdin.read()
    if not prompt.strip():
        emit({"ok": False, "error": {"type": "invalid_prompt", "message": "Provide --prompt, stdin, or short-form positional prompt."}}, 2)
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
            errors = outer.get("errors") if isinstance(outer.get("errors"), list) else None
            subtype = outer.get("subtype")
            message = (
                (errors[0] if errors else None)
                or outer.get("result")
                or completed.stderr.strip()
                or f"Claude CLI failed (subtype={subtype!r}, is_error={outer.get('is_error')})."
            )
            emit({
                "ok": False,
                "error": {
                    "type": "claude_failed",
                    "message": message,
                    "subtype": subtype,
                    "errors": errors,
                    "is_error": outer.get("is_error"),
                },
            }, completed.returncode)
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
