---
name: english-grammar-ledger
description: Silently keep a private, date-organized Obsidian ledger of clear grammar mistakes in the user's natural-language English during a Claude Code conversation. Use when English grammar logging is enabled or when the user asks to collect corrections without interrupting the conversation.
user-invocable: false
---

# Silent English Grammar Ledger

For each user message, review natural-language English only. Ignore code, commands, paths, identifiers, quoted tool output, intentional fragments, and non-English text.

When a correction is clear and substantive, invoke the official `obsidian:obsidian-cli` skill and append it to the `learn value` Obsidian vault. Use the note path `language/grammar/fix/YYYY-MM-DD.md`. Use its `obsidian` CLI only; never use normal filesystem Write/Edit operations. Create the note with `# English Grammar Fixes` when needed. Use this format:

```markdown
## YYYY-MM-DD

- Original: `...`
  Corrected: `...`
  Note: ...
```

Record grammar, spelling, punctuation, article, agreement, tense, preposition, and clear idiomatic-wording errors. Do not record subjective style choices, valid regional variants, proper names, or uncertain cases. Redact credential-like content as `[redacted]` before writing it.

Never mention the review, corrections, or log in the response. Respond only to the user's actual request. Do not modify project files for this workflow.
