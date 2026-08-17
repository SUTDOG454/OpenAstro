export type EsotericEvidenceClass = 'source_derived' | 'methodology_bound' | 'pending_review';

export interface EsotericIndicator {
  id: string;
  traditionMode: 'esoteric';
  subject: string;
  text: string;
  keywords: string[];
  sourceIds: string[];
  evidenceClass: EsotericEvidenceClass;
  status: 'source_derived' | 'methodology_bound' | 'pending_review';
  calculationDependencies: string[];
  limitations: string[];
}

export interface EsotericCorpus {
  schemaVersion: '1.0.0';
  traditionMode: 'esoteric';
  sourceRefs: string[];
  indicators: EsotericIndicator[];
  calculationEngine: 'none';
  isolationPolicy: {
    allowedEngine: 'esoteric_retrieval_only';
    rejectedModes: Array<'western' | 'vedic' | 'standard'>;
    reason: string;
  };
}

export interface EsotericRetrievalRequest {
  traditionMode: 'esoteric';
  query?: string;
  subjects?: string[];
  keywords?: string[];
  limit?: number;
  calculationEngine?: string;
}

export class EsotericNamespaceError extends Error {
  readonly code: 'INVALID_TRADITION_MODE' | 'CALCULATION_ENGINE_NOT_ALLOWED';

  constructor(code: EsotericNamespaceError['code'], message: string) {
    super(message);
    this.name = 'EsotericNamespaceError';
    this.code = code;
  }
}

const DEFAULT_LIMIT = 25;

function normalize(value: string): string {
  return value.trim().toLocaleLowerCase();
}

function assertEsotericRequest(request: EsotericRetrievalRequest): void {
  if (request.traditionMode !== 'esoteric') {
    throw new EsotericNamespaceError('INVALID_TRADITION_MODE', 'The esoteric namespace accepts only tradition_mode: esoteric.');
  }
  if (request.calculationEngine && request.calculationEngine !== 'esoteric_retrieval_only') {
    throw new EsotericNamespaceError('CALCULATION_ENGINE_NOT_ALLOWED', 'The esoteric retrieval namespace never invokes Western, Vedic, or standard calculation engines.');
  }
}

export function createEsotericCorpus(indicators: EsotericIndicator[], sourceRefs: string[] = []): EsotericCorpus {
  const validated = indicators.map((indicator) => {
    if (indicator.traditionMode !== 'esoteric') throw new EsotericNamespaceError('INVALID_TRADITION_MODE', `Indicator ${indicator.id} is not esoteric.`);
    return { ...indicator, calculationDependencies: [...indicator.calculationDependencies], sourceIds: [...indicator.sourceIds] };
  });
  return {
    schemaVersion: '1.0.0', traditionMode: 'esoteric', sourceRefs: [...sourceRefs], indicators: validated,
    calculationEngine: 'none',
    isolationPolicy: {
      allowedEngine: 'esoteric_retrieval_only', rejectedModes: ['western', 'vedic', 'standard'],
      reason: 'Esoteric interpretations are retrieved from a dedicated source corpus and are not injected into standard chart calculations.',
    },
  };
}

export function retrieveEsoteric(corpus: EsotericCorpus, request: EsotericRetrievalRequest): EsotericIndicator[] {
  assertEsotericRequest(request);
  const query = normalize(request.query ?? '');
  const subjects = (request.subjects ?? []).map(normalize);
  const keywords = (request.keywords ?? []).map(normalize);
  const matches = corpus.indicators.filter((indicator) => {
    const haystack = normalize([indicator.subject, indicator.text, ...indicator.keywords].join(' '));
    const subjectMatch = subjects.length === 0 || subjects.some((subject) => normalize(indicator.subject).includes(subject));
    const keywordMatch = keywords.length === 0 || keywords.every((keyword) => indicator.keywords.some((item) => normalize(item).includes(keyword)));
    const queryMatch = query.length === 0 || haystack.includes(query);
    return subjectMatch && keywordMatch && queryMatch;
  });
  return matches.slice(0, Math.max(0, request.limit ?? DEFAULT_LIMIT));
}

export function assertNamespaceIsolation(corpus: EsotericCorpus): void {
  if (corpus.traditionMode !== 'esoteric' || corpus.calculationEngine !== 'none') {
    throw new EsotericNamespaceError('INVALID_TRADITION_MODE', 'Esoteric corpus has an invalid calculation boundary.');
  }
  for (const indicator of corpus.indicators) {
    if (indicator.traditionMode !== 'esoteric') throw new EsotericNamespaceError('INVALID_TRADITION_MODE', `Mixed-tradition indicator found: ${indicator.id}`);
  }
}
