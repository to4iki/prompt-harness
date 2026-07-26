# to4iki/prompt-harness

Work modes for AI coding agents. A mode declares the decision principles to follow, the stop conditions to run to, and the gates left to a human. The mode whose triggers match your prompt is attached automatically, so the guardrails never depend on the agent deciding to read them.

Modes are plain Markdown and agent-agnostic. Attaching one is agent-specific and lives in `adapters/`. Claude Code is the only adapter today.

## Install

```sh
make install
```

This installs the Claude Code adapter, which registers a `UserPromptSubmit` hook in `~/.claude/settings.json` pointing at this checkout. Nothing is copied, so `git pull` is enough to pick up mode changes. Re-run `make install` after moving the repo.

## Modes

- **[implement](./modes/implement.md)** — Change code with a minimal diff, verified by build/test/lint and a fresh-context subagent.
- **[review](./modes/review.md)** — Review a diff with grounded findings, separating nits from blockers.
