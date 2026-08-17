from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path('/home/ubuntu/openastro_worktree')
RAW = ROOT / 'data/sources/2026-08-user-uploads/raw'
PDF_TEXT = ROOT / 'data/sources/2026-08-user-uploads/derived-pdf-text'
REFERENCED_TASKS = ROOT / 'data/sources/2026-08-user-uploads/referenced_task_inventory.json'
OUT = ROOT / 'data/ingested-user-corpus'


SENSITIVE_FILES = {
    'ASTROLOGICAL_SYNTHESIS_REPORT.md',
    'UAROSv6datacharts.txt',
}
PRIVATE_FILES = {
    'astrodash-4m7y4aef.manus.md',
    'astrodash-4m7y4aef.manus.space_.pdf',
    'antiscion_synastry-2.jsx(1).txt',
}
CODE_FILES = {
    'afe_quantreo_pipeline-2.py',
    'backtest-validation-guardrails-prevent-look-ahead-bias-state-leakage-and-research-live-divergence.py',
    'antiscion_synastry-2.jsx(1).txt',
    'astro_intelligence_ui.html',
}
FINANCIAL_FILES = {
    'FinancialAstrologyPlanetaryCycles_DetailedExploration.txt',
    'AstrologyPredictionandFinancialTimingSystem.txt',
    'HistoricalData_1785490203238.csv',
    'afe_quantreo_pipeline-2.py',
    'backtest-validation-guardrails-prevent-look-ahead-bias-state-leakage-and-research-live-divergence.py',
}
ESOTERIC_FILES = {'esoteric_astro.txt'}


def slug(value: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(prefix: str, source_id: str, subject: str, text: str) -> str:
    payload = f'{source_id}|{subject}|{text}'.encode('utf-8')
    return f'{prefix}_{hashlib.sha256(payload).hexdigest()[:20]}'


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='replace')


def try_json(text: str) -> tuple[Any | None, str]:
    try:
        return json.loads(text), 'json'
    except json.JSONDecodeError:
        stripped = text.lstrip('\ufeff\n\r\t ')
        # A UTF-8 byte-order mark is transport metadata; remove it before attempting the same parse.
        try:
            return json.loads(stripped), 'utf8_bom_removed'
        except json.JSONDecodeError:
            pass
        # Bounded structural repair: preserve a documented source missing only its outer opening brace.
        if stripped.startswith('"meta"') and stripped.rstrip().endswith('}'):
            try:
                return json.loads('{\n' + stripped), 'bounded_missing_outer_open_brace_repair'
            except json.JSONDecodeError:
                pass
        blocks = re.findall(r'```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```', text, flags=re.I | re.S)
        for block in blocks:
            try:
                return json.loads(block), 'fenced_json'
            except json.JSONDecodeError:
                continue
    return None, 'text'


def source_category(name: str) -> str:
    if name in CODE_FILES:
        return 'untrusted_code_or_ui'
    if name in SENSITIVE_FILES:
        return 'sensitive_interpretive_material'
    if name in PRIVATE_FILES:
        return 'private_chart_or_personalized_output'
    if name in FINANCIAL_FILES:
        return 'financial_or_market_research_material'
    if name == 'MasterAstrologyChartTypes.txt':
        return 'chart_type_reference'
    if name == 'Astrological_Glossary.txt':
        return 'terminology_reference'
    if name == 'Fixed_Stars_1.txt':
        return 'fixed_star_interpretation_reference'
    if name == 'Astrological_Aspects.txt':
        return 'aspect_interpretation_reference'
    if name in ESOTERIC_FILES:
        return 'esoteric_astrology_source'
    if name == 'Astrology_Nakshatra.txt':
        return 'sparse_presentation_extract'
    if name == 'Chart_Interpretation_Arroyo.txt':
        return 'near_empty_extract'
    return 'astrology_source_material'


