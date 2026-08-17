import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))

from unified_delineation_ontology import (  # noqa: E402
    build_formula_reference,
    build_interpretation,
    normalize_observation,
    validate_chart_methodology,
)


class OntologyUtilityTests(unittest.TestCase):
    def test_observation_preserves_provenance_and_settings(self):
        record = normalize_observation(
            observation_id='obs-1', point='Sun', source_ids=['src-1', 'src-1'],
            status='computed', calculated_value={'longitude': 12.5},
            settings={'zodiac': 'tropical', 'house_system': 'P'},
        )
        self.assertEqual(record['source_ids'], ['src-1'])
        self.assertEqual(record['settings']['house_system'], 'P')

    def test_invalid_status_rejected(self):
        with self.assertRaises(ValueError):
            normalize_observation(observation_id='obs-1', point='Moon', source_ids=['src'], status='fact')

    def test_interpretation_requires_evidence_refs(self):
        record = build_interpretation(
            interpretation_id='int-1', tradition='western', statement='Source-labeled statement',
            evidence_refs=['obs-1'], source_ids=['src-1'], status='source_derived',
        )
        self.assertEqual(record['evidence_refs'], ['obs-1'])

    def test_formula_contract_has_failure_mode(self):
        record = build_formula_reference(
            formula_id='midpoint', formula='circular midpoint', source_ids=['calc'],
            required_inputs=['point_longitudes'], outputs=['midpoint_longitude'],
        )
        self.assertEqual(record['failure_mode'], 'unavailable_with_recommendation')

    def test_chart_methodology_validation(self):
        method = {'chart_type': 'natal', 'status': 'contracted', 'inputs': ['datetime'], 'outputs': ['positions'], 'source_ids': ['calc'], 'limitations': ['settings required']}
        self.assertEqual(validate_chart_methodology(method), [])


class ExpansionPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = ROOT / 'data/unified'
        cls.master = json.loads((cls.package / 'unified_astrology_master.json').read_text())
        cls.validation = json.loads((cls.package / 'validation_report.json').read_text())

    def test_all_canonical_chart_types_have_contracts(self):
        registry = self.master['framework_registry']
        self.assertEqual(registry['chart_type_count'], len(registry['chart_type_contracts']))
        for contract in registry['chart_type_contracts'].values():
            self.assertIn('inputs', contract)
            self.assertIn('outputs', contract)
            self.assertIn('limitations', contract)

    def test_unimplemented_predictive_methods_are_explicit(self):
        contracts = self.master['framework_registry']['chart_type_contracts']
        self.assertEqual(contracts['firdaria']['status'], 'not_implemented')
        self.assertEqual(contracts['primary_direction']['status'], 'not_implemented')

    def test_financial_research_is_non_advisory(self):
        prohibited = self.master['research_contract']['financial_astrology']['prohibited_uses']
        self.assertIn('trading instructions', prohibited)
        self.assertIn('personal financial advice', prohibited)

    def test_validation_preserves_registry_boundary(self):
        self.assertTrue(self.validation['checks']['canonical_registry_not_forked'])
        self.assertTrue(self.validation['checks']['source_code_not_executed'])


if __name__ == '__main__':
    unittest.main()
