#!/usr/bin/env python3
"""Validate the checked-in Open Astrology source extract without loading it all into memory."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

EXPECTED_ROWS = 19_522
EXPECTED_COLUMNS = 412
EXPECTED_SHA256 = "c41bfdae55c80be454c702ac4f67ac231e9de21bf73812f78f8fdf5b5cc267b1"
EXPECTED_HEADER_PREFIX = (
    "Chart_A_Name",
    "Chart_A_UTCDate",
    "Chart_B_Name",
    "Chart_B_UTCDate",
)


def validate(path: Path) -> dict[str, int | str]:
    digest = hashlib.sha256()
    rows = 0
    duplicates = 0
    identities: set[tuple[str, str, str, str]] = set()
    with path.open("rb") as binary_stream:
        for chunk in iter(lambda: binary_stream.read(1024 * 1024), b""):
            digest.update(chunk)
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        header = tuple(reader.fieldnames or ())
        if len(header) != EXPECTED_COLUMNS or header[:4] != EXPECTED_HEADER_PREFIX:
            raise ValueError(f"unexpected header: {len(header)} columns")
        for row in reader:
            rows += 1
            identity = tuple(row.get(key, "") or "" for key in EXPECTED_HEADER_PREFIX)
            if identity in identities:
                duplicates += 1
            identities.add(identity)
    if rows != EXPECTED_ROWS:
        raise ValueError(f"expected {EXPECTED_ROWS} rows, found {rows}")
    if duplicates != 0:
        raise ValueError(f"found {duplicates} duplicate identity rows")
    if digest.hexdigest() != EXPECTED_SHA256:
        raise ValueError(f"sha256 mismatch: {digest.hexdigest()}")
    return {"file": str(path), "rows": rows, "columns": len(header), "duplicate_identity_rows": duplicates, "sha256": digest.hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=Path("data/extractions/open-astrology-datasets/gauq-couples-aspects-real-7deg-20000-noa2b-cdata4.csv"))
    args = parser.parse_args()
    print(json.dumps(validate(args.path), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
