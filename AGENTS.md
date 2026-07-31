# AGENTS.md - maintenance notes

This repo defines work modes for AI coding agents. Modes are agent-agnostic Markdown under `modes/`; everything agent-specific lives under `adapters/<agent>/`.

## Layout

- `modes/*.md` — the assets. One mode per file
- `adapters/<agent>/` — per-agent wiring: how a matching mode reaches that agent's context, and how to install and uninstall it. `claude-code` is the only adapter today. Debug tooling belongs here too, since reading back what an agent received depends on that agent's own formats

## When editing a mode

Modes are read straight from this checkout, so an edit takes effect on the next prompt with no reinstall. Reinstall only when the repo moves, or when something overwrites the config the adapter wrote to — `~/.claude/settings.json` in the case of Claude Code.

`triggers:` is a comma-separated list of literal words, not a regular expression. The adapter compiles the pattern: matching ignores case, a space inside a word also matches without one, and a word only matches where it is not glued to other ASCII letters — that boundary is what keeps `pr` out of `priority`. Because it is ASCII-only, Japanese suffixes still match (`PR` fires on `PRを作って`), but an English inflection needs its own entry (`review` does not cover `reviewed`). Leaving the boundary to the adapter also keeps modes portable, since it needs lookarounds that Python allows and Go's RE2 rejects.

## Checking what was injected

`make injections` lists the modes the Claude Code hook actually attached, newest first, across every project. `N=20` raises the limit. It reads session transcripts rather than asking the agent, so it reports what the hook did, not what the agent believes.

## Before committing

- The file name under `modes/` must match the `name:` in its frontmatter.
- Check a trigger through the adapter you touched. The Claude Code hook takes that agent's `UserPromptSubmit` payload on stdin: `echo '{"prompt":"..."}' | ./adapters/claude-code/attach_mode.py`
- An adapter must never fail loudly. Claude Code erases the submitted prompt when a `UserPromptSubmit` hook exits 2, so its hook swallows every error and stays quiet.

## Language policy

English everywhere except the body of `modes/*.md`, which is written in the language the agent is prompted in.
