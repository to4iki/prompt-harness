#!/usr/bin/env python3
"""Register the attach_mode hook in Claude Code settings. Pass --remove to unregister."""
import json
import os
import stat
import sys
from pathlib import Path

EVENT = 'UserPromptSubmit'
TIMEOUT_SECONDS = 5
HOOK = Path(__file__).resolve().parent / 'attach_mode.py'
SETTINGS = Path(os.environ.get('CLAUDE_CONFIG_DIR') or Path.home() / '.claude') / 'settings.json'


def load_settings():
    if not SETTINGS.exists():
        return {}
    text = SETTINGS.read_text(encoding='utf-8')
    if not text.strip():
        return {}
    try:
        return json.loads(text)
    except ValueError as error:
        sys.exit('%s is not valid JSON, refusing to overwrite it: %s' % (SETTINGS, error))


def without_our_entries(entries):
    """Drop entries pointing at attach_mode.py so repeated installs never duplicate."""
    return [
        entry for entry in entries
        if not any(HOOK.name in hook.get('command', '') for hook in entry.get('hooks', []))
    ]


def our_entry():
    # UserPromptSubmit takes no matcher. Reading one Markdown file fits well inside 5s,
    # and a timeout would discard the output, leaving the prompt without its mode.
    return {
        'hooks': [
            {
                'command': "'%s'" % HOOK,
                'timeout': TIMEOUT_SECONDS,
                'type': 'command',
            }
        ]
    }


def drop_empty_containers(settings):
    hooks = settings.get('hooks', {})
    if not hooks.get(EVENT):
        hooks.pop(EVENT, None)
    if not hooks:
        settings.pop('hooks', None)


def main():
    remove = '--remove' in sys.argv[1:]
    if remove and not SETTINGS.exists():
        print('%s does not exist, nothing to remove' % SETTINGS)
        return

    settings = load_settings()
    hooks = settings.setdefault('hooks', {})
    hooks[EVENT] = without_our_entries(hooks.get(EVENT, []))
    if not remove:
        hooks[EVENT].append(our_entry())
        HOOK.chmod(HOOK.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    drop_empty_containers(settings)

    SETTINGS.parent.mkdir(parents=True, exist_ok=True)
    body = json.dumps(settings, ensure_ascii=False, indent=2, sort_keys=True)
    SETTINGS.write_text(body + '\n', encoding='utf-8')
    print('%s %s in %s' % (EVENT, 'removed' if remove else 'registered', SETTINGS))


main()
