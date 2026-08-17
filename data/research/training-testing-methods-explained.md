# Training and Testing Methods: Detailed Specification Review

## Scope and boundary

The file `training_testing_methods.json` is a **methodology-bound research contract**, not a record of completed backtests or validated trading performance. Its twelve methods form a controlled lifecycle: register a study, acquire and preserve eligible data, define features and labels, prevent temporal leakage, run time-aware evaluation, report uncertainty, and then decide whether any narrowly scoped research signal or indicator is eligible for independent review.

> Financial and market materials remain **research-only**. The contract prohibits trading instructions, position sizing, personal financial advice, guaranteed forecasts, and causal claims from symbolic associations. A later promotion to a research-exploratory signal or indicator would not remove those prohibitions.

## Summary map

| No. | Method ID | Primary role | Required for promotion? |
|---:|---|---|---|
| 1 | `hypothesis_registration` | Lock the question and decision rule before analysis. | Yes |
| 2 | `observation_acquisition_and_lineage` | Preserve rights, raw inputs, hashes, and provider metadata. | Yes |
| 3 | `feature_dictionary_and_availability_mapping` | Make every feature auditable at its historical cutoff. | Yes |
| 4 | `independent_label_construction` | Build outcomes after the cutoff without tautology. | Yes |
| 5 | `walk_forward_time_split` | Test future periods using chronological folds. | Yes |
| 6 | `purged_time_split_and_embargo` | Remove overlapping outcome information between folds. | When outcome windows overlap |
| 7 | `fold_local_preprocessing` | Prevent validation or holdout information entering preparation. | Yes |
| 8 | `baseline_and_ablation_comparison` | Compare candidate effects with simpler explanations. | Yes |
| 9 | `uncertainty_and_regime_reporting` | Report instability, missingness, and negative results. | Yes |
| 10 | `data_revision_and_survivorship_audit` | Detect historical-vintage and sample-selection bias. | Yes |
| 11 | `validation_gated_signal_indicator_promotion` | Apply an independent, non-automatic promotion decision. | Governing method |
| 12 | `sentiment_as_feature_family` | Govern sentiment proxies as time-stamped source inputs. | Requires separate validation |

## 1. Hypothesis registration

`hypothesis_registration` is the research-governance entry point. It requires a falsifiable research question, a null hypothesis, population, row grain, observation window, feature family, independent target, baseline, metric, split design, decision rule, and prohibited uses before feature engineering or model selection begins.

Its purpose is to distinguish a confirmatory test from retrospective pattern search. A timestamped, immutable experiment identifier prevents the research question from being silently changed after outcomes are visible. The method fails if the null is missing, the target window is undefined, the feature family was not registered, or the question has been shaped around a known outcome. Its output is a versioned experiment record and an explicit approval or rejection record.

## 2. Observation acquisition and lineage

`observation_acquisition_and_lineage` establishes whether a real dataset is eligible to enter research. It requires a source decision record, rights status, a historical universe definition, and a raw response or file. It produces a source inventory, raw-artifact manifest, content hashes, and a normalized-dataset lineage.

The controls are deliberately broader than simple downloading. The source must have an allowed research use, raw content must be preserved before transformation, provider schema drift must be profiled, and the provider’s price-adjustment and data-revision policies must be captured. The method fails when rights are unresolved, raw hashes are absent, timestamp basis is unknown, or adjusted-versus-unadjusted price treatment is unknown.

## 3. Feature dictionary and availability mapping

`feature_dictionary_and_availability_mapping` makes each input independently auditable. A feature must receive a stable ID, definition, source or deterministic calculation, unit, type, source IDs, `available_at` boundary, version, missing-value policy, and transformation metadata. It uses normalized observations, calculation requests, and source availability timestamps to create a feature dictionary, a feature version, and an availability map.

The control set retains raw values, records circular encodings separately from angular values, retains deterministic astrology settings, and represents missingness with reason codes. A feature cannot be used when it lacks an availability timestamp, uses a derived calculation without recorded engine settings, or silently blends semantic traditions. This method is what lets the system test the statement: “Could this exact value have been known at the row’s feature cutoff?”

## 4. Independent label construction

`independent_label_construction` defines outcomes separately from candidate features. It takes a feature cutoff, a declared censor gap, an outcome source, and a label definition; it produces a versioned label dictionary, label-quality report, and outcome-window records.

The target must begin after the cutoff plus the censor gap. The coding rule must be independent of the feature being tested, ambiguity must be handled explicitly, and historical data revisions must be evaluated using their actual availability. The method rejects a row if its outcome overlaps the cutoff, if the label merely restates a candidate feature, or if a later revised label is treated as historically available. This avoids both target leakage and tautology.

## 5. Walk-forward time split

`walk_forward_time_split` is the central temporal evaluation method. It uses a frozen dataset, a pre-registered split configuration, a feature-cutoff audit, and baseline definitions. It produces a split manifest, fold logs, an aggregate validation log, and a final-holdout record.

The method builds either expanding or rolling training windows, each followed by a contiguous future validation window. It requires chronological boundaries, fold-local preprocessing, fold-level metrics, negative-result reporting, and a later untouched final holdout. It fails if validation data enter training transformations, future windows enter training, or the final holdout is reused for candidate selection. In other words, this is the method that asks whether a fully specified procedure generalizes to future periods rather than merely fitting the past.

