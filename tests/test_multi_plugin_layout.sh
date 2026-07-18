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

for branch in codex claude main; do
  git -C "$repo_root" rev-parse --verify --quiet "$branch^{commit}" >/dev/null || {
    print -u2 "Missing required branch: $branch"
    exit 1
  }
done

[[ "$(branch_files main)" == "README.md" ]]

assert_branch_has_only codex '.agents/plugins/marketplace.json' '.claude-plugin/marketplace.json'
assert_branch_has_only claude '.claude-plugin/marketplace.json' '.agents/plugins/marketplace.json'

for plugin in git-workflow todo-board; do
  assert_branch_has_only codex "plugins/$plugin/.codex-plugin/plugin.json" "plugins/$plugin/.claude-plugin/plugin.json"
  assert_branch_has_only claude "plugins/$plugin/.claude-plugin/plugin.json" "plugins/$plugin/.codex-plugin/plugin.json"
done

for branch in codex claude; do
  for plugin in git-workflow todo-board; do
    branch_files "$branch" | rg -q "^plugins/$plugin/skills/"
  done
  if branch_files "$branch" | rg -q '^shared/'; then
    print -u2 "$branch must not retain the obsolete shared skill directory"
    exit 1
  fi
done

for plugin in git-workflow todo-board; do
  [[ ! -L "$repo_root/plugins/$plugin/skills" ]] || {
    print -u2 "$plugin skills must be a local directory, not a symbolic link"
    exit 1
  }
done

if rg -Fq 'The CLI is implemented in Python and must be run with the `agents` Mamba' \
  "$repo_root/plugins/todo-board/skills/todo-board/SKILL.md"; then
  print -u2 'todo-board must not prescribe the Python/Mamba implementation details'
  exit 1
fi

if ! rg -Fq 'Never read files in `scripts/`.' \
  "$repo_root/plugins/todo-board/skills/todo-board/SKILL.md"; then
  print -u2 'todo-board must prohibit reading bundled script sources'
  exit 1
fi

codex_readme="$(git -C "$repo_root" show codex:README.md)"
claude_readme="$(git -C "$repo_root" show claude:README.md)"

[[ "$codex_readme" == *"Codex plugins"* ]]
[[ "$codex_readme" != *"Claude"* ]]
[[ "$claude_readme" == *"Claude Code plugins"* ]]
[[ "$claude_readme" != *"Codex"* ]]

assert_skill_model() {
  local branch="$1"
  local skill="$2"
  local expected="$3"
  local skill_path="plugins/git-workflow/skills/$skill/SKILL.md"
  local current_branch
  local actual

  current_branch="$(git -C "$repo_root" branch --show-current)"
  if [[ "$branch" == "$current_branch" ]]; then
    actual="$(sed -n 's/^model: //p' "$repo_root/$skill_path" | head -n 1)"
  else
    actual="$(git -C "$repo_root" show "$branch:$skill_path" | sed -n 's/^model: //p' | head -n 1)"
  fi
  [[ "$actual" == "$expected" ]] || {
    print -u2 "$branch $skill model must be $expected (got $actual)"
    exit 1
  }
}

for skill in commit push; do
  assert_skill_model codex "$skill" "gpt-5.5-mini"
  assert_skill_model claude "$skill" "haiku"
done

print "agent branches: isolated"
