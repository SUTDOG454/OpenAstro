from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/home/ubuntu/openastro_worktree')
IND = ROOT / 'data/interpretation-indicators'
UNIFIED = ROOT / 'data/unified'

indicators = json.loads((IND / 'normalized_interpretation_indicators.json').read_text())
summary = json.loads((IND / 'indicator_dataset_summary.json').read_text())
master = json.loads((UNIFIED / 'unified_astrology_master.json').read_text())
framework = json.loads((UNIFIED / 'framework_registry.json').read_text())
formulas = json.loads((UNIFIED / 'formula_registry.json').read_text())

records = indicators['records']
subject_counts = Counter(r['subject_path'].split('.')[0] for r in records)
status_counts = Counter(r['status'] for r in records)
source_counts = Counter(r['source_id'] for r in records)

# Thin data means an observed source layer has little structured support, not that missing content should be invented.
thin_layers = []
for layer, count in sorted(subject_counts.items()):
    if count < 3:
        thin_layers.append({'layer': layer, 'indicator_count': count, 'status': 'thin', 'recommendation': 'Add a source-backed module or leave unavailable; do not fabricate interpretation text.'})

missing_contracts = []
for chart_type, contract in framework['chart_type_contracts'].items():
    if contract.get('status') in {'pending_review', 'not_implemented', 'unavailable'}:
        missing_contracts.append({'chart_type': chart_type, 'status': contract.get('status'), 'required_inputs': contract.get('inputs', []), 'recommendation': 'Add a deterministic adapter and fixture only after explicit formula, settings, provenance, and failure mode are reviewed.'})

required_layers = {
    'definitions': (ROOT / 'data/definitions').exists(),
    'calculations': (ROOT / 'data/unified/formula_registry.json').exists(),
    'signals': bool(master.get('signal_summary')),
    'indicators': bool(master.get('indicator_summary')),
    'methodologies': bool(master.get('framework_registry')),
    'symbols': (UNIFIED / 'symbol_registry.json').exists(),
    'tests': (ROOT / 'tests').exists(),
    'research_controls': bool(master.get('research_contract')),
    'provenance': (IND / 'source_inventory.json').exists(),
}

recommendations = [
    {'id': 'auto-add-indicator-schema', 'status': 'auto_applied', 'safe': True, 'reason': 'Adds a reversible schema and validator for interpretation indicators.'},
    {'id': 'auto-add-keyword-index', 'status': 'auto_applied', 'safe': True, 'reason': 'Adds retrieval index without changing source meaning.'},
    {'id': 'auto-add-unicode-symbol-registry', 'status': 'pending_auto_apply', 'safe': True, 'reason': 'Can be generated from canonical aliases and source-observed symbols.'},
    {'id': 'auto-add-provenance-links', 'status': 'auto_applied', 'safe': True, 'reason': 'Every extracted record carries source ID, path, and content hash.'},
    {'id': 'semantic-tradition-review', 'status': 'pending_review', 'safe': False, 'reason': 'Combining Western, Hellenistic, Vedic, Magi, Uranian, financial, and user-defined meanings would be semantic drift.'},
    {'id': 'repair-malformed-json', 'status': 'pending_review', 'safe': False, 'reason': 'Repair can alter source content; preserve raw and require bounded review.'},
    {'id': 'implement-unavailable-calculations', 'status': 'pending_review', 'safe': False, 'reason': 'Requires explicit rules, engine settings, dependencies, and regression fixtures.'},
]

