# Validation-Gated Signal or Indicator Promotion Criteria

## 1. Governing status

The promotion policy is **`review_gated_not_automatic`**. Financial and market material begins as `methodology_bound_research_only`, with a default status of `not_eligible_without_validated_experiment`. A source record, an interpretation text, a formula, a strategy description, or a model output does not become a research signal or indicator merely because it exists in the corpus.

> Promotion means only that a precisely scoped research result may be registered as `research_exploratory_scoped_signal_or_indicator`. It does **not** establish causality, guarantee predictive value, authorize a financial action, or supersede the prohibited-use boundary.

## 2. Evidence classes before and after review

| Stage | Evidence class or status | Meaning |
|---|---|---|
| Initial material | `source_derived` or `methodology_bound` | The source or method is preserved, but it has no validated performance claim. |
| Candidate under evaluation | `methodology_bound` / `pending_review` | An experiment is in design or execution; evidence is not yet eligible for signal registration. |
| Approved promotion | `research_exploratory_scoped_signal_or_indicator` | A review-approved, reproducible, bounded research record with full limitations. |
| Inconclusive result | `methodology_bound` or `pending_review` | The result was null, unstable, underpowered, or otherwise insufficient. |
| Rejected result | Source retained with rejection rationale | The material must not be exposed as a signal or indicator. |

## 3. Minimum promotion criteria

Every condition below is mandatory. A proposal does not pass through partial compliance or compensating strengths; for example, strong in-sample results cannot compensate for absent source rights or a missing final holdout.

| Criterion | Required evidence | Review question |
|---|---|---|
| Pre-registration | Versioned experiment record and explicit null hypothesis. | Was the research question, feature family, target, baseline, metric, split design, and decision rule registered before outcome-driven refinement? |
| Source rights and lineage | Source inventory, permitted-use status, raw artifact locations, retrieval timestamps, and hashes. | Is every included input traceable, permitted for the stated research use, and reproducible from preserved raw material? |
| Frozen dataset | Dataset manifest hash, source inventory hash, feature dictionary hash, label dictionary hash, and recorded code/environment versions. | Can a reviewer identify the exact data and transformations evaluated? |
| Clean leakage audit | Feature-cutoff report; outcome-window checks; timezone/calendar checks; preprocessing audit; purge/embargo audit; holdout-isolation audit; revision-vintage audit. | Did any feature, transform, label, or selection step receive information not available at the historical cutoff? |
| Walk-forward evidence | Split manifest and all fold logs, including baseline and candidate metrics. | Does the predeclared candidate generalize across chronological future windows rather than only fitting the past? |
| Baseline comparison | Naive/buy-and-hold or other predeclared simple comparator; feature ablation when astrology or sentiment inputs are used. | Is the candidate evaluated on the same folds, target, and metric as simpler non-astrological explanations? |
| Final holdout | One later chronological holdout, declared before selection and used only after candidate selection. | Was the final holdout completely untouched during feature discovery, tuning, threshold selection, and model selection? |
| Full-result reporting | Negative, null, unstable, and favorable results; sample counts; exclusions; missingness; fold dispersion; confidence/bootstrapped intervals. | Does the package disclose failures and uncertainty rather than preserving favorable outcomes only? |
| Regime and survivorship limitations | Predefined regime rules, per-regime sample counts, historical universe policy, membership/exclusion records, and delisting limitations. | Is the claimed scope limited to the actual historical population and market regimes observed? |
| Independent human review | Reviewer identity/role, review date, checklist outcome, conflicts disclosure, and decision rationale. | Did a reviewer independent of the result-generation process verify compliance and wording? |
| Scoped non-advisory language | Registered domain, feature version, label, metric, uncertainty, limitations, and permanent prohibited-use notice. | Does the description avoid causal, predictive-certainty, buy/sell, allocation, execution, or personalized-finance language? |

## 4. Required temporal-leakage review gates

The promotion reviewer must confirm each temporal gate, rather than relying only on an aggregate performance number.

