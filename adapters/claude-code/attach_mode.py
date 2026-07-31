#!/usr/bin/env python3
"""UserPromptSubmit hook: inject every mode whose triggers match the prompt."""
import json, re, sys
from pathlib import Path

MODES_DIR = Path(__file__).resolve().parents[2] / 'modes'

PREAMBLE = (
    'Work modes matching this request: %s. All of them apply, so satisfy every '
    'stop condition and respect every gate below. Hook output does not reach '
    'subagents, so delegating requires copying these bodies into the subagent '
    'instructions.'
)


def parse_mode(text):
    """Return the frontmatter triggers and the body. No frontmatter means no triggers."""
    if not text.startswith('---\n'):
        return '', text
    front, _, body = text[4:].partition('\n---\n')
    triggers = ''
    for line in front.splitlines():
        key, sep, value = line.partition(':')
        if sep and key.strip() == 'triggers':
            triggers = value.strip()
    return triggers, body


def build_pattern(triggers):
    """Compile the comma-separated trigger words into one case-insensitive pattern.

    Each word is matched literally, and an end that is an ASCII letter may not be
    glued to another one, so `pr` stays out of `priority`. Only such ends are
    guarded: `実装して` has to keep matching in `実装してPR作って`, and `\\b` cannot
    draw that line at all, since Python counts kana as word characters.
    """
    alts = []
    for term in re.split(r'[,|]', triggers):
        term = term.strip()
        if not term:
            continue
        word = r'\s?'.join(map(re.escape, term.split()))
        if re.match(r'[A-Za-z]', term):
            word = r'(?<![A-Za-z])' + word
        if re.search(r'[A-Za-z]$', term):
            word = word + r'(?![A-Za-z])'
        alts.append(word)
    return '(?i)' + '|'.join(alts) if alts else ''


def find_modes(prompt, modes_dir):
    """Collect every matching mode, in file name order.

    Modes are phases of one job, and a request routinely spans several -- implement
    this, then open the PR. Picking a single winner would drop the other phase's
    stop conditions, so all of them are attached and their guardrails add up.
    """
    found = []
    for path in sorted(modes_dir.glob('*.md')):
        triggers, body = parse_mode(path.read_text(encoding='utf-8'))
        pattern = build_pattern(triggers)
        if pattern and re.search(pattern, prompt):
            found.append((path.stem, body.strip()))
    return found


# Swallow every failure: exiting 2 would erase the prompt the user just submitted.
try:
    found = find_modes(json.load(sys.stdin).get('prompt', ''), MODES_DIR)
    if found:
        names = ', '.join(name for name, _ in found)
        # Name each body, so a section heading is never read as the other mode's.
        bodies = '\n\n'.join('# %s\n\n%s' % (name, body) for name, body in found)
        print('%s\n\n%s' % (PREAMBLE % names, bodies))
except Exception:
    pass
