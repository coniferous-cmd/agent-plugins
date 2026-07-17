# Git Commit Plugin

A Claude Code plugin for creating clear, consistent Git commit messages and safely pushing local commits.

## Skills

- `commit`: Generate or review commit messages using the seven commonly recommended rules:
  - Use a concise subject line
  - Keep the subject within 50 characters when practical
  - Capitalize the subject
  - Do not end the subject with a period
  - Use the imperative mood
  - Wrap the body at 72 characters
  - Explain what changed and why, not how
- `push`: Push the current branch to its tracked remote safely. It only pushes when explicitly requested and never force-pushes by default.

## Installation

### From the Claude plugin marketplace

1. In Claude Code, add the GitHub-hosted marketplace:

```text
/plugin marketplace add coniferous-cmd/agent-plugins
```

2. Install the plugin:

```text
/plugin install git-workflow@coniferous-cmd-plugins
```

3. Reload plugins if Claude Code is already running:

```text
/reload-plugins
```

### From a local directory

Load the plugin for a session:

```bash
claude --plugin-dir /path/to/git-commit-skill
```

The skills are then available as:

```text
/git-workflow:commit
/git-workflow:push
```

## License

MIT License. See [LICENSE](LICENSE).

## Author

coniferous-cmd
