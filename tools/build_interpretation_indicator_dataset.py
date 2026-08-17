from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path('/home/ubuntu/openastro_worktree')
OUT = ROOT / 'data/interpretation-indicators'
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / 'tools'))
from interpretation_indicator_engine import extract_keywords, normalize_text, stable_indicator_id, unicode_symbols  # noqa: E402

INTERPRETATION_KEYS = {
    'interpretation', 'interpretations', 'meaning', 'theme', 'themes', 'description', 'effect', 'effects',
    'delineation', 'delineation_template', 'psychological', 'karmic', 'tantric', 'financial_interpretation',
    'astrological_commentary', 'use_in_delineation', 'significance', 'purpose', 'rationale', 'function',
    'core_purpose', 'interpretation_focus', 'interpretation_approach', 'interpretation_guidelines',
    'example_interpretations', 'shadow', 'signal', 'signals', 'keywords', 'keyword', 'archetype',
}
SOURCE_ROOTS = [ROOT / 'data', ROOT / 'docs', ROOT / 'skills', ROOT / 'data/extractions']
EXCLUDE_PARTS = {'.git', 'node_modules', '__pycache__'}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_type(path: Path) -> str:
    if path.suffix.lower() == '.json':
        return 'json'
    if path.suffix.lower() in {'.md', '.txt'}:
        return 'text'
    if path.suffix.lower() in {'.py', '.ts', '.tsx', '.js', '.jsx', '.rs'}:
        return 'code_or_schema'
    return 'other'


def source_id(path: Path) -> str:
    return f'openastro:{path.relative_to(ROOT).as_posix()}'


def add_indicator(records, *, sid, path, record_type, subject_path, raw_text, evidence_class='source_derived', status='source_derived', extra=None):
    text = normalize_text(raw_text)
    if not text or len(text) < 3:
        return
    record = {
        'indicator_id': stable_indicator_id(sid, subject_path, record_type, text),
        'source_id': sid,
        'source_path': str(path.relative_to(ROOT)),
        'source_sha256': sha256(path),
        'record_type': record_type,
        'subject_path': subject_path,
        'raw_text': raw_text,
        'normalized_text': text,
        'keywords': extract_keywords(text),
        'unicode_symbols': unicode_symbols(text),
        'evidence_class': evidence_class,
        'status': status,
        'limitations': ['Interpretive text is source-derived and not empirical evidence.'],
    }
    if extra:
        record.update(extra)
    records.append(record)


def walk_json(value, path_parts, path, sid, records):
    if isinstance(value, dict):
        for key, child in value.items():
            key_norm = str(key).lower()
            child_path = path_parts + [str(key)]
            if key_norm in INTERPRETATION_KEYS:
                if isinstance(child, str):
                    add_indicator(records, sid=sid, path=path, record_type='interpretation_text', subject_path='.'.join(child_path[:-1]) or '$', raw_text=child)
                elif isinstance(child, list):
                    strings = [x for x in child if isinstance(x, str)]
                    if strings:
                        add_indicator(records, sid=sid, path=path, record_type='interpretation_list', subject_path='.'.join(child_path[:-1]) or '$', raw_text='; '.join(strings), extra={'items': strings})
                elif isinstance(child, dict):
                    for subkey, subvalue in child.items():
                        if isinstance(subvalue, str):
                            add_indicator(records, sid=sid, path=path, record_type='interpretation_field', subject_path='.'.join(child_path + [str(subkey)]), raw_text=subvalue)
            walk_json(child, child_path, path, sid, records)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            walk_json(child, path_parts + [str(index)], path, sid, records)
    elif isinstance(value, str) and path_parts and str(path_parts[-1]).lower() in INTERPRETATION_KEYS:
        add_indicator(records, sid=sid, path=path, record_type='interpretation_text', subject_path='.'.join(path_parts[:-1]) or '$', raw_text=value)


def extract_json_block(text: str):
    try:
        return json.loads(text), 'json'
    except json.JSONDecodeError:
        blocks = re.findall(r'```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```', text, flags=re.S | re.I)
        for block in blocks:
            try:
                return json.loads(block), 'fenced_json'
            except json.JSONDecodeError:
                pass
    return None, 'unparseable'


files = []
seen_paths = set()
for root in SOURCE_ROOTS:
    if not root.exists():
        continue
    for path in root.rglob('*'):
        if not path.is_file() or path in seen_paths:
            continue
        if any(part in EXCLUDE_PARTS for part in path.parts):
            continue
        if path.suffix.lower() not in {'.json', '.md', '.txt'}:
            continue
        seen_paths.add(path)
        files.append(path)

