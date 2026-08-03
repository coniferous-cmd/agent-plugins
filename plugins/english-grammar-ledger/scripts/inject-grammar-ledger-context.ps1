$datePath = Get-Date -Format 'yyyy-MM-dd'
$context = @"
Silent English grammar ledger is active for this user prompt.

Before answering, inspect only the user's natural-language English (not code, command lines, paths, identifiers, quoted program output, or intentionally abbreviated fragments). If it has a clear grammar, spelling, punctuation, article, agreement, tense, preposition, or idiomatic-wording error, append one concise entry to the Obsidian vault `learn value`, using the note path `language/grammar/fix/$datePath.md`. Invoke the official `obsidian:obsidian-cli` skill and use its `obsidian` CLI only; do not use normal filesystem Write/Edit operations. Create the note with `# English Grammar Fixes` if it does not exist. Each entry must contain the original sentence, a corrected version, and a brief explanation. Do not log style preferences, valid regional variants, proper names, or uncertain corrections. Preserve secrets by replacing any apparent credential, token, key, password, or private value with `[redacted]` before writing.

Keep this entirely out of the conversation: do not mention, summarize, quote, apologize for, or visibly correct the user's English. Answer the actual request normally. Do not alter any project source file for this workflow.
"@

@{
  hookSpecificOutput = @{
    hookEventName = 'UserPromptSubmit'
    additionalContext = $context
  }
} | ConvertTo-Json -Compress
