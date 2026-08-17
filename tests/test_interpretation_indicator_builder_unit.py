import importlib
import json
import tempfile
import unittest
from pathlib import Path

from tools import build_interpretation_indicator_dataset as builder


class InterpretationIndicatorBuilderUnitTests(unittest.TestCase):
    def _fixture(self, directory: str, name: str, text: str) -> Path:
        path = Path(directory) / name
        path.write_text(text, encoding='utf-8')
        return path

    def test_import_exposes_main_without_scanning_source_roots(self):
        reloaded = importlib.reload(builder)
        self.assertTrue(callable(reloaded.main))

    def test_source_type_and_source_id(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = self._fixture(directory, 'fixture.json', '{}')
            original_root = builder.ROOT
            try:
                builder.ROOT = root
                self.assertEqual(builder.source_type(path), 'json')
                self.assertEqual(builder.source_id(path), 'openastro:fixture.json')
                self.assertEqual(builder.source_type(root / 'notes.md'), 'text')
                self.assertEqual(builder.source_type(root / 'engine.py'), 'code_or_schema')
                self.assertEqual(builder.source_type(root / 'image.png'), 'other')
            finally:
                builder.ROOT = original_root

    def test_extract_json_block_supports_raw_and_fenced_json(self):
        parsed, mode = builder.extract_json_block('{"meaning": "Preserved source text"}')
        self.assertEqual(mode, 'json')
        self.assertEqual(parsed['meaning'], 'Preserved source text')
        parsed, mode = builder.extract_json_block('before\n```json\n{"theme": "Source theme"}\n```\nafter')
        self.assertEqual(mode, 'fenced_json')
        self.assertEqual(parsed['theme'], 'Source theme')
        parsed, mode = builder.extract_json_block('{not valid}')
        self.assertIsNone(parsed)
        self.assertEqual(mode, 'unparseable')

    def test_add_indicator_normalizes_text_and_preserves_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self._fixture(directory, 'source.json', json.dumps({'meaning': 'Sun ☉ symbolism'}))
            original_root = builder.ROOT
            try:
                builder.ROOT = Path(directory)
                records = []
                builder.add_indicator(records, sid='openastro:source.json', path=path, record_type='interpretation_text', subject_path='sun', raw_text='  Sun  ☉\n symbolism  ')
                builder.add_indicator(records, sid='openastro:source.json', path=path, record_type='interpretation_text', subject_path='empty', raw_text='x')
            finally:
                builder.ROOT = original_root
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record['normalized_text'], 'Sun ☉ symbolism')
        self.assertEqual(record['source_path'], 'source.json')
        self.assertEqual(record['status'], 'source_derived')
        self.assertIn('☉', record['unicode_symbols'])
        self.assertIn('not empirical evidence', record['limitations'][0])

    def test_walk_json_extracts_string_list_and_nested_interpretations(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self._fixture(directory, 'source.json', json.dumps({'root': 'fixture'}))
            original_root = builder.ROOT
            try:
                builder.ROOT = Path(directory)
                records = []
                payload = {
                    'planet': {
                        'meaning': 'A source-derived meaning with enough content.',
                        'themes': ['First theme from source.', 'Second theme from source.'],
                        'interpretations': {'shadow': 'Nested source wording with enough content.'},
                    },
                    'items': [{'description': 'List-contained source description with enough content.'}],
                }
                builder.walk_json(payload, [], path, 'openastro:source.json', records)
            finally:
                builder.ROOT = original_root
        types = {record['record_type'] for record in records}
        self.assertIn('interpretation_text', types)
        self.assertIn('interpretation_list', types)
        self.assertIn('interpretation_field', types)
        self.assertTrue(any(record['subject_path'] == 'planet' for record in records))
        self.assertTrue(any(record['subject_path'] == 'planet.interpretations.shadow' for record in records))
        listed = next(record for record in records if record['record_type'] == 'interpretation_list')
        self.assertEqual(listed['items'], ['First theme from source.', 'Second theme from source.'])

    def test_walk_json_ignores_short_and_non_interpretive_values(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self._fixture(directory, 'source.json', '{}')
            original_root = builder.ROOT
            try:
                builder.ROOT = Path(directory)
                records = []
                builder.walk_json({'meaning': 'x', 'count': 3, 'metadata': {'label': 'Not an interpretation key'}}, [], path, 'openastro:source.json', records)
            finally:
                builder.ROOT = original_root
        self.assertEqual(records, [])

    def test_stable_indicator_ids_are_deterministic_for_the_same_source_text(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self._fixture(directory, 'source.json', '{}')
            original_root = builder.ROOT
            try:
                builder.ROOT = Path(directory)
                first, second = [], []
                kwargs = {'sid': 'openastro:source.json', 'path': path, 'record_type': 'interpretation_text', 'subject_path': 'sun', 'raw_text': 'A durable source sentence.'}
                builder.add_indicator(first, **kwargs)
                builder.add_indicator(second, **kwargs)
            finally:
                builder.ROOT = original_root
        self.assertEqual(first[0]['indicator_id'], second[0]['indicator_id'])

    def test_interpretation_key_registry_has_expected_boundaries(self):
        self.assertIn('meaning', builder.INTERPRETATION_KEYS)
        self.assertIn('financial_interpretation', builder.INTERPRETATION_KEYS)
        self.assertNotIn('raw_price', builder.INTERPRETATION_KEYS)
        self.assertNotIn('prediction', builder.INTERPRETATION_KEYS)


if __name__ == '__main__':
    unittest.main()
