#!/usr/bin/env zsh

set -euo pipefail

repo_root="${0:A:h:h}"
marketplace="$repo_root/.claude-plugin/marketplace.json"
plugin_root="$repo_root/plugins/git-workflow"
manifest="$plugin_root/.claude-plugin/plugin.json"
todo_plugin_root="$repo_root/plugins/todo-board"
todo_manifest="$todo_plugin_root/.claude-plugin/plugin.json"
todo_codex_manifest="$todo_plugin_root/.codex-plugin/plugin.json"
readme="$repo_root/README.md"

[[ -f "$marketplace" ]]
[[ -f "$manifest" ]]
[[ -f "$todo_manifest" ]]
[[ -f "$todo_codex_manifest" ]]
[[ -d "$plugin_root/skills/commit" ]]
[[ -d "$plugin_root/skills/push" ]]
[[ -d "$todo_plugin_root/skills/todo-board" ]]
[[ ! -f "$repo_root/.claude-plugin/plugin.json" ]]
[[ "$(sed -n '1p' "$readme")" == "# Agent Plugins" ]]
rg -q "collection of Claude Code plugins" "$readme"
rg -q 'Retrieve and remove the next task' "$readme"
! rg -q "^# Git Workflow Plugin$" "$readme"

jq -e '.plugins | type == "array" and length == 2' "$marketplace" >/dev/null
jq -e '.plugins[0].name == "git-workflow"' "$marketplace" >/dev/null
jq -e '.plugins[0].source == "./plugins/git-workflow"' "$marketplace" >/dev/null
jq -e '.plugins[1].name == "todo-board"' "$marketplace" >/dev/null
jq -e '.plugins[1].source == "./plugins/todo-board"' "$marketplace" >/dev/null
jq -e '.name == "git-workflow" and (type == "object")' "$manifest" >/dev/null
jq -e '.name == "todo-board" and (type == "object")' "$todo_manifest" >/dev/null
jq -e '.name == "todo-board" and (type == "object")' "$todo_codex_manifest" >/dev/null
jq -e '.interface.displayName == "Todo Board"' "$todo_codex_manifest" >/dev/null

print "multi-plugin layout: ok"
