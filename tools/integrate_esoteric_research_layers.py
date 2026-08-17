from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/home/ubuntu/openastro_worktree')
master_path = ROOT / 'data/unified/unified_astrology_master.json'
master = json.loads(master_path.read_text())
summary = json.loads((ROOT / 'data/research/research_layer_summary.json').read_text())
research_contract = json.loads((ROOT / 'data/unified/research_contract.json').read_text())

master['status'] = 'expanded_with_isolated_esoteric_and_research_layer'
master['research_contract'] = research_contract
master['esoteric_retrieval_namespace'] = {
    'status': 'isolated_source_retrieval',
    'tradition_mode': 'esoteric',
    'typescript_module': 'client/src/lib/astro/delineation/esotericNamespace.ts',
    'corpus_loader': 'client/src/lib/astro/delineation/esotericCorpus.ts',
    'calculation_engine': 'none',
    'allowed_engine': 'esoteric_retrieval_only',
    'rejected_modes': ['western', 'vedic', 'standard'],
    'source_refs': ['data/interpretation-indicators/normalized_interpretation_indicators.json', 'gw4yP30qoqPeIhTA3L9cO0'],
    'policy': 'Esoteric records are retrieved only when tradition_mode is explicitly esoteric and are never injected into standard Western or Vedic calculation engines.',
}
master['research_layer'] = {
    'status': summary['status'],
    'evidence_class': 'methodology_bound',
    'evidence_boundary': summary['evidence_boundary'],
    'economic_indicators_ref': 'data/research/economic_indicators.json',
    'training_testing_methods_ref': 'data/research/training_testing_methods.json',
    'market_sentiment_and_strategies_ref': 'data/research/market_sentiment_and_strategies.json',
    'observation_acquisition_plan_ref': 'data/research/observation_acquisition_plan.json',
    'temporal_leakage_controls_ref': 'data/research/temporal_leakage_controls.json',
    'walk_forward_validation_plan_ref': 'data/research/walk_forward_validation_plan.json',
    'signal_indicator_promotion_policy_ref': 'data/research/signal_indicator_promotion_policy.json',
    'manifest_ref': 'data/research/research_dataset_manifest.json',
    'summary_ref': 'data/research/research_layer_summary.json',
    'upstream_research_contract_ref': 'data/unified/research_contract.json',
    'counts': {
        'economic_indicators': summary['economic_indicator_count'],
        'training_testing_methods': summary['method_count'],
        'strategy_or_sentiment_text': summary['strategy_or_sentiment_text_count'],
        'contract_artifacts': summary['contract_artifact_count'],
    },
    'observations_acquired': summary['observations_acquired'],
    'labels_acquired': summary['labels_acquired'],
    'execution_status': summary['execution_status'],
    'walk_forward_validation_status': summary['walk_forward_validation_status'],
    'execution_readiness': summary['execution_readiness'],
    'promotion_policy': {
        'status': research_contract['signal_indicator_promotion_contract']['status'],
        'default_evidence_class': research_contract['signal_indicator_promotion_contract']['default_evidence_class'],
        'promotion_target': research_contract['signal_indicator_promotion_contract']['promotion_target'],
        'policy_ref': 'data/research/signal_indicator_promotion_policy.json',
    },
    'policy': 'Configuration and methodology records only. Financial and market materials remain methodology-bound and research-only; promotion to a scoped research-exploratory signal or indicator requires the separately documented leakage-safe validation and review gate. No synthetic observations, validated strategy performance, trading instructions, position sizing, personal financial advice, guaranteed forecasts, or causal claims are produced.',
}
master.setdefault('implementation_notes', {})['esoteric_namespace_isolation'] = 'TypeScript retrieval-only namespace; no Western, Vedic, or standard calculation engine calls.'
master['implementation_notes']['research_layer'] = 'Expanded research contracts under data/research define acquisition gates, feature cutoff and temporal-leakage controls, walk-forward execution requirements, required execution logs, and review-gated research signal or indicator promotion. The active layer contains no observations, labels, or executed validation results.'
master['generated_at'] = datetime.now(timezone.utc).isoformat()
master_path.write_text(json.dumps(master, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({
    'status': master['status'],
    'research_counts': master['research_layer']['counts'],
    'walk_forward_validation_status': master['research_layer']['walk_forward_validation_status'],
}, indent=2))
