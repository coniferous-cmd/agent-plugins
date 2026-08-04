$datePath = Get-Date -Format 'yyyy-MM-dd'
$context = @"
Silent language ledger is active for this user prompt.

## Task 1: English Grammar Fixes
Inspect only the user's natural-language English (not code, command lines, paths, identifiers, quoted tool output, intentional fragments, or non-English text). If it has a clear grammar, spelling, punctuation, article, agreement, tense, preposition, or clear idiomatic-wording error, append one concise entry to the Obsidian vault `learn value` at path `language/english/grammar/prompt/fix/$datePath.md`. Invoke the official `obsidian:obsidian-cli` skill and use its `obsidian` CLI only; do not use normal filesystem Write/Edit operations. Create the note with `# English Grammar Fixes` if it does not exist. Each entry must contain the original sentence, a corrected version, and a brief explanation. Do not log style preferences, valid regional variants, proper names, or uncertain corrections. Preserve secrets by replacing any apparent credential, token, key, password, or private value with `[redacted]` before writing.

## Task 2: Chinese to English Translation
Detect natural-language Chinese text in the user message. Ignore code, command lines, paths, identifiers, quoted tool output, and intentional fragments. When Chinese text is found, append a translation entry to the Obsidian vault `learn value` at path `language/english/grammar/prompt/translate/$datePath.md`. Invoke the official `obsidian:obsidian-cli` skill and use its `obsidian` CLI only; do not use normal filesystem Write/Edit operations. Create the note with `# Chinese to English Translation` if it does not exist. Each entry must contain the original Chinese sentence, its English translation, and a brief note explaining why the translation is phrased that way (especially for idiomatic expressions, structural differences, or cultural context). Do not log uncertain translations.

Keep both tasks entirely out of the conversation: do not mention, summarize, quote, apologize for, or visibly correct the user's input. Answer the actual request normally. Do not alter any project source file for this workflow.
"@

@{
  hookSpecificOutput = @{
    hookEventName = 'UserPromptSubmit'
    additionalContext = $context
  }
} | ConvertTo-Json -Compress
