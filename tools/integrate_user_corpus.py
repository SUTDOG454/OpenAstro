from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path('/home/ubuntu/openastro_worktree')
MASTER_PATH = ROOT / 'data/unified/unified_astrology_master.json'
CORPUS = ROOT / 'data/ingested-user-corpus'


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


master = read_json(MASTER_PATH)
summary = read_json(CORPUS / 'user_corpus_summary.json')
source_inventory = read_json(CORPUS / 'user_corpus_source_inventory.json')
normalized = read_json(CORPUS / 'normalized_user_corpus_records.json')
quarantine = read_json(CORPUS / 'sensitive_content_quarantine.json')
discrepancies = read_json(CORPUS / 'user_corpus_discrepancies.json')
validation = read_json(CORPUS / 'user_corpus_validation_report.json')
records: list[dict[str, Any]] = normalized['records']

# Focused, source-attributed derivatives are intentionally references, not additions to canonical registries.
esoteric = [record for record in records if 'esoteric' in record.get('tradition_scope', [])]
signal_candidates = [record for record in records if record.get('record_type') == 'unvalidated_signal_candidate']
chart_type_proposals = [record for record in records if record.get('record_type') == 'chart_type_proposal']
definition_records = [
    record for record in records
    if record.get('record_type') in {'glossary_definition', 'aspect_taxonomy_reference', 'aspect_pair_reference', 'fixed_star_source_reference'}
]
code_inventory = [record for record in records if record.get('record_type') == 'unexecuted_code_metadata']
financial_records = [record for record in records if 'financial_astrology' in record.get('tradition_scope', [])]

write_json(CORPUS / 'esoteric_retrieval_records.json', {
    'schema_version': '1.0.0',
    'tradition_mode': 'esoteric',
    'calculation_engine': 'none',
    'status': 'isolated_source_retrieval',
    'record_count': len(esoteric),
    'records': esoteric,
    'policy': 'Records are source-grounded retrieval material only. They must be requested with tradition_mode esoteric and never enter Western, Vedic, or standard calculation engines.',
})
write_json(CORPUS / 'unvalidated_signal_candidates.json', {
    'schema_version': '1.0.0',
    'status': 'pending_review_not_promoted',
    'record_count': len(signal_candidates),
    'records': signal_candidates,
    'promotion_policy_ref': 'data/research/signal_indicator_promotion_policy.json',
    'policy': 'Source claims and source-provided confidence values are not calibrated performance measures. No candidate is a signal or indicator until the research-contract validation and independent review gates are met.',
})
write_json(CORPUS / 'chart_type_proposals.json', {
    'schema_version': '1.0.0',
    'status': 'source_derived_pending_registry_reconciliation',
    'record_count': len(chart_type_proposals),
    'records': chart_type_proposals,
    'canonical_registry_boundary': 'No chart type is added to the canonical registry or calculation catalog by this ingestion. The source taxonomy requires entity, input, output, methodology, and adapter review.',
})
write_json(CORPUS / 'source_definitions.json', {
    'schema_version': '1.0.0',
    'status': 'source_derived_reference_definitions',
    'record_count': len(definition_records),
    'records': definition_records,
    'policy': 'Definitions, aspect references, and fixed-star material retain source scope and are not universal semantic or calculation rules.',
})
write_json(CORPUS / 'unexecuted_code_inventory.json', {
    'schema_version': '1.0.0',
    'status': 'static_inspection_only',
    'record_count': len(code_inventory),
    'records': code_inventory,
    'policy': 'Uploaded code was preserved and statically inventoried. It was not executed, dependency-resolved, adopted, or treated as a trustworthy calculation engine.',
})
write_json(CORPUS / 'financial_research_candidate_material.json', {
    'schema_version': '1.0.0',
    'status': 'methodology_bound_research_only',
    'record_count': len(financial_records),
    'records': financial_records,
    'research_layer_status': 'configuration_and_method_records_only',
    'observations_acquired': False,
    'labels_acquired': False,
    'policy': 'Financial materials are retained as source proposals, static code metadata, or unverified candidate data. They do not alter the research manifest, execute a backtest, establish a valid observation dataset, or authorize signals, forecasts, position sizing, or advice.',
})

relative = lambda path: str(path.relative_to(ROOT))
existing_esoteric = master.setdefault('esoteric_retrieval_namespace', {})
refs = list(existing_esoteric.get('source_refs', []))
for reference in [relative(CORPUS / 'esoteric_retrieval_records.json'), 'referenced-task:gw4yP30qoqPeIhTA3L9cO0']:
    if reference not in refs:
        refs.append(reference)
existing_esoteric.update({
    'status': 'isolated_source_retrieval',
    'tradition_mode': 'esoteric',
    'calculation_engine': 'none',
    'allowed_engine': 'esoteric_retrieval_only',
    'rejected_modes': ['western', 'vedic', 'standard'],
    'source_refs': refs,
    'user_corpus_record_count': len(esoteric),
    'user_corpus_policy': 'User-supplied esoteric source text is separately preserved and supplied only to the explicit esoteric retrieval namespace. It is not a standard calculation rule.',
})

