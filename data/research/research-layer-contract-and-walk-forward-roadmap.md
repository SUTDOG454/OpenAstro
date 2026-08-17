# Research-Layer Contract and First Walk-Forward Validation Roadmap

**Status:** Methodology-bound research design; no observations, labels, model fits, backtests, or validation results are present.

## 1. Purpose and evidence boundary

The research layer defines a reproducible framework for investigating time-indexed financial or market associations with explicitly versioned astrological, economic, company, and sentiment features. It does not claim that an association exists, that a methodology predicts an outcome, or that a feature should be used to make a financial decision.

> Financial and market materials remain **methodology-bound and research-only**. They may be considered for registration only as a narrowly scoped `research_exploratory` signal or indicator after a separately documented, reproducible, leakage-safe experiment completes the promotion gate. The result still cannot constitute trading instruction, position sizing, personal financial advice, a guaranteed forecast, or a causal claim from a symbolic association.

| Evidence class | Permitted role in this layer | Not permitted |
|---|---|---|
| `source_derived` | Preserve source text and input definitions with source IDs and rights metadata. | Treat prose as validated performance. |
| `methodology_bound` | Define hypotheses, datasets, acquisition rules, calculations, split procedures, baselines, and leakage controls. | Claim empirical support before execution. |
| `research_exploratory` | Record a reviewed, scoped result only after the promotion gate has been completed. | Present a result as universal, causal, or advisory. |
| `unavailable` / `pending_review` | Preserve missing data, unresolved rights, unsupported calculations, or incomplete evidence. | Replace missing evidence with a plausible claim. |

## 2. Current research-layer inventory

| Artifact | Role | Current status |
|---|---|---|
| `data/unified/research_contract.json` | Authoritative contract for evidence boundaries, acquisition, temporal controls, walk-forward execution, and promotion. | Complete methodology contract; version 1.1.0. |
| `data/research/training_testing_methods.json` | Twelve detailed methodology records with inputs, outputs, controls, and failure conditions. | Methodology-bound. |
| `data/research/observation_acquisition_plan.json` | Eight acquisition gates and row-level contract. | Not started; no observations acquired. |
| `data/research/temporal_leakage_controls.json` | Eight temporal controls and runtime-validator alignment. | Required before evaluation. |
| `data/research/walk_forward_validation_plan.json` | Dataset eligibility conditions, 12 execution steps, and required log schemas. | Not executed; requires observations and labels. |
| `data/research/signal_indicator_promotion_policy.json` | Review-gated promotion rules and non-qualifying evidence. | Not automatic. |
| `data/research/research_dataset_manifest.json` | Active dataset state, blockers, references, and execution prerequisites. | `configuration_and_method_records_only`. |

## 3. Observation acquisition: required sequence

The first executable experiment begins only after the following eight gates have records. Each gate must be retained as an artifact with its timestamp, source references, and content hash where applicable.

| Gate | Required action | Required evidence | Stop condition |
|---|---|---|---|
| `acq-01` | Register the hypothesis. | Research question, null, population, unit, windows, candidate features, target, baseline, metric, split, decision rule. | No registered hypothesis or outcome-shaped question. |
| `acq-02` | Resolve the historical universe. | Instrument IDs, exchange, currency, membership rule, delisting policy, timezone, and calendar. | Present-day constituents silently stand in for history. |
| `acq-03` | Choose sources and resolve rights. | Provider, endpoint, URL/locator, license/terms, retrieval time, coverage, timezone, adjustment and revision policy. | Rights, timing, or adjustment basis cannot be established. |
| `acq-04` | Preserve raw data. | Immutable raw artifact path, SHA-256 hash, parser version, schema snapshot, and row count. | Raw source or hash is missing. |
| `acq-05` | Normalize and profile data. | Field mapping, duplicate policy, missingness, coverage, schema-drift and quality reports. | Silent deduplication, undocumented imputation, or absent availability timestamps. |
| `acq-06` | Compute deterministic astrology features. | Engine/version, ephemeris, timezone, coordinate frame, zodiac, house system/ayanamsa/orbs if relevant. | Unsupported factor is approximated or traditions are silently blended. |
| `acq-07` | Build independent labels. | Outcome source, start/end, censor gap, rule, label version, ambiguity handling. | Label begins at/before cutoff or is a restated candidate feature. |
| `acq-08` | Freeze the research package. | Manifest hash, data card, feature and label dictionaries, source inventory, validation report. | Dataset is tuned or evaluated without a frozen version. |

Every observation row must include `row_id`, `entity_id`, `observation_timestamp`, `feature_cutoff`, `availability_timezone`, `feature_set_version`, `source_ids`, `outcome_window_start`, `outcome_window_end`, `label_version`, and `data_quality_status`.

## 4. Leakage-control contract

A feature cutoff is necessary but not sufficient. The complete contract contains eight controls.

| Control | Required test | Failure action |
|---|---|---|
| Availability | `available_at <= feature_cutoff` for every feature value. | Exclude the feature-row value and record `FEATURE_AFTER_CUTOFF`. |
| Outcome separation | Outcome begins after cutoff plus the declared censor gap. | Exclude the row and record `OUTCOME_OVERLAP`. |
| Timezone and calendar | Parse timezone-aware timestamps against declared exchange calendar and market-close convention. | Block temporally ambiguous rows. |
| Fold-local preprocessing | Fit imputation, scaling, selection, encoding, resampling, and tuning on training rows only. | Invalidate the fold. |
| Purge and embargo | Remove overlapping target windows and apply an explicit gap where dependence or publication lag requires it. | Regenerate the split. |
| Final-holdout isolation | Reserve a later chronological interval before candidate selection. | Reclassify as exploratory and register a new confirmatory holdout. |
| Data revisions | Use the historically available value/vintage, not a later revised value. | Exclude or mark unavailable at that cutoff. |
| Survivorship and selection | Record historical membership, delistings, suspensions, and exclusions. | Limit claims to the observed survivor sample and disclose risk. |

