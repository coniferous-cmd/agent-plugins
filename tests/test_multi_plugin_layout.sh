#!/usr/bin/env zsh

set -euo pipefail

repo_root="${0:A:h:h}"
marketplace="$repo_root/.claude-plugin/marketplace.json"
codex_marketplace="$repo_root/.agents/plugins/marketplace.json"
plugin_root="$repo_root/plugins/git-workflow"
manifest="$plugin_root/.claude-plugin/plugin.json"
codex_manifest="$plugin_root/.codex-plugin/plugin.json"
shared_git_workflow_skills="$repo_root/shared/git-workflow/skills"
todo_plugin_root="$repo_root/plugins/todo-board"
todo_manifest="$todo_plugin_root/.claude-plugin/plugin.json"
todo_codex_manifest="$todo_plugin_root/.codex-plugin/plugin.json"
shared_todo_board_skills="$repo_root/shared/todo-board/skills"
readme="$repo_root/README.md"

[[ -f "$marketplace" ]]
[[ -f "$codex_marketplace" ]]
[[ -f "$manifest" ]]
[[ -f "$codex_manifest" ]]
[[ -f "$todo_manifest" ]]
[[ -f "$todo_codex_manifest" ]]
[[ -d "$shared_git_workflow_skills/commit" ]]
[[ -d "$shared_git_workflow_skills/push" ]]
[[ -d "$shared_todo_board_skills/todo-board" ]]
[[ -L "$plugin_root/skills" ]]
[[ -L "$todo_plugin_root/skills" ]]
[[ "$(readlink "$plugin_root/skills")" == "../../shared/git-workflow/skills" ]]
[[ "$(readlink "$todo_plugin_root/skills")" == "../../shared/todo-board/skills" ]]
[[ -d "$plugin_root/skills/commit" ]]
[[ -d "$plugin_root/skills/push" ]]
[[ -d "$todo_plugin_root/skills/todo-board" ]]
[[ ! -f "$repo_root/.claude-plugin/plugin.json" ]]

if rg -q '^disable-model-invocation: true$' "$shared_git_workflow_skills/commit/SKILL.md" "$shared_git_workflow_skills/push/SKILL.md"; then
  print -u2 "Shared skills must allow Codex model invocation"
  exit 1
fi
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

jq -e '.name == "coniferous-cmd-plugins"' "$codex_marketplace" >/dev/null
jq -e '.interface.displayName == "Coniferous Cmd Plugins"' "$codex_marketplace" >/dev/null
jq -e '.plugins | type == "array" and length == 2' "$codex_marketplace" >/dev/null
jq -e '.plugins[0] == {
  name: "git-workflow",
  source: {source: "local", path: "./plugins/git-workflow"},
  policy: {installation: "AVAILABLE", authentication: "ON_INSTALL"},
  category: "Productivity"
}' "$codex_marketplace" >/dev/null
jq -e '.plugins[1] == {
  name: "todo-board",
  source: {source: "local", path: "./plugins/todo-board"},
  policy: {installation: "AVAILABLE", authentication: "ON_INSTALL"},
  category: "Productivity"
}' "$codex_marketplace" >/dev/null
jq -e '.name == "git-workflow" and .skills == "./skills/" and .interface.displayName == "Git Workflow"' "$codex_manifest" >/dev/null
jq -e '.name == "todo-board" and .skills == "./skills/" and .interface.displayName == "Todo Board"' "$todo_codex_manifest" >/dev/null

[[ ! -f "$repo_root/.codex-plugin/plugin.json" ]]

print "multi-plugin layout: ok"
