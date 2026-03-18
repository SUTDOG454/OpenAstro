#!/usr/bin/env python3
"""Normalize aspect payloads that may arrive as escaped JSON strings.

Usage:
  python tools/normalize_aspects_json.py input.json > normalized.json
  cat input.txt | python tools/normalize_aspects_json.py --summary
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ESCAPED_WHITESPACE = re.compile(r"\\[nrt]")


def _repair_escaped_whitespace(raw: str) -> str:
    """
    Repair common pasted payload format:
    - literal '\\n', '\\r', '\\t' between JSON tokens
    - literal '\\"' around keys/values
    """
    return ESCAPED_WHITESPACE.sub(
        lambda m: {"\\n": "\n", "\\r": "\r", "\\t": "\t"}[m.group(0)],
        raw,
    )


def load_payload(raw: str) -> Any:
    """Decode payload that may be normal JSON or escaped JSON-like text."""
    current: Any = raw
    for _ in range(5):
        if not isinstance(current, str):
            break

        stripped = current.strip()
        try:
            current = json.loads(stripped)
            continue
        except json.JSONDecodeError:
            pass

        repaired = _repair_escaped_whitespace(stripped)
        try:
            current = json.loads(repaired)
            continue
        except json.JSONDecodeError:
            pass

        # Some payloads also escape every quote (e.g. \"point1\").
        quote_repaired = repaired.replace('\\"', '"')
        try:
            current = json.loads(quote_repaired)
            continue
        except json.JSONDecodeError:
            return stripped

    return current


def summarize(aspects: list[dict[str, Any]]) -> str:
    by_aspect = Counter(item.get("aspect", "Unknown") for item in aspects)
    by_point = Counter()
    for item in aspects:
        p1 = (item.get("point1") or {}).get("name")
        p2 = (item.get("point2") or {}).get("name")
        if p1:
            by_point[p1] += 1
        if p2:
            by_point[p2] += 1

    lines = [
        f"Total aspects: {len(aspects)}",
        "Top aspect types:",
    ]
    for name, count in by_aspect.most_common(10):
        lines.append(f"  - {name}: {count}")

    lines.append("Most frequent points:")
    for name, count in by_point.most_common(10):
        lines.append(f"  - {name}: {count}")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", help="Path to payload file. Reads stdin if omitted.")
    parser.add_argument("--summary", action="store_true", help="Print a summary to stderr.")
    args = parser.parse_args()

    raw = Path(args.input).read_text(encoding="utf-8") if args.input else sys.stdin.read()
    payload = load_payload(raw)

    if isinstance(payload, str):
        print("Unable to decode payload into JSON.", file=sys.stderr)
        return 1

    if not isinstance(payload, list):
        print("Decoded payload is JSON, but not a list of aspects.", file=sys.stderr)
        return 1

    json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
    print()

    if args.summary:
        print(summarize(payload), file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