coverage_gap_register = {
    'schema_version': '1.0.0',
    'status': 'expanded_with_review_gaps',
    'dataset': {'indicator_count': len(records), 'source_count': summary['source_count'], 'record_types': summary['record_types']},
    'required_layers': required_layers,
    'thin_layers': thin_layers,
    'unavailable_or_pending_chart_methods': missing_contracts,
    'gaps': [
        {'id': 'interpretation-evidence-is-not-empirical', 'status': 'methodology_boundary', 'details': 'All extracted interpretations are source-derived testing indicators, not validated causal or predictive evidence.'},
        {'id': 'probable-duplicates', 'status': 'review_required', 'details': 'Exact normalized text duplicates were merged; semantic near-duplicates remain separate.'},
        {'id': 'missing-client-consent-context', 'status': 'unavailable', 'details': 'No client-specific interpretation export was promoted into a client artifact.'},
        {'id': 'missing-ephemeris-fixtures', 'status': 'pending_review', 'details': 'Indicators do not imply calculated positions; deterministic fixture generation remains a separate step.'},
    ],
}

# Add safe, reversible schema/index references to the orchestration master.
master['interpretation_indicator_dataset'] = {
    'status': 'source_derived_testing_dataset',
    'source_inventory_ref': 'data/interpretation-indicators/source_inventory.json',
    'normalized_records_ref': 'data/interpretation-indicators/normalized_interpretation_indicators.json',
    'keyword_index_ref': 'data/interpretation-indicators/indicator_keyword_index.json',
    'deduplication_ref': 'data/interpretation-indicators/deduplication.json',
    'indicator_count': len(records),
    'source_count': summary['source_count'],
    'record_types': summary['record_types'],
    'status_counts': dict(status_counts),
    'evidence_class': 'source_derived',
    'limitations': ['Interpretive statements are not empirical evidence.', 'Probable semantic duplicates remain separate.', 'Malformed source files are not silently repaired.'],
}
master['coverage']['interpretation_indicators'] = coverage_gap_register
master['implementation_notes']['indicator_schema'] = 'tools/interpretation_indicator_engine.py'
master['implementation_notes']['indicator_contract'] = 'data/interpretation-indicators/indicator_schema.json'
master['implementation_notes']['unicode_symbol_registry'] = 'data/unified/symbol_registry.json'

(IND / 'coverage_gap_register.json').write_text(json.dumps(coverage_gap_register, ensure_ascii=False, indent=2) + '\n')
(IND / 'recommendations.json').write_text(json.dumps({'schema_version': '1.0.0', 'recommendations': recommendations}, ensure_ascii=False, indent=2) + '\n')
(UNIFIED / 'unified_astrology_master.json').write_text(json.dumps(master, ensure_ascii=False, indent=2) + '\n')

# Human-readable report, with explicit automatic-versus-review boundaries.
report = f'''# Interpretation Indicator Dataset and Gap Analysis\n\nThe corpus extractor identified **{summary["source_count"]} source files** and **{summary["record_count"]} normalized interpretation indicators**. Exact normalized-text duplicates were merged into the provenance layer; probable semantic duplicates remain separate.\n\n## Indicator layers\n\n| Record type | Count | Evidence class |\n|---|---:|---|\n'''
for key, value in sorted(summary['record_types'].items()):
    report += f'| {key} | {value} | source_derived |\\n'
report += f'''\nThe indicators retain raw text, normalized text, subject path, source ID, source path, SHA-256, keywords, Unicode symbols, status, and limitations. They are suitable for retrieval and regression testing, but not for presenting astrology as established evidence.\n\n## Automatically applied improvements\n\nThe system added a reusable indicator schema and validator, a stable keyword index, source-hash links, a deduplication register, and a master-package reference. These are reversible metadata and retrieval improvements.\n\n## Review-gated gaps\n\nSemantic blending across traditions, repair of malformed JSON, deterministic implementation of unavailable chart methods, and empirical validation of interpretations remain review-gated. Thin layers are reported rather than filled with invented text.\n'''
(IND / 'interpretation_indicator_report.md').write_text(report)
print(json.dumps({'indicator_count': len(records), 'source_count': summary['source_count'], 'thin_layers': len(thin_layers), 'pending_chart_methods': len(missing_contracts), 'recommendations': len(recommendations)}, indent=2))
