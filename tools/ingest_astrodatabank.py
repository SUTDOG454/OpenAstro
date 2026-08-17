#!/usr/bin/env python3
"""Ingest approved AstroDatabank scraper output into OpenAstro source extracts.

The script accepts individual JSON files, directories of JSON files, or SQLite databases
containing the upstream scraper's ``scraped_data`` table. It creates one provenance-rich,
source-extract JSON document per source record plus a manifest. Output is intentionally
classified as a machine-readable source extract; it is not promoted to a validated chart,
calculation, or delineation schema.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import sys
from collections.abc import Iterable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "data" / "extractions" / "astrodatabank"
SCHEMA_VERSION = "1.0.0"
UPSTREAM_REPOSITORY = "https://github.com/adyanandi/astrodatabank_scraper"

SQL_COLUMNS = (
    "url, name, date, time, place_name, latitude, longitude, timezone, "
    "data_source, rodden_rating, collector, biography, relationships, events, "
    "source_notes, category, html_content"
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def list_text(value: Any) -> list[str]:
    if isinstance(value, list):
        return [text(item) for item in value if text(item)]
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return []


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "unknown-profile"


def canonical_key(url: str, name: str, fallback: str) -> str:
    material = url or name or fallback
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def content_hash(record: dict[str, Any]) -> str:
    canonical = json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def normalise_upstream_record(raw: dict[str, Any], input_label: str, include_html: bool) -> dict[str, Any]:
    nested = raw.get("data") if isinstance(raw.get("data"), dict) else {}
    biography = nested.get("biography") if isinstance(nested.get("biography"), dict) else {}
    relationships = nested.get("relationships") if isinstance(nested.get("relationships"), dict) else {}
    events = nested.get("events") if isinstance(nested.get("events"), dict) else {}
    source_notes = nested.get("source notes") if isinstance(nested.get("source notes"), dict) else {}

    url = text(raw.get("URL") or raw.get("url"))
    name = text(raw.get("Name") or raw.get("name"))
    fallback = input_label + ":" + content_hash(raw)[:12]
    record_key = canonical_key(url, name, fallback)
    source_url = url if url.startswith(("https://", "http://")) else ""

    profile = {
        "name": name,
        "birth": {
            "date_text": text(raw.get("Date") or raw.get("date")),
            "time_text": text(raw.get("Time") or raw.get("time")),
            "place_name": text(raw.get("Place Name") or raw.get("place_name")),
            "latitude_text": text(raw.get("Latitude") or raw.get("latitude")),
            "longitude_text": text(raw.get("Longitude") or raw.get("longitude")),
            "timezone_text": text(raw.get("Timezone") or raw.get("timezone")),
        },
        "source_metadata": {
            "data_source": text(raw.get("Data Source") or raw.get("data_source")),
            "rodden_rating": text(raw.get("Rodden Rating") or raw.get("rodden_rating")),
            "collector": text(raw.get("Collector") or raw.get("collector")),
        },
    }
    normalized = {
        "schema_version": SCHEMA_VERSION,
        "record_type": "astrodatabank-profile-source-extract",
        "source": {
            "provider": "Astro-Databank",
            "source_url": source_url,
            "source_host": urlparse(source_url).netloc if source_url else "",
            "upstream_scraper_repository": UPSTREAM_REPOSITORY,
            "original_record_key": record_key,
        },
        "profile": profile,
        "content": {
            "biography_text": text(biography.get("text") or raw.get("biography")),
            "relationships_text": text(relationships.get("text") or raw.get("relationships")),
            "events_text": text(events.get("text") or raw.get("events")),
            "source_notes_text": text(source_notes.get("text") or raw.get("source_notes")),
            "categories": list_text(nested.get("category") or raw.get("category")),
        },
        "ingestion": {
            "input_label": input_label,
            "ingested_at": utc_now(),
            "review_status": "source-extract-unreviewed",
            "html_retained": include_html,
            "notes": "This is a provenance-preserving source extract. It is not a validated OpenAstro chart or interpretation record.",
        },
    }
    if include_html:
        normalized["content"]["raw_html"] = text(raw.get("HTML Content") or raw.get("html_content"))
    return normalized


def sqlite_records(path: Path) -> Iterable[tuple[dict[str, Any], str]]:
    with sqlite3.connect(path) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='scraped_data'")
        if cursor.fetchone() is None:
            raise ValueError(f"{path} has no scraped_data table")
        rows = connection.execute(f"SELECT {SQL_COLUMNS} FROM scraped_data")
        for index, row in enumerate(rows, start=1):
            yield dict(row), f"{path.name}:row-{index}"


def json_records(path: Path) -> Iterable[tuple[dict[str, Any], str]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"{path} is not valid JSON: {error.msg}") from error
    if isinstance(payload, dict):
        yield payload, path.name
    elif isinstance(payload, list):
        for index, item in enumerate(payload, start=1):
            if not isinstance(item, dict):
                raise ValueError(f"{path} item {index} is not an object")
            yield item, f"{path.name}:item-{index}"
    else:
        raise ValueError(f"{path} must contain a JSON object or list of objects")


def input_paths(input_path: Path) -> list[Path]:
    supported_suffixes = {".json", ".db", ".sqlite", ".sqlite3"}
    if input_path.is_file() and input_path.suffix.lower() in supported_suffixes:
        return [input_path]
    if input_path.is_dir():
        files = sorted(
            path for path in input_path.rglob("*")
            if path.is_file() and path.suffix.lower() in supported_suffixes
        )
        if files:
            return files
    raise ValueError(f"No supported JSON or SQLite input found at {input_path}")


def existing_keys(output_dir: Path) -> set[str]:
    keys: set[str] = set()
    if not output_dir.exists():
        return keys
    for path in output_dir.glob("*.json"):
        if path.name == "manifest.json":
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            key = payload.get("source", {}).get("original_record_key")
            if isinstance(key, str):
                keys.add(key)
        except (json.JSONDecodeError, OSError):
            continue
    return keys


def write_manifest(output_dir: Path, entries: list[dict[str, str]], source_input: Path) -> None:
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "record_type": "astrodatabank-ingestion-manifest",
        "generated_at": utc_now(),
        "source_input": str(source_input),
        "upstream_scraper_repository": UPSTREAM_REPOSITORY,
        "record_count": len(entries),
        "records": entries,
        "promotion_rule": "Source extracts remain unreviewed until an explicit schema and provenance review promotes them to another OpenAstro data category.",
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON file, SQLite database, or directory containing approved scraper output")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help=f"Output directory (default: {DEFAULT_OUTPUT})")
    parser.add_argument("--include-html", action="store_true", help="Retain raw HTML content when it is present in input records")
    parser.add_argument("--dry-run", action="store_true", help="Validate inputs and report the planned import without writing files")
    parser.add_argument("--overwrite", action="store_true", help="Rewrite output files for records already present in the output directory")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_input = args.input.expanduser().resolve()
    output_dir = args.output.expanduser().resolve()
    try:
        paths = input_paths(source_input)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    prepared: list[tuple[dict[str, Any], str]] = []
    failures: list[str] = []
    for path in paths:
        try:
            reader = sqlite_records if path.suffix.lower() in {".db", ".sqlite", ".sqlite3"} else json_records
            prepared.extend(reader(path))
        except (OSError, ValueError, sqlite3.Error) as error:
            failures.append(str(error))

    normalized = [normalise_upstream_record(raw, label, args.include_html) for raw, label in prepared]
    if args.dry_run:
        print(json.dumps({"input_files": len(paths), "valid_records": len(normalized), "input_errors": failures}, indent=2))
        return 1 if failures else 0

    output_dir.mkdir(parents=True, exist_ok=True)
    known_keys = existing_keys(output_dir)
    entries: list[dict[str, str]] = []
    written = 0
    skipped = 0
    for record in normalized:
        key = record["source"]["original_record_key"]
        if key in known_keys and not args.overwrite:
            skipped += 1
            continue
        profile_name = record["profile"]["name"] or "unknown-profile"
        filename = f"{slugify(profile_name)}-{key[:12]}.json"
        target = output_dir / filename
        target.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        entries.append({"filename": filename, "original_record_key": key, "source_url": record["source"]["source_url"]})
        known_keys.add(key)
        written += 1

    write_manifest(output_dir, entries, source_input)
    print(json.dumps({"input_files": len(paths), "valid_records": len(normalized), "written": written, "skipped_existing": skipped, "input_errors": failures, "output": str(output_dir)}, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
