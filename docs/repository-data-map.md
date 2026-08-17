# Repository Data Map and Validation Status

This map separates machine-readable project data from preserved source drafts. It reflects the structural cleanup performed in August 2026 and is intended to prevent invalid or unfinished content from being accidentally consumed by tooling.

## Validated data categories

| Category | Location | Intended contents |
|---|---|---|
| Frameworks | `data/frameworks/` | Unified references and delineation frameworks that parse as JSON. |
| Definitions | `data/definitions/` | Rulership information and other structured terminology. |
| Calculations | `data/calculations/` | Chart-type and calculation material that parses as JSON. |
| Methodologies | `data/methodologies/` | Structured methodology and scoring protocols. |
| Delineations | `data/delineations/` | Structured interpretation and delineation records. |
| Charts | `data/charts/` | Saved chart data, which may contain personal information. |
| Extractions | `data/extractions/` | Machine-readable source extracts. |
| Sources | `data/sources/` | Human-readable source text retained for reference. |

## Preserved drafts

The files in `data/drafts/` were retained without semantic edits because the audit found malformed JSON, a truncated document, or explicit placeholder text. They remain available for future repair, but should not be imported as validated data.

| Preserved file | Audit finding |
|---|---|
| `enriched-master-dataset-framework.json` | JSON parse error. |
| `astrological-methodology-module-1.json` | JSON parse error. |
| `astrological-methodology-module-2.json` | JSON parse error. |
| `astrological-methodology-module-3.json` | JSON parse error. |
| `biseptile-interpretation.json` | JSON parse error. |
| `chart-types.json` | Truncated JSON document. |
| `chiron-compendium-unified.json` | JSON parse error. |
| `master-astrology-chart-types.json` | JSON parse error. |
| `master-synastry-engine.json` | Truncated JSON document. |
| `progressions-calculation-system.json` | JSON parse error. |
| `sun-moon-mp.json` | Truncated JSON string. |
| `master-relationship-astrology-compendium.json` | Contains explicit placeholder material. |

## Deduplication decision

The audit found no byte-identical tracked files. Two astrology-overview source files were near duplicates, differing primarily in Markdown formatting and minor copy edits. The Markdown version is retained as the canonical source at `data/sources/astrology-overview.md`; the redundant text copy was removed. Karmic-framework files share material by design and remain separate because they serve different top-level schemas and are connected to the normalization workflow.

The numbered SVG files were retained. Although a small number are textually similar, they are not byte-identical and the audit did not establish that they are interchangeable visual assets.
