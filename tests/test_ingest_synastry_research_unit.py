import importlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import ingest_synastry_research as synastry


class SynastryResearchIngestionUnitTests(unittest.TestCase):
    def _write(self, directory: str, name: str, text: str) -> Path:
        path = Path(directory) / name
        path.write_text(text, encoding='utf-8')
        return path

    def test_import_exposes_main_without_processing_default_raw_directory(self):
        reloaded = importlib.reload(synastry)
        self.assertTrue(callable(reloaded.main))

    def test_classify_preserves_template_report_cohort_and_code_boundaries(self):
        code = synastry.classify('synastry_scoring.py')
        template = synastry.classify('astro_workflow_plan.csv')
        report = synastry.classify('celebrity_effect_sizes_ci_report.csv')
        cohort = synastry.classify('celebrity_synastry_25.csv')
        generic = synastry.classify('unknown_table.csv')
        self.assertEqual(code['family'], 'untrusted_scoring_code_template')
        self.assertIn('not executed', code['limitations'][0])
        self.assertEqual(template['evidence_class'], 'methodology_bound')
        self.assertEqual(report['family'], 'source_reported_statistical_output')
        self.assertIn('not independently recomputed', report['limitations'][0])
        self.assertEqual(cohort['family'], 'small_named_synastry_cohort_candidate')
        self.assertIn('not a representative training', cohort['limitations'][0])
        self.assertEqual(generic['family'], 'synastry_source_table')
        self.assertTrue(all(item['status'] == 'pending_review' for item in [code, template, report, cohort, generic]))

    def test_scalar_parses_numeric_blank_and_text_values(self):
        self.assertIsNone(synastry.scalar(''))
        self.assertIsNone(synastry.scalar('   '))
        self.assertEqual(synastry.scalar(' -12 '), -12)
        self.assertEqual(synastry.scalar('1.25'), 1.25)
        self.assertEqual(synastry.scalar('-1.5e+2'), -150.0)
        self.assertEqual(synastry.scalar('AA'), 'AA')
        self.assertEqual(synastry.slug('Celebrity Synastry 25!'), 'celebrity-synastry-25')

    def test_profile_csv_handles_bom_numbers_missing_values_and_empty_files(self):
        with tempfile.TemporaryDirectory() as directory:
            populated = self._write(directory, 'profile.csv', '\ufeffname,score,p_value\nPair A,2,0.05\nPair B,,text\n')
            rows, profile = synastry.profile_csv(populated)
            self.assertEqual(rows[0]['score'], 2)
            self.assertEqual(rows[0]['p_value'], 0.05)
            self.assertIsNone(rows[1]['score'])
            self.assertEqual(profile['row_count'], 2)
            self.assertEqual(profile['numeric_columns'], ['score'])
            self.assertEqual(profile['missing_value_counts']['score'], 1)
            self.assertEqual(profile['first_row']['name'], 'Pair A')
            empty = self._write(directory, 'empty.csv', '')
            rows, profile = synastry.profile_csv(empty)
            self.assertEqual(rows, [])
            self.assertEqual(profile['columns'], [])
            self.assertIsNone(profile['first_row'])

    def test_code_metadata_is_static_and_does_not_execute_fixture(self):
        with tempfile.TemporaryDirectory() as directory:
            code = self._write(directory, 'scoring.py', 'import os\nfrom package.module import Item\nMAX_SCORE = 10\ndef score_pair():\n    return 1\nclass Engine:\n    pass\n')
            metadata = synastry.code_metadata(code)
        self.assertEqual(metadata['execution_policy'], 'do_not_execute')
        self.assertEqual(metadata['named_symbols'], ['Engine', 'MAX_SCORE', 'score_pair'])
        self.assertEqual(metadata['imports'], ['os', 'package.module'])

    def test_main_generates_pending_review_records_and_unverified_claims(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = root / 'raw'
            output = root / 'out'
            raw.mkdir()
            (raw / 'celebrity_effect_sizes_ci_report.csv').write_text('metric,effect,p_value\nA,0.4,0.03\nB,0.2,\n', encoding='utf-8')
            (raw / 'celebrity_synastry_25.csv').write_text('pair,score\nA-B,2\n', encoding='utf-8')
            (raw / 'astro_workflow_plan.csv').write_text('step,detail\n1,template only\n', encoding='utf-8')
            (raw / 'synastry_scoring.py').write_text('import math\ndef score_pair():\n    return 1\n', encoding='utf-8')
            with patch.object(synastry, 'ROOT', root), patch.object(synastry, 'RAW', raw), patch.object(synastry, 'OUT', output):
                synastry.main()
            inventory = json.loads((output / 'synastry_source_inventory.json').read_text(encoding='utf-8'))
            records = json.loads((output / 'synastry_normalized_records.json').read_text(encoding='utf-8'))
            claims = json.loads((output / 'synastry_statistical_claim_register.json').read_text(encoding='utf-8'))
            discrepancies = json.loads((output / 'synastry_discrepancy_register.json').read_text(encoding='utf-8'))
            validation = json.loads((output / 'synastry_validation_report.json').read_text(encoding='utf-8'))
        self.assertEqual(len(inventory['sources']), 4)
        self.assertEqual(len(records['records']), 4)
        self.assertEqual(len(claims['claims']), 1)
        self.assertEqual(claims['claims'][0]['status'], 'unverified_pending_recalculation')
        code_record = next(item for item in records['records'] if item['record_type'] == 'unexecuted_scoring_code_metadata')
        self.assertEqual(code_record['normalized_value']['execution_policy'], 'do_not_execute')
        self.assertTrue(any(item['discrepancy_id'].startswith('cohort-provenance-') for item in discrepancies['records']))
        self.assertGreaterEqual(sum(item['discrepancy_id'].startswith('small-sample-') for item in discrepancies['records']), 3)
        self.assertTrue(all(validation['checks'].values()))
        self.assertTrue(all(item['status'] == 'pending_review' for item in records['records']))

    def test_main_on_empty_directory_emits_valid_empty_research_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = root / 'raw'
            output = root / 'out'
            raw.mkdir()
            with patch.object(synastry, 'ROOT', root), patch.object(synastry, 'RAW', raw), patch.object(synastry, 'OUT', output):
                synastry.main()
            summary = json.loads((output / 'synastry_research_summary.json').read_text(encoding='utf-8'))
            validation = json.loads((output / 'synastry_validation_report.json').read_text(encoding='utf-8'))
        self.assertEqual(summary['source_count'], 0)
        self.assertEqual(summary['record_count'], 0)
        self.assertEqual(validation['status'], 'passed_with_review_warnings')
        self.assertTrue(all(validation['checks'].values()))


if __name__ == '__main__':
    unittest.main()
