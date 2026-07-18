# Agent Plugins — Codex

A marketplace of Codex plugins. This branch contains only plugins and
metadata compatible with the `codex` CLI.

## Available plugins

### `git-workflow`

- `commit`: Create or review clear, consistent Git commit messages.
- `push`: Push the current branch safely without force-pushing by default.

### `todo-board`

- `push`: Save a finalized implementation task.
- `list`: View incomplete tasks.
- `next`: Retrieve and remove the next task.

## Installation

Add this branch as a Codex marketplace, then install the plugins you need:

```bash
codex plugin marketplace add coniferous-cmd/agent-plugins#codex
codex plugin add git-workflow@coniferous-cmd-plugins
codex plugin add todo-board@coniferous-cmd-plugins
```

For local development, use the absolute path to a checkout of the `codex`
branch in place of `coniferous-cmd/agent-plugins#codex`. Start a new Codex
thread after installing or updating a plugin so its skills are loaded.

## Adding a plugin

Create `plugins/<plugin-name>/` with a `.codex-plugin/plugin.json` manifest
and a `skills/` directory. Add it to `.agents/plugins/marketplace.json`.
Plugin names, directory names, and manifest `name` values must match.

## License

MIT License. See [LICENSE](LICENSE).