source_inventory = []
records = []
for path in sorted(files):
    sid = source_id(path)
    raw = path.read_text(encoding='utf-8', errors='replace')
    parsed = None
    parser = 'text'
    warning = None
    if path.suffix.lower() == '.json':
        parsed, parser = extract_json_block(raw)
        if parsed is None:
            warning = 'json_unparseable_or_truncated'
    source_inventory.append({
        'source_id': sid,
        'source_path': str(path.relative_to(ROOT)),
        'sha256': sha256(path),
        'media_type': source_type(path),
        'parser': parser,
        'parse_warning': warning,
        'trust_status': 'untrusted_data',
        'rights_status': 'source_rights_pending_review',
    })
    if parsed is not None:
        walk_json(parsed, [], path, sid, records)
    else:
        # Extract only explicit interpretation-bearing lines from malformed or prose sources.
        for lineno, line in enumerate(raw.splitlines(), 1):
            if re.search(r'interpret|delineat|meaning|theme|keyword|archetype|signal', line, re.I):
                clean = re.sub(r'^\s*[#>*`-]+\s*', '', line).strip()
                if len(clean) >= 12:
                    add_indicator(records, sid=sid, path=path, record_type='interpretation_line', subject_path=f'line:{lineno}', raw_text=clean)

# Exact normalized content deduplication preserves all source IDs and paths.
key_to_record = {}
dedup_groups = []
for record in records:
    key = (record['record_type'], record['subject_path'], record['normalized_text'].casefold())
    if key in key_to_record:
        kept = key_to_record[key]
        kept['source_ids'] = list(dict.fromkeys(kept.get('source_ids', [kept['source_id']]) + [record['source_id']]))
        kept['source_paths'] = list(dict.fromkeys(kept.get('source_paths', [kept['source_path']]) + [record['source_path']]))
        dedup_groups.append({'duplicate_indicator_id': record['indicator_id'], 'kept_indicator_id': kept['indicator_id'], 'status': 'exact_text_duplicate'})
    else:
        record['source_ids'] = [record['source_id']]
        record['source_paths'] = [record['source_path']]
        key_to_record[key] = record

records = list(key_to_record.values())
record_types = Counter(r['record_type'] for r in records)
source_counts = Counter(r['source_id'] for r in records)
keyword_index: dict[str, list[str]] = defaultdict(list)
for record in records:
    for keyword in record.get('keywords', []):
        keyword_index[keyword].append(record['indicator_id'])

layer_counts = {
    'interpretation_text': sum(1 for r in records if r['record_type'] in {'interpretation_text', 'interpretation_field', 'interpretation_list'}),
    'interpretation_lines': sum(1 for r in records if r['record_type'] == 'interpretation_line'),
    'keyword_sets': sum(1 for r in records if r['record_type'] == 'interpretation_list'),
}

(OUT / 'source_inventory.json').write_text(json.dumps({'schema_version': '1.0.0', 'source_count': len(source_inventory), 'sources': source_inventory}, ensure_ascii=False, indent=2) + '\n')
(OUT / 'normalized_interpretation_indicators.json').write_text(json.dumps({'schema_version': '1.0.0', 'record_count': len(records), 'records': records}, ensure_ascii=False, indent=2) + '\n')
(OUT / 'indicator_keyword_index.json').write_text(json.dumps({'schema_version': '1.0.0', 'keywords': {k: sorted(set(v)) for k, v in sorted(keyword_index.items())}}, ensure_ascii=False, indent=2) + '\n')
(OUT / 'deduplication.json').write_text(json.dumps({'schema_version': '1.0.0', 'policy': 'exact normalized text and subject-path duplicates are merged; probable semantic duplicates remain separate', 'duplicate_group_count': len(dedup_groups), 'groups': dedup_groups}, ensure_ascii=False, indent=2) + '\n')
(OUT / 'indicator_dataset_summary.json').write_text(json.dumps({'schema_version': '1.0.0', 'source_count': len(source_inventory), 'record_count': len(records), 'record_types': dict(record_types), 'layer_counts': layer_counts, 'source_record_counts_top_20': source_counts.most_common(20), 'unicode_symbol_count': len(set(symbol for r in records for symbol in r.get('unicode_symbols', []))), 'dedup_group_count': len(dedup_groups), 'status': 'source_derived_testing_dataset', 'warnings': ['Interpretive text is not empirical evidence.', 'Malformed JSON sources were preserved and line-scanned conservatively.', 'Probable semantic duplicates were not auto-merged.']}, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'sources': len(source_inventory), 'records': len(records), 'record_types': dict(record_types), 'dedup_groups': len(dedup_groups)}, indent=2))
