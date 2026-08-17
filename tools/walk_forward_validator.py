from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path('/home/ubuntu/openastro_worktree')
DEFAULT_MANIFEST = ROOT / 'data/research/research_dataset_manifest.json'
DEFAULT_PLAN = ROOT / 'data/research/walk_forward_validation_plan.json'
DEFAULT_CANDIDATES = ROOT / 'data/ingested-user-corpus/financial_research_candidate_material.json'
DEFAULT_OUTPUT = ROOT / 'data/research/walk_forward_validation_blocked_run.json'


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8'))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def candidate_dataset_status(candidates: dict[str, Any]) -> dict[str, Any] | None:
    for record in candidates.get('records', []):
        if record.get('record_type') == 'unverified_ohlcv_dataset_profile':
            return record
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description='Run contract-gated walk-forward validation readiness checks.')
    parser.add_argument('--manifest', type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument('--plan', type=Path, default=DEFAULT_PLAN)
    parser.add_argument('--candidate-material', type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    manifest = load_json(args.manifest)
    plan = load_json(args.plan)
    candidates = load_json(args.candidate_material)
    candidate = candidate_dataset_status(candidates)

    blockers: list[dict[str, str]] = []
    if manifest.get('observations_acquired') is not True:
        blockers.append({'gate': 'observations_acquired', 'status': 'blocked', 'detail': 'No approved, normalized observation dataset is registered.'})
    if manifest.get('labels_acquired') is not True:
        blockers.append({'gate': 'labels_acquired', 'status': 'blocked', 'detail': 'No independently constructed, frozen label dataset is registered.'})
    if manifest.get('source_rights') != 'resolved':
        blockers.append({'gate': 'source_rights', 'status': 'blocked', 'detail': 'Source rights are not resolved for all included observations.'})
    if manifest.get('execution_status') != 'ready_for_execution':
        blockers.append({'gate': 'execution_status', 'status': 'blocked', 'detail': f"Manifest execution status is {manifest.get('execution_status')!r}, not 'ready_for_execution'."})
    if plan.get('status') != 'ready_for_execution':
        blockers.append({'gate': 'walk_forward_plan_status', 'status': 'blocked', 'detail': f"Plan status is {plan.get('status')!r}; it is a methodology contract rather than an executable split manifest."})
    if candidate is not None:
        candidate_extensions = candidate.get('extensions', {})
        candidate_status = candidate_extensions.get('research_dataset_status', 'unknown')
        blockers.append({'gate': 'candidate_dataset_lineage', 'status': 'blocked', 'detail': f"Supplied OHLCV-like candidate is {candidate_status!r}; instrument, provider, rights, adjustment basis, timezone, availability timestamps, and outcome labels are not established."})
    else:
        blockers.append({'gate': 'candidate_dataset_presence', 'status': 'blocked', 'detail': 'No tabular candidate record was found in the integrated corpus.'})

    started = datetime.now(timezone.utc)
    result = {
        'schema_version': '1.0.0',
        'run_id': f"wf-readiness-{started.strftime('%Y%m%dT%H%M%SZ')}",
        'run_type': 'walk_forward_pre_execution_gate',
        'is_walk_forward_validation_result': False,
        'execution_status': 'blocked_pre_execution',
        'run_started_at': started.isoformat(),
        'run_finished_at': datetime.now(timezone.utc).isoformat(),
        'experiment_id': None,
        'dataset_manifest_hash': sha256(args.manifest),
        'walk_forward_plan_hash': sha256(args.plan),
        'candidate_material_hash': sha256(args.candidate_material),
        'source_inventory_hash': None,
        'feature_dictionary_hash': None,
        'label_dictionary_hash': None,
        'split_manifest_hash': None,
        'code_version': 'local_contract_gate_only',
        'environment_lock_or_dependency_versions': 'not_applicable_no_model_execution',
        'random_seed': None,
        'observation_count_before_exclusions': 0,
        'observation_count_after_exclusions': 0,
        'exclusion_reasons': ['No eligible observations were acquired; no rows were admitted to validation.'],
        'missingness_summary': {'status': 'not_computed_no_eligible_observation_dataset'},
        'leakage_audit_summary': {
            'status': 'not_run_no_rows',
            'feature_cutoff_audit': 'not_run',
            'outcome_separation_audit': 'not_run',
            'purge_embargo_audit': 'not_run',
            'final_holdout_audit': 'not_run',
        },
        'folds': [],
        'baseline_results': {'status': 'not_run'},
        'candidate_results': {'status': 'not_run'},
        'uncertainty_method': 'not_run',
        'regime_results': {'status': 'not_run'},
        'negative_or_null_results': {'status': 'not_applicable_validation_not_executed'},
        'blockers': blockers,
        'required_next_step_ids': ['wf-01', 'wf-02', 'wf-03', 'wf-04', 'wf-05', 'wf-06'],
        'limitations': [
            'This is a pre-execution gate record, not a backtest, fold log, model result, or performance report.',
            'No synthetic observations, labels, folds, metrics, baselines, or statistical claims were created.',
            'Financial and market materials remain methodology-bound and research-only.',
        ],
        'prohibited_use_notice': 'This record is not a trading instruction, position-sizing rule, personal financial recommendation, guaranteed forecast, or causal claim.',
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'execution_status': result['execution_status'], 'blocker_count': len(blockers), 'output': str(args.output)}, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
