# Agent Plugins

This repository provides plugins for both Codex and Claude Code from the
single `main` branch. Shared implementation stays under `plugins/*/skills/`;
platform-specific marketplace metadata and skill frontmatter live alongside it.

## Available plugins

- `git-workflow`: create clear commit messages and push branches safely.
- `todo-board`: save, list, and retrieve queued implementation work.

## Install plugins

### Claude Code

```bash
claude plugins install coniferous-cmd/agent-plugins/git-workflow
claude plugins install coniferous-cmd/agent-plugins/todo-board
```

### Codex

```bash
codex plugins install coniferous-cmd/agent-plugins/git-workflow
codex plugins install coniferous-cmd/agent-plugins/todo-board
```

Start a new agent session after installing or updating a plugin.

## License

MIT License. See [LICENSE](LICENSE).
