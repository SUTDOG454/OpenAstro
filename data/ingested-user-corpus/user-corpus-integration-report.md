# User Corpus and Referenced-Task Integration Report

**Status:** Integrated with provenance and review boundaries  
**Generated:** 2026-08-17  
**Scope:** Twenty-three user-supplied uploads and six referenced-task contexts were inventoried, preserved, normalized where eligible, and linked into the OpenAstro unified master.

## Integration Outcome

The integration adds a source-attributed corpus layer without changing the canonical `astrology-data-unifi` entity registry, calculation catalog, or existing research-layer execution state. Every staged source is represented in a source inventory with a SHA-256 hash, parser classification, flags, rights status, and raw-preservation path. The raw copies remain in the local source archive; the distributable package contains metadata and normalized records rather than copying private or sensitive raw text.

| Layer | Result | Evidence class and status |
|---|---:|---|
| Source inventory | 29 sources | User-supplied or referenced-task context; rights pending review |
| Normalized corpus | 1,785 records | Source-derived, methodology-bound, or pending review according to record family |
| Esoteric retrieval derivative | 76 records | Source-derived, explicit `tradition_mode: esoteric`, retrieval only |
| Signal candidates from supplied PDF | 1,050 records | Source-derived and `pending_review`; not promoted |
| Chart-type proposals | 25 records | Source-derived and pending canonical-registry reconciliation |
| Definition and reference records | 518 records | Source-derived; not universal calculation rules |
| Static code metadata | 4 records | Source-derived static inspection only; uploaded code was not executed |
| Quarantined sensitive sources | 2 sources | Preserved but excluded from general delineation and training |
| Explicit discrepancies | 4 records | Unavailable or pending review; none silently resolved |

## Materials Integrated

The normalized layer includes glossary definitions, aspect taxonomy references, fixed-star source references, source headings, esoteric source headings, chart-type proposals, unvalidated signal candidates, static code metadata, and an unverified OHLCV-like CSV profile. A UTF-8 byte-order mark in `MasterAstrologyChartTypes.txt` was removed only for parsing. The original file remains unchanged, and the resulting twenty-five chart-type records remain `pending_review` because no source proposal was added to a canonical registry or calculation adapter.

The referenced-task inventory links the prior text-extraction, chart-analysis website, Astrodash dashboard, compendium, solar-arcs methodology, and esoteric-PDF tasks. Referenced tasks are treated as **contextual provenance**, not as substitute canonical sources: un-hashed task outputs were not silently imported.

## Boundaries Applied

> A raw source, source-derived interpretation, deterministic astronomical calculation, methodology score, research association, and validated signal are different evidence classes. This integration preserves rather than collapses those distinctions.

| Boundary | Implementation |
|---|---|
| Esoteric material | The `esoteric_retrieval_records.json` derivative is linked only through the isolated namespace. Its calculation engine is `none`; Western, Vedic, and standard calculation modes remain rejected by that namespace. |
| Financial and market material | Financial-cycle text, the CSV profile, static code references, and the supplied signal candidates remain methodology-bound or source-derived research material. Research observations and labels remain `false`; no backtest ran. |
| Signal promotion | All 1,050 candidates remain `pending_review` and `not_eligible_without_validated_experiment`. The existing promotion policy requires a registered experiment, temporal controls, walk-forward evidence, baselines, uncertainty, final holdout, and independent review. |
| Uploaded code | All four code/UI artifacts are marked `do_not_execute` and were only statically inventoried. No dependencies were installed and no uploaded script was run. |
| Personal chart context | Astrodash outputs and personalized synastry/UI content are preserved as private context and excluded from generalized corpus records. |
| Sensitive interpretive content | Two sources containing explicit sexual or medical-psychological claims are quarantined from general delineation, scoring, automatic retrieval, and training. |
| Canonical calculations | No positions, aspects, transits, solar arcs, or predictive outputs were computed from the uploads. No canonical registry, formula, orb policy, house system, or zodiac setting was silently changed. |

## Unresolved Items

| ID | Status | Reason |
|---|---|---|
| `nakshatra-extract-sparse` | Unavailable | The uploaded text contains presentation markers but not substantive Nakshatra instruction. |
| `arroyo-extract-near-empty` | Unavailable | The uploaded text contains form-feed characters but no usable content. |
| `ohlcv-candidate-missing-identity-and-lineage` | Pending review | The CSV has OHLCV-like columns but no instrument identity, provider, rights, timezone, adjustment basis, or availability lineage. It is not an active research observation dataset. |
| `private-source-generalization-block-astrodash-4m7y4aef-manus-md` | Pending review | Personalized chart material may not be generalized into the corpus. |

## Validation Evidence

The source-artifact validator passed with review warnings. The full repository suites also passed after regeneration and integration.

| Check | Result |
|---|---:|
| Corpus source/record validation | Passed with review warnings |
| Corpus integration regression tests | 8 passed |
| Vitest | 29 passed across 5 files |
| TypeScript strict type-check | Passed |
| Python unittest suite | 53 passed |
| Esoteric calculation-engine isolation | Passed |
| Financial observations and labels unchanged | Passed; both remain `false` |
| Uploaded-code non-execution control | Passed |

## Included Artifacts

The primary package contains the authoritative source inventory, normalized records, quarantine ledger, discrepancy log, esoteric retrieval derivative, financial candidate-material boundary, unvalidated signal candidate register, chart-type proposal register, definition references, integration report, scripts, and regression tests. It intentionally excludes raw private and sensitive source bodies; those remain preserved locally in `data/sources/2026-08-user-uploads/raw/` and are represented by hashes and access flags in the inventory.

## Next Review Actions

Before any new source-derived material can become an executable calculation, canonical entity, or promoted research signal, it needs a narrower review. Chart-type proposals require canonical-registry and adapter-contract reconciliation. The OHLCV candidate requires full source lineage and historical availability metadata before observation acquisition. Solar-arcs weights and any other source scoring rules require methodology registration and independent review. A future signal promotion needs the already documented hypothesis, walk-forward, leakage, baseline, uncertainty, holdout, and reviewer gates.

## References

[1] [User corpus source inventory](user_corpus_source_inventory.json)  
[2] [Normalized user corpus records](normalized_user_corpus_records.json)  
[3] [User corpus validation report](user_corpus_validation_report.json)  
[4] [User corpus integration report](user_corpus_integration_report.json)  
[5] [Signal and indicator promotion policy](../research/signal_indicator_promotion_policy.json)  
[6] [Temporal leakage controls](../research/temporal_leakage_controls.json)
