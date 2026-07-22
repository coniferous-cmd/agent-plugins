#!/usr/bin/env zsh

set -euo pipefail

repo_root="${0:A:h:h}"

[[ "$(git -C "$repo_root" branch --show-current)" == "main" ]] || {
  print -u2 'tests must run from main'
  exit 1
}

for plugin in git-workflow todo-board; do
  [[ -f "$repo_root/plugins/$plugin/.codex-plugin/plugin.json" ]] || exit 1
  [[ -f "$repo_root/plugins/$plugin/.claude-plugin/plugin.json" ]] || exit 1
done

[[ -f "$repo_root/.agents/plugins/marketplace.json" ]]
[[ -f "$repo_root/.claude-plugin/marketplace.json" ]]

readme="$repo_root/README.md"
rg -F 'codex plugin marketplace add https://github.com/coniferous-cmd/agent-plugins.git --ref main' "$readme"
rg -F 'codex plugin add git-workflow@coniferous-cmd-plugins' "$readme"
rg -F 'codex plugin add todo-board@coniferous-cmd-plugins' "$readme"
rg -F '/plugin marketplace add https://github.com/coniferous-cmd/agent-plugins.git' "$readme"
rg -F '/plugin install git-workflow@coniferous-cmd-plugins' "$readme"
rg -F '/plugin install todo-board@coniferous-cmd-plugins' "$readme"
! rg -F 'plugins install coniferous-cmd/agent-plugins' "$readme"

[[ "$(sed -n 's/^model: //p' "$repo_root/plugins/git-workflow/skills/commit/SKILL.md" | head -n 1)" == 'gpt-5.5-mini' ]]
[[ "$(sed -n 's/^model: //p' "$repo_root/plugins/git-workflow/claude/skills/commit/SKILL.md" | head -n 1)" == 'haiku' ]]

[[ "$(jq -r '.skills' "$repo_root/plugins/todo-board/.claude-plugin/plugin.json")" == './codex/skills/' ]]

print 'single-branch dual-platform layout: ok'