def source_flags(name: str) -> list[str]:
    flags = ['user_supplied', 'untrusted_data', 'source_rights_pending_review']
    if name in CODE_FILES:
        flags.extend(['do_not_execute', 'static_inspection_only'])
    if name in SENSITIVE_FILES:
        flags.extend(['sensitive_adult_interpretive_content', 'quarantined_from_general_delineation'])
    if name in PRIVATE_FILES:
        flags.extend(['personal_data_or_personalized_chart', 'private_context_not_for_general_corpus'])
    if name in FINANCIAL_FILES:
        flags.extend(['financial_research_only', 'not_a_validated_signal', 'non_advisory'])
    if name in ESOTERIC_FILES:
        flags.extend(['esoteric_retrieval_only', 'not_for_standard_calculation_engine'])
    return flags


def add_record(records: list[dict[str, Any]], *, source: dict[str, Any], record_type: str, subject: str, text: str,
               tradition_scope: list[str], status: str = 'source_derived', evidence_class: str = 'source_derived',
               limitations: list[str] | None = None, extensions: dict[str, Any] | None = None) -> None:
    cleaned = re.sub(r'\s+', ' ', text).strip()
    if len(cleaned) < 3:
        return
    record = {
        'record_id': stable_id('usr', source['source_id'], subject, cleaned),
        'source_id': source['source_id'],
        'source_sha256': source['sha256'],
        'source_path': source['source_path'],
        'record_type': record_type,
        'subject_path': subject,
        'raw_text': text,
        'normalized_text': cleaned,
        'tradition_scope': tradition_scope,
        'evidence_class': evidence_class,
        'status': status,
        'limitations': limitations or ['Source-derived material is not an empirical finding or deterministic calculation.'],
    }
    if extensions:
        record['extensions'] = extensions
    records.append(record)


def extract_glossary(text: str, source: dict[str, Any], records: list[dict[str, Any]]) -> None:
    for line_number, line in enumerate(text.splitlines(), 1):
        line = re.sub(r'\s+', ' ', line).strip()
        if not line or len(line) < 24:
            continue
        match = re.match(r'^([A-Za-z][A-Za-z0-9 ,;()\-\'’]+?)\s{1,}([A-Z].{15,})$', line)
        if match and len(match.group(1)) < 80:
            add_record(records, source=source, record_type='glossary_definition', subject=f'term:{slug(match.group(1))}',
                       text=match.group(2), tradition_scope=['mixed_historical_reference'],
                       extensions={'term': match.group(1), 'line_number': line_number})


def extract_heading_blocks(text: str, source: dict[str, Any], records: list[dict[str, Any]], record_type: str,
                           tradition_scope: list[str], max_blocks: int = 160) -> None:
    heading_patterns = [
        re.compile(r'^(?:\d+\.?\s+)?[A-Z][A-Z &/\-:]{5,}$'),
        re.compile(r'^#{1,4}\s+(.+)$'),
        re.compile(r'^(?:PART|CHAPTER|SECTION)\s+[A-Z0-9IVXLC]+[:.\s].*$', re.I),
    ]
    lines = text.splitlines()
    heading_indices: list[tuple[int, str]] = []
    for index, original in enumerate(lines):
        line = re.sub(r'\s+', ' ', original).strip()
        if not line or len(line) > 150:
            continue
        if any(pattern.match(line) for pattern in heading_patterns):
            heading_indices.append((index, line.lstrip('#').strip()))
    for position, (start, heading) in enumerate(heading_indices[:max_blocks]):
        end = heading_indices[position + 1][0] if position + 1 < len(heading_indices) else min(len(lines), start + 35)
        paragraph = ' '.join(re.sub(r'\s+', ' ', item).strip() for item in lines[start + 1:end] if item.strip())
        if len(paragraph) >= 80:
            add_record(records, source=source, record_type=record_type, subject=f'heading:{slug(heading)}', text=paragraph[:2200],
                       tradition_scope=tradition_scope, extensions={'heading': heading, 'line_start': start + 1, 'line_end': end})


