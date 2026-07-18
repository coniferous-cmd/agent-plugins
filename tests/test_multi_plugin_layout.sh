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
rg -Fq 'Codex or Claude Code' "$repo_root/README.md" || {
  print -u2 'README must document one shared Codex and Claude Code flow'
  exit 1
}
rg -Fq '/plugins' "$repo_root/README.md" || {
  print -u2 'README must document the /plugins entry point'
  exit 1
}
if rg -Fq 'github.com' "$repo_root/README.md"; then
  print -u2 'README must not include a GitHub domain'
  exit 1
fi

[[ "$(sed -n 's/^model: //p' "$repo_root/plugins/git-workflow/skills/commit/SKILL.md" | head -n 1)" == 'gpt-5.5-mini' ]]
[[ "$(sed -n 's/^model: //p' "$repo_root/plugins/git-workflow/claude/skills/commit/SKILL.md" | head -n 1)" == 'haiku' ]]

for link_path in \
  "$repo_root/plugins/todo-board/claude/skills/todo-board/scripts" \
  "$repo_root/plugins/todo-board/claude/skills/todo-board/handbooks"; do
  [[ -L "$link_path" && -e "$link_path" ]] || {
    print -u2 "Missing shared link: $link_path"
    exit 1
  }
done

print 'single-branch dual-platform layout: ok'
