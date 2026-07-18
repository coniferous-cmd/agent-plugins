#!/usr/bin/env zsh

set -euo pipefail

repo_root="${0:A:h:h}"

branch_files() {
  git -C "$repo_root" ls-tree -r --name-only "$1"
}

assert_branch_has_only() {
  local branch="$1"
  local required_path="$2"
  local forbidden_path="$3"

  branch_files "$branch" | rg -qx "$required_path"
  if branch_files "$branch" | rg -qx "$forbidden_path"; then
    print -u2 "$branch must not contain $forbidden_path"
    exit 1
  fi
}

for branch in codex claude; do
  git -C "$repo_root" rev-parse --verify --quiet "$branch^{commit}" >/dev/null || {
    print -u2 "Missing required branch: $branch"
    exit 1
  }
done

assert_branch_has_only codex '.agents/plugins/marketplace.json' '.claude-plugin/marketplace.json'
assert_branch_has_only claude '.claude-plugin/marketplace.json' '.agents/plugins/marketplace.json'

for plugin in git-workflow todo-board; do
  assert_branch_has_only codex "plugins/$plugin/.codex-plugin/plugin.json" "plugins/$plugin/.claude-plugin/plugin.json"
  assert_branch_has_only claude "plugins/$plugin/.claude-plugin/plugin.json" "plugins/$plugin/.codex-plugin/plugin.json"
done

codex_readme="$(git -C "$repo_root" show codex:README.md)"
claude_readme="$(git -C "$repo_root" show claude:README.md)"

[[ "$codex_readme" == *"Codex plugins"* ]]
[[ "$codex_readme" != *"Claude Code plugins"* ]]
[[ "$claude_readme" == *"Claude Code plugins"* ]]
[[ "$claude_readme" != *"Codex plugins"* ]]

print "agent branches: isolated"
