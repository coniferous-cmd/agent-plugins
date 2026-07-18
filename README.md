# Agent Plugins

A collection of Claude Code plugins distributed through a shared marketplace.
Each plugin is independently installable and lives under `plugins/<plugin-name>/`.

## Available plugins

### `git-workflow`

Provides two Git workflow skills:

- `commit`: Create or review clear, consistent Git commit messages.
- `push`: Push the current branch safely without force-pushing by default.

### `todo-board`

Manages queued implementation work for a project:

- `push`: Save a finalized implementation task.
- `list`: View incomplete tasks.
- `next`: Retrieve and remove the next task.

## Installation

### From the Claude plugin marketplace

1. Add the GitHub-hosted marketplace:

```text
/plugin marketplace add coniferous-cmd/agent-plugins
```

2. Install the plugin you need:

```text
/plugin install todo-board@coniferous-cmd-plugins
```

3. Reload plugins if Claude Code is already running:

```text
/reload-plugins
```

### From a local directory

Load an individual plugin for a session:

```bash
claude --plugin-dir /path/to/agent-plugins/plugins/todo-board
```

Its skills are then available as:

```text
/todo-board:push
/todo-board:list
/todo-board:next
```

### From the Codex plugin marketplace

Add this repository as a Codex marketplace, then install the plugins you want:

```bash
codex plugin marketplace add coniferous-cmd/agent-plugins
codex plugin add git-workflow@coniferous-cmd-plugins
codex plugin add todo-board@coniferous-cmd-plugins
```

For local development, replace `coniferous-cmd/agent-plugins` with the absolute
path to this repository. Start a new Codex thread after installing or updating
a plugin so its skills are loaded.

## Adding a plugin

Create a plugin directory with its own manifest and skills:

```text
plugins/
└── <plugin-name>/
    ├── .claude-plugin/
    │   └── plugin.json
    └── skills/
```

Add the plugin to `.claude-plugin/marketplace.json`:

```json
{
  "name": "coniferous-cmd-plugins",
  "plugins": [
    {
      "name": "<plugin-name>",
      "source": "./plugins/<plugin-name>"
    }
  ]
}
```

The `plugin.json` file describes one plugin and remains a JSON object. The
marketplace's `plugins` field is the array that lists all installable plugins.

For Codex compatibility, also add a `.codex-plugin/plugin.json` to the plugin
directory and list it in `.agents/plugins/marketplace.json`. The plugin name,
plugin directory name, and both manifests' `name` values must match.

Shared skill sources live in `shared/<plugin-name>/skills/`. Each plugin's
`skills/` directory is a symbolic link to that source for both Claude Code and
Codex. Add a host-specific copy only when a future requirement cannot be
expressed in a shared skill; Codex manifests must continue to use `./skills/`.

## License

MIT License. See [LICENSE](LICENSE).

## Author

coniferous-cmd