| Gate | Minimum audit evidence | Critical failure |
|---|---|---|
| Feature availability | Each feature’s `available_at` is on or before its row’s `feature_cutoff`. | A future feature enters any evaluated row. |
| Outcome separation | Target starts after cutoff plus declared censor gap. | Outcome overlaps the feature window. |
| Timestamp semantics | Timezone-aware timestamps, declared trading calendar, and market-close convention. | Ambiguous or invalid temporal ordering. |
| Fold-local preprocessing | Scaling, imputation, selection, encoding, and tuning fit only on training rows. | Validation or holdout rows affect any fitted transform. |
| Purge and embargo | Overlapping target windows are purged; embargo is applied when required. | Train and validation share outcome information. |
| Final-holdout isolation | Holdout was reserved before selection and evaluated once. | Holdout was reused for feature/model/threshold selection. |
| Data-vintage control | Historical availability and revisions are documented. | A later restatement is treated as earlier knowledge. |
| Survivorship control | Universe construction, delistings, suspensions, and exclusions are disclosed. | Present-day survivors silently substitute for historical population. |

An unresolved **critical** violation blocks approval. The contract does not allow a reviewer to waive it on the strength of better metrics.

## 5. Evidence that cannot qualify a candidate

The following are expressly insufficient, even if they appear persuasive in isolation:

| Non-qualifying evidence | Why it fails |
|---|---|
| Source prose alone | Descriptive source material is not an empirical validation record. |
| Unregistered backtest | The design may have been altered after outcomes were visible. |
| Single favorable time window | It can represent selection bias or a regime-specific anomaly. |
| In-sample performance | It does not demonstrate temporal generalization. |
| Result without a baseline | It cannot show improvement over simpler explanations. |
| Unresolved availability timestamps | The historical information set cannot be audited. |
| Missing source-rights documentation | The data cannot be confirmed as permissible or reproducible. |

## 6. Independent review workflow

The required review is a sequence of decisions, not an informal sign-off.

| Gate | Reviewer action | Required outcome to continue |
|---:|---|---|
| 1 | Confirm the experiment is pre-registered and the null hypothesis is falsifiable. | Approved experiment scope. |
| 2 | Audit source inventory, rights, raw artifacts, hashes, and provider metadata. | Resolved lineage and permitted research use. |
| 3 | Audit feature/label dictionaries, availability timestamps, calculation settings, and missingness. | Reproducible and time-aligned inputs. |
| 4 | Review leakage report and split manifest, including purge, embargo, preprocessing, revision, and holdout controls. | No unresolved critical leakage violation. |
| 5 | Compare candidate, baseline, and ablation results across the same folds. | Comparable evaluation evidence. |
| 6 | Inspect uncertainty, negative results, regime stability, and survivorship limitations. | Full and bounded interpretation. |
| 7 | Confirm one untouched final-holdout evaluation and package hashes. | Final evaluation is genuinely held out. |
| 8 | Decide approval, inconclusive status, or rejection; record rationale and reviewer conflicts. | Durable review decision. |

## 7. Decision outcomes

### Approved

Approval registers the record as `research_exploratory_scoped_signal_or_indicator`. The record must contain a defined domain, feature version, label definition, evaluation metrics, uncertainty, limitations, source/data hashes, and the review decision. The following prohibited uses continue to apply: trading instructions, position sizing, personal financial advice, guaranteed forecasts, and causal claims from symbolic associations.

### Inconclusive

An inconclusive result remains `methodology_bound` or `pending_review`. The package must preserve and document null, unstable, underpowered, or regime-dependent results. A later study may be registered independently; it must not retroactively alter or erase the inconclusive record.

### Rejected

A rejected proposal retains its source record and explicit rejection rationale. It must not be exposed to downstream consumers as a signal or indicator. Typical causes include unresolved leakage, invalid source timing, missing rights, selective reporting, a reused final holdout, or a failure to outperform the declared baseline under the registered decision rule.

## 8. Permanent limits after promotion

Promotion is a research-governance decision, not an investment recommendation. A promoted record must remain explicitly bounded by its instrument universe, observation period, feature version, target definition, data-source vintages, metric, uncertainty, regime constraints, and known limitations. It must never be described as proof that a symbolic association causes a market outcome, and it must never generate financial instructions or personalized advice.

## References

1. `data/research/signal_indicator_promotion_policy.json`
2. `data/unified/research_contract.json`
3. `data/research/temporal_leakage_controls.json`
4. `data/research/walk_forward_validation_plan.json`
5. `data/research/research_dataset_manifest.json`
