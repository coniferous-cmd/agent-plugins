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
/plugin marketplace add https://github.com/coniferous-cmd/agent-plugins.git
/plugin install git-workflow@coniferous-cmd-plugins
/plugin install todo-board@coniferous-cmd-plugins
```

### Codex

```bash
codex plugin marketplace add https://github.com/coniferous-cmd/agent-plugins.git --ref main
codex plugin add git-workflow@coniferous-cmd-plugins
codex plugin add todo-board@coniferous-cmd-plugins
```

Start a new agent session after installing or updating a plugin.

## License

MIT License. See [LICENSE](LICENSE).
