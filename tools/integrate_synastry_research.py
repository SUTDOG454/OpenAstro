from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path('/home/ubuntu/openastro_worktree')
MASTER_PATH = ROOT / 'data/unified/unified_astrology_master.json'
SYN = ROOT / 'data/ingested-synastry-research'


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8'))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


master = read_json(MASTER_PATH)
summary = read_json(SYN / 'synastry_research_summary.json')
inventory = read_json(SYN / 'synastry_source_inventory.json')
claims = read_json(SYN / 'synastry_statistical_claim_register.json')
discrepancies = read_json(SYN / 'synastry_discrepancy_register.json')
validation = read_json(SYN / 'synastry_validation_report.json')
records = read_json(SYN / 'synastry_normalized_records.json')

relative = lambda path: str(path.relative_to(ROOT))
code_records = [record for record in records['records'] if record['record_type'] == 'unexecuted_scoring_code_metadata']
table_records = [record for record in records['records'] if record['record_type'] == 'synastry_table_profile']

synastry_layer = {
    'status': 'source_ingested_with_research_boundaries',
    'evidence_class': 'source_derived_and_methodology_bound',
    'source_inventory_ref': relative(SYN / 'synastry_source_inventory.json'),
    'normalized_records_ref': relative(SYN / 'synastry_normalized_records.json'),
    'statistical_claim_register_ref': relative(SYN / 'synastry_statistical_claim_register.json'),
    'discrepancy_register_ref': relative(SYN / 'synastry_discrepancy_register.json'),
    'validation_ref': relative(SYN / 'synastry_validation_report.json'),
    'summary_ref': relative(SYN / 'synastry_research_summary.json'),
    'counts': {
        'sources': summary['source_count'],
        'records': summary['record_count'],
        'reported_statistical_claims': summary['source_reported_statistical_claim_count'],
        'small_cohort_candidates': summary['small_cohort_candidate_count'],
        'unexecuted_code_templates': summary['unexecuted_code_template_count'],
    },
    'methodology_and_training_boundary': {
        'observations_acquired': False,
        'labels_acquired': False,
        'model_training_authorized': False,
        'statistical_claims_independently_recomputed': False,
        'source_reported_scores_adopted': False,
        'uploaded_code_executed': False,
        'policy': 'Templates, mocks, source-reported statistical outputs, small named-pair cohorts, and unexecuted scoring code remain pending-review research materials. They cannot be used as empirical replication, deployed compatibility scoring, model training, outcome prediction, or personal decision support without a separately registered, rights-resolved, leakage-safe study and independent review.',
    },
    'canonical_registry_boundary': 'No source row, aspect weight, orb rule, harmonic rule, compatibility score, statistical claim, or code template is added to the canonical entity registry, calculation catalog, or standard delineation engine by this integration.',
    'boundaries': summary['boundaries'],
}

master['synastry_research_layer'] = synastry_layer
research_layer = master.setdefault('research_layer', {})
research_layer['synastry_candidate_material'] = {
    'status': 'pending_review_research_material',
    'refs': {
        'source_inventory': relative(SYN / 'synastry_source_inventory.json'),
        'statistical_claim_register': relative(SYN / 'synastry_statistical_claim_register.json'),
        'validation': relative(SYN / 'synastry_validation_report.json'),
    },
    'observations_acquired': False,
    'labels_acquired': False,
    'backtests_executed': False,
    'model_training_authorized': False,
    'policy': 'Synastry source tables are not active model data. Source-reported statistical outputs are unverified pending recomputation; templates/mocks are methodology examples; uploaded code remains static-inspection-only.',
}
notes = master.setdefault('implementation_notes', {})
notes['synastry_research_layer'] = 'The new synastry ingestion attaches source table profiles, static-code metadata, reported-claim warnings, and discrepancy records. It does not authorize compatibility or relationship predictions, modify canonical calculation rules, or promote reported results into training evidence.'
master['generated_at'] = datetime.now(timezone.utc).isoformat()
write_json(MASTER_PATH, master)

report = {
    'status': 'integrated_with_research_boundaries',
    'master_ref': relative(MASTER_PATH),
    'artifact_hashes': {
        relative(path): sha256(path)
        for path in [
            SYN / 'synastry_source_inventory.json',
            SYN / 'synastry_normalized_records.json',
            SYN / 'synastry_statistical_claim_register.json',
            SYN / 'synastry_discrepancy_register.json',
            SYN / 'synastry_validation_report.json',
        ]
    },
    'checks': {
        'validation_passed_with_warnings': validation['status'] == 'passed_with_review_warnings',
        'source_count_matches': len(inventory['sources']) == summary['source_count'],
        'unexecuted_code_remains_unexecuted': len(code_records) == summary['unexecuted_code_template_count'],
        'reported_claims_remain_unverified': all(claim['status'] == 'unverified_pending_recalculation' for claim in claims['claims']),
        'cohort_provenance_gaps_visible': any(record['discrepancy_id'].startswith('cohort-provenance-') for record in discrepancies['records']),
        'no_active_observations_or_labels': not research_layer['synastry_candidate_material']['observations_acquired'] and not research_layer['synastry_candidate_material']['labels_acquired'],
    },
}
write_json(SYN / 'synastry_integration_report.json', report)
print(json.dumps({'status': report['status'], 'counts': synastry_layer['counts'], 'checks': report['checks']}, indent=2))
