# CLAUDE.md

This file provides guidance to Claude Code (Codex) when working with code in this repository.

## Overview

Plugin repository for Claude Code and Codex platforms. A single `main` branch serves both platforms — shared implementation lives under `plugins/*/skills/` or `shared/`, while platform-specific metadata and skill frontmatter live alongside it.

## Architecture

```
plugins/<name>/           # Plugin implementations
├── .claude-plugin/       # Claude Code registration
├── .codex-plugin/        # Codex registration
├── claude/agents/        # Claude-specific agents (.md files with frontmatter)
├── claude/skills/        # Claude-specific skills
├── codex/agents/          # Codex-specific agents
├── codex/skills/          # Codex-specific skills
└── skills/                # Shared skills (symlinked from shared/ or codex/skills/)

shared/                   # Cross-plugin shared code (identical configs for both platforms)
├── <name>/skills/         # Shared skills to symlink
└── ...
```

### Shared Pattern

When both platforms use identical agents or skills, place them in `shared/<name>/` and symlink:
- `plugins/<name>/claude/agents/` → symlink to `shared/<name>/agents/`
- `plugins/<name>/claude/skills/` → symlink to `shared/<name>/skills/`

This avoids duplicating identical configuration across `claude/` and `codex/` directories.

### Plugin vs Agent

- **Plugin**: Package distributed via marketplace (has `plugin.json`)
- **Agent**: Defined in `plugin.json` `agents:` field, a `.md` file with YAML frontmatter (`name`, `model`, `description`, `tools`)
- **Skill**: Defined in `skills:` field, a `SKILL.md` file

### Registration

Plugin registration requires two steps:

1. **Create plugin config** in `plugins/<name>/`:

 - Claude: `.claude-plugin/plugin.json` — `agents: ["./claude/agents/..."]`
 - Codex: `.codex-plugin/plugin.json` — `agents: ["./codex/agents/..."]`

2. **Register in root marketplace**:

 - Claude: `.claude-plugin/marketplace.json` — add to `plugins[]` with `name`, `source`, `description`, `version`
 - Codex: `.agents/plugins/marketplace.json` — add to `plugins[]` with `name`, `source.path`, `policy`, `category`; requires `interface` field at root

Claude can symlink shared scripts from Codex's `skills/` directory.

