from pathlib import Path


REPO_ROOT = Path(__file__).parents[1]
AGENTS = REPO_ROOT / "plugins/git/codex/agents"
ALL_AGENT_FILES = tuple((REPO_ROOT / "plugins/git").glob("*/agents/*.md"))


def test_git_agents_keep_safety_rules_in_a_compact_prompt():
    commit = (AGENTS / "commit.md").read_text()
    push = (AGENTS / "push.md").read_text()

    assert len(commit) <= 1_500
    assert len(push) <= 900
    assert "Never commit unstaged changes." in commit
    assert "Never stage files automatically unless explicitly requested." in commit
    assert "Never amend, rebase, or force-push unless explicitly requested." in commit
    assert "Push only when the user explicitly requests it." in push
    assert "Never use `--force` unless explicitly requested." in push


def test_git_agents_describe_intent_instead_of_exact_commands():
    for agent in ALL_AGENT_FILES:
        assert "`git " not in agent.read_text(), agent
