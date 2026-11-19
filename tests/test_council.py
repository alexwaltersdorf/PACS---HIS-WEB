import hashlib
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from council import validate_message, validator


class MessageContractTests(unittest.TestCase):
    def setUp(self):
        body = 'Proposta sintética de teste, sem dados clínicos.'
        self.message = {
            'schema_version': '0.1.0', 'id': 'test-proposal', 'topic': 'test-topic',
            'author': 'codex', 'recipients': ['claude-code', 'gemini'], 'kind': 'proposal',
            'created_at': '2026-11-18T12:00:00Z', 'base_commit': 'a' * 40,
            'in_reply_to': [], 'body': body,
            'provenance': {'mode': 'direct_session', 'recorded_by': 'codex',
                           'surface': 'codex_session', 'model_label': None,
                           'body_sha256': hashlib.sha256(body.encode()).hexdigest()}}
        self.check = validator()

    def test_direct_message(self):
        validate_message(self.message, {}, self.check)

    def test_body_tampering_rejected(self):
        self.message['body'] += ' Changed'
        with self.assertRaises(ValueError):
            validate_message(self.message, {}, self.check)

    def test_missing_parent_rejected(self):
        self.message['in_reply_to'] = ['missing']
        with self.assertRaises(ValueError):
            validate_message(self.message, {}, self.check)

    def test_cross_topic_reply_rejected(self):
        self.message['in_reply_to'] = ['parent']
        with self.assertRaises(ValueError):
            validate_message(self.message, {'parent': {'topic': 'different'}}, self.check)

    def test_false_direct_recording_rejected(self):
        self.message['author'] = 'gemini'
        self.message['provenance']['surface'] = 'gemini_web'
        with self.assertRaises(ValueError):
            validate_message(self.message, {}, self.check)

    def test_explicit_relay_accepted(self):
        self.message['author'] = 'gemini'
        self.message['recipients'] = ['codex']
        self.message['provenance']['surface'] = 'gemini_web'
        self.message['provenance']['mode'] = 'relayed_output'
        validate_message(self.message, {}, self.check)

    def test_wrong_surface_rejected(self):
        self.message['provenance']['surface'] = 'claude_code_cli'
        with self.assertRaises(ValueError):
            validate_message(self.message, {}, self.check)


if __name__ == '__main__':
    unittest.main()
