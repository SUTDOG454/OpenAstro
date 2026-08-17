import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import ingest_astrodatabank as adb


class AstroDatabankIngestionUnitTests(unittest.TestCase):
    def _raw_record(self):
        return {
            'URL': 'https://www.astro.com/astro-databank/Test_Person',
            'Name': 'Test Person',
            'Date': '1 January 2000',
            'Time': '12:30',
            'Place Name': 'Example City',
            'Latitude': '12.34',
            'Longitude': '56.78',
            'Timezone': 'UTC',
            'Data Source': 'Public source',
            'Rodden Rating': 'AA',
            'Collector': 'Collector',
            'data': {
                'biography': {'text': 'A source biography.'},
                'relationships': {'text': 'A source relationship field.'},
                'events': {'text': 'A source event field.'},
                'source notes': {'text': 'A source note.'},
                'category': 'Actor, Writer',
            },
            'HTML Content': '<p>source html</p>',
        }

    def _create_sqlite(self, path: Path, row):
        columns = [part.strip() for part in adb.SQL_COLUMNS.split(',')]
        with sqlite3.connect(path) as connection:
            connection.execute('CREATE TABLE scraped_data (' + ', '.join(f'{column} TEXT' for column in columns) + ')')
            connection.execute(
                'INSERT INTO scraped_data (' + ', '.join(columns) + ') VALUES (' + ', '.join('?' for _ in columns) + ')',
                row,
            )

    def test_text_list_slug_key_and_hash_helpers(self):
        self.assertEqual(adb.text(None), '')
        self.assertEqual(adb.text('  value  '), 'value')
        self.assertEqual(adb.list_text([' first ', '', None, 'second']), ['first', 'second'])
        self.assertEqual(adb.list_text('one, two, ,three'), ['one', 'two', 'three'])
        self.assertEqual(adb.list_text(7), [])
        self.assertEqual(adb.slugify('Test Person / Example!'), 'test-person-example')
        self.assertEqual(adb.slugify('***'), 'unknown-profile')
        self.assertEqual(adb.canonical_key('url', 'name', 'fallback'), adb.canonical_key('url', 'other', 'fallback'))
        self.assertNotEqual(adb.canonical_key('', 'name', 'fallback'), adb.canonical_key('', 'other', 'fallback'))
        self.assertEqual(adb.content_hash({'b': 2, 'a': 1}), adb.content_hash({'a': 1, 'b': 2}))

    def test_normalise_record_preserves_source_boundary_and_optional_html(self):
        raw = self._raw_record()
        normalized = adb.normalise_upstream_record(raw, 'fixture.json', include_html=False)
        self.assertEqual(normalized['record_type'], 'astrodatabank-profile-source-extract')
        self.assertEqual(normalized['source']['source_host'], 'www.astro.com')
        self.assertEqual(normalized['profile']['name'], 'Test Person')
        self.assertEqual(normalized['content']['categories'], ['Actor', 'Writer'])
        self.assertNotIn('raw_html', normalized['content'])
        self.assertEqual(normalized['ingestion']['review_status'], 'source-extract-unreviewed')
        self.assertIn('not a validated OpenAstro chart', normalized['ingestion']['notes'])
        with_html = adb.normalise_upstream_record(raw, 'fixture.json', include_html=True)
        self.assertEqual(with_html['content']['raw_html'], '<p>source html</p>')
        invalid_url = adb.normalise_upstream_record({'name': 'No URL'}, 'fixture.json', include_html=False)
        self.assertEqual(invalid_url['source']['source_url'], '')
        self.assertEqual(invalid_url['source']['source_host'], '')

    def test_json_records_support_objects_lists_and_validation_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            object_path = root / 'object.json'
            object_path.write_text(json.dumps({'name': 'One'}), encoding='utf-8')
            records = list(adb.json_records(object_path))
            self.assertEqual(records, [({'name': 'One'}, 'object.json')])
            list_path = root / 'list.json'
            list_path.write_text(json.dumps([{'name': 'One'}, {'name': 'Two'}]), encoding='utf-8')
            records = list(adb.json_records(list_path))
            self.assertEqual([label for _, label in records], ['list.json:item-1', 'list.json:item-2'])
            invalid_path = root / 'invalid.json'
            invalid_path.write_text('{bad json}', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'not valid JSON'):
                list(adb.json_records(invalid_path))
            scalar_path = root / 'scalar.json'
            scalar_path.write_text('7', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'must contain'):
                list(adb.json_records(scalar_path))
            mixed_path = root / 'mixed.json'
            mixed_path.write_text(json.dumps([{'name': 'One'}, 'not a record']), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'item 2'):
                list(adb.json_records(mixed_path))

    def test_sqlite_records_read_supported_schema_and_reject_missing_table(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            database = root / 'records.sqlite'
            row = (
                'https://example.test/person', 'Sql Person', '2000-01-01', '12:00', 'City', '1', '2', 'UTC',
                'source', 'A', 'collector', 'bio', 'relationship', 'event', 'note', 'category', '<html>',
            )
            self._create_sqlite(database, row)
            records = list(adb.sqlite_records(database))
            self.assertEqual(records[0][0]['name'], 'Sql Person')
            self.assertEqual(records[0][1], 'records.sqlite:row-1')
            empty = root / 'empty.sqlite'
            with sqlite3.connect(empty) as connection:
                connection.execute('CREATE TABLE other (value TEXT)')
            with self.assertRaisesRegex(ValueError, 'no scraped_data table'):
                list(adb.sqlite_records(empty))

    def test_input_paths_and_existing_keys_handle_supported_and_invalid_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            nested = root / 'nested'
            nested.mkdir()
            json_path = nested / 'one.json'
            db_path = root / 'two.sqlite'
            ignored = root / 'ignore.txt'
            json_path.write_text('{}', encoding='utf-8')
            db_path.write_bytes(b'')
            ignored.write_text('ignore', encoding='utf-8')
            self.assertEqual(adb.input_paths(json_path), [json_path])
            self.assertEqual(adb.input_paths(root), [json_path, db_path])
            with self.assertRaisesRegex(ValueError, 'No supported'):
                adb.input_paths(ignored)
            output = root / 'out'
            output.mkdir()
            (output / 'manifest.json').write_text('{}', encoding='utf-8')
            (output / 'valid.json').write_text(json.dumps({'source': {'original_record_key': 'key-1'}}), encoding='utf-8')
            (output / 'malformed.json').write_text('{bad', encoding='utf-8')
            self.assertEqual(adb.existing_keys(output), {'key-1'})
            self.assertEqual(adb.existing_keys(root / 'absent'), set())

    def test_write_manifest_preserves_unreviewed_promotion_rule(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            entries = [{'filename': 'person.json', 'original_record_key': 'key', 'source_url': 'https://example.test'}]
            adb.write_manifest(output, entries, Path('/fixtures/source.json'))
            manifest = json.loads((output / 'manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['record_count'], 1)
        self.assertEqual(manifest['records'], entries)
        self.assertIn('remain unreviewed', manifest['promotion_rule'])

    def test_main_dry_run_writes_nothing_and_makes_no_external_request(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'records.json'
            output = root / 'out'
            source.write_text(json.dumps([self._raw_record()]), encoding='utf-8')
            with patch.object(sys, 'argv', ['ingest_astrodatabank.py', str(source), '--output', str(output), '--dry-run']):
                self.assertEqual(adb.main(), 0)
            self.assertFalse(output.exists())

    def test_main_writes_then_deduplicates_existing_source_extracts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'records.json'
            output = root / 'out'
            source.write_text(json.dumps([self._raw_record()]), encoding='utf-8')
            argv = ['ingest_astrodatabank.py', str(source), '--output', str(output)]
            with patch.object(sys, 'argv', argv):
                self.assertEqual(adb.main(), 0)
            extracts = [path for path in output.glob('*.json') if path.name != 'manifest.json']
            self.assertEqual(len(extracts), 1)
            first_manifest = json.loads((output / 'manifest.json').read_text(encoding='utf-8'))
            self.assertEqual(first_manifest['record_count'], 1)
            with patch.object(sys, 'argv', argv):
                self.assertEqual(adb.main(), 0)
            second_manifest = json.loads((output / 'manifest.json').read_text(encoding='utf-8'))
            self.assertEqual(second_manifest['record_count'], 0)
            self.assertEqual(len([path for path in output.glob('*.json') if path.name != 'manifest.json']), 1)


if __name__ == '__main__':
    unittest.main()