def extract_aspect_headings(text: str, source: dict[str, Any], records: list[dict[str, Any]]) -> None:
    seen: set[str] = set()
    for line_number, line in enumerate(text.splitlines(), 1):
        clean = re.sub(r'\s+', ' ', line).strip()
        match = re.match(r'^ASPECTS OF ([A-Z]+)(?:\s*&\s*|\s+AND\s+)([A-Z]+)$', clean)
        if match:
            pair = f'{match.group(1).title()}-{match.group(2).title()}'
            if pair not in seen:
                seen.add(pair)
                add_record(records, source=source, record_type='aspect_pair_reference', subject=f'aspect_pair:{slug(pair)}',
                           text=f'Source contains a delineation section for {pair} across harmonious, conjunction, and inharmonious categories.',
                           tradition_scope=['western_historical'], extensions={'planet_pair': pair, 'line_number': line_number})
    for aspect, degree in [('conjunction', '0'), ('semi-sextile', '30'), ('semi-square', '45'), ('sextile', '60'), ('quintile', '72'), ('square', '90'), ('trine', '120'), ('sesquiquadrate', '135'), ('quincunx', '150'), ('opposition', '180')]:
        add_record(records, source=source, record_type='aspect_taxonomy_reference', subject=f'aspect:{aspect}',
                   text=f'The source discusses {aspect} as a distinct aspect category and frames application as contextual to planets, signs, houses, and concurrent aspects.',
                   tradition_scope=['western_historical'], extensions={'aspect': aspect, 'nominal_degrees': degree})


def extract_fixed_stars(text: str, source: dict[str, Any], records: list[dict[str, Any]]) -> None:
    pattern = re.compile(r'^[A-Z](?::|[-–])\s*([A-Za-z][A-Za-z\- ]{2,40})\s*[-–].{0,240}$')
    for line_number, line in enumerate(text.splitlines(), 1):
        clean = re.sub(r'\s+', ' ', line).strip()
        match = pattern.match(clean)
        if match and 'constellation' in clean.lower():
            star = match.group(1).strip()
            add_record(records, source=source, record_type='fixed_star_source_reference', subject=f'fixed_star:{slug(star)}',
                       text=clean, tradition_scope=['western_fixed_star', 'esoteric'],
                       limitations=['Position, orb, and interpretation are source-specific and may be epoch-dependent; no current position is computed from this record.'],
                       extensions={'star_name': star, 'line_number': line_number})


def extract_chart_type_proposals(value: Any, source: dict[str, Any], records: list[dict[str, Any]], discrepancies: list[dict[str, Any]]) -> None:
    if not isinstance(value, dict) or not isinstance(value.get('chart_types'), list):
        discrepancies.append({'discrepancy_id': 'chart-types-json-not-parseable', 'source_id': source['source_id'], 'status': 'unavailable', 'detail': 'Expected chart_types array was not present.'})
        return
    for item in value['chart_types']:
        if not isinstance(item, dict) or not item.get('id'):
            continue
        title = str(item.get('label') or item['id'])
        purpose = str(item.get('core_purpose') or '')
        system = str(item.get('system') or 'source_unspecified')
        add_record(records, source=source, record_type='chart_type_proposal', subject=f'chart_type:{item["id"]}',
                   text=purpose or f'Source defines chart type {title}.', tradition_scope=[system.lower().replace(' ', '_')],
                   status='pending_review', evidence_class='source_derived',
                   limitations=['Candidate chart-type metadata requires reconciliation with the configured canonical chart-type registry before implementation.'],
                   extensions={'source_chart_type': item})


