from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path('/home/ubuntu/openastro_worktree')
RAW = ROOT / 'data/sources/2026-08-synastry-research/raw'
OUT = ROOT / 'data/ingested-synastry-research'

TEMPLATE_MARKERS = ('template', 'mock', 'sample', 'workflow', 'weighting_examples')
REPORT_MARKERS = ('report', 'test_results', 'effect_sizes', 'significance', 'correlation_matrix', 'score_summary', 'harmonic_support', 'pair_summary')
DATASET_MARKERS = ('celebrity_synastry_25', 'scored_25_couple_dataset', 'synastry_with_overlays', 'obama_obama_synastry_test')


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def slug(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def classify(name: str) -> dict[str, Any]:
    lower = name.lower()
    if lower.endswith('.py'):
        return {
            'family': 'untrusted_scoring_code_template',
            'evidence_class': 'source_derived',
            'status': 'pending_review',
            'limitations': ['Static code inspection only. The file was not executed, dependency-resolved, security-reviewed, or adopted as a scoring engine.'],
        }
    if any(marker in lower for marker in TEMPLATE_MARKERS):
        return {
            'family': 'template_or_mock_methodology',
            'evidence_class': 'methodology_bound',
            'status': 'pending_review',
            'limitations': ['Template/mock/example material is not an observed cohort, empirical validation, or deployed score.'],
        }
    if any(marker in lower for marker in REPORT_MARKERS):
        return {
            'family': 'source_reported_statistical_output',
            'evidence_class': 'source_derived',
            'status': 'pending_review',
            'limitations': ['Reported statistics are preserved as source claims and were not independently recomputed from a frozen raw cohort.'],
        }
    if any(marker in lower for marker in DATASET_MARKERS):
        return {
            'family': 'small_named_synastry_cohort_candidate',
            'evidence_class': 'source_derived',
            'status': 'pending_review',
            'limitations': ['Small named-pair cohort with source rights, sampling frame, inclusion criteria, birth-data provenance, and outcome definitions pending review. It is not a representative training or validation dataset.'],
        }
    return {
        'family': 'synastry_source_table',
        'evidence_class': 'source_derived',
        'status': 'pending_review',
        'limitations': ['Source table requires schema, provenance, and methodology review before use.'],
    }


def scalar(value: str) -> Any:
    text = value.strip()
    if text == '':
        return None
    try:
        if re.fullmatch(r'-?\d+', text):
            return int(text)
        if re.fullmatch(r'-?(?:\d+\.\d*|\d*\.\d+)(?:[eE][+-]?\d+)?', text):
            return float(text)
    except ValueError:
        pass
    return text


def profile_csv(path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    with path.open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        rows = [{key: scalar(value or '') for key, value in row.items()} for row in reader]
        headers = reader.fieldnames or []
    numeric_columns = []
    missing_counts = {}
    for header in headers:
        values = [row.get(header) for row in rows]
        missing_counts[header] = sum(value is None for value in values)
        present = [value for value in values if value is not None]
        if present and all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in present):
            numeric_columns.append(header)
    return rows, {
        'row_count': len(rows),
        'columns': headers,
        'numeric_columns': numeric_columns,
        'missing_value_counts': missing_counts,
        'first_row': rows[0] if rows else None,
    }


def code_metadata(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding='utf-8', errors='replace')
    symbols = []
    for pattern in [r'^\s*(?:def|class)\s+([A-Za-z_][A-Za-z0-9_]*)', r'^\s*([A-Z][A-Z0-9_]+)\s*=']:
        symbols.extend(re.findall(pattern, text, flags=re.M))
    imports = re.findall(r'^(?:from\s+([^\s]+)|import\s+([^\s,]+))', text, flags=re.M)
    return {
        'named_symbols': sorted(set(symbols)),
        'imports': sorted({left or right for left, right in imports}),
        'execution_policy': 'do_not_execute',
    }

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    discrepancies: list[dict[str, Any]] = []
    claim_register: list[dict[str, Any]] = []

    for path in sorted(RAW.iterdir()):
        if not path.is_file():
            continue
        meta = classify(path.name)
        source_id = f'openastro:synastry-upload:{slug(path.name)}'
        source = {
            'source_id': source_id,
            'source_path': str(path.relative_to(ROOT)),
            'filename': path.name,
            'sha256': sha256(path),
            'size_bytes': path.stat().st_size,
            'media_type': 'text/csv' if path.suffix.lower() == '.csv' else 'text/x-python',
            'family': meta['family'],
            'evidence_class': meta['evidence_class'],
            'status': meta['status'],
            'trust_status': 'untrusted_user_supplied_data',
            'rights_status': 'source_rights_pending_review',
            'raw_preservation': 'staged_copy',
            'limitations': meta['limitations'],
            'flags': ['user_supplied', 'untrusted_data', 'source_rights_pending_review'],
        }
        sources.append(source)
        if path.suffix.lower() == '.py':
            source['parser'] = 'static_code_inspection'
            source['flags'].extend(['do_not_execute', 'static_inspection_only'])
            metadata = code_metadata(path)
            records.append({
                'record_id': f'syn_code_{sha256(path)[:20]}',
                'source_id': source_id,
                'source_sha256': source['sha256'],
                'record_type': 'unexecuted_scoring_code_metadata',
                'evidence_class': 'source_derived',
                'status': 'pending_review',
                'normalized_value': metadata,
                'limitations': meta['limitations'],
            })
            continue

        source['parser'] = 'csv_dict_reader'
        rows, profile = profile_csv(path)
        source['profile'] = profile
        record_id = f'syn_table_{sha256(path)[:20]}'
        records.append({
            'record_id': record_id,
            'source_id': source_id,
            'source_sha256': source['sha256'],
            'record_type': 'synastry_table_profile',
            'evidence_class': meta['evidence_class'],
            'status': meta['status'],
            'normalized_value': profile,
            'raw_rows': rows,
            'limitations': meta['limitations'],
        })
        if meta['family'] == 'source_reported_statistical_output':
            claim_register.append({
                'claim_id': f'claim_{sha256(path)[:20]}',
                'source_id': source_id,
                'record_id': record_id,
                'claim_type': 'source_reported_statistical_output',
                'status': 'unverified_pending_recalculation',
                'evidence_class': 'source_derived',
                'reported_table_columns': profile['columns'],
                'reported_row_count': profile['row_count'],
                'limitations': ['No independent recomputation or multiple-testing review was performed.', 'Reported p-values, effect sizes, confidence intervals, correlations, and score summaries are not validation evidence until raw cohort lineage and analysis code are frozen and independently rerun.'],
            })
        if meta['family'] == 'small_named_synastry_cohort_candidate':
            discrepancies.append({
                'discrepancy_id': f'cohort-provenance-{slug(path.name)}',
                'source_id': source_id,
                'status': 'pending_review',
                'detail': 'Cohort use is blocked until sampling frame, inclusion/exclusion criteria, relationship-outcome coding, birth-data source/Rodden ratings, consent or public-data basis, duplicate policy, and missingness policy are documented.',
            })
        if profile['row_count'] < 30:
            discrepancies.append({
                'discrepancy_id': f'small-sample-{slug(path.name)}',
                'source_id': source_id,
                'status': 'pending_review',
                'detail': f"Table has {profile['row_count']} rows. It may be useful as a fixture or exploratory source table but is not sufficient by itself for generalizable model training or confirmatory validation.",
            })

    summary = {
        'schema_version': '1.0.0',
        'status': 'source_ingested_with_research_boundaries',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'source_count': len(sources),
        'record_count': len(records),
        'family_counts': dict(Counter(source['family'] for source in sources)),
        'source_reported_statistical_claim_count': len(claim_register),
        'small_cohort_candidate_count': sum(source['family'] == 'small_named_synastry_cohort_candidate' for source in sources),
        'unexecuted_code_template_count': sum(source['family'] == 'untrusted_scoring_code_template' for source in sources),
        'boundaries': [
            'Templates, mocks, examples, and source-reported result tables are not empirical replication evidence.',
            'Uploaded scoring code was statically inspected only and was not executed or adopted.',
            'Small named-pair cohorts are research candidates only; they are not representative training or validation data.',
            'No relationship outcome prediction, compatibility score, or personal decision support is produced by this ingestion.',
            'No statistical claim is promoted without frozen raw inputs, provenance, pre-registration, appropriate controls, and independent review.',
        ],
    }
    validation = {
        'schema_version': '1.0.0',
        'status': 'passed_with_review_warnings',
        'checks': {
            'all_sources_hashed': all(len(source['sha256']) == 64 for source in sources),
            'all_records_reference_sources': all(record['source_id'] in {source['source_id'] for source in sources} for record in records),
            'all_uploaded_code_not_executed': all('do_not_execute' in source['flags'] for source in sources if source['family'] == 'untrusted_scoring_code_template'),
            'mock_and_template_not_promoted': all(record['status'] == 'pending_review' for record in records if any(marker in record['source_id'] for marker in ('template', 'mock', 'sample'))),
            'reported_statistics_not_promoted': all(claim['status'] == 'unverified_pending_recalculation' for claim in claim_register),
        },
        'warnings': [
            'All source rights and data-use permissions remain pending review.',
            'Reported significance, effect-size, correlation, and scoring outputs were not independently recomputed.',
            'Observed-looking cohorts are small and lack documented cohort construction, birth-data provenance, outcome coding, and control design.',
            'No source table was accepted as a production training, testing, or prediction dataset.',
        ],
    }

    for name, value in {
        'synastry_source_inventory.json': {'schema_version': '1.0.0', 'sources': sources},
        'synastry_normalized_records.json': {'schema_version': '1.0.0', 'records': records},
        'synastry_statistical_claim_register.json': {'schema_version': '1.0.0', 'claims': claim_register},
        'synastry_discrepancy_register.json': {'schema_version': '1.0.0', 'records': discrepancies},
        'synastry_research_summary.json': summary,
        'synastry_validation_report.json': validation,
    }.items():
        (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print(json.dumps({'sources': len(sources), 'records': len(records), 'statistical_claims': len(claim_register), 'discrepancies': len(discrepancies), 'validation': validation['status']}, indent=2))


if __name__ == '__main__':
    main()
