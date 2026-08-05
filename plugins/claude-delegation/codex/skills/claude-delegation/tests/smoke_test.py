#!/usr/bin/env python3
"""End-to-end smoke test for call_claude.py.

Unlike test_call_claude.py (which mocks subprocess.run), this script invokes
the real `claude` CLI on PATH. It is intentionally **not** part of the unit
test suite — run it manually after env changes to confirm the scripted
contract still holds end-to-end.

Usage:
    conda run -n agents python tests/smoke_test.py

Exits 0 on success, non-zero on any contract violation. The full JSON
envelope it captures is written to tests/smoke_out/last_run.json so the
result is reviewable as an artifact.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "scripts" / "call_claude.py"
OUT_DIR = HERE / "smoke_out"
SCHEMA = {
    "type": "object",
    "properties": {
        "answer": {"type": "string"},
        "model": {"type": "string"},
    },
    "required": ["answer", "model"],
    "additionalProperties": False,
}


def _require_claude_on_path() -> None:
    """Refuse to run if the real CLI is missing — mocks are not allowed here."""
    from shutil import which

    if which("claude") is None:
        print("smoke_test: `claude` not on PATH; refusing to run.", file=sys.stderr)
        sys.exit(2)


def _run_script() -> dict:
    """Invoke call_claude.py with the smoke prompt and parse its JSON envelope."""
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--prompt",
            "What are you model?",
            "--schema",
            json.dumps(SCHEMA, ensure_ascii=False),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    out = completed.stdout.strip()
    if not out:
        raise RuntimeError(
            f"call_claude.py produced no stdout. stderr={completed.stderr!r}"
        )
    try:
        envelope = json.loads(out)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"call_claude.py stdout was not JSON: {out!r} (stderr={completed.stderr!r})"
        ) from exc
    envelope["_exit_code"] = completed.returncode
    envelope["_stderr"] = completed.stderr
    return envelope


def _validate(envelope: dict) -> list[str]:
    """Return a list of human-readable contract violations (empty = clean)."""
    fails: list[str] = []
    if envelope.get("ok") is not True:
        fails.append(f"envelope.ok is not True: {envelope.get('ok')!r}")
    if envelope.get("_exit_code") != 0:
        fails.append(f"process exit code was {envelope['_exit_code']}, expected 0")
    result = envelope.get("result")
    if not isinstance(result, dict):
        fails.append(f"envelope.result is not a dict: {result!r}")
        return fails
    answer = result.get("answer")
    if not isinstance(answer, str) or not answer.strip():
        fails.append(f"result.answer missing or empty: {answer!r}")
    model = result.get("model")
    if not isinstance(model, str) or not model.strip():
        fails.append(f"result.model missing or empty: {model!r}")
    metadata = envelope.get("metadata") or {}
    session_id = metadata.get("session_id")
    if not isinstance(session_id, str):
        fails.append(f"metadata.session_id missing or not a string: {session_id!r}")
    else:
        try:
            uuid.UUID(session_id)
        except ValueError:
            fails.append(f"metadata.session_id is not a UUID: {session_id!r}")
    return fails


def _persist(envelope: dict) -> Path:
    """Write the envelope to a stable path plus a timestamped copy."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stable = OUT_DIR / "last_run.json"
    stamp = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    rotated = OUT_DIR / f"run_{stamp}.json"
    payload = json.dumps(envelope, ensure_ascii=False, indent=2, sort_keys=True)
    stable.write_text(payload, encoding="utf-8")
    rotated.write_text(payload, encoding="utf-8")
    return rotated


def main() -> int:
    _require_claude_on_path()
    envelope = _run_script()
    failures = _validate(envelope)
    artifact = _persist(envelope)
    print(f"smoke_test: artifact written to {artifact}")
    if failures:
        print("smoke_test: CONTRACT VIOLATIONS:", file=sys.stderr)
        for line in failures:
            print(f"  - {line}", file=sys.stderr)
        return 1
    result = envelope["result"]
    print(f"smoke_test: OK — model={result['model']!r} answer={result['answer']!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