def extract_json_framework(value: Any, source: dict[str, Any], records: list[dict[str, Any]], discrepancies: list[dict[str, Any]]) -> None:
    if not isinstance(value, dict):
        return
    metadata = value.get('framework_metadata')
    if isinstance(metadata, dict):
        add_record(records, source=source, record_type='financial_framework_metadata', subject='framework_metadata', text=json.dumps(metadata, ensure_ascii=False),
                   tradition_scope=['financial_astrology'], status='pending_review', evidence_class='methodology_bound',
                   limitations=['Financial-framework statements are methodology proposals, not validated strategies, performance evidence, or advice.'])
    techniques = value.get('expanded_techniques_manifest')
    if isinstance(techniques, dict):
        for technique_id, technique in techniques.items():
            if isinstance(technique, dict):
                definition = str(technique.get('definition') or technique.get('interpretation') or '')
                if definition:
                    add_record(records, source=source, record_type='financial_technique_proposal', subject=f'technique:{technique_id}', text=definition,
                               tradition_scope=['financial_astrology'], status='pending_review', evidence_class='methodology_bound',
                               limitations=['This is an unvalidated source proposal. It cannot generate trading instructions, position sizing, forecasts, or causal claims.'],
                               extensions={'technique_id': technique_id, 'source_fields': technique})
    if 'economic_cycles' in value.get('astronomical_and_calculation_parameters', {}):
        add_record(records, source=source, record_type='economic_cycle_reference', subject='economic_cycles',
                   text=json.dumps(value['astronomical_and_calculation_parameters']['economic_cycles'], ensure_ascii=False),
                   tradition_scope=['financial_astrology'], status='pending_review', evidence_class='methodology_bound',
                   limitations=['Economic-cycle statements are preserved as source proposals and require a registered research protocol before use.'])


def extract_signal_candidates(text: str, source: dict[str, Any], records: list[dict[str, Any]]) -> None:
    cleaned = text.replace('\x0c', '\n')
    object_pattern = re.compile(r'"id"\s*:\s*"([^"]+)".*?"description"\s*:\s*"(.*?)".*?"trigger"\s*:\s*"(.*?)".*?"expected_effect"\s*:\s*"(.*?)".*?"source"\s*:\s*"(.*?)".*?"confidence"\s*:\s*([0-9.]+).*?"category"\s*:\s*"(.*?)".*?"testable"\s*:\s*(true|false)', re.S | re.I)
    for match in object_pattern.finditer(cleaned):
        signal_id, description, trigger, effect, signal_source, confidence, category, testable = match.groups()
        description = re.sub(r'\s+', ' ', description).strip()
        trigger = re.sub(r'\s+', ' ', trigger).strip()
        effect = re.sub(r'\s+', ' ', effect).strip()
        add_record(records, source=source, record_type='unvalidated_signal_candidate', subject=f'signal:{signal_id}',
                   text=description, tradition_scope=['source_unspecified'], status='pending_review', evidence_class='source_derived',
                   limitations=['Source confidence is retained as an unverified source claim, not a calibrated probability.', 'Candidate cannot be surfaced as a validated signal without the research promotion gate.'],
                   extensions={'source_signal_id': signal_id, 'trigger': trigger, 'expected_effect': effect, 'claimed_source': signal_source, 'claimed_confidence': confidence, 'claimed_category': category, 'source_testable_flag': testable.lower() == 'true', 'promotion_status': 'not_eligible_without_validated_experiment'})


def static_code_metadata(text: str, source: dict[str, Any], records: list[dict[str, Any]]) -> None:
    names = []
    for pattern in [r'^\s*(?:def|class|function)\s+([A-Za-z_][A-Za-z0-9_]*)', r'^\s*const\s+([A-Za-z_][A-Za-z0-9_]*)']:
        names.extend(re.findall(pattern, text, flags=re.M))
    add_record(records, source=source, record_type='unexecuted_code_metadata', subject='static_api_surface',
               text=f'Static inspection identified {len(set(names))} named symbols: {", ".join(sorted(set(names))[:80])}.',
               tradition_scope=['implementation_reference'], status='pending_review', evidence_class='source_derived',
               limitations=['Uploaded code was not executed, dependency-resolved, trusted, or adopted as a calculation engine.'],
               extensions={'named_symbols': sorted(set(names)), 'execution_policy': 'do_not_execute'})