The runtime validator in `client/src/lib/astro/research/featureCutoff.ts` currently enforces invalid timestamps, feature availability after cutoff, and outcome overlap. Fold-local preprocessing, purge/embargo, final-holdout isolation, revision-vintage, and survivorship controls are explicitly required in the execution audit and have not yet been run because no real rows exist.

## 5. First walk-forward validation: execution sequence

After acquisition and freezing, execute the following pre-registered sequence. No fold, baseline, threshold, or feature family should be selected because it produces a favorable outcome.

| Step | Action | Required output |
|---|---|---|
| `wf-01` | Approve/reject the experiment record and rights inventory. | Approval or rejection record. |
| `wf-02` | Acquire actual time-indexed observations and preserve raw inputs. | Source inventory and hashes. |
| `wf-03` | Normalize and profile the rows; record all exclusions. | Normalized data and quality report. |
| `wf-04` | Compute deterministic features with recorded settings. | Feature dictionary and calculation provenance. |
| `wf-05` | Construct labels after cutoff plus censor gap. | Label dictionary and label audit. |
| `wf-06` | Freeze the dataset and run the leakage audit. | Frozen manifest and leakage report. |
| `wf-07` | Materialize chronological train/purge/embargo/validation/holdout boundaries. | `split_manifest.json`. |
| `wf-08` | Fit declared naive and feature-ablated baselines, then the pre-registered candidate, fold by fold. | Fold-local artifacts and baseline metrics. |
| `wf-09` | Evaluate without retuning on validation outcomes; include missingness and regime context. | Fold metrics and uncertainty report. |
| `wf-10` | Aggregate all folds, retaining null and unstable results. | `walk_forward_validation_log.json`. |
| `wf-11` | Use the final chronological holdout one time only, after selection. | Holdout record, experiment record, model card. |
| `wf-12` | Conduct independent promotion review. | Promotion review record. |

The default split family is an expanding-window walk-forward design. A rolling-window variant is permitted only when the training window is predeclared. Where outcome windows overlap, the train set must be purged and an embargo must be documented. A final chronological holdout must remain untouched until the candidate is fixed.

## 6. Required validation logs

A future run must create an aggregate log containing the run, experiment, data, feature, label, split, code, environment, and seed hashes; all row counts and exclusions; missingness; leakage-audit outcomes; baseline and candidate results; uncertainty procedure; regime results; negative/null findings; limitations; and a permanent prohibited-use notice.

Each fold must preserve its train, purge, embargo, and validation boundaries; row counts; cutoff audit; preprocessing fit scope; baseline and candidate metrics; metric definition; uncertainty interval; regime tags; and warnings. The absence of any required log item blocks promotion.

## 7. Validation-gated promotion

Promotion is never automatic. The proposal may be approved only if all conditions below are satisfied and independently reviewed.

| Required condition | Why it is necessary |
|---|---|
| Pre-registered hypothesis and null. | Avoid retrospectively tailored claims. |
| Resolved source rights and full lineage. | Preserve legal and reproducibility boundaries. |
| Frozen dataset plus hashes. | Identify the exact material evaluated. |
| No unresolved critical leakage violation. | Prevent future information from contaminating results. |
| Walk-forward folds with comparably evaluated baselines. | Test temporal generalization against simpler explanations. |
| One untouched final holdout. | Distinguish selection from final evaluation. |
| Null, negative, and unstable results retained. | Prevent selective reporting. |
| Regime and survivorship limitations. | Constrain external validity. |
| Independent human review. | Prevent self-approval of a research claim. |
| Scoped non-advisory wording. | Keep the result non-causal and non-prescriptive. |

Source prose, an unregistered backtest, a single favorable window, in-sample performance, a result without a baseline, and a result lacking historical availability or source-rights documentation are all explicitly non-qualifying evidence.

## 8. Current blockers and next operational action

The contract is ready, but an execution is blocked because there is no actual approved experiment record, no resolved provider rights, no raw observation source, no normalized rows, no independently built labels, no frozen manifest, no split manifest, and no validation log. The immediate next operation is therefore not a backtest: it is a research-design approval that fixes the population, historical window, source/provider and rights decision, row grain, deterministic feature settings, outcome definition, baseline, metrics, fold geometry, and final-holdout period.

Until those inputs exist, the correct system status remains `configuration_and_method_records_only` and `not_executed_requires_observations_and_labels`.

## 9. Validation results for this contract expansion

The generated contract was parsed successfully as JSON. The full TypeScript suite passed **29 tests across 5 files**, strict TypeScript type-checking passed, and the Python suite passed **45 tests**. These tests validate contract structure and integration only; they do not validate market performance because no observations or labels have been acquired.

## References

1. `data/unified/research_contract.json`
2. `data/research/research_dataset_manifest.json`
3. `data/research/temporal_leakage_controls.json`
4. `data/research/walk_forward_validation_plan.json`
5. `data/research/signal_indicator_promotion_policy.json`
6. `client/src/lib/astro/research/featureCutoff.ts`
