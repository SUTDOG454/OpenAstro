import { createEsotericCorpus, type EsotericIndicator, type EsotericCorpus } from './esotericNamespace';

export interface NormalizedInterpretationRecord {
  indicator_id: string;
  source_id: string;
  source_path: string;
  subject_path: string;
  normalized_text: string;
  keywords?: string[];
  source_ids?: string[];
  evidence_class?: string;
  status?: string;
  limitations?: string[];
  tradition_mode?: string;
}

const ESOTERIC_MARKERS = [
  'esoteric', 'theosoph', 'kala_purusha', 'pravritti', 'nivritti', 'sanchita', 'kriyaman', 'holy_order',
  'bepin', 'behari', 'soul_purpose',
];

function isExplicitlyEsoteric(record: NormalizedInterpretationRecord): boolean {
  const haystack = [record.tradition_mode, record.source_path, record.subject_path, record.normalized_text, ...(record.keywords ?? [])]
    .filter(Boolean).join(' ').toLocaleLowerCase();
  return ESOTERIC_MARKERS.some((marker) => haystack.includes(marker));
}

export function toEsotericIndicator(record: NormalizedInterpretationRecord): EsotericIndicator | undefined {
  if (!isExplicitlyEsoteric(record)) return undefined;
  return {
    id: record.indicator_id,
    traditionMode: 'esoteric',
    subject: record.subject_path,
    text: record.normalized_text,
    keywords: [...(record.keywords ?? []), 'esoteric'],
    sourceIds: [...(record.source_ids ?? [record.source_id])],
    evidenceClass: record.evidence_class === 'methodology_bound' ? 'methodology_bound' : record.status === 'pending_review' ? 'pending_review' : 'source_derived',
    status: record.status === 'pending_review' ? 'pending_review' : record.evidence_class === 'methodology_bound' ? 'methodology_bound' : 'source_derived',
    calculationDependencies: [],
    limitations: [...(record.limitations ?? []), 'Retrieved in esoteric namespace only; not a standard Western or Vedic calculation rule.'],
  };
}

export function buildEsotericCorpusFromRecords(records: NormalizedInterpretationRecord[], sourceRefs: string[] = []): EsotericCorpus {
  const indicators = records.map(toEsotericIndicator).filter((record): record is EsotericIndicator => record !== undefined);
  return createEsotericCorpus(indicators, sourceRefs);
}