def extract_csv_profile(path: Path, source: dict[str, Any], records: list[dict[str, Any]], discrepancies: list[dict[str, Any]]) -> None:
    with path.open(encoding='utf-8-sig', newline='') as handle:
        rows = list(csv.DictReader(handle))
    headers = list(rows[0].keys()) if rows else []
    dates = [row.get('Date', '') for row in rows if row.get('Date')]
    add_record(records, source=source, record_type='unverified_ohlcv_dataset_profile', subject='dataset_profile',
               text=f'User-supplied CSV has {len(rows)} rows with columns {headers}.', tradition_scope=['financial_astrology'],
               status='pending_review', evidence_class='source_derived',
               limitations=['Instrument identifier, exchange, price-adjustment basis, timezone, source rights, and historical availability are not established.', 'This file is not registered as an active research observation dataset and does not change observations_acquired in the research-layer manifest.'],
               extensions={'row_count': len(rows), 'columns': headers, 'first_date_as_supplied': dates[0] if dates else None, 'last_date_as_supplied': dates[-1] if dates else None, 'research_dataset_status': 'unverified_candidate_not_acquired'})
    discrepancies.append({'discrepancy_id': 'ohlcv-candidate-missing-identity-and-lineage', 'source_id': source['source_id'], 'status': 'pending_review', 'detail': 'CSV has OHLCV-like columns but no instrument identifier, exchange, timezone, adjustment basis, provider, rights, or availability timestamps.'})

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    discrepancies: list[dict[str, Any]] = []
    quarantine: list[dict[str, Any]] = []

    for raw_path in sorted(RAW.iterdir()):
        if not raw_path.is_file():
            continue
        name = raw_path.name
        category = source_category(name)
        source = {
            'source_id': f'openastro:user-upload:{slug(name)}',
            'source_path': str(raw_path.relative_to(ROOT)),
            'filename': name,
            'sha256': digest(raw_path),
            'size_bytes': raw_path.stat().st_size,
            'category': category,
            'trust_status': 'untrusted_user_supplied_data',
            'rights_status': 'source_rights_pending_review',
            'flags': source_flags(name),
            'parser': 'not_run',
            'raw_preservation': 'staged_copy',
        }
        sources.append(source)
        if name in SENSITIVE_FILES:
            quarantine.append({
                'source_id': source['source_id'],
                'source_path': source['source_path'],
                'classification': 'sensitive_adult_interpretive_content',
                'status': 'quarantined_from_general_delineation',
                'reason': 'Contains explicit sexual, psychological, medical, or consent-related interpretive claims that must not be generalized, diagnosed, scored, or automatically retrieved.',
                'permitted_processing': ['raw preservation', 'provenance inventory', 'non-interpretive structural metadata'],
                'prohibited_processing': ['general delineation', 'diagnosis', 'risk scoring', 'sexual preference inference', 'automated aspect-to-sexuality mapping', 'model training without separately approved rights and ethics review'],
            })
            source['parser'] = 'quarantine_metadata_only'
            continue
        if name in CODE_FILES:
            text = read_text(raw_path)
            source['parser'] = 'static_code_inspection'
            static_code_metadata(text, source, records)
            continue
        if raw_path.suffix.lower() == '.csv':
            source['parser'] = 'csv_dict_reader'
            extract_csv_profile(raw_path, source, records, discrepancies)
            continue
        if raw_path.suffix.lower() == '.pdf':
            derived = PDF_TEXT / f'{raw_path.stem}.txt'
            if derived.exists():
                source['parser'] = 'pdftotext_layout'
                source['derived_text_path'] = str(derived.relative_to(ROOT))
                text = read_text(derived)
                if name == 'Signals.pdf':
                    extract_signal_candidates(text, source, records)
                else:
                    extract_heading_blocks(text, source, records, 'pdf_source_heading', ['mixed_source_reference'])
            else:
                source['parser'] = 'unavailable_pdf_text'
                discrepancies.append({'discrepancy_id': f'pdf-text-missing-{slug(name)}', 'source_id': source['source_id'], 'status': 'unavailable', 'detail': 'No derived PDF text was found.'})
            continue
        text = read_text(raw_path)
        value, parser = try_json(text)
        source['parser'] = parser
        if name == 'Astrological_Glossary.txt':
            extract_glossary(text, source, records)
        elif name == 'Astrological_Aspects.txt':
            extract_aspect_headings(text, source, records)
            extract_heading_blocks(text, source, records, 'aspect_source_heading', ['western_historical'], max_blocks=80)
        elif name == 'Fixed_Stars_1.txt':
            extract_fixed_stars(text, source, records)
        elif name == 'MasterAstrologyChartTypes.txt':
            extract_chart_type_proposals(value, source, records, discrepancies)
        elif name == 'AstrologyPredictionandFinancialTimingSystem.txt':
            extract_json_framework(value, source, records, discrepancies)
        elif name == 'esoteric_astro.txt':
            extract_heading_blocks(text, source, records, 'esoteric_source_heading', ['esoteric', 'vedic'], max_blocks=100)
        elif name == 'extracted_knowledge.txt':
            extract_heading_blocks(text, source, records, 'source_knowledge_heading', ['mixed_source_reference'], max_blocks=100)
        elif name == 'FinancialAstrologyPlanetaryCycles_DetailedExploration.txt':
            extract_heading_blocks(text, source, records, 'financial_cycle_source_proposal', ['financial_astrology'], max_blocks=40)
            for record in records:
                if record['source_id'] == source['source_id']:
                    record['status'] = 'pending_review'
                    record['evidence_class'] = 'methodology_bound'
                    record['limitations'] = ['Financial-cycle statements are unvalidated source proposals. They are research-only and cannot generate advice, signals, position sizing, or causal claims.']
        elif name in PRIVATE_FILES:
            source['parser'] = 'privacy_metadata_only'
            discrepancies.append({'discrepancy_id': f'private-source-generalization-block-{slug(name)}', 'source_id': source['source_id'], 'status': 'pending_review', 'detail': 'Personalized birth-chart content is preserved as private source context and excluded from general corpus extraction.'})
        elif name == 'Astrology_Nakshatra.txt':
            discrepancies.append({'discrepancy_id': 'nakshatra-extract-sparse', 'source_id': source['source_id'], 'status': 'unavailable', 'detail': 'The supplied text contains presentation credits and page markers but no substantive Nakshatra teaching extract.'})
        elif name == 'Chart_Interpretation_Arroyo.txt':
            discrepancies.append({'discrepancy_id': 'arroyo-extract-near-empty', 'source_id': source['source_id'], 'status': 'unavailable', 'detail': 'The supplied text extract contains only form-feed characters and no usable interpretation content.'})
        else:
            extract_heading_blocks(text, source, records, 'source_heading', ['mixed_source_reference'], max_blocks=60)

    referenced_task_data = json.loads(REFERENCED_TASKS.read_text())
    for task in referenced_task_data['records']:
        sources.append({
            'source_id': task['source_id'],
            'source_path': 'data/sources/2026-08-user-uploads/referenced_task_inventory.json',
            'filename': task['title'],
            'sha256': digest(REFERENCED_TASKS),
            'size_bytes': REFERENCED_TASKS.stat().st_size,
            'category': 'referenced_task_context',
            'trust_status': 'untrusted_referenced_task_context',
            'rights_status': 'task_access_scope_owned_but_external_source_rights_not_verified',
            'flags': ['referenced_task_context_only', task['status']],
            'parser': 'manual_provenance_inventory',
            'raw_preservation': 'referenced_task_inventory',
            'limitations': task['limitations'],
        })

    # Exact normalized text deduplication preserves source provenance rather than deleting competing records.
    key_to_record: dict[tuple[str, str, str], dict[str, Any]] = {}
    dedup_groups: list[dict[str, Any]] = []
    for record in records:
        key = (record['record_type'], record['subject_path'], record['normalized_text'].casefold())
        if key in key_to_record:
            kept = key_to_record[key]
            kept.setdefault('source_ids', [kept['source_id']])
            kept['source_ids'] = list(dict.fromkeys(kept['source_ids'] + [record['source_id']]))
            dedup_groups.append({'duplicate_record_id': record['record_id'], 'kept_record_id': kept['record_id'], 'status': 'exact_normalized_duplicate'})
        else:
            record['source_ids'] = [record['source_id']]
            key_to_record[key] = record
    records = list(key_to_record.values())

    record_counts = Counter(record['record_type'] for record in records)
    source_counts = Counter(record['source_id'] for record in records)
    tradition_counts = Counter(scope for record in records for scope in record['tradition_scope'])
    validation_errors: list[str] = []
    for record in records:
        for required in ['record_id', 'source_id', 'source_sha256', 'record_type', 'subject_path', 'normalized_text', 'tradition_scope', 'evidence_class', 'status', 'limitations']:
            if required not in record:
                validation_errors.append(f'{record.get("record_id", "unknown")}: missing {required}')
    known_source_ids = {source['source_id'] for source in sources}
    for record in records:
        if record['source_id'] not in known_source_ids:
            validation_errors.append(f'{record["record_id"]}: unknown source {record["source_id"]}')

    summary = {
        'schema_version': '1.0.0',
        'status': 'source_ingested_with_review_boundaries',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'source_count': len(sources),
        'normalized_record_count': len(records),
        'quarantined_source_count': len(quarantine),
        'discrepancy_count': len(discrepancies),
        'record_type_counts': dict(record_counts),
        'tradition_scope_counts': dict(tradition_counts),
        'top_source_record_counts': source_counts.most_common(20),
        'high_level_boundaries': [
            'Uploaded code is statically inspected only and never executed.',
            'Personalized chart material is private context and excluded from generalized corpus records.',
            'Sensitive sexual or medical-psychological interpretive material is quarantined from general delineation and training.',
            'Financial or market material remains methodology-bound, research-only, and ineligible as a validated signal without the existing promotion gate.',
            'Esoteric source material is retrieval-only and cannot enter Western, Vedic, or standard calculation engines.',
        ],
    }
    validation_report = {
        'schema_version': '1.0.0',
        'status': 'passed_with_review_warnings' if not validation_errors else 'failed',
        'checks': {
            'raw_source_directory_exists': RAW.is_dir(),
            'referenced_task_inventory_exists': REFERENCED_TASKS.is_file(),
            'sources_have_hashes': all(bool(source.get('sha256')) for source in sources),
            'records_reference_known_sources': not any('unknown source' in error for error in validation_errors),
            'record_required_fields_present': not validation_errors,
            'code_execution_prohibited': all('do_not_execute' in source['flags'] for source in sources if source['category'] == 'untrusted_code_or_ui'),
            'sensitive_content_quarantined': len(quarantine) == len(SENSITIVE_FILES),
            'financial_records_not_promoted': all(record.get('status') != 'research_exploratory' for record in records if 'financial_astrology' in record['tradition_scope']),
        },
        'errors': validation_errors,
        'warnings': [
            'All source rights remain pending review unless separately documented.',
            'No uploaded calculation code was executed or adopted.',
            'No chart position or predictive timing value was calculated from uploaded source material.',
            'The supplied OHLCV-like CSV is not an active research dataset because identity, rights, adjustment, timezone, and availability lineage are missing.',
        ],
    }

    (OUT / 'user_corpus_source_inventory.json').write_text(json.dumps({'schema_version': '1.0.0', 'sources': sources}, ensure_ascii=False, indent=2) + '\n')
    (OUT / 'normalized_user_corpus_records.json').write_text(json.dumps({'schema_version': '1.0.0', 'records': records}, ensure_ascii=False, indent=2) + '\n')
    (OUT / 'sensitive_content_quarantine.json').write_text(json.dumps({'schema_version': '1.0.0', 'records': quarantine}, ensure_ascii=False, indent=2) + '\n')
    (OUT / 'user_corpus_discrepancies.json').write_text(json.dumps({'schema_version': '1.0.0', 'records': discrepancies}, ensure_ascii=False, indent=2) + '\n')
    (OUT / 'user_corpus_deduplication.json').write_text(json.dumps({'schema_version': '1.0.0', 'policy': 'exact normalized duplicates merge source links; semantic conflicts remain separate', 'groups': dedup_groups}, ensure_ascii=False, indent=2) + '\n')
    (OUT / 'user_corpus_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    (OUT / 'user_corpus_validation_report.json').write_text(json.dumps(validation_report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'sources': len(sources), 'records': len(records), 'quarantined': len(quarantine), 'discrepancies': len(discrepancies), 'validation_status': validation_report['status']}, indent=2))


if __name__ == '__main__':
    main()
