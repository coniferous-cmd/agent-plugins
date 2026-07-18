#!/usr/bin/env zsh

set -euo pipefail

repo_root="${0:A:h:h}"
marketplace="$repo_root/.claude-plugin/marketplace.json"
plugin_root="$repo_root/plugins/git-workflow"
manifest="$plugin_root/.claude-plugin/plugin.json"

[[ -f "$marketplace" ]]
[[ -f "$manifest" ]]
[[ -d "$plugin_root/skills/commit" ]]
[[ -d "$plugin_root/skills/push" ]]
[[ ! -f "$repo_root/.claude-plugin/plugin.json" ]]

jq -e '.plugins | type == "array" and length == 1' "$marketplace" >/dev/null
jq -e '.plugins[0].name == "git-workflow"' "$marketplace" >/dev/null
jq -e '.plugins[0].source == "./plugins/git-workflow"' "$marketplace" >/dev/null
jq -e '.name == "git-workflow" and (type == "object")' "$manifest" >/dev/null

print "multi-plugin layout: ok"
