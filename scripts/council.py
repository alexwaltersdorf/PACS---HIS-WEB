"""Append-only-by-convention local message exchange; no provider calls or Git writes."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]


def validator(root: Path = ROOT):
    schema = json.loads((root / 'schemas/llm-message.schema.json').read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate_message(message: dict, messages: dict, check) -> None:
    check.validate(message)
    digest = hashlib.sha256(message['body'].encode('utf-8')).hexdigest()
    if digest != message['provenance']['body_sha256']:
        raise ValueError('Body hash mismatch')
    if message['id'] in message['in_reply_to']:
        raise ValueError('A message cannot reply to itself')
    for parent_id in message['in_reply_to']:
        parent = messages.get(parent_id)
        if parent is None:
            raise ValueError(f'Missing parent message: {parent_id}')
        if parent['topic'] != message['topic']:
            raise ValueError('Reply must use the parent topic')
    origin = message['provenance']
    if origin['mode'] == 'direct_session' and origin['recorded_by'] != message['author']:
        raise ValueError('A different recorder must declare relayed_output')
    allowed = {'codex': {'codex_session', 'manual'}, 'claude-code': {'claude_code_cli', 'claude_code_desktop', 'manual'}, 'gemini': {'gemini_cli', 'gemini_web', 'manual'}}
    if origin['surface'] not in allowed[message['author']]:
        raise ValueError('Surface and declared author disagree')


def load_messages(root: Path = ROOT) -> dict:
    messages = {}
    directory = root / 'collaboration/messages'
    for path in sorted(directory.glob('*.json')):
        message = json.loads(path.read_text(encoding='utf-8-sig'))
        if path.stem != message.get('id'):
            raise ValueError(f'Filename/ID mismatch: {path.name}')
        if message['id'] in messages:
            raise ValueError('Duplicate message ID')
        messages[message['id']] = message
    check = validator(root)
    for message in messages.values():
        validate_message(message, messages, check)
    visiting, visited = set(), set()

    def visit(key):
        if key in visiting:
            raise ValueError('Reply graph contains a cycle')
        if key in visited:
            return
        visiting.add(key)
        for parent in messages[key]['in_reply_to']:
            visit(parent)
        visiting.remove(key)
        visited.add(key)
    for key in messages:
        visit(key)
    return messages


def append_message(message: dict, root: Path = ROOT) -> Path:
    messages = load_messages(root)
    validate_message(message, messages, validator(root))
    if message['id'] in messages:
        raise ValueError('Message already exists; create a reply instead of editing it')
    directory = root / 'collaboration/messages'
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / (message['id'] + '.json')
    # Exclusive creation prevents accidental overwrite, including concurrent same-ID writes.
    with destination.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(message, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('validate')
    listing = commands.add_parser('list')
    listing.add_argument('--recipient', choices=['codex', 'claude-code', 'gemini'])
    listing.add_argument('--topic')
    bundle = commands.add_parser('bundle')
    bundle.add_argument('--topic', required=True)
    posting = commands.add_parser('post')
    posting.add_argument('message_file', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'post':
            message = json.loads(args.message_file.read_text(encoding='utf-8-sig'))
            print(append_message(message).relative_to(ROOT))
            return 0
        messages = load_messages()
        if args.command == 'validate':
            print(f'{len(messages)} messages validated; no provider authentication or consensus inferred.')
            return 0
        selected = [item for item in messages.values() if not getattr(args, 'topic', None) or item['topic'] == args.topic]
        selected = [item for item in selected if not getattr(args, 'recipient', None) or args.recipient in item['recipients']]
        selected.sort(key=lambda item: (item['created_at'], item['id']))
        for item in selected:
            print(f"{item['id']} | {item['author']} -> {', '.join(item['recipients'])} | {item['kind']} | base {item['base_commit'][:7]}")
            if args.command == 'bundle':
                print(item['body'] + '\n')
        return 0
    except (ValueError, OSError, KeyError, ValidationError) as error:
        print(f'Council error: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
