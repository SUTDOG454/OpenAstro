import importlib
import json
import tempfile
import unittest
from pathlib import Path

from tools import ingest_user_corpus as corpus


class UserCorpusUnitTests(unittest.TestCase):
    def setUp(self):
        self.source = {
            'source_id': 'test:source',
            'source_sha256': 'a' * 64,
            'source_path': 'fixtures/source.txt',
            'sha256': 'a' * 64,
        }

    def test_import_exposes_main_without_running_dataset_builder(self):
        reloaded = importlib.reload(corpus)
        self.assertTrue(callable(reloaded.main))

    def test_slug_digest_stable_id_and_json_parse_modes(self):
        self.assertEqual(corpus.slug('Sun / Moon: Test!'), 'sun-moon-test')
        self.assertEqual(corpus.stable_id('usr', 's', 'subject', 'text'), corpus.stable_id('usr', 's', 'subject', 'text'))
        self.assertNotEqual(corpus.stable_id('usr', 's', 'subject', 'text'), corpus.stable_id('usr', 's', 'subject', 'other'))
        parsed, mode = corpus.try_json('{"chart_types": []}')
        self.assertEqual(mode, 'json')
        self.assertEqual(parsed['chart_types'], [])
        parsed, mode = corpus.try_json('\ufeff{"meta": "ok"}')
        self.assertEqual(mode, 'utf8_bom_removed')
        self.assertEqual(parsed['meta'], 'ok')
        parsed, mode = corpus.try_json('"meta": "repaired"}')
        self.assertEqual(mode, 'bounded_missing_outer_open_brace_repair')
        self.assertEqual(parsed['meta'], 'repaired')
        parsed, mode = corpus.try_json('```json\n{"key": "value"}\n```')
        self.assertEqual(mode, 'fenced_json')
        self.assertEqual(parsed['key'], 'value')
        parsed, mode = corpus.try_json('not json at all')
        self.assertIsNone(parsed)
        self.assertEqual(mode, 'text')

    def test_source_categories_and_flags_preserve_boundaries(self):
        self.assertEqual(corpus.source_category('afe_quantreo_pipeline-2.py'), 'untrusted_code_or_ui')
        self.assertIn('do_not_execute', corpus.source_flags('afe_quantreo_pipeline-2.py'))
        self.assertEqual(corpus.source_category('ASTROLOGICAL_SYNTHESIS_REPORT.md'), 'sensitive_interpretive_material')
        self.assertIn('quarantined_from_general_delineation', corpus.source_flags('ASTROLOGICAL_SYNTHESIS_REPORT.md'))
        self.assertEqual(corpus.source_category('astrodash-4m7y4aef.manus.md'), 'private_chart_or_personalized_output')
        self.assertIn('private_context_not_for_general_corpus', corpus.source_flags('astrodash-4m7y4aef.manus.md'))
        self.assertEqual(corpus.source_category('HistoricalData_1785490203238.csv'), 'financial_or_market_research_material')
        flags = corpus.source_flags('HistoricalData_1785490203238.csv')
        self.assertIn('financial_research_only', flags)
        self.assertIn('not_a_validated_signal', flags)
        self.assertEqual(corpus.source_category('esoteric_astro.txt'), 'esoteric_astrology_source')
        self.assertIn('not_for_standard_calculation_engine', corpus.source_flags('esoteric_astro.txt'))

    def test_add_record_normalizes_text_and_rejects_short_values(self):
        records = []
        corpus.add_record(records, source=self.source, record_type='test', subject='subject', text='  A   normalized\nvalue  ', tradition_scope=['test'])
        corpus.add_record(records, source=self.source, record_type='test', subject='short', text='x', tradition_scope=['test'])
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['normalized_text'], 'A normalized value')
        self.assertEqual(records[0]['source_sha256'], 'a' * 64)
        self.assertEqual(records[0]['status'], 'source_derived')

    def test_text_extraction_families_produce_bounded_source_records(self):
        records = []
        corpus.extract_glossary('Ascendant A sufficiently detailed glossary definition describing the chart angle.', self.source, records)
        corpus.extract_heading_blocks('# ESOTERIC SECTION\n' + ('Source wording preserved for retrieval only. ' * 4), self.source, records, 'heading', ['esoteric'])
        corpus.extract_aspect_headings('ASPECTS OF SUN AND MOON\nASPECTS OF SUN AND MOON', self.source, records)
        corpus.extract_fixed_stars('A: Aldebaran - constellation reference with source-specific wording', self.source, records)
        types = {record['record_type'] for record in records}
        self.assertIn('glossary_definition', types)
        self.assertIn('heading', types)
        self.assertIn('aspect_pair_reference', types)
        self.assertIn('aspect_taxonomy_reference', types)
        self.assertIn('fixed_star_source_reference', types)
        fixed = next(record for record in records if record['record_type'] == 'fixed_star_source_reference')
        self.assertIn('epoch-dependent', fixed['limitations'][0])
        self.assertEqual(sum(record['record_type'] == 'aspect_pair_reference' for record in records), 1)

    def test_structured_framework_and_chart_type_records_remain_pending_review(self):
        records, discrepancies = [], []
        corpus.extract_chart_type_proposals({'chart_types': [{'id': 'solar-arc', 'label': 'Solar Arc', 'core_purpose': 'A source proposal.', 'system': 'Western'}]}, self.source, records, discrepancies)
        corpus.extract_chart_type_proposals({'unexpected': []}, self.source, records, discrepancies)
        corpus.extract_json_framework({
            'framework_metadata': {'name': 'proposal'},
            'expanded_techniques_manifest': {'cycle': {'definition': 'Unvalidated source method.'}},
            'astronomical_and_calculation_parameters': {'economic_cycles': {'cycle': 'source only'}},
        }, self.source, records, discrepancies)
        chart = next(record for record in records if record['record_type'] == 'chart_type_proposal')
        self.assertEqual(chart['status'], 'pending_review')
        financial = [record for record in records if record['record_type'].startswith('financial_') or record['record_type'] == 'economic_cycle_reference']
        self.assertTrue(financial)
        self.assertTrue(all(record['evidence_class'] == 'methodology_bound' for record in financial))
        self.assertTrue(any(item['discrepancy_id'] == 'chart-types-json-not-parseable' for item in discrepancies))

    def test_signal_and_static_code_metadata_do_not_promote_or_execute(self):
        records = []
        signal = ('{"id":"signal-1","description":"Source claim only","trigger":"condition",'
                  '"expected_effect":"effect","source":"document","confidence":0.7,'
                  '"category":"timing","testable":true}')
        corpus.extract_signal_candidates(signal, self.source, records)
        corpus.static_code_metadata('def calculate():\n    return 1\nclass Engine:\n    pass\n', self.source, records)
        candidate = next(record for record in records if record['record_type'] == 'unvalidated_signal_candidate')
        metadata = next(record for record in records if record['record_type'] == 'unexecuted_code_metadata')
        self.assertEqual(candidate['status'], 'pending_review')
        self.assertEqual(candidate['extensions']['promotion_status'], 'not_eligible_without_validated_experiment')
        self.assertEqual(metadata['extensions']['execution_policy'], 'do_not_execute')
        self.assertIn('calculate', metadata['extensions']['named_symbols'])

    def test_csv_profile_remains_an_unverified_candidate(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'candidate.csv'
            path.write_text('Date,Open,Close\n2024-01-01,1,2\n2024-01-02,2,3\n', encoding='utf-8')
            records, discrepancies = [], []
            corpus.extract_csv_profile(path, self.source, records, discrepancies)
        self.assertEqual(records[0]['record_type'], 'unverified_ohlcv_dataset_profile')
        self.assertEqual(records[0]['status'], 'pending_review')
        self.assertEqual(records[0]['extensions']['research_dataset_status'], 'unverified_candidate_not_acquired')
        self.assertEqual(discrepancies[0]['status'], 'pending_review')


if __name__ == '__main__':
    unittest.main()
