# Company-Research Repository Search Report

## Search scope

The search covered the user-provided repository inventory and the accessible repositories most likely to contain company, executive, fundamentals, market, financial, or research code. Candidate checkouts included `OpenAstro`, `Astro_INtelligence`, `astrology_intelligence-`, `Financial-astrology-system-`, `ML-Finance`, `finance-query`, `trading-signals`, `AstroChart_Analysis`, `astro44`, `Apps-Synthesis-`, `financial-astrology-stats`, `Gann-and-Financial-Astrology-Indicators`, and `ASTROLOGY-BOOKS-DATABASE`.

Search terms included `company_research`, `companyResearch`, `executiveEngine`, `getCLevelTenureScore`, `CLevel`, `cLevel`, `tenureYears`, `avgCTenure`, `company`, `executive`, `fundamental`, `leadership`, `IPO`, and `market research`.

## Findings

No exact `company_research` TypeScript path or executive scoring symbol was found in the searched repositories. `OpenAstro` contains the locally added executive module from the preceding task, but its upstream repository history does not contain the broader company-research module family. `Astro_INtelligence` contains extensive astrological and financial-astrology frameworks, but the matches are prose, framework documents, or broad JSON artifacts rather than a directly reusable company-research TypeScript implementation.

The strongest executable-source match was `finance-query`, which contains explicit company quote, fundamentals, financial-data, market, and research models. The selected Rust files were copied as quarantined source extracts under `data/extractions/company-research/finance-query/`. They were not compiled, executed, or silently converted into OpenAstro application code.

## Ingested material

The extraction includes the FMP company quote adapter, FMP fundamentals core and analysis models, financial-data and fundamentals response models, the discovery research model, the repository MIT license, and the user-provided economic-market timing configuration. Every file is hashed in `manifest.json`.

## Promotion boundary

The ingested files are reference material only. A future implementation must define a canonical TypeScript company-research schema, map Rust response fields explicitly, preserve field-level provenance, confirm MIT compatibility, and add Vitest or Jest tests before promotion. The user-provided configuration remains separately labeled because it has no independently declared license.