## 6. Purged time split and embargo

`purged_time_split_and_embargo` is applied where row outcomes overlap, events are serially dependent, or publication delays can transfer outcome information across folds. It takes outcome-window boundaries, entity IDs, fold definition, and an embargo policy. It produces row IDs removed from training, embargo boundaries, and an updated split manifest.

The controls calculate overlap explicitly, record purge counts, record embargo duration, and preserve the remaining row count. The method fails if overlapping targets remain in both train and validation sets or if an embargo is needed but undocumented. A simple chronological split is not enough when a training row’s outcome window extends into a validation period.

## 7. Fold-local preprocessing

`fold_local_preprocessing` prevents leakage introduced by data preparation rather than by raw timestamps. Scaling, imputation, feature selection, encoding, resampling, and hyperparameter tuning must be fitted inside each training fold and only then applied to that fold’s validation data.

The inputs are training and validation row IDs and the preprocessing configuration. The outputs are a fold-pipeline record, hashes for transformation artifacts, and a fit-scope audit. Controls require fit row IDs, transform versions, a random seed where applicable, and no global pre-split fit. The method fails if an imputer or scaler saw validation values during fitting or if feature selection uses the final holdout.

## 8. Baseline and ablation comparison

`baseline_and_ablation_comparison` requires every candidate to compete against a predeclared simpler explanation. At minimum, this includes a naive market or buy-and-hold baseline; a seasonal or regime baseline when applicable; and a feature-ablated comparator when astrology or sentiment features are included.

The method uses pre-registered baselines, a candidate specification, and the same folds. It produces baseline fold metrics, an ablation comparison, and a metric delta with uncertainty. The key controls require the same split manifest, target definition, metric, and a ban on replacing the baseline after results are known. It fails when a candidate is reported with no baseline or when baseline and candidate use different fold structures.

## 9. Uncertainty and regime reporting

`uncertainty_and_regime_reporting` controls how results are described rather than how a model is fit. It requires fold metrics, data-quality reports, predeclared regime definitions, and an uncertainty procedure. It produces an uncertainty report, a regime report, and an explicit negative-results section.

The method requires sample counts, exclusions, target distribution or class balance, missingness, fold dispersion, confidence or bootstrap intervals, provider drift, regime sensitivity, and null or unstable results. Regime rules must be predeclared and include sample count; reporting only a favorable subset of folds is a failure. This method makes performance claims conditional on the actual uncertainty and historical context.

## 10. Data revision and survivorship audit

`data_revision_and_survivorship_audit` addresses two risks that remain even when timestamps are correctly ordered. First, a provider may revise, restate, or backfill historical values. Second, a present-day universe may omit delisted, acquired, or suspended instruments that were part of the historical population.

Its inputs are the provider revision policy, availability snapshots, a historical universe file, and an exclusion log. It produces revision and survivorship audits plus a limitations register. The controls preserve vintage timestamps, historical membership dates, adjustment basis, and exclusions. The method fails if present-day survivors are assumed to represent the original population or if revised values are treated as known earlier than they were.

## 11. Validation-gated signal or indicator promotion

`validation_gated_signal_indicator_promotion` is a governance method, not a model. It determines whether a methodology-bound material may be registered as a narrowly scoped `research_exploratory` signal or indicator. Inputs are a completed research package and promotion-review record; outputs are an approved, inconclusive, or rejected promotion decision.

Promotion requires reproducible pre-registration, resolved data rights, a leakage-safe walk-forward evaluation, an untouched final holdout, uncertainty reporting, and independent review. The result must retain a defined scope and permanently non-advisory wording. The method rejects source prose alone as evidence, rejects a result without a final holdout, and rejects a package with any unresolved critical leakage violation. Approval does not create a trading or causal claim.

## 12. Sentiment as a feature family

`sentiment_as_feature_family` governs news, analyst-recommendation, holder, and related sentiment proxies. It is marked `pending_review`, reflecting that source-specific rights, timing, revisions, and historical availability require particular care. It treats sentiment as a timestamped data feature, not a direct instruction.

It requires a source decision record, `available_at`, feature cutoff, and missingness policy, and produces only feature records with availability metadata. It requires source licensing, historical availability, a feature cutoff, a missingness policy, and provider revision treatment. It fails if historical availability cannot be established. Any later use also requires the same independently registered validation pathway as another candidate feature family.

## How the methods work together

The proper order is: register the hypothesis; acquire and preserve sources; map feature availability; construct independent labels; freeze the dataset; apply feature-cutoff and temporal-leakage checks; materialize walk-forward folds with purge and embargo where required; fit preprocessing and models within folds; compare baselines; report uncertainty and data-quality limits; evaluate a final holdout once; and submit the complete record for independent promotion review.

At present, the repository contains this methodology contract but no acquired observations, labels, split manifest, fold logs, baseline metrics, candidate metrics, or holdout results. Therefore, none of the methods has generated empirical performance evidence, and the correct status remains `configuration_and_method_records_only`.

## References

1. `data/research/training_testing_methods.json`
2. `data/unified/research_contract.json`
3. `data/research/temporal_leakage_controls.json`
4. `data/research/walk_forward_validation_plan.json`
5. `data/research/signal_indicator_promotion_policy.json`
