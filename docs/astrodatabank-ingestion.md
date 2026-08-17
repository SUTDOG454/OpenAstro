# AstroDatabank Source-Extract Ingestion

`tools/ingest_astrodatabank.py` converts **approved, lawfully obtained** JSON or SQLite output that follows the upstream [`adyanandi/astrodatabank_scraper`](https://github.com/adyanandi/astrodatabank_scraper) shape into provenance-rich OpenAstro source extracts.

## Data boundary

The script writes to `data/extractions/astrodatabank/`. These records have `record_type: astrodatabank-profile-source-extract` and `review_status: source-extract-unreviewed`. They are **not** automatically promoted to `data/charts/`, frameworks, interpretations, or other validated schemas.

Each output record retains its source URL, upstream scraper repository, stable original-record key, source metadata, raw source text fields, ingestion time, and HTML-retention status. The manifest records all files written during the ingestion run.

> Before acquiring input, confirm that collection is authorized by the source site’s terms, robots directives, applicable law, and any relevant privacy obligations. Do not use user-agent spoofing, undisclosed parallel fetching, or raw HTML retention unless there is a clear permitted need.

## Accepted inputs

The input may be a single JSON file, a directory containing JSON files, or a SQLite database. A JSON input must contain either one object or a list of objects that follow the scraper’s record structure. A SQLite input must contain the `scraped_data` table emitted by the upstream scraper.

## Usage

```bash
# Inspect approved input without writing repository files.
python3 tools/ingest_astrodatabank.py /approved/path/output.json --dry-run

# Ingest approved JSON or SQLite source output.
python3 tools/ingest_astrodatabank.py /approved/path/output.db

# Retain raw HTML only when an approved retention need exists.
python3 tools/ingest_astrodatabank.py /approved/path/output.json --include-html
```

The utility skips records with an existing original-record key by default. Use `--overwrite` only when a deliberate refresh of the existing source extract is required.

## Promotion review

Promotion from `data/extractions/astrodatabank/` requires a separate review that checks parseability, schema compatibility, deduplication, provenance, source terms, and whether potentially sensitive birth or relationship data may be stored in the destination category.
