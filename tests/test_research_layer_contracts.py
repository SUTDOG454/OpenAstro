from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / 'data' / 'research'
UNIFIED = ROOT / 'data' / 'unified'


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


class ResearchLayerContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = load_json(UNIFIED / 'research_contract.json')
        self.master = load_json(UNIFIED / 'unified_astrology_master.json')
        self.manifest = load_json(RESEARCH / 'research_dataset_manifest.json')
        self.summary = load_json(RESEARCH / 'research_layer_summary.json')
        self.methods = load_json(RESEARCH / 'training_testing_methods.json')
        self.acquisition = load_json(RESEARCH / 'observation_acquisition_plan.json')
        self.leakage = load_json(RESEARCH / 'temporal_leakage_controls.json')
        self.walk_forward = load_json(RESEARCH / 'walk_forward_validation_plan.json')
        self.promotion = load_json(RESEARCH / 'signal_indicator_promotion_policy.json')

    def test_financial_market_boundary_remains_methodology_bound_and_research_only(self) -> None:
        boundary = self.contract['evidence_boundary']
        self.assertEqual(boundary['financial_and_market_materials'], 'methodology_bound_research_only')
        self.assertEqual(boundary['default_promotion_status'], 'not_eligible_without_validated_experiment')
        self.assertEqual(
            boundary['prohibited_uses'],
            [
                'trading instructions',
                'position sizing',
                'personal financial advice',
                'guaranteed forecasts',
                'causal claims from symbolic associations',
            ],
        )
        self.assertEqual(self.manifest['evidence_boundary'], boundary)
        self.assertFalse(self.manifest['observations_acquired'])
        self.assertFalse(self.manifest['labels_acquired'])
        self.assertEqual(self.manifest['execution_status'], 'not_executed')

    def test_observation_acquisition_contract_has_all_required_gates(self) -> None:
        steps = self.acquisition['contract']['preconditions']
        step_ids = [step['step_id'] for step in steps]
        self.assertEqual(step_ids, [
            'acq-01-register-hypothesis',
            'acq-02-resolve-universe',
            'acq-03-select-source-and-rights',
            'acq-04-preserve-raw-inputs',
            'acq-05-normalize-and-profile',
            'acq-06-compute-astrology-features',
            'acq-07-construct-labels',
            'acq-08-freeze-dataset',
        ])
        required_row_fields = self.acquisition['contract']['observation_row_contract']['required_fields']
        self.assertIn('feature_cutoff', required_row_fields)
        self.assertIn('outcome_window_start', required_row_fields)
        self.assertIn('data_quality_status', required_row_fields)

    def test_leakage_controls_cover_runtime_and_execution_level_risks(self) -> None:
        controls = self.leakage['contract']['core_invariants']
        control_ids = {control['control_id'] for control in controls}
        self.assertTrue({
            'leak-01-availability',
            'leak-02-outcome-separation',
            'leak-03-timezone-and-calendar',
            'leak-04-fold-local-preprocessing',
            'leak-05-overlap-purge-and-embargo',
            'leak-06-final-holdout',
            'leak-07-data-revisions',
            'leak-08-survivorship-and-selection',
        }.issubset(control_ids))
        alignment = self.leakage['contract']['validator_alignment']
        self.assertEqual(alignment['runtime_module'], 'client/src/lib/astro/research/featureCutoff.ts')
        self.assertIn('FEATURE_AFTER_CUTOFF', alignment['implemented_error_codes'])
        self.assertIn('final_holdout_isolation', alignment['additional_execution_audits_required'])

    def test_walk_forward_plan_requires_real_data_and_complete_log(self) -> None:
        plan = self.walk_forward['contract']
        self.assertEqual(self.walk_forward['status'], 'not_executed_requires_observations_and_labels')
        self.assertIn('observations_acquired is true', plan['eligible_dataset_conditions'])
        self.assertIn('labels_acquired is true', plan['eligible_dataset_conditions'])
        self.assertEqual([step['step_id'] for step in plan['first_execution_steps']], [
            'wf-01', 'wf-02', 'wf-03', 'wf-04', 'wf-05', 'wf-06',
            'wf-07', 'wf-08', 'wf-09', 'wf-10', 'wf-11', 'wf-12',
        ])
        self.assertIn('dataset_manifest_hash', plan['required_execution_log_fields'])
        self.assertIn('leakage_audit_summary', plan['required_execution_log_fields'])
        self.assertIn('negative_or_null_results', plan['required_execution_log_fields'])
        self.assertIn('feature_cutoff_audit', plan['required_fold_log_fields'])
        self.assertIn('preprocessing_fit_scope', plan['required_fold_log_fields'])

    def test_promotion_is_review_gated_and_not_based_on_source_text(self) -> None:
        policy = self.promotion['contract']
        self.assertEqual(self.promotion['status'], 'review_gated_not_automatic')
        self.assertEqual(policy['default_evidence_class'], 'methodology_bound')
        self.assertEqual(policy['promotion_target'], 'research_exploratory_scoped_signal_or_indicator')
        self.assertIn('one untouched final holdout evaluation', policy['minimum_requirements'])
        self.assertIn('independent human review', policy['minimum_requirements'])
        self.assertIn('source prose alone', policy['non_qualifying_evidence'])
        self.assertIn('in-sample performance', policy['non_qualifying_evidence'])
        self.assertIn('Keep prohibited uses in force.', policy['promotion_outcomes']['approved'])

    def test_method_records_are_detailed_and_match_summary(self) -> None:
        records = self.methods['records']
        self.assertGreaterEqual(len(records), 12)
        record_ids = {record['method_id'] for record in records}
        self.assertIn('walk_forward_time_split', record_ids)
        self.assertIn('purged_time_split_and_embargo', record_ids)
        self.assertIn('fold_local_preprocessing', record_ids)
        self.assertIn('validation_gated_signal_indicator_promotion', record_ids)
        for record in records:
            self.assertEqual(record['evidence_class'], 'methodology_bound')
            self.assertTrue(record['inputs'])
            self.assertTrue(record['outputs'])
            self.assertTrue(record['required_controls'])
            self.assertTrue(record['failure_conditions'])
        self.assertEqual(self.summary['method_count'], len(records))

    def test_master_links_every_expanded_contract_artifact(self) -> None:
        layer = self.master['research_layer']
        self.assertEqual(layer['evidence_class'], 'methodology_bound')
        self.assertEqual(layer['walk_forward_validation_status'], 'not_executed_requires_observations_and_labels')
        for reference_key in [
            'observation_acquisition_plan_ref',
            'temporal_leakage_controls_ref',
            'walk_forward_validation_plan_ref',
            'signal_indicator_promotion_policy_ref',
            'upstream_research_contract_ref',
        ]:
            self.assertTrue((ROOT / layer[reference_key]).is_file(), reference_key)
        self.assertEqual(layer['counts']['training_testing_methods'], self.summary['method_count'])
        self.assertEqual(layer['counts']['contract_artifacts'], 5)


if __name__ == '__main__':
    unittest.main()
