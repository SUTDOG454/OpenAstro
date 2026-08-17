from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "tools" / "ingest_astrodatabank.py"


def run_script(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, check=False)


def sample_payload() -> dict[str, object]:
    return {
        "URL": "https://example.test/profile",
        "Name": "Example Profile",
        "Date": "1 January 1900",
        "Time": "12:00",
        "Place Name": "Example City",
        "Latitude": "10N00",
        "Longitude": "20E00",
        "Timezone": "UTC",
        "Data Source": "Test source",
        "Rodden Rating": "A",
        "Collector": "Test collector",
        "HTML Content": "<html>sample</html>",
        "data": {
            "biography": {"text": "Biography"},
            "relationships": {"text": "Relationships"},
            "events": {"text": "Events"},
            "source notes": {"text": "Notes"},
            "category": ["Category"],
        },
    }


class IngestAstroDatabankTests(unittest.TestCase):
    def test_json_ingest_and_deduplicate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.json"
            source.write_text(json.dumps(sample_payload()), encoding="utf-8")
            output = root / "output"

            dry_run = run_script(str(source), "--output", str(output), "--dry-run")
            self.assertEqual(dry_run.returncode, 0, dry_run.stderr)
            self.assertFalse(output.exists())

            first = run_script(str(source), "--output", str(output))
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(json.loads(first.stdout)["written"], 1)
            record_files = [path for path in output.glob("*.json") if path.name != "manifest.json"]
            self.assertEqual(len(record_files), 1)
            record = json.loads(record_files[0].read_text(encoding="utf-8"))
            self.assertEqual(record["record_type"], "astrodatabank-profile-source-extract")
            self.assertEqual(record["ingestion"]["review_status"], "source-extract-unreviewed")
            self.assertNotIn("raw_html", record["content"])

            second = run_script(str(source), "--output", str(output))
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(json.loads(second.stdout)["skipped_existing"], 1)

    def test_sqlite_ingest_with_optional_html(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.db"
            with sqlite3.connect(source) as connection:
                connection.execute("""
                    CREATE TABLE scraped_data (
                        url TEXT, name TEXT, date TEXT, time TEXT, place_name TEXT,
                        latitude TEXT, longitude TEXT, timezone TEXT, data_source TEXT,
                        rodden_rating TEXT, collector TEXT, biography TEXT, relationships TEXT,
                        events TEXT, source_notes TEXT, category TEXT, html_content TEXT
                    )
                """)
                connection.execute(
                    "INSERT INTO scraped_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    ("https://example.test/sqlite", "SQLite Profile", "2 February 1901", "13:00", "Town", "11N", "21E", "UTC+1", "Source", "B", "Collector", "Bio", "Rel", "Events", "Notes", "Category", "<html>sqlite</html>"),
                )
            output = root / "output"
            result = run_script(str(source), "--output", str(output), "--include-html")
            self.assertEqual(result.returncode, 0, result.stderr)
            records = [path for path in output.glob("*.json") if path.name != "manifest.json"]
            self.assertEqual(len(records), 1)
            record = json.loads(records[0].read_text(encoding="utf-8"))
            self.assertEqual(record["content"]["raw_html"], "<html>sqlite</html>")


if __name__ == "__main__":
    unittest.main()
