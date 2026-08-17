# Review-Gated Recommendations and Semantic Tradition-Boundary Analysis

**Prepared by:** Manus AI  
**Package inspected:** `data/unified/unified_astrology_master.json` and `data/unified/symbol_registry.json`  
**Analysis status:** Complete; no semantic formulas or traditions were silently promoted.

## Executive assessment

The unified master is structurally strong as an orchestration and provenance layer. It distinguishes observations, interpretations, formula references, research associations, and retrieval protocols; it also declares the canonical registry boundary in `astrology-data-unifi`. The current interpretation corpus contains **3,011 source-derived testing indicators from 133 source files**, but these records are retrieval and regression fixtures rather than validated psychological, causal, predictive, medical, or financial evidence.

The principal governance issue is not missing text. It is **semantic separation**. The package contains Western, Hellenistic, modern, Vedic, esoteric/Theosophical, Magi, Uranian/midpoint, financial-astrology, company-research, and user-defined scoring material. These layers may coexist in one package, but they must not be combined into a universal interpretation rule without an explicit bridge methodology, tradition scope, formula contract, input settings, and approval record.

## 1. Review-gated recommendations

| Recommendation | Current status | Why it is gated | Safe next action |
|---|---|---|---|
| Indicator schema | `auto_applied` | Reversible metadata change | Keep validating required fields, stable IDs, hashes, and status vocabulary. |
| Keyword index | `auto_applied` | Retrieval-only change | Add ranking tests without treating frequency as interpretive truth. |
| Unicode symbol registry | `auto_applied` | Display and alias metadata only | Add provenance to aliases when sourced from a tradition-specific corpus. |
| Provenance links | `auto_applied` | Reversible lineage improvement | Require source IDs and hashes for every normalized record. |
| Semantic tradition review | `pending_review` | Combining traditions can change meaning | Keep separate tradition modes and add explicit bridge records only after review. |
| Malformed JSON repair | `pending_review` | Repair can alter source content | Preserve raw files; apply bounded repairs only with before/after hashes and review. |
| Unavailable calculations | `pending_review` | Requires exact rules, settings, engines, and failure modes | Implement one adapter at a time with a failing fixture, regression fixture, and calculation manifest. |

The master explicitly preserves a **38-versus-52 chart-type conflict** rather than promoting the manually assembled count of 52 over the canonical registry count of 38. It also keeps semantic score claims methodology-bound, records secret redaction for the latest AFE inputs, preserves the midpoint-axis ellipsis as provisional, and retains formula variants as conflicted rather than overwriting the canonical catalog.

## 2. Semantic tradition-boundary analysis

### 2.1 Esoteric/Theosophical layer

The referenced esoteric-framework task produced dedicated framework artifacts and extracted concepts including **Kala Purusha, Pravritti and Nivritti, Sanchita and Kriyaman karma, planetary pairs, Holy Orders, and Theosophical influence**. These are appropriate as a distinct `tradition_mode: esoteric` corpus with source-grounded interpretation indicators. They should not be merged into Hellenistic rulership, Vedic timing, Western psychological interpretation, or financial scoring as if the terms were interchangeable.

The safe integration pattern is:

| Layer | Allowed content | Not allowed without review |
|---|---|---|
| Source | Verbatim esoteric terms and passages | Rewriting concepts as universal laws |
| Normalized interpretation | Stable IDs, keywords, tradition label, source reference | Deleting the tradition label |
| Calculation | Only explicit formulas with documented inputs | Inferring esoteric calculations from prose |
| Delineation | Retrieve esoteric modules when `tradition_mode` requests them | Blending esoteric meanings into default Western output |
| Research | Hypothesis records with explicit labels | Treating esoteric symbolism as validated outcome evidence |

### 2.2 Hellenistic and traditional techniques

The master’s conflict records include material associated with sect, applying/separating aspects, overcoming, aversion, rulership, and traditional timing. These techniques depend on settings such as sect, zodiac, house system, aspect doctrine, orb policy, and significator rules. A modern or psychological interpretation layer cannot silently reuse them without retaining those settings.

### 2.3 Midpoints, Uranian, and harmonic material

Midpoint activations, planetary pictures, harmonics, and related indicators belong to a separate methodology family. Their output may be normalized into the same record envelope, but the semantic key must retain the method, axis, activator, harmonic number, orb policy, and tradition scope. A midpoint interpretation should not be deduplicated with an apparently similar natal aspect statement merely because the prose shares keywords.

### 2.4 Financial and company-research material

The master’s financial-astrology contract is correctly marked `research_only_pending_review`. It requires time-aligned features, a feature cutoff rule, walk-forward or purged splits, market baselines, missingness, sample size, uncertainty, regime sensitivity, and negative results. It prohibits trading instructions, position sizing, personal financial advice, guaranteed forecasts, and causal claims from symbolic associations.

Company-research indicators such as executive tenure, fundamentals, ratios, and market data are ordinary financial/company data. Astrological signals must remain a separate feature family. Any join between them must be time-indexed, licensed, reproducible, and leakage-safe.

## 3. Unified master findings

The master contains the required ontology classes for `observation`, `interpretation`, `formula_reference`, `research_association`, and `retrieval_protocol`. Its research contract covers historical OHLCV, asset profile, financial metrics, earnings, news, dividends, recommendations, holders, macro/cross-asset data, feature cutoffs, walk-forward/purged splits, baselines, uncertainty, and prohibited uses.

