#!/usr/bin/env python
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
        "Your task depends on the language of the user's input:\n\n"
        "## If the user wrote in Chinese\n"
        "Translate the user's natural-language Chinese text into English. "
        f"Append the translation to Obsidian vault at path language/english/grammar/prompt/translate/{date_path}.md. "
        "Invoke the official obsidian:obsidian-cli skill and use its CLI only; "
        "do not use normal filesystem Write/Edit operations. "
        "Create the note with title # Chinese to English Translation if it does not exist. "
        "Format each entry as:\n"
        "## YYYY-MM-DD\n"
        "- Chinese: `...`\n"
        "  English: `...`\n"
        "  Note: ...\n"
        "Include a note explaining why the translation is phrased that way (idiomatic expressions, "
        "structural differences, or cultural context). Do not translate code, command lines, paths, "
        "identifiers, quoted tool output, or intentional fragments. Do not log uncertain translations.\n\n"
        "## If the user wrote in English\n"
        "Inspect the user's natural-language English (not code, command lines, paths, identifiers, "
        "quoted tool output, intentional fragments, or non-English text). If there is a clear grammar, "
        "spelling, punctuation, article, agreement, tense, preposition, or clear idiomatic-wording error, "
        f"append the correction to Obsidian vault at path language/english/grammar/prompt/fix/{date_path}.md. "
        "Invoke the official obsidian:obsidian-cli skill and use its CLI only; "
        "do not use normal filesystem Write/Edit operations. "
        "Create the note with title # English Grammar Fixes if it does not exist. "
        "Format each entry as:\n"
        "## YYYY-MM-DD\n"
        "- Original: `...`\n"
        "  Corrected: `...`\n"
        "  Note: ...\n"
        "Do not log style preferences, valid regional variants, proper names, or uncertain corrections. "
        "Preserve secrets by replacing any apparent credential, token, key, password, or private value "
        "with [redacted] before writing.\n\n"
        "Keep this task entirely out of the conversation: do not mention, summarize, quote, apologize for, "
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
