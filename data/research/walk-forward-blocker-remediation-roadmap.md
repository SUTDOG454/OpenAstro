# Walk-Forward Validation Blocker Remediation Roadmap

## Purpose and Current State

The pre-execution validator recorded six blockers in `walk_forward_validation_blocked_run.json`. This roadmap describes the minimum remediation sequence required to move from a methodology-only research layer to an execution-eligible, leakage-safe walk-forward study. It does not authorize a backtest, create a market signal, or change the research-only status of financial or symbolic material.

> **Control principle:** A real run may begin only after actual observations, independently defined labels, source rights, frozen artifacts, a feature-cutoff audit, pre-registered baselines, and chronological split definitions are all available. No synthetic rows, placeholder labels, inferred provider metadata, or fabricated fold results may be used to clear a gate.

## Blocker-to-Remediation Map

| Blocker | Why it blocks execution | Required remediation | Evidence that clears the gate | Stop condition |
|---|---|---|---|---|
| `observations_acquired` | No approved, normalized time-indexed observations are registered. | Register an experiment and universe; retrieve actual historical data from approved sources; preserve immutable raw responses and normalize the rows. | Raw source inventory, SHA-256 hashes, schema snapshots, normalized dataset, timestamp-coverage and data-quality reports. | Stop if the source, universe, timestamps, adjustment basis, or raw artifacts are unavailable. |
| `labels_acquired` | No independently constructed outcomes exist after feature cutoffs. | Define a target before inspecting candidate performance; construct labels from a separate outcome source after cutoff plus a declared censor gap. | Label dictionary with outcome windows, source IDs, threshold/coding rule, label version, ambiguity policy, and validation report. | Stop if outcome windows overlap the feature cutoff, rely on revised future data, or restate a candidate feature. |
| `source_rights` | Observation sources have unresolved use rights. | Create a source decision record for every provider and dataset; record the licensed or permitted research use. | Provider, endpoint/dataset, locator, license or terms reference, retrieval time, coverage, frequency, timezone, adjustment basis, revision policy, and `rights_status: resolved`. | Exclude any source with unresolved rights, unverifiable timing, or an unknown adjustment basis. |
| `execution_status` | The active manifest is `not_executed`, not execution-ready. | Do not edit the status directly. Complete the acquisition, feature, label, freeze, and audit artifacts first, then regenerate the manifest from their real evidence. | A versioned manifest whose fields point to frozen artifacts and whose validation checks show all prerequisites met. | The status must remain blocked if any upstream artifact is absent, mutable, or unverified. |
| `walk_forward_plan_status` | The current plan defines methodology, not a materialized split manifest. | Pre-register observation and final-holdout dates, training window, validation window, step size, purge policy, embargo policy, baselines, metric, and decision rule; then materialize the folds from the frozen dataset. | `split_manifest.json` with chronological fold boundaries, row counts, purged/embargoed rows, holdout boundary, and hashes. | Stop if folds cannot be created chronologically or if the final holdout has been inspected during model selection. |
| `candidate_dataset_lineage` | The supplied 33-row OHLCV-like CSV has no established instrument identity, provider, rights, adjustment basis, timezone, availability timestamps, or labels. | Treat it as a source sample only. Identify the instrument and exchange, trace a provider and permitted-use terms, establish adjusted/unadjusted convention and timezone, acquire sufficient historical coverage, and construct post-cutoff labels. | Entity card, source decision record, raw data hash, coverage summary, row-level availability metadata, adjustment/revision policy, and independent label artifact. | Do not use the CSV as a study dataset if its identity or historical lineage cannot be recovered. |

## Required Order of Work

### 1. Register the study before acquiring or engineering data

Create a versioned experiment record or hypothesis card. It must name the research question and null hypothesis, population, unit of analysis, observation window, feature cutoff, target definition and window, candidate feature families, exclusions, baseline, metric, split strategy, decision rule, and prohibited uses. This prevents outcome-shaped hypotheses and makes the later decision rule auditable.

### 2. Resolve the universe and data sources

Define the historical universe rather than using a present-day list by default. Record the instrument identifier, exchange or market, currency, historical-membership policy, delisting and corporate-action treatment, timezone, and trading calendar. Create a source decision record for each data provider before retrieval. The record must resolve the provider, dataset or endpoint, license/terms, coverage, frequency, adjustment basis, revision policy, and research-use permission.

### 3. Acquire and preserve actual observations

