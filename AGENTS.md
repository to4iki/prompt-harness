# AGENTS.md - maintenance notes

This repo defines work modes for AI coding agents. Modes are agent-agnostic Markdown under `modes/`; everything agent-specific lives under `adapters/<agent>/`.

## Layout

- `modes/*.md` — the assets. One mode per file
- `adapters/<agent>/` — per-agent wiring: how a matching mode reaches that agent's context, and how to install and uninstall it. `claude-code` is the only adapter today. Debug tooling belongs here too, since reading back what an agent received depends on that agent's own formats

## When editing a mode

Modes are read straight from this checkout, so an edit takes effect on the next prompt with no reinstall. Reinstall only when the repo moves, or when something overwrites the config the adapter wrote to — `~/.claude/settings.json` in the case of Claude Code.

A mode has to stand on its own, because every mode that matches is attached at once. Modes are phases, and a request that names two phases gets both, with their stop conditions and gates taken together — so nothing in a mode may assume it is the only one in effect, and a mode with nothing to gate says so rather than claiming there are no gates.

`triggers:` is a comma-separated list of literal words, not a regular expression. The adapter compiles the pattern: matching ignores case, and a space inside a word also matches without one. An end of a word that is an ASCII letter may not be glued to another ASCII letter, which is what keeps `pr` out of `priority`; an English inflection therefore needs its own entry, as `review` does not cover `reviewed`. Ends that are not ASCII stay unguarded, since `実装して` has to keep matching in `実装してPR作って`. Leaving all of this to the adapter also keeps modes portable, because the guard needs lookarounds that Python allows and Go's RE2 rejects.

## Checking what was injected

`make injections` lists the modes the Claude Code hook actually attached, newest first, across every project — one row per prompt, listing every mode that prompt received. `N=20` raises the limit. It reads session transcripts rather than asking the agent, so it reports what the hook did, not what the agent believes. It finds injections by the preamble the hook prints, so changing that wording hides older rows.

## Before committing

- The file name under `modes/` must match the `name:` in its frontmatter.
- Check a trigger through the adapter you touched. The Claude Code hook takes that agent's `UserPromptSubmit` payload on stdin: `echo '{"prompt":"..."}' | ./adapters/claude-code/attach_mode.py`
- An adapter must never fail loudly. Claude Code erases the submitted prompt when a `UserPromptSubmit` hook exits 2, so its hook swallows every error and stays quiet.

## Language policy

English everywhere except the body of `modes/*.md`, which is written in the language the agent is prompted in.
