import { describe, expect, it } from 'vitest';
import { createEsotericCorpus, EsotericNamespaceError, retrieveEsoteric, assertNamespaceIsolation } from '../delineation/esotericNamespace';
import { mapProviderNeutralFinancialStatement, FinancialStatementParseError } from '../company_research/financialStatement';
import { validateFeatureCutoffs } from '../research/featureCutoff';

describe('esoteric tradition namespace isolation', () => {
  const corpus = createEsotericCorpus([
    {
      id: 'esoteric:kala_purusha', traditionMode: 'esoteric', subject: 'kala_purusha',
      text: 'Esoteric source-derived subject record.', keywords: ['esoteric', 'kala'], sourceIds: ['esoteric-source'],
      evidenceClass: 'source_derived', status: 'source_derived', calculationDependencies: [], limitations: ['symbolic'],
    },
  ], ['esoteric-source']);

  it('retrieves only esoteric records and does not use a calculation engine', () => {
    assertNamespaceIsolation(corpus);
    expect(corpus.calculationEngine).toBe('none');
    expect(retrieveEsoteric(corpus, { traditionMode: 'esoteric', keywords: ['kala'] })).toHaveLength(1);
  });

  it('rejects Western, Vedic, and standard calculation requests', () => {
    for (const mode of ['western', 'vedic', 'standard'] as const) {
      expect(() => retrieveEsoteric(corpus, { traditionMode: mode as 'esoteric' })).toThrow(EsotericNamespaceError);
    }
    expect(() => retrieveEsoteric(corpus, { traditionMode: 'esoteric', calculationEngine: 'western_ephemeris' })).toThrow(EsotericNamespaceError);
  });
});

describe('provider-neutral financial statement mapping', () => {
  const options = { symbol: 'aapl', statementType: 'income' as const, frequency: 'annual' as const, providerId: 'fmp' };

  it('maps Yahoo timeseries payloads with nested reported values and prefixes', () => {
    const mapped = mapProviderNeutralFinancialStatement({
      timeseries: { result: [{ meta: { type: ['annualTotalRevenue'] }, annualTotalRevenue: [{ asOfDate: '2024-12-31', reportedValue: { raw: 123 } }] }] },
    }, options);
    expect(mapped.symbol).toBe('AAPL');
    expect(mapped.statement).toEqual({ TotalRevenue: { '2024-12-31': 123 } });
    expect(mapped.provenance?.sourcePayloadShape).toBe('yahoo_timeseries');
    expect(mapped.evidenceClass).toBe('source_derived');
  });

  it('maps FMP rows, primitive numbers, numeric strings, and ignores metadata', () => {
    const mapped = mapProviderNeutralFinancialStatement({
      data: [{ date: '2024-12-31', revenue: 100, netIncome: '25', symbol: 'AAPL', period: 'FY' }],
    }, options);
    expect(mapped.statement.revenue['2024-12-31']).toBe(100);
    expect(mapped.statement.netIncome['2024-12-31']).toBe(25);
    expect(mapped.provenance?.sourcePayloadShape).toBe('fmp_statement');
  });

  it('rejects malformed, empty, and unusable payloads', () => {
    expect(() => mapProviderNeutralFinancialStatement('{bad', options)).toThrow(FinancialStatementParseError);
    expect(() => mapProviderNeutralFinancialStatement({ timeseries: { result: [] } }, options)).toThrow(FinancialStatementParseError);
    expect(() => mapProviderNeutralFinancialStatement({ data: [{ date: '2024-12-31', revenue: 'not-a-number' }] }, options)).toThrow(FinancialStatementParseError);
  });
});

describe('ML feature cutoff validation', () => {
  it('accepts available features before cutoff and outcome after cutoff', () => {
    const report = validateFeatureCutoffs([{ rowId: 'r1', featureCutoff: '2024-01-10T00:00:00Z', outcomeWindowStart: '2024-01-11T00:00:00Z', features: [{ name: 'vix', value: 15, availableAt: '2024-01-09T23:00:00Z', sourceId: 'market' }] }]);
    expect(report.valid).toBe(true);
    expect(report.violations).toHaveLength(0);
  });

  it('rejects future features, overlapping outcomes, and invalid timestamps', () => {
    const report = validateFeatureCutoffs([
      { rowId: 'future', featureCutoff: '2024-01-10T00:00:00Z', features: [{ name: 'news_sentiment', value: 1, availableAt: '2024-01-10T00:01:00Z', sourceId: 'news' }] },
      { rowId: 'overlap', featureCutoff: '2024-01-10T00:00:00Z', outcomeWindowStart: '2024-01-09T00:00:00Z', features: [] },
      { rowId: 'invalid', featureCutoff: 'not-a-date', features: [] },
    ]);
    expect(report.valid).toBe(false);
    expect(report.violations.map((violation) => violation.code)).toEqual(expect.arrayContaining(['FEATURE_AFTER_CUTOFF', 'OUTCOME_OVERLAP', 'INVALID_TIMESTAMP']));
  });

  it('counts explicit missing feature values without inventing imputation', () => {
    const report = validateFeatureCutoffs([{ rowId: 'missing', featureCutoff: '2024-01-10T00:00:00Z', features: [{ name: 'macro', value: null, availableAt: '2024-01-09T00:00:00Z', sourceId: 'macro' }] }]);
    expect(report.valid).toBe(true);
    expect(report.missingValueCount).toBe(1);
  });
});
