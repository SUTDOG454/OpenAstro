import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYN = ROOT / 'data/ingested-synastry-research'
MASTER = ROOT / 'data/unified/unified_astrology_master.json'


def read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


class SynastryResearchIngestionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = read_json(SYN / 'synastry_source_inventory.json')
        cls.records = read_json(SYN / 'synastry_normalized_records.json')
        cls.claims = read_json(SYN / 'synastry_statistical_claim_register.json')
        cls.discrepancies = read_json(SYN / 'synastry_discrepancy_register.json')
        cls.summary = read_json(SYN / 'synastry_research_summary.json')
        cls.validation = read_json(SYN / 'synastry_validation_report.json')
        cls.integration = read_json(SYN / 'synastry_integration_report.json')
        cls.master = read_json(MASTER)

    def test_all_sources_are_hashed_and_pending_rights_review(self):
        self.assertEqual(self.summary['source_count'], 29)
        self.assertEqual(len(self.inventory['sources']), 29)
        for source in self.inventory['sources']:
            self.assertEqual(len(source['sha256']), 64)
            self.assertEqual(source['rights_status'], 'source_rights_pending_review')
            self.assertEqual(source['raw_preservation'], 'staged_copy')

    def test_family_classification_is_explicit(self):
        self.assertEqual(self.summary['family_counts']['template_or_mock_methodology'], 6)
        self.assertEqual(self.summary['family_counts']['untrusted_scoring_code_template'], 5)
        self.assertEqual(self.summary['family_counts']['source_reported_statistical_output'], 11)
        self.assertEqual(self.summary['family_counts']['small_named_synastry_cohort_candidate'], 5)

    def test_uploaded_code_remains_static_only(self):
        code_sources = [source for source in self.inventory['sources'] if source['family'] == 'untrusted_scoring_code_template']
        self.assertEqual(len(code_sources), 5)
        for source in code_sources:
            self.assertIn('do_not_execute', source['flags'])
            self.assertEqual(source['parser'], 'static_code_inspection')
        code_records = [record for record in self.records['records'] if record['record_type'] == 'unexecuted_scoring_code_metadata']
        self.assertEqual(len(code_records), 5)
        self.assertTrue(self.validation['checks']['all_uploaded_code_not_executed'])

    def test_reported_statistics_remain_unverified(self):
        self.assertEqual(len(self.claims['claims']), 11)
        for claim in self.claims['claims']:
            self.assertEqual(claim['status'], 'unverified_pending_recalculation')
            self.assertIn('not validation evidence', ' '.join(claim['limitations']))
        self.assertTrue(self.validation['checks']['reported_statistics_not_promoted'])

    def test_cohort_and_small_sample_limits_remain_visible(self):
        records = self.discrepancies['records']
        self.assertEqual(sum(item['discrepancy_id'].startswith('cohort-provenance-') for item in records), 5)
        self.assertGreaterEqual(sum(item['discrepancy_id'].startswith('small-sample-') for item in records), 20)

    def test_master_integration_preserves_research_boundaries(self):
        layer = self.master['synastry_research_layer']
        self.assertEqual(layer['status'], 'source_ingested_with_research_boundaries')
        self.assertEqual(layer['counts']['sources'], 29)
        self.assertFalse(layer['methodology_and_training_boundary']['observations_acquired'])
        self.assertFalse(layer['methodology_and_training_boundary']['labels_acquired'])
        self.assertFalse(layer['methodology_and_training_boundary']['model_training_authorized'])
        self.assertFalse(layer['methodology_and_training_boundary']['uploaded_code_executed'])
        candidate = self.master['research_layer']['synastry_candidate_material']
        self.assertFalse(candidate['observations_acquired'])
        self.assertFalse(candidate['labels_acquired'])
        self.assertFalse(candidate['model_training_authorized'])

    def test_raw_sources_are_excluded_from_repository_publication(self):
        gitignore = (ROOT / '.gitignore').read_text(encoding='utf-8')
        self.assertIn('data/sources/2026-08-synastry-research/raw/', gitignore)
        self.assertTrue(all(self.integration['checks'].values()))


if __name__ == '__main__':
    unittest.main()
