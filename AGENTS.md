# AGENTS.md - maintenance notes

This repo defines work modes for AI coding agents. Modes are agent-agnostic Markdown under `modes/`; everything agent-specific lives under `adapters/<agent>/`.

## Layout

- `modes/*.md` — the assets. One mode per file
- `adapters/<agent>/` — per-agent wiring: how a matching mode reaches that agent's context, and how to install and uninstall it. `claude-code` is the only adapter today

## When editing a mode

Modes are read straight from this checkout, so an edit takes effect on the next prompt with no reinstall. Reinstall only when the repo moves, or when something overwrites the config the adapter wrote to — `~/.claude/settings.json` in the case of Claude Code.

## Before committing

- The file name under `modes/` must match the `name:` in its frontmatter.
- Check a trigger through the adapter you touched. The Claude Code hook takes that agent's `UserPromptSubmit` payload on stdin: `echo '{"prompt":"..."}' | ./adapters/claude-code/attach_mode.py`
- An adapter must never fail loudly. Claude Code erases the submitted prompt when a `UserPromptSubmit` hook exits 2, so its hook swallows every error and stays quiet.

## Language policy

English everywhere except the body of `modes/*.md`, which is written in the language the agent is prompted in.
