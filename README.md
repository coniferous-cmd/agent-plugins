# Agent Plugins — Claude Code

A marketplace of Claude Code plugins. This branch contains only plugins and
metadata compatible with the `claude` CLI.

## Available plugins

### `git-workflow`

- `commit`: Create or review clear, consistent Git commit messages.
- `push`: Push the current branch safely without force-pushing by default.

### `todo-board`

- `push`: Save a finalized implementation task.
- `list`: View incomplete tasks.
- `next`: Retrieve and remove the next task.

## Installation

1. Add the GitHub-hosted marketplace from this branch:

   ```text
   /plugin marketplace add coniferous-cmd/agent-plugins#claude
   ```

2. Install a plugin:

   ```text
   /plugin install todo-board@coniferous-cmd-plugins
   ```

3. Reload plugins if Claude Code is already running:

   ```text
   /reload-plugins
   ```

For local development, load an individual plugin from a checkout of the
`claude` branch:

```bash
claude --plugin-dir /path/to/agent-plugins/plugins/todo-board
```

## Adding a plugin

Create `plugins/<plugin-name>/` with a `.claude-plugin/plugin.json` manifest
and a `skills/` directory. Add it to `.claude-plugin/marketplace.json`.
Plugin names, directory names, and manifest `name` values must match.

## License

MIT License. See [LICENSE](LICENSE).
