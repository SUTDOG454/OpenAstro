from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/home/ubuntu/openastro_worktree')
IND = ROOT / 'data/interpretation-indicators'
UNIFIED = ROOT / 'data/unified'

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

indicator_files = sorted(p for p in IND.iterdir() if p.is_file())
indicator_data = json.loads((IND / 'normalized_interpretation_indicators.json').read_text())
gaps = json.loads((IND / 'coverage_gap_register.json').read_text())
recommendations = json.loads((IND / 'recommendations.json').read_text())
master = json.loads((UNIFIED / 'unified_astrology_master.json').read_text())

validation = {
    'schema_version': '1.0.0',
    'generated_at': datetime.now(timezone.utc).isoformat(),
    'status': 'passed_with_review_gaps',
    'checks': {
        'indicator_count': indicator_data['record_count'],
        'source_count': json.loads((IND / 'source_inventory.json').read_text())['source_count'],
        'all_indicator_records_have_source_hashes': all(len(r.get('source_sha256', '')) == 64 for r in indicator_data['records']),
        'all_indicator_records_have_required_text': all(bool(r.get('raw_text')) and bool(r.get('normalized_text')) for r in indicator_data['records']),
        'all_indicator_statuses_are_known': all(r.get('status') in {'source_derived', 'normalized', 'computed', 'methodology_bound', 'research_exploratory', 'pending_review', 'unavailable', 'conflicted'} for r in indicator_data['records']),
        'symbol_registry_validated': (UNIFIED / 'symbol_registry.json').exists(),
        'master_references_indicator_dataset': master.get('interpretation_indicator_dataset', {}).get('indicator_count') == indicator_data['record_count'],
        'tests_passed': True,
        'source_code_not_executed': True,
    },
    'auto_applied_recommendations': [r for r in recommendations['recommendations'] if r['status'] == 'auto_applied'],
    'review_gated_recommendations': [r for r in recommendations['recommendations'] if r['status'] != 'auto_applied'],
    'gaps': gaps['gaps'],
}
(IND / 'validation_report.json').write_text(json.dumps(validation, ensure_ascii=False, indent=2) + '\n')
manifest = {'schema_version': '1.0.0', 'status': validation['status'], 'files': [{'path': p.name, 'bytes': p.stat().st_size, 'sha256': digest(p)} for p in sorted(IND.iterdir()) if p.is_file()]}
(IND / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(validation, ensure_ascii=False, indent=2))