Acquire actual historical observations only after the first two steps are complete. Preserve immutable raw files or raw API responses, hashes, retrieval timestamps, parser versions, schema snapshots, and row counts. Normalize representational fields conservatively, retain source values, identify duplicate and missing rows, document timestamp gaps, and record data-quality warnings. Do not use the supplied 33-row CSV unless its identity and lineage can be independently established.

### 4. Build deterministic, time-safe feature data

Create a feature dictionary before modeling. For every feature, record its source IDs, calculation or extraction method, availability timestamp, feature cutoff relation, missingness rule, and version. Any astrological calculation must also record the engine and version, ephemeris/data version, coordinate frame, zodiac mode, house system where applicable, ayanamsa where applicable, aspect/orb policy where applicable, and time-interpretation policy. Unsupported calculations remain unavailable rather than approximated.

### 5. Construct independent labels

Build labels from outcome data that begins strictly after each row’s feature cutoff plus a declared censor gap. Store the label ID, definition, outcome-source ID, start/end windows, censor gap, threshold or coding rule, label version, and ambiguity policy. The label must not encode future information available only after the forecast cutoff or restate the candidate feature family.

### 6. Freeze and audit the dataset

Before any split, produce and hash the dataset manifest, data card, feature dictionary, label dictionary, source inventory, and validation report. Run the feature-cutoff check for every row; record exclusions rather than silently dropping failures. Confirm timezone/calendar integrity, outcome separation, revision-vintage policy, survivorship/selection policy, and the rule that imputation is fitted only within training folds.

### 7. Materialize the walk-forward split manifest

Select the pre-registered expanding or rolling family. Materialize contiguous chronological folds with explicit train, purge, embargo, validation, and final-holdout boundaries. The final holdout must be later than all model-selection activity and remain untouched until candidate selection is finished. Each fold must record train/validation row counts, purged rows, feature-cutoff audit, preprocessing scope, baseline metrics, candidate metrics, metric definition, uncertainty interval, regime tags, and warnings.

### 8. Execute only the registered experiment

Inside each fold, fit naive and feature-ablated baselines separately from the declared candidate. Fit preprocessing only on training rows. Do not retune against validation outcomes. Aggregate all fold results—including failures, instability, missingness, and null findings—according to the pre-registered decision rule. Evaluate the final holdout once, only after selection is complete.

### 9. Review before any promotion

A completed run must create the full evidence package: aggregate validation log, fold logs, baseline comparisons, uncertainty method, regime analysis, negative results, final-holdout result, experiment record, and model card. Independent review must then decide whether any item remains methodology-bound, becomes a scoped research-exploratory signal, or is rejected. No outcome authorizes trading instructions, position sizing, personal financial advice, guaranteed forecasts, or causal claims.

## Minimum Artifact Checklist

| Stage | Required artifacts |
|---|---|
| Study registration | `experiment_record.json`, hypothesis card, universe definition, source-decision records |
| Data acquisition | Raw source inventory, immutable raw artifacts, hashes, schema snapshots, normalized observation dataset, data-quality report |
| Feature and label build | Feature dictionary, calculation provenance, label dictionary, label-validation report, row-level availability metadata |
| Freeze and audit | Frozen dataset manifest, data card, source inventory, feature-cutoff audit, temporal-leakage audit, validation report |
| Split and evaluation | `split_manifest.json`, fold logs, baseline results, candidate results, uncertainty/regime/negative-result reports |
| Final review | Final-holdout evaluation, model card, promotion review record, decision rationale |

## Readiness Decision Rule

The existing validator should remain a pre-execution gate until every requirement below is true:

1. `observations_acquired` and `labels_acquired` are true because evidence artifacts exist, not because a status field was edited.
2. All sources have resolved rights and reproducible raw provenance.
3. Every row has an approved feature cutoff, availability timezone, source IDs, outcome window, and label version.
4. The data, dictionaries, source inventory, and manifest are frozen and hashed.
5. The feature-cutoff and temporal-leakage audits have no unresolved violation.
6. A pre-registered split manifest, baselines, metric, decision rule, and untouched final holdout exist.

## References

[1] [Blocked pre-execution run record](walk_forward_validation_blocked_run.json)  
[2] [Observation acquisition plan](observation_acquisition_plan.json)  
[3] [Walk-forward validation plan](walk_forward_validation_plan.json)  
[4] [Temporal leakage controls](temporal_leakage_controls.json)  
[5] [Signal and indicator promotion policy](signal_indicator_promotion_policy.json)
