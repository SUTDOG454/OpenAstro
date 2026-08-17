from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
EXTRACTION_ROOT = ROOT / "data" / "extractions" / "company-research"
MANIFEST = EXTRACTION_ROOT / "manifest.json"


class CompanyResearchExtractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_manifest_is_source_extract_only(self) -> None:
        self.assertEqual(self.manifest["status"], "source_extract_unreviewed")
        self.assertFalse(self.manifest["validation"]["source_code_executed"])
        self.assertFalse(self.manifest["validation"]["application_promotion"])

    def test_recorded_files_exist_and_hashes_match(self) -> None:
        files = self.manifest["files"]
        self.assertEqual(len(files), 8)
        for entry in files:
            path = EXTRACTION_ROOT / entry["path"]
            self.assertTrue(path.is_file(), entry["path"])
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(digest, entry["sha256"], entry["path"])
            self.assertEqual(path.stat().st_size, entry["bytes"], entry["path"])

    def test_repository_provenance_is_pinned(self) -> None:
        source = next(item for item in self.manifest["sources"] if item["source_id"] == "github.SUTDOG454.finance-query")
        self.assertEqual(source["repository_url"], "https://github.com/SUTDOG454/finance-query")
        self.assertEqual(source["commit"], "e95b3e0185d170324eaae216c8db302d841e29ae")
        self.assertEqual(source["declared_license"], "MIT")

    def test_user_provided_source_is_separately_labeled(self) -> None:
        source = next(item for item in self.manifest["sources"] if item["source_id"] == "user.upload.economic-market-timing-system")
        self.assertEqual(source["declared_license"], "not_declared")
        self.assertIn("user-provided", source["promotion_rule"])


if __name__ == "__main__":
    unittest.main()