The interpretation-indicator integration is correctly marked `source_derived_testing_dataset`. It references the source inventory, normalized records, keyword index, and deduplication register. The master reports 3,011 indicators from 133 sources, with all records currently classified as `source_derived`. That is appropriate for testing and retrieval, but it means the dataset does not itself establish calculated chart facts or empirical validity.

The main unresolved master-level issues are:

1. **Malformed drafts:** Several draft JSON files remain unavailable and should not be repaired silently.
2. **Chart-type mismatch:** Canonical registry coverage and manual metadata must remain separate until reconciled.
3. **Methodology-bound scores:** Recursive strength, transit strength, house affinity, financial scores, and similar values are configurable methods, not probabilities.
4. **No new astronomical calculations:** The latest integration did not execute ephemeris calculations, so interpretation indicators must not be mislabeled as computed placements.
5. **Midpoint incompleteness:** Literal ellipsis in the available axes list is provisional and must not be expanded by invention.

## 4. Symbol-registry review

The symbol registry is useful and appropriately scoped as a display and retrieval alias layer. It contains 12 signs, the classical and outer planets, nodes, Chiron, major asteroids, angles, houses, and major aspects with glyphs and aliases. The explicit policy states that aliases and glyphs do not assert a tradition or calculation rule.

| Strength | Review note |
|---|---|
| Stable lowercase IDs | Good for normalized joins and retrieval. |
| Glyph preservation | Good for UI and source-text matching. |
| Aliases such as True Node and Mean Node | Must retain node mode when used in calculations. |
| ASC, MC, IC, DSC aliases | Display metadata only; calculation settings remain separate. |
| Major aspect angle values | Useful metadata, but orb policy and aspect doctrine remain methodology-specific. |
| Parallel and contraparallel with `null` angles | Correctly avoids forcing an ecliptic angle onto declination aspects. |
| Unknown-symbol preservation policy | Correct and necessary for asteroids, fixed stars, and tradition-specific glyphs. |

A future improvement should add `source_ids`, `tradition_scope`, and `calculation_dependency` to each nonstandard alias, especially for asteroid, Uranian, esoteric, and Arabic-Part symbols. This is a metadata enhancement, not a semantic decision.

## 5. Referenced-task provenance

### ML-testing task

The referenced ML task produced packaged artifacts including `dataset.jsonl`, `dataset.csv`, `schema.json`, `manifest.json`, `validation_report.json`, `README.md`, and a ZIP bundle. These artifacts establish a useful testing precedent: dataset lineage, schema, validation, and packaging should remain separate. The current interpretation-indicator dataset follows that pattern, but it should not be treated as an outcome-labeled ML dataset until a hypothesis card, feature dictionary, time windows, labels, baselines, uncertainty, and leakage controls are supplied.

### Supabase export task

The referenced database task produced `create_import_records.sql`. Its replay records an HTTP 401 caused by a secret-key requirement and the inability to use a nonexistent REST `exec_sql` RPC. The proposed staging schema used JSONB records, provenance fields, content hashes, validation status, indexes, and RLS, but table creation remained blocked pending a Management API personal access token with `database:write`. Therefore, the current unified package should remain file-based and auditable; it should not claim that the indicator corpus has been exported to Supabase.

### Esoteric delineation task

The referenced esoteric task produced a dedicated framework package with implementation artifacts such as `ephemeris.ts`, `BirthDataCalculator.tsx`, test findings, and the final delineation outputs. The relevant governance lesson is that esoteric concepts were extracted into a dedicated framework rather than silently merged into the canonical registry. That pattern should be retained for future esoteric indicators and retrieval modules.

## 6. Recommended next implementation order

1. Add `tradition_scope`, `source_ids`, and `calculation_dependency` metadata to symbol aliases and indicator records.
2. Create explicit per-tradition retrieval namespaces: Western, Hellenistic, Vedic, esoteric, Magi, Uranian/midpoint, financial research, and user-defined methodology.
3. Add validation that refuses cross-tradition joins unless a bridge methodology is present.
4. Convert the ML-testing package contract into a reusable `research_dataset_manifest.json` for any future astrology–market experiment.
5. Treat Supabase export as a separate deployment step requiring verified credentials, schema migration, RLS policies, and a dry-run import report.
6. Implement unavailable chart methods only with explicit formulas, settings, engine metadata, and regression fixtures.

## References

[1]: `data/unified/unified_astrology_master.json` — current unified orchestration master.
[2]: `data/unified/symbol_registry.json` — integrated Unicode and alias registry.
[3]: `data/interpretation-indicators/recommendations.json` — recommendation statuses and review gates.
[4]: `data/interpretation-indicators/coverage_gap_register.json` — coverage and thin-layer register.
[5]: `PjcV4wmY0PK7vxX96KsVsF` — referenced task: Extracting Astrology and Financial Data for ML Testing.
[6]: `IcxAoqsRjJtXJfZCfUuWx5` — referenced task: Export Data to Database Using Supabase API.
[7]: `gw4yP30qoqPeIhTA3L9cO0` — referenced task: Detailed Delineation Framework from Esoteric Astrology PDF.
