# AGENTS.md - maintenance notes

This repo is a modes pack for [rigmode](https://github.com/to4iki/rigmode). Modes are agent-agnostic Markdown under `modes/`.

## When editing a mode

Modes are read straight from this checkout (via `modes_dirs` in `~/.config/rigmode/config.toml`), so an edit takes effect on the next prompt with no reinstall.

A mode has to stand on its own — every matching mode attaches at once, and their stop conditions and gates add up. A mode with nothing to gate says so rather than claiming there are no gates.

`triggers:` is a comma-separated list of literal words, not a regex. Matching ignores case; a space inside a word is optional; an ASCII-letter end may not glue to another ASCII letter (`pr` stays out of `priority`).

## Before committing

- The file name under `modes/` must match the `name:` in its frontmatter.
- Validate with `rigmode check --modes-dir ./modes`.
- Dry-run a trigger: `echo '{"prompt":"..."}' | rigmode attach claude-code --modes-dir ./modes`

## Language policy

English everywhere except the body of `modes/*.md`, which is written in the language the agent is prompted in.
