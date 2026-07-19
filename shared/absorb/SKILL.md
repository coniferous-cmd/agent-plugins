---
name: absorb
description: >
  Absorb a plugin or single skill from a GitHub repository or local directory into the marketplace.
  Use when user says "absorb plugin from <source>", "add plugin from GitHub",
  "install plugin from local directory", "absorb <repo-url-or-path>",
  "plugin absorb <source>", or asks to add/import/install a plugin from a URL or path.
  Trigger also when user says "pull plugin from" or "import plugin from".
  Also use when user says "absorb skill from <path>" or "install skill from <path>".
---

# Absorb

Absorbs a plugin or single skill from a GitHub repository or local directory into the marketplace.

## Usage

```
absorb <source> [--path <subdir>] [--force]
absorb <source> --skill <skill-path>
```

- **GitHub**: `absorb https://github.com/owner/repo`
- **GitHub with subdir**: `absorb https://github.com/owner/repo --path plugins/my-plugin`
- **Local directory**: `absorb /path/to/local/plugin`
- **Force overwrite**: `absorb <source> --force`
- **Single skill**: `absorb /path/to/repo --skill skills/my-skill`

## Workflow

### For full plugin absorption

1. **Detect source type** — GitHub URL or local path
2. **For GitHub**: clone repo to temp dir (shallow clone)
3. **Find plugin** — Look for `.codex-plugin/plugin.json` in source
4. **Validate** — Require `.codex-plugin/plugin.json` and `skills/` directory
5. **Copy** — Copy plugin to `plugins/<name>/`
6. **Register** — Add entry to `.agents/plugins/marketplace.json`

### For single skill absorption

1. **Find skill** — Look for `SKILL.md` at `<source>/<skill-path>`
2. **Parse name** — Read frontmatter `name` field, fallback to directory name
3. **Create plugin structure**:
   ```
   plugins/<skill-name>/
   ├── .codex-plugin/
   │   └── plugin.json
   └── skills/
       └── <skill-name>/
           └── SKILL.md
   ```
4. **Copy skill files** — SKILL.md and any scripts/ directory
5. **Register** — Add entry to marketplace.json

## Error Cases

- **Invalid GitHub URL**: `Error: Invalid GitHub URL: <url>`
- **Git clone failure**: `Error: Failed to clone <url>: <stderr>`
- **No plugin found**: `Error: No plugin found in repository`
- **Invalid structure**: `Error: Invalid plugin structure - <validation error>`
- **Name conflict**: `Error: Plugin '<name>' already exists at plugins/<name>/`
- **Marketplace update failure**: `Error: Failed to update marketplace`

## Rules

1. Always validate plugin/skill structure before copying
2. Create backup of marketplace.json before modifying
3. Rollback plugin copy if marketplace update fails
4. Use shallow clone (`--depth 1`) for GitHub
5. Clean up temporary directories after operation
