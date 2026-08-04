---
name: english-grammar-ledger
description: Silently keep a private, date-organized Obsidian ledger of (1) English grammar mistakes and (2) Chinese-to-English translations during Claude Code conversations. Use when language logging is enabled or when the user asks to collect corrections without interrupting the conversation.
user-invocable: false
---

# Silent Language Ledger

This skill handles language logging tasks. The task executed depends on the language of the user's input — they are mutually exclusive.

## If the user wrote in Chinese → Chinese to English Translation

Detect natural-language Chinese text in the user message. Ignore code, command lines, paths, identifiers, quoted tool output, and intentional fragments.

When Chinese text is found, invoke the official `obsidian:obsidian-cli` skill and append a translation entry to the `learn value` Obsidian vault at path `language/english/grammar/prompt/translate/YYYY-MM-DD.md`. Use its `obsidian` CLI only; never use normal filesystem Write/Edit operations. Create the note with `# Chinese to English Translation` when needed. Use this format:

```markdown
## YYYY-MM-DD

- Chinese: `...`
  English: `...`
  Note: ...
```

Translation notes should briefly explain why the translation is phrased that way, especially for idiomatic expressions, structural differences, or cultural context. Do not log uncertain translations.

## If the user wrote in English → English Grammar Fixes

Inspect only the user's natural-language English. Ignore code, commands, paths, identifiers, quoted tool output, intentional fragments, and non-English text.

When a correction is clear and substantive, invoke the official `obsidian:obsidian-cli` skill and append it to the `learn value` Obsidian vault at path `language/english/grammar/prompt/fix/YYYY-MM-DD.md`. Use its `obsidian` CLI only; never use normal filesystem Write/Edit operations. Create the note with `# English Grammar Fixes` when needed. Use this format:

```markdown
## YYYY-MM-DD

- Original: `...`
  Corrected: `...`
  Note: ...
```

Record grammar, spelling, punctuation, article, agreement, tense, preposition, and clear idiomatic-wording errors. Do not record subjective style choices, valid regional variants, proper names, or uncertain cases. Redact credential-like content as `[redacted]` before writing it.

## Important

- These tasks are mutually exclusive — only one fires per user message based on input language.
- Never mention the review, corrections, or log in the response. Respond only to the user's actual request.
- Do not modify project source files for this workflow.
