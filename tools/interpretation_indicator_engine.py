from __future__ import annotations

import hashlib
import re
import unicodedata
from typing import Any, Iterable

STATUS_VALUES = {
    'source_derived', 'normalized', 'computed', 'methodology_bound',
    'research_exploratory', 'pending_review', 'unavailable', 'conflicted',
}


def normalize_text(value: str) -> str:
    value = unicodedata.normalize('NFKC', str(value))
    value = re.sub(r'\s+', ' ', value).strip()
    return value


def stable_indicator_id(source_id: str, subject_path: str, record_type: str, text: str) -> str:
    payload = '|'.join([source_id, subject_path, record_type, normalize_text(text).casefold()])
    return 'indicator_' + hashlib.sha256(payload.encode('utf-8')).hexdigest()[:20]


def extract_keywords(text: str, limit: int = 24) -> list[str]:
    words = re.findall(r"[\w'‑-]{4,}", normalize_text(text).lower(), flags=re.UNICODE)
    stop = {'that', 'this', 'with', 'from', 'into', 'their', 'there', 'which', 'when', 'where', 'will', 'have', 'being', 'also', 'than', 'through'}
    return list(dict.fromkeys(w for w in words if w not in stop))[:limit]


def unicode_symbols(text: str) -> list[str]:
    symbols = []
    for char in normalize_text(text):
        category = unicodedata.category(char)
        if category.startswith('S') or char in '☉☽☿♀♂♃♄♅♆♇☊☋⚷⚳⚴⚵⚶⚷⚸⚹⚺⚻⚼⚽⚾':
            if char not in symbols:
                symbols.append(char)
    return symbols


def validate_indicator(record: dict[str, Any]) -> list[str]:
    required = ['indicator_id', 'source_id', 'source_path', 'record_type', 'subject_path', 'raw_text', 'normalized_text', 'evidence_class', 'status']
    errors = [f'missing:{key}' for key in required if key not in record]
    if record.get('status') not in STATUS_VALUES:
        errors.append('invalid:status')
    if record.get('evidence_class') not in STATUS_VALUES:
        errors.append('invalid:evidence_class')
    if not isinstance(record.get('keywords', []), list):
        errors.append('invalid:keywords')
    return errors


def indicator_matches(record: dict[str, Any], *, text: str | None = None, subject: str | None = None) -> bool:
    if text is not None and normalize_text(text).casefold() not in record.get('normalized_text', '').casefold():
        return False
    if subject is not None and subject.casefold() not in record.get('subject_path', '').casefold():
        return False
    return True
