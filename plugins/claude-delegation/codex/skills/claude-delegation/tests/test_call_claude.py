#!/usr/bin/env python3
"""Regression tests for call_claude.py — focus on the short-form positional API
and the validation paths that should reject misuse without invoking Claude.

These tests stub `shutil.which` and `subprocess.run` so no real `claude` CLI
call is performed; they exercise only argument parsing, error envelopes, and
the shape of the command the script builds.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

# Make the script importable regardless of where pytest is run from.
HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "scripts" / "call_claude.py"

import importlib.util

spec = importlib.util.spec_from_file_location("call_claude", SCRIPT)
call_claude = importlib.util.module_from_spec(spec)
spec.loader.exec_module(call_claude)


VALID_SCHEMA = {
    "type": "object",
    "properties": {"x": {"type": "string"}},
    "required": ["x"],
    "additionalProperties": False,
}


def write_schema(tmpdir: Path) -> str:
    p = tmpdir / "schema.json"
    p.write_text(json.dumps(VALID_SCHEMA), encoding="utf-8")
    return str(p)


def run_cli(argv, *, which_return="/usr/bin/claude", run_return=None):
    """Invoke call_claude.main() with parsed argv; stub claude on PATH.

    `subprocess.run` is always stubbed. If `run_return` is None, the stub raises
    so callers can detect tests that forgot to supply a fake CompletedProcess.
    """
    payload = {"value": None}

    def capture(payload_, code=0):
        payload["value"] = payload_
        payload["_exit_code"] = code
        # Real emit() raises SystemExit; the mock must mimic that or the script
        # will continue past every error path and call subprocess.run anyway.
        raise SystemExit(code)

    def fake_run(*args, **kwargs):
        if run_return is None:
            # Default to a benign CompletedProcess so tests that exercise
            # validation paths don't have to construct one.
            return make_run_return({
                "model": "fake", "session_id": "fake",
                "structured_output": {"x": "ok"},
            })
        return run_return

    with mock.patch.object(sys, "argv", ["call_claude.py", *argv]), \
         mock.patch.object(call_claude.shutil, "which", return_value=which_return), \
         mock.patch.object(call_claude.subprocess, "run", side_effect=fake_run), \
         mock.patch.object(call_claude, "emit", side_effect=capture):
        try:
            call_claude.main()
        except SystemExit as e:
            payload["_exit_code"] = e.code
    return payload.get("_exit_code"), payload["value"]


def make_run_return(stdout_obj, returncode=0):
    """Build a fake CompletedProcess carrying a JSON stdout body."""
    return subprocess.CompletedProcess(
        args=[], returncode=returncode,
        stdout=json.dumps(stdout_obj), stderr="",
    )


class ShortFormParsing(unittest.TestCase):
    def test_short_form_too_few_args_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            schema = write_schema(Path(td))
            code, body = run_cli(["model", "balanced", "--schema", schema])
        self.assertEqual(code, 2)
        self.assertFalse(body["ok"])
        self.assertEqual(body["error"]["type"], "invalid_usage")
        self.assertIn("Short form needs", body["error"]["message"])

    def test_short_form_with_explicit_model_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            schema = write_schema(Path(td))
            code, body = run_cli([
                "model", "balanced", "summarize this PR",
                "--model", "other", "--schema", schema,
            ])
        self.assertEqual(code, 2)
        self.assertFalse(body["ok"])
        self.assertEqual(body["error"]["type"], "invalid_usage")
        self.assertIn("mutually exclusive", body["error"]["message"])

    def test_short_form_with_explicit_prompt_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            schema = write_schema(Path(td))
            code, body = run_cli([
                "model", "balanced", "summarize this PR",
                "--prompt", "override", "--schema", schema,
            ])
        self.assertEqual(code, 2)
        self.assertFalse(body["ok"])
        self.assertEqual(body["error"]["type"], "invalid_usage")
        self.assertIn("mutually exclusive", body["error"]["message"])

    def test_short_form_first_token_must_be_model(self):
        with tempfile.TemporaryDirectory() as td:
            schema = write_schema(Path(td))
            code, body = run_cli(["oops", "balanced", "hi", "--schema", schema])
        self.assertEqual(code, 2)
        self.assertFalse(body["ok"])
        self.assertEqual(body["error"]["type"], "invalid_usage")
        self.assertIn("must be `model`", body["error"]["message"])

    def test_short_form_builds_correct_command(self):
        """Short-form should produce the same command shape as the long form,
        with --model and --prompt derived from positionals."""
        with tempfile.TemporaryDirectory() as td:
            schema = write_schema(Path(td))
            outer = {
                "model": "claude-x",
                "session_id": "sess-1",
                "structured_output": {"x": "ok"},
            }
            run_ret = make_run_return(outer, returncode=0)

            code, body = run_cli(
                ["model", "balanced", "summarize this PR", "--schema", schema],
                run_return=run_ret,
            )
            self.assertEqual(code, 0, body)
            self.assertTrue(body["ok"], body)
            self.assertEqual(body["result"], {"x": "ok"})
            self.assertEqual(body["metadata"]["model"], "claude-x")
            self.assertEqual(body["metadata"]["session_id"], "sess-1")


class SchemaValidation(unittest.TestCase):
    def test_non_object_schema_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "s.json"
            p.write_text(json.dumps({"type": "array"}), encoding="utf-8")
            code, body = run_cli(["--prompt", "hi", "--schema", str(p)])
        self.assertEqual(code, 2)
        self.assertFalse(body["ok"])
        self.assertEqual(body["error"]["type"], "invalid_schema")

    def test_inline_schema_string_accepted(self):
        inline = json.dumps(VALID_SCHEMA)
        outer = {"model": "x", "session_id": "y", "structured_output": {"x": "ok"}}
        run_ret = make_run_return(outer, returncode=0)
        code, body = run_cli(["--prompt", "hi", "--schema", inline], run_return=run_ret)
        self.assertEqual(code, 0, body)
        self.assertTrue(body["ok"], body)


class PromptHandling(unittest.TestCase):
    def test_empty_prompt_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            schema = write_schema(Path(td))
            code, body = run_cli(["--schema", schema])
        self.assertEqual(code, 2)
        self.assertFalse(body["ok"])
        self.assertEqual(body["error"]["type"], "invalid_prompt")

    def test_stdin_prompt_accepted(self):
        outer = {"model": "x", "session_id": "y", "structured_output": {"x": "ok"}}
        run_ret = make_run_return(outer, returncode=0)
        with tempfile.TemporaryDirectory() as td:
            schema = write_schema(Path(td))
            with mock.patch.object(sys, "stdin") as fake_stdin:
                fake_stdin.read.return_value = "stdin prompt"
                code, body = run_cli(["--schema", schema], run_return=run_ret)
        self.assertEqual(code, 0, body)
        self.assertTrue(body["ok"], body)


class ClaudeCliErrors(unittest.TestCase):
    def test_claude_not_found(self):
        with tempfile.TemporaryDirectory() as td:
            schema = write_schema(Path(td))
            code, body = run_cli(["--prompt", "hi", "--schema", schema],
                                 which_return=None)
        self.assertEqual(code, 127)
        self.assertFalse(body["ok"])
        self.assertEqual(body["error"]["type"], "claude_not_found")

    def test_nonzero_return_with_message(self):
        outer = {"result": "boom"}
        run_ret = make_run_return(outer, returncode=2)
        with tempfile.TemporaryDirectory() as td:
            schema = write_schema(Path(td))
            code, body = run_cli(["--prompt", "hi", "--schema", schema],
                                 run_return=run_ret)
        self.assertEqual(code, 2)
        self.assertFalse(body["ok"])
        self.assertEqual(body["error"]["type"], "claude_failed")
        self.assertEqual(body["error"]["message"], "boom")

    def test_nonzero_return_surfaces_errors_and_subtype(self):
        outer = {
            "is_error": True,
            "subtype": "error_max_turns",
            "errors": ["Reached maximum number of turns (1)"],
        }
        run_ret = make_run_return(outer, returncode=1)
        with tempfile.TemporaryDirectory() as td:
            schema = write_schema(Path(td))
            code, body = run_cli(["--prompt", "hi", "--schema", schema],
                                 run_return=run_ret)
        self.assertEqual(code, 1)
        self.assertFalse(body["ok"])
        self.assertEqual(body["error"]["type"], "claude_failed")
        self.assertEqual(body["error"]["message"], "Reached maximum number of turns (1)")
        self.assertEqual(body["error"]["subtype"], "error_max_turns")
        self.assertEqual(body["error"]["errors"], ["Reached maximum number of turns (1)"])
        self.assertTrue(body["error"]["is_error"])


if __name__ == "__main__":
    unittest.main()
