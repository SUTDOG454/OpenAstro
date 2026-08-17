import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from interpretation_indicator_engine import (  # noqa: E402
    extract_keywords,
    indicator_matches,
    normalize_text,
    stable_indicator_id,
    unicode_symbols,
    validate_indicator,
)

IND = ROOT / 'data/interpretation-indicators'
UNIFIED = ROOT / 'data/unified'


class IndicatorUtilityTests(unittest.TestCase):
    def test_normalization_and_stable_id_are_deterministic(self):
        self.assertEqual(normalize_text('  Sun\n trine   Moon '), 'Sun trine Moon')
        first = stable_indicator_id('source', 'path', 'type', 'Sun trine Moon')
        second = stable_indicator_id('source', 'path', 'type', 'Sun trine Moon')
        self.assertEqual(first, second)
        self.assertEqual(len(first), len('indicator_') + 20)

    def test_keywords_and_unicode_symbols(self):
        text = 'Sun ☉ trine Moon ☽ supports creative identity.'
        self.assertIn('creative', extract_keywords(text))
        self.assertIn('☉', unicode_symbols(text))
        self.assertIn('☽', unicode_symbols(text))

    def test_indicator_contract_and_retrieval(self):
        record = {
            'indicator_id': 'indicator_test', 'source_id': 'source', 'source_path': 'x.json',
            'record_type': 'interpretation_text', 'subject_path': 'signals.sun',
            'raw_text': 'Sun supports identity', 'normalized_text': 'Sun supports identity',
            'keywords': ['supports'], 'unicode_symbols': [], 'evidence_class': 'source_derived',
            'status': 'source_derived', 'limitations': ['source-derived'],
        }
        self.assertEqual(validate_indicator(record), [])
        self.assertTrue(indicator_matches(record, subject='signals.sun'))
        self.assertFalse(indicator_matches(record, subject='signals.moon'))


class IndicatorDatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = json.loads((IND / 'source_inventory.json').read_text())
        cls.dataset = json.loads((IND / 'normalized_interpretation_indicators.json').read_text())
        cls.dedup = json.loads((IND / 'deduplication.json').read_text())
        cls.summary = json.loads((IND / 'indicator_dataset_summary.json').read_text())
        cls.gaps = json.loads((IND / 'coverage_gap_register.json').read_text())
        cls.master = json.loads((UNIFIED / 'unified_astrology_master.json').read_text())

    def test_dataset_is_large_and_source_linked(self):
        self.assertGreaterEqual(self.dataset['record_count'], 3000)
        self.assertGreaterEqual(self.inventory['source_count'], 100)
        for record in self.dataset['records'][:100]:
            self.assertTrue(record['source_id'])
            self.assertEqual(len(record['source_sha256']), 64)
            self.assertTrue(record['normalized_text'])
            self.assertEqual(validate_indicator(record), [])

    def test_deduplication_is_explicit(self):
        self.assertGreater(self.dedup['duplicate_group_count'], 0)
        self.assertIn('exact normalized text', self.dedup['policy'])

    def test_symbol_registry_and_master_integration(self):
        symbols = json.loads((UNIFIED / 'symbol_registry.json').read_text())
        self.assertEqual(symbols['signs']['aries']['glyph'], '♈')
        self.assertEqual(symbols['planets_and_points']['sun']['glyph'], '☉')
        self.assertIn('interpretation_indicator_dataset', self.master)
        self.assertEqual(self.master['interpretation_indicator_dataset']['indicator_count'], self.dataset['record_count'])
        self.assertTrue(self.gaps['required_layers']['symbols'])

    def test_review_boundaries_are_visible(self):
        gap_ids = {gap['id'] for gap in self.gaps['gaps']}
        self.assertIn('interpretation-evidence-is-not-empirical', gap_ids)
        self.assertIn('missing-ephemeris-fixtures', gap_ids)
        self.assertIn('semantic-tradition-review', {r['id'] for r in json.loads((IND / 'recommendations.json').read_text())['recommendations']})


if __name__ == '__main__':
    unittest.main()
