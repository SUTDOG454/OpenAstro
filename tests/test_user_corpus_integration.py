import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / 'data/ingested-user-corpus'
MASTER = ROOT / 'data/unified/unified_astrology_master.json'


def read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


class UserCorpusIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = read_json(CORPUS / 'user_corpus_source_inventory.json')
        cls.records = read_json(CORPUS / 'normalized_user_corpus_records.json')
        cls.quarantine = read_json(CORPUS / 'sensitive_content_quarantine.json')
        cls.discrepancies = read_json(CORPUS / 'user_corpus_discrepancies.json')
        cls.validation = read_json(CORPUS / 'user_corpus_validation_report.json')
        cls.integration = read_json(CORPUS / 'user_corpus_integration_report.json')
        cls.esoteric = read_json(CORPUS / 'esoteric_retrieval_records.json')
        cls.financial = read_json(CORPUS / 'financial_research_candidate_material.json')
        cls.signals = read_json(CORPUS / 'unvalidated_signal_candidates.json')
        cls.chart_types = read_json(CORPUS / 'chart_type_proposals.json')
        cls.master = read_json(MASTER)

    def test_all_sources_are_hashed_and_preserved(self):
        self.assertGreaterEqual(len(self.inventory['sources']), 29)
        for source in self.inventory['sources']:
            self.assertEqual(len(source['sha256']), 64)
            self.assertTrue(source['source_path'])
        user_sources = [source for source in self.inventory['sources'] if source['source_id'].startswith('openastro:user-upload:')]
        self.assertGreaterEqual(len(user_sources), 20)
        for source in user_sources:
            self.assertEqual(source['raw_preservation'], 'staged_copy')
            self.assertIn('source_rights_pending_review', source['flags'])
        gitignore = (ROOT / '.gitignore').read_text(encoding='utf-8')
        self.assertIn('data/sources/2026-08-user-uploads/raw/', gitignore)
        self.assertIn('data/sources/2026-08-user-uploads/derived-pdf-text/', gitignore)

    def test_records_are_source_linked_and_complete(self):
        known_source_ids = {source['source_id'] for source in self.inventory['sources']}
        self.assertGreaterEqual(len(self.records['records']), 1700)
        for record in self.records['records']:
            self.assertIn(record['source_id'], known_source_ids)
            self.assertEqual(len(record['source_sha256']), 64)
            self.assertTrue(record['record_id'])
            self.assertTrue(record['normalized_text'])
            self.assertTrue(record['tradition_scope'])
            self.assertTrue(record['limitations'])

    def test_sensitive_and_private_material_is_not_generalized(self):
        self.assertEqual(len(self.quarantine['records']), 2)
        for item in self.quarantine['records']:
            self.assertEqual(item['status'], 'quarantined_from_general_delineation')
            self.assertIn('general delineation', ' '.join(item['prohibited_processing']))
        private_discrepancies = [item for item in self.discrepancies['records'] if item['discrepancy_id'].startswith('private-source-generalization-block')]
        self.assertTrue(private_discrepancies)
        general_records = self.records['records']
        quarantined_ids = {item['source_id'] for item in self.quarantine['records']}
        self.assertFalse(any(record['source_id'] in quarantined_ids for record in general_records))

    def test_uploaded_code_is_static_inspection_only(self):
        code_sources = [source for source in self.inventory['sources'] if source['category'] == 'untrusted_code_or_ui']
        self.assertEqual(len(code_sources), 4)
        for source in code_sources:
            self.assertIn('do_not_execute', source['flags'])
            self.assertEqual(source['parser'], 'static_code_inspection')
        self.assertTrue(self.validation['checks']['code_execution_prohibited'])

    def test_esoteric_records_remain_retrieval_only(self):
        self.assertEqual(self.esoteric['tradition_mode'], 'esoteric')
        self.assertEqual(self.esoteric['calculation_engine'], 'none')
        self.assertGreaterEqual(self.esoteric['record_count'], 70)
        namespace = self.master['esoteric_retrieval_namespace']
        self.assertEqual(namespace['calculation_engine'], 'none')
        self.assertEqual(namespace['allowed_engine'], 'esoteric_retrieval_only')
        self.assertEqual(set(namespace['rejected_modes']), {'western', 'vedic', 'standard'})
        self.assertTrue(all('esoteric' in record['tradition_scope'] for record in self.esoteric['records']))

    def test_financial_and_signal_material_is_unpromoted(self):
        self.assertEqual(self.financial['status'], 'methodology_bound_research_only')
        self.assertFalse(self.financial['observations_acquired'])
        self.assertFalse(self.financial['labels_acquired'])
        self.assertEqual(self.signals['status'], 'pending_review_not_promoted')
        self.assertGreaterEqual(self.signals['record_count'], 1000)
        for record in self.signals['records'][:100]:
            self.assertEqual(record['status'], 'pending_review')
            self.assertEqual(record['extensions']['promotion_status'], 'not_eligible_without_validated_experiment')
        candidate_material = self.master['research_layer']['user_corpus_candidate_material']
        self.assertFalse(candidate_material['observations_acquired'])
        self.assertFalse(candidate_material['labels_acquired'])
        self.assertFalse(candidate_material['backtests_executed'])

    def test_chart_type_proposals_do_not_modify_canonical_registry(self):
        self.assertEqual(self.chart_types['status'], 'source_derived_pending_registry_reconciliation')
        self.assertGreaterEqual(self.chart_types['record_count'], 20)
        self.assertTrue(all(record['status'] == 'pending_review' for record in self.chart_types['records']))
        integration = self.master['user_corpus_integration']
        self.assertIn('does not modify', integration['canonical_registry_boundary'].lower())

    def test_integration_report_checks_pass(self):
        self.assertEqual(self.integration['status'], 'integrated_with_review_boundaries')
        self.assertTrue(all(self.integration['checks'].values()))
        self.assertEqual(self.validation['status'], 'passed_with_review_warnings')


if __name__ == '__main__':
    unittest.main()
