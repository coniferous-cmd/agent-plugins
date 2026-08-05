---
name: claude-delegation
description: Call an installed, authenticated Claude CLI through Python and return one schema-shaped JSON value. Use when Codex needs Claude to classify, extract, summarize, review, or transform information into a JSON object for downstream processing.
argument-hint: model <alias> <prompt> | --prompt "<task>" --schema <file> [--system <text>] [--model <alias>] [--max-turns N]
---

# Claude JSON

Use `scripts/call_claude.py`; it invokes `claude -p --output-format json --json-schema`, extracts the structured response, and writes one JSON envelope to stdout.

Require the user to be authenticated in the local Claude CLI. Do not pass secrets on the command line.

## Invoke

Create a JSON Schema file whose root type is `object`, then run:

```sh
python scripts/call_claude.py `
  --prompt "Extract the title and up to three action items." `
  --schema .\result-schema.json
```

Use `--system` for task-wide instructions, `--model` to select a Claude CLI model alias (fast, balanced, or most capable — pass any alias `claude` accepts), and `--max-turns` to bound agentic work. Pipe a prompt through stdin only when `--prompt` is omitted.

### Short form

When a schema file is already in scope (for example the active task already references `result-schema.json`), invoke with the model alias and prompt positionally:

```
/claude-delegation model <alias> <prompt text>
```

Example:

```
/claude-delegation model balanced Summarize the three open PR titles and return JSON.
```

The short form forwards `<alias>` to `--model` and the trailing text to `--prompt`.

## Output contract

On success, stdout is exactly:

```json
{"ok": true, "result": {}}
```

On failure, stdout is a JSON envelope with `ok: false` and the process exits non-zero. The script rejects non-object schemas and invalid model output. Claude CLI validates output against the supplied schema; the CLI's outer JSON response is retained only as compact metadata in the envelope.

Do not depend on Markdown fences or explanatory text in Claude's answer. Fix the schema or prompt and retry if output parsing fails.
