# Open Astrology Dataset Source Extract

This directory contains the selected real-chart source file from the public [Open Astrology Datasets](https://www.kaggle.com/datasets/gokhanyu/open-astrology-datasets) dataset.

## Provenance

| Field | Value |
|---|---|
| Dataset page | <https://www.kaggle.com/datasets/gokhanyu/open-astrology-datasets> |
| Declared license | GPL-2.0, as shown on the dataset page |
| License text | <http://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html> |
| Selected artifact | `gauq-couples-aspects-real-7deg-20000-noa2b-cdata4.csv` |
| Source format | Tab-delimited text despite the `.csv` extension |
| Profiled rows | 19,522 data rows |
| Profiled columns | 412 |
| Identity duplicates | 0 across chart-A/chart-B name and UTC-date tuple |
| Retrieval date | 2026-08-17 |

## Scope and handling

The selected file is a **source extract** for relationship-aspect data. It is not promoted to `data/charts/`, a framework, a delineation, or a validated interpretation schema. The original dataset also publishes randomized-control artifacts; those were not copied because this ingestion targets the real-chart artifact and avoids mixing controls with observed records.

The data contains chart identifiers, UTC dates, coordinates, age-difference values, and aspect-feature columns. Treat chart-linked dates and locations as potentially sensitive. Any downstream publication, enrichment, or promotion requires a separate privacy, schema, and license review.

The complete retrieval metadata and file hash are recorded in `manifest.json`.
