# Agent Plugins

A collection of Claude Code plugins distributed through a shared marketplace.
Each plugin is independently installable and lives under `plugins/<plugin-name>/`.

## Available plugins

### `git-workflow`

Provides two Git workflow skills:

- `commit`: Create or review clear, consistent Git commit messages.
- `push`: Push the current branch safely without force-pushing by default.

## Installation

### From the Claude plugin marketplace

1. Add the GitHub-hosted marketplace:

```text
/plugin marketplace add coniferous-cmd/agent-plugins
```

2. Install the plugin you need:

```text
/plugin install git-workflow@coniferous-cmd-plugins
```

3. Reload plugins if Claude Code is already running:

```text
/reload-plugins
```

### From a local directory

Load an individual plugin for a session:

```bash
claude --plugin-dir /path/to/agent-plugins/plugins/git-workflow
```

Its skills are then available as:

```text
/git-workflow:commit
/git-workflow:push
```

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

## License

MIT License. See [LICENSE](LICENSE).

## Author

coniferous-cmd