research_layer = master.setdefault('research_layer', {})
research_layer['user_corpus_candidate_material'] = {
    'status': 'methodology_bound_research_only',
    'financial_research_candidate_material_ref': relative(CORPUS / 'financial_research_candidate_material.json'),
    'unvalidated_signal_candidates_ref': relative(CORPUS / 'unvalidated_signal_candidates.json'),
    'unexecuted_code_inventory_ref': relative(CORPUS / 'unexecuted_code_inventory.json'),
    'candidate_record_counts': {
        'financial_material': len(financial_records),
        'unvalidated_source_signal_candidates': len(signal_candidates),
        'static_code_metadata_records': len(code_inventory),
    },
    'observations_acquired': False,
    'labels_acquired': False,
    'backtests_executed': False,
    'promotion_status': 'not_eligible_without_registered_experiment_and_review',
    'policy': 'These materials do not change the active research-layer execution status. Financial and market material remains research-only and non-advisory, with no validated performance, causal claim, prediction, position sizing, or trade instruction.',
}

master['user_corpus_integration'] = {
    'status': 'integrated_with_provenance_and_review_boundaries',
    'source_inventory_ref': relative(CORPUS / 'user_corpus_source_inventory.json'),
    'normalized_records_ref': relative(CORPUS / 'normalized_user_corpus_records.json'),
    'summary_ref': relative(CORPUS / 'user_corpus_summary.json'),
    'validation_ref': relative(CORPUS / 'user_corpus_validation_report.json'),
    'discrepancies_ref': relative(CORPUS / 'user_corpus_discrepancies.json'),
    'quarantine_ref': relative(CORPUS / 'sensitive_content_quarantine.json'),
    'referenced_task_inventory_ref': 'data/sources/2026-08-user-uploads/referenced_task_inventory.json',
    'derivative_artifacts': {
        'esoteric_retrieval_records_ref': relative(CORPUS / 'esoteric_retrieval_records.json'),
        'unvalidated_signal_candidates_ref': relative(CORPUS / 'unvalidated_signal_candidates.json'),
        'chart_type_proposals_ref': relative(CORPUS / 'chart_type_proposals.json'),
        'source_definitions_ref': relative(CORPUS / 'source_definitions.json'),
        'unexecuted_code_inventory_ref': relative(CORPUS / 'unexecuted_code_inventory.json'),
        'financial_research_candidate_material_ref': relative(CORPUS / 'financial_research_candidate_material.json'),
    },
    'counts': {
        'sources': summary['source_count'],
        'normalized_records': summary['normalized_record_count'],
        'quarantined_sources': summary['quarantined_source_count'],
        'discrepancies': summary['discrepancy_count'],
        'esoteric_retrieval_records': len(esoteric),
        'unvalidated_signal_candidates': len(signal_candidates),
        'chart_type_proposals': len(chart_type_proposals),
        'source_definition_records': len(definition_records),
    },
    'boundaries': summary['high_level_boundaries'],
    'canonical_registry_boundary': 'This integration attaches source artifacts and pending-review proposals. It does not modify astrology-data-unifi canonical registries, formulas, or calculation catalogs.',
}

notes = master.setdefault('implementation_notes', {})
notes['user_corpus_integration'] = 'The uploaded and referenced-task corpus is preserved under data/sources and data/ingested-user-corpus. Integration is artifact-link based: source-derived text, methodology-bound research proposals, private content, sensitive content, static code metadata, and canonical registries remain distinct.'
master['generated_at'] = datetime.now(timezone.utc).isoformat()
write_json(MASTER_PATH, master)

report = {
    'status': 'integrated_with_review_boundaries',
    'master_ref': relative(MASTER_PATH),
    'artifacts': {
        name: {'path': relative(path), 'sha256': sha256(path), 'size_bytes': path.stat().st_size}
        for name, path in {
            'source_inventory': CORPUS / 'user_corpus_source_inventory.json',
            'normalized_records': CORPUS / 'normalized_user_corpus_records.json',
            'validation': CORPUS / 'user_corpus_validation_report.json',
            'esoteric_retrieval_records': CORPUS / 'esoteric_retrieval_records.json',
            'unvalidated_signal_candidates': CORPUS / 'unvalidated_signal_candidates.json',
            'chart_type_proposals': CORPUS / 'chart_type_proposals.json',
            'source_definitions': CORPUS / 'source_definitions.json',
            'financial_candidate_material': CORPUS / 'financial_research_candidate_material.json',
        }.items()
    },
    'checks': {
        'corpus_validation_passed': validation['status'] == 'passed_with_review_warnings',
        'esoteric_isolated': master['esoteric_retrieval_namespace']['calculation_engine'] == 'none',
        'research_observations_unchanged_false': research_layer.get('observations_acquired') is False,
        'research_labels_unchanged_false': research_layer.get('labels_acquired') is False,
        'quarantine_linked': bool(quarantine.get('records')),
        'discrepancies_linked': isinstance(discrepancies.get('records'), list),
    },
}
write_json(CORPUS / 'user_corpus_integration_report.json', report)
print(json.dumps({'status': report['status'], 'counts': master['user_corpus_integration']['counts'], 'checks': report['checks']}, indent=2))
