#!/usr/bin/env python3
"""Debug tool: list the modes attach_mode actually injected, newest first.

Reads Claude Code session transcripts, where a hook's stdout is recorded as an
attachment. That record is the ground truth for which mode a prompt received --
asking the agent only gets you self-reporting.

Every project is scanned, not just this checkout. Filter by the project column
to narrow it down.

Usage: ./adapters/claude-code/list_injected_modes.py [count]  (or: make injections N=20)
"""
import glob
import json
import os
import sys

PHRASE = 'The work mode matching'
TRANSCRIPTS = '~/.claude/projects/*/*.jsonl'


def injections():
    """Yield (timestamp, mode, project) per injection. Skip whatever cannot be read."""
    skipped = 0
    for path in glob.glob(os.path.expanduser(TRANSCRIPTS)):
        try:
            # utf-8-sig drops a BOM that would otherwise break the first json.loads.
            handle = open(path, encoding='utf-8-sig', errors='replace')
        except OSError:
            continue
        with handle:
            for line in handle:
                if PHRASE not in line:
                    continue
                try:
                    record = json.loads(line)
                except ValueError:
                    # A transcript being written right now can hand us a partial line.
                    skipped += 1
                    continue
                # The phrase also appears in prompts and replies that merely discuss it,
                # so match on the hook attachment rather than on the text.
                attachment = record.get('attachment') or {}
                if attachment.get('hookEvent') != 'UserPromptSubmit' or 'stdout' not in attachment:
                    continue
                mode = attachment['stdout'].split('request is ', 1)[1].split('.', 1)[0]
                yield (
                    record.get('timestamp', ''),
                    mode,
                    os.path.basename(os.path.dirname(path)),
                )
    if skipped:
        print('skipped %d unparseable line(s)' % skipped, file=sys.stderr)


def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    rows = sorted(injections(), reverse=True)[:count]
    if not rows:
        print('no injection found in %s' % TRANSCRIPTS)
        return
    for timestamp, mode, project in rows:
        print('%s  %-10s %s' % (timestamp, mode, project))


main()
