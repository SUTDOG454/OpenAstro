import json
import os
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LATEST = ROOT / 'data/extractions/latest-afe'
UNIFIED = ROOT / 'data/unified'


class LatestAfeIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = json.loads((LATEST / 'source_inventory.json').read_text())
        cls.normalized = json.loads((LATEST / 'normalized_records.json').read_text())
        cls.integration = json.loads((UNIFIED / 'latest_afe_integration.json').read_text())
        cls.master = json.loads((UNIFIED / 'unified_astrology_master.json').read_text())
        cls.formulas = json.loads((UNIFIED / 'formula_registry.json').read_text())

    def test_all_sources_are_hashed_and_raw_copies_are_repository_safe(self):
        self.assertEqual(len(self.inventory['sources']), 12)
        for source in self.inventory['sources']:
            raw = ROOT / source['raw_path']
            self.assertTrue(raw.exists())
            # Git tracks the executable bit but not a strict 0600 mode. The portable
            # repository invariant is that source artifacts are never group/other writable.
            self.assertFalse(raw.stat().st_mode & 0o022)
            self.assertEqual(len(source['sha256']), 64)

    def test_secret_values_are_not_in_distributable_redacted_files(self):
        redacted = '\n'.join(p.read_text(errors='replace') for p in (LATEST / 'redacted').iterdir())
        for secret in ('fred_key_12345', 'alpha_key_67890', 'iex_token_abc', 'news_key_123', 'twitter_bearer_xyz', 'fmp_key_456'):
            self.assertNotIn(secret, redacted)
        self.assertIn('[REDACTED]', redacted)

    def test_arabic_part_fields_are_normalized(self):
        parts = [r for r in self.normalized['records'] if r['canonical_type'] == 'arabic_part']
        self.assertEqual(len(parts), 3)
        fortune = next(r for r in parts if r['normalized_value']['part_id'] == 'part_of_fortune')
        self.assertEqual(fortune['normalized_value']['longitude_degrees'], 120.45)
        self.assertEqual(fortune['normalized_value']['house_number'], 4)
        self.assertEqual(fortune['status'], 'source_derived')

    def test_methodology_and_provisional_statuses_are_preserved(self):
        transit = next(r for r in self.normalized['records'] if r['canonical_type'] == 'transit_strength')
        self.assertEqual(transit['status'], 'methodology_bound')
        midpoint = next(r for r in self.normalized['records'] if r['canonical_type'] == 'midpoint_activation')
        self.assertEqual(midpoint['normalized_value']['interpretation_status'], 'source_derived_methodology_bound')
        self.assertEqual(self.integration['available_midpoint_metadata']['status'], 'source_derived_with_provisional_ellipsis')

    def test_merge_counts_and_formula_registry_are_consistent(self):
        self.assertEqual(self.integration['counts']['arabic_parts'], 3)
        self.assertEqual(self.integration['counts']['transit_strength'], 1)
        self.assertEqual(self.integration['counts']['midpoint_activations'], 3)
        ids = [item['id'] for item in self.formulas['formulas']]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 19)
        self.assertIn('latest_afe_integration', self.master)

    def test_research_manifest_is_non_advisory_and_no_api_calls_were_needed(self):
        manifest = self.integration['research_dataset_manifest']
        self.assertFalse(manifest['observations_acquired'])
        self.assertIn('trading instructions', manifest['prohibited_uses'])
        self.assertIn('No API calls were made.', manifest['limitations'])


if __name__ == '__main__':
    unittest.main()
