#!/usr/bin/env python3
"""
Cross-platform context injector for english-grammar-ledger hook.
Injects translation + grammar fix reminder into UserPromptSubmit context.
Works on Windows (PowerShell), Linux, macOS, and WSL.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import date

def get_date_path() -> str:
    return date.today().strftime("%Y-%m-%d")

def get_plugin_root() -> str:
    # Prefer explicit env var
    if env_val := os.environ.get("CLAUDE_PLUGIN_ROOT"):
        return env_val
    # WSL compat
    if env_val := os.environ.get("CLAUDE_PLUGIN_ROOT_WSL"):
        return env_val
    # Derive from script location (works in all cases)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(script_dir)  # scripts/ -> plugin root

def build_context(date_path: str) -> str:
    return (
        "Silent language ledger is active for this user prompt.\n\n"
        "## Task 1: English Grammar Fixes\n"
        "Inspect only the user's natural-language English (not code, command lines, paths, identifiers, "
        "quoted tool output, intentional fragments, or non-English text). If it has a clear grammar, "
        "spelling, punctuation, article, agreement, tense, preposition, or clear idiomatic-wording error, "
        f"append one concise entry to the Obsidian vault learn value at path "
        f"language/english/grammar/prompt/fix/{date_path}.md. "
        "Invoke the official obsidian:obsidian-cli skill and use its obsidian CLI only; "
        "do not use normal filesystem Write/Edit operations. "
        "Create the note with # English Grammar Fixes if it does not exist. "
        "Each entry must contain the original sentence, a corrected version, and a brief explanation. "
        "Do not log style preferences, valid regional variants, proper names, or uncertain corrections. "
        "Preserve secrets by replacing any apparent credential, token, key, password, or private value "
        "with [redacted] before writing.\n\n"
        "## Task 2: Chinese to English Translation\n"
        "Detect natural-language Chinese text in the user message. Ignore code, command lines, paths, "
        "identifiers, quoted tool output, and intentional fragments. When Chinese text is found, append "
        f"a translation entry to the Obsidian vault learn value at path "
        f"language/english/grammar/prompt/translate/{date_path}.md. "
        "Invoke the official obsidian:obsidian-cli skill and use its obsidian CLI only; "
        "do not use normal filesystem Write/Edit operations. "
        "Create the note with # Chinese to English Translation if it does not exist. "
        "Each entry must contain the original Chinese sentence, its English translation, and a brief note "
        "explaining why the translation is phrased that way (especially for idiomatic expressions, "
        "structural differences, or cultural context). Do not log uncertain translations.\n\n"
        "Keep both tasks entirely out of the conversation: do not mention, summarize, quote, apologize for, "
        "or visibly correct the user's input. Answer the actual request normally. "
        "Do not alter any project source file for this workflow."
    )

def main() -> None:
    date_path = get_date_path()
    context = build_context(date_path)

    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context
        }
    }

    # Use compact JSON output
    json.dump(output, sys.stdout, ensure_ascii=False, separators=(",", ":"))
    sys.stdout.write("\n")

if __name__ == "__main__":
    main()
