#!/usr/bin/env python3
"""UserPromptSubmit hook: inject the one mode whose triggers match the prompt."""
import json, re, sys
from pathlib import Path

MODES_DIR = Path(__file__).resolve().parents[2] / 'modes'

PREAMBLE = (
    'The work mode matching this request is %s. Its contents follow. '
    'Hook output does not reach subagents, so delegating requires copying '
    'this body into the subagent instructions.'
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

    Each word is matched literally and only where it is not glued to other letters,
    so a short one like `pr` stays out of `priority`. The lookarounds name ASCII
    letters rather than using `\\b` because Python counts kana as word characters,
    which would stop `PR` from matching `PRを作って`.
    """
    words = [r'\s?'.join(map(re.escape, t.split())) for t in re.split(r'[,|]', triggers)]
    alts = ['(?<![A-Za-z])%s(?![A-Za-z])' % w for w in words if w]
    return '(?i)' + '|'.join(alts) if alts else ''


def find_mode(prompt, modes_dir):
    for path in sorted(modes_dir.glob('*.md')):
        triggers, body = parse_mode(path.read_text(encoding='utf-8'))
        pattern = build_pattern(triggers)
        if pattern and re.search(pattern, prompt):
            return path.stem, body.strip()
    return None


# Swallow every failure: exiting 2 would erase the prompt the user just submitted.
try:
    found = find_mode(json.load(sys.stdin).get('prompt', ''), MODES_DIR)
    if found:
        print('%s\n\n%s' % (PREAMBLE % found[0], found[1]))
except Exception:
    pass
