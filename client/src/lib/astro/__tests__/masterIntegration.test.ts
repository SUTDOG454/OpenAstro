import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';

function readJson<T>(relativePath: string): T {
  return JSON.parse(readFileSync(resolve(process.cwd(), relativePath), 'utf8')) as T;
}

describe('unified astrology master integration', () => {
  it('declares the ontology evidence classes and retrieval protocol', () => {
    const master = readJson<any>('../data/unified/unified_astrology_master.json');
    expect(master.delineation_ontology.evidence_classes).toEqual(expect.arrayContaining(['source_derived', 'computed', 'methodology_bound', 'research_exploratory']));
    expect(master.delineation_ontology.retrieval_protocol.steps).toContain('separate observation from meaning');
    expect(master.canonical_registry_boundary.policy).toMatch(/Do not fork canonical registries/);
  });

  it('integrates an isolated esoteric namespace with no calculation engine', () => {
    const master = readJson<any>('../data/unified/unified_astrology_master.json');
    expect(master.esoteric_retrieval_namespace.tradition_mode).toBe('esoteric');
    expect(master.esoteric_retrieval_namespace.calculation_engine).toBe('none');
    expect(master.esoteric_retrieval_namespace.rejected_modes).toEqual(expect.arrayContaining(['western', 'vedic', 'standard']));
    expect(master.esoteric_retrieval_namespace.policy).toMatch(/never injected into standard Western or Vedic/);
  });

  it('integrates the research layer with a research-only financial and market boundary', () => {
    const master = readJson<any>('../data/unified/unified_astrology_master.json');
    const manifest = readJson<any>('../data/research/research_dataset_manifest.json');
    const contract = readJson<any>('../data/unified/research_contract.json');

    expect(master.research_layer.evidence_class).toBe('methodology_bound');
    expect(master.research_layer.observations_acquired).toBe(false);
    expect(master.research_layer.labels_acquired).toBe(false);
    expect(master.research_layer.execution_status).toBe('not_executed');
    expect(master.research_layer.walk_forward_validation_status).toBe('not_executed_requires_observations_and_labels');
    expect(master.research_layer.counts.economic_indicators).toBeGreaterThan(0);
    expect(master.research_layer.counts.training_testing_methods).toBeGreaterThanOrEqual(12);
    expect(master.research_layer.counts.contract_artifacts).toBe(5);
    expect(manifest.feature_cutoff_rule).toMatch(/feature cutoff/i);
    expect(manifest.split_strategy).toMatch(/walk_forward|purged/i);
    expect(manifest.blocking_conditions.length).toBeGreaterThanOrEqual(5);
    expect(manifest.prohibited_uses).toEqual(expect.arrayContaining(['trading instructions', 'position sizing', 'personal financial advice', 'guaranteed forecasts', 'causal claims from symbolic associations']));
    expect(contract.evidence_boundary.financial_and_market_materials).toBe('methodology_bound_research_only');
    expect(contract.evidence_boundary.default_promotion_status).toBe('not_eligible_without_validated_experiment');
  });

  it('requires detailed availability, outcome separation, fold-local, purge, and holdout controls', () => {
    const controls = readJson<any>('../data/research/temporal_leakage_controls.json');
    const controlIds = controls.contract.core_invariants.map((control: { control_id: string }) => control.control_id);
    const runtimeCodes = controls.contract.validator_alignment.implemented_error_codes;

    expect(controlIds).toEqual(expect.arrayContaining([
      'leak-01-availability',
      'leak-02-outcome-separation',
      'leak-04-fold-local-preprocessing',
      'leak-05-overlap-purge-and-embargo',
      'leak-06-final-holdout',
      'leak-07-data-revisions',
      'leak-08-survivorship-and-selection',
    ]));
    expect(runtimeCodes).toEqual(expect.arrayContaining(['FEATURE_AFTER_CUTOFF', 'INVALID_TIMESTAMP', 'OUTCOME_OVERLAP']));
    expect(controls.contract.validator_alignment.additional_execution_audits_required).toEqual(expect.arrayContaining(['fold_local_preprocessing', 'purge_and_embargo', 'final_holdout_isolation']));
  });

  it('defines a blocked first walk-forward execution and a non-automatic promotion gate', () => {
    const plan = readJson<any>('../data/research/walk_forward_validation_plan.json');
    const promotion = readJson<any>('../data/research/signal_indicator_promotion_policy.json');

    expect(plan.status).toBe('not_executed_requires_observations_and_labels');
    expect(plan.contract.eligible_dataset_conditions).toEqual(expect.arrayContaining(['observations_acquired is true', 'labels_acquired is true']));
    expect(plan.contract.first_execution_steps.map((step: { step_id: string }) => step.step_id)).toEqual(expect.arrayContaining(['wf-01', 'wf-06', 'wf-07', 'wf-10', 'wf-11', 'wf-12']));
    expect(plan.contract.required_execution_log_fields).toEqual(expect.arrayContaining(['dataset_manifest_hash', 'split_manifest_hash', 'leakage_audit_summary', 'baseline_results', 'negative_or_null_results']));
    expect(promotion.status).toBe('review_gated_not_automatic');
    expect(promotion.contract.minimum_requirements).toEqual(expect.arrayContaining(['one untouched final holdout evaluation', 'independent human review']));
    expect(promotion.contract.non_qualifying_evidence).toEqual(expect.arrayContaining(['source prose alone', 'in-sample performance', 'a result without a baseline']));
  });
});
