# Unified Astrology Expansion Report

## Scope

This orchestration layer expands the existing OpenAstro package without forking the canonical entity or calculation registries. It integrates **38 canonical chart types**, **13 formula references**, **522 signal/source records**, **60 explicit indicator records**, and research safeguards for financial astrology, company research, and content-gap workflows.

## Evidence boundaries

Source-derived definitions, deterministic astronomy, methodology-bound scores, exploratory financial associations, and interpretive prose remain separate. No new astronomical positions or market observations were calculated in this build.

## Chart-type coverage

Every canonical chart type now has a contract record containing inputs, outputs, method, status, and limitations. Existing adapters are marked `contracted`; source-backed but unimplemented methods are `pending_review`; firdaria, zodiacal releasing, and primary directions are explicitly `not_implemented` rather than approximated.

## Refactoring and naming

New orchestration artifacts live under `data/unified/` with stable snake_case JSON filenames. Existing data and tool paths remain backward-compatible. The reusable ontology helper is `tools/unified_delineation_ontology.py`, and the deterministic builder is `tools/build_unified_astrology_package.py`.

## Research controls

Financial-astrology records require time-aligned features, walk-forward or purged splits, baselines, missingness, uncertainty, regime sensitivity, negative results, and prohibited-use labels. Content-gap analysis is registered but unavailable until a target domain, competitors, market, language, and tool exports are supplied.

## Known gaps

Several local draft JSON files are malformed or truncated, the manual chart-type file declares 52 types while the canonical registry contains 38, and no live market data was acquired for a specific asset. These items remain visible in `discrepancy.json` and `coverage_gap_register.json`.
