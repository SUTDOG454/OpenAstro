import {
  FinancialStatementParseError,
  extractReportedValue,
  mapProviderNeutralFinancialStatement,
  parseFinancialStatementJson,
  stripFrequencyPrefix,
} from '../financialStatement';

describe('financial statement normalization helpers', () => {
  test('strips supported provider frequency prefixes', () => {
    expect(stripFrequencyPrefix('annualTotalRevenue')).toBe('TotalRevenue');
    expect(stripFrequencyPrefix('quarterlyNetIncome')).toBe('NetIncome');
    expect(stripFrequencyPrefix('trailingMarketCap')).toBe('MarketCap');
    expect(stripFrequencyPrefix('SomeOtherMetric')).toBe('SomeOtherMetric');
  });

  test('extracts direct and nested raw numeric values', () => {
    expect(extractReportedValue({ raw: 123.45 })).toBe(123.45);
    expect(extractReportedValue({ raw: { parsedValue: 123000000000 } })).toBe(123000000000);
    expect(extractReportedValue({ raw: '123.45' })).toBeUndefined();
    expect(extractReportedValue({ raw: { parsedValue: '123.45' } })).toBeUndefined();
    expect(extractReportedValue(null)).toBeUndefined();
  });
});

describe('provider-neutral financial statement mapping', () => {
  const samplePayload = {
    timeseries: {
      result: [
        {
          meta: { symbol: ['AAPL'], type: ['annualTotalRevenue'] },
          annualTotalRevenue: [
            { asOfDate: '2024-09-30', reportedValue: { raw: 391035000000 } },
            { asOfDate: '2023-09-30', reportedValue: { raw: 383285000000 } },
            { asOfDate: '', reportedValue: { raw: 1 } },
            { asOfDate: '2022-09-30', reportedValue: null },
          ],
        },
        {
          meta: { type: ['annualNetIncome'] },
          annualNetIncome: [
            { asOfDate: '2024-09-30', reportedValue: { raw: { parsedValue: 100913000000 } } },
          ],
        },
      ],
    },
  };

  test('flattens provider payload into metric-to-date maps', () => {
    const result = mapProviderNeutralFinancialStatement(samplePayload, {
      symbol: 'aapl',
      statementType: 'income',
      frequency: 'annual',
      providerId: 'yahoo',
    });

    expect(result).toMatchObject({
      symbol: 'AAPL',
      statementType: 'income',
      frequency: 'annual',
      providerId: 'yahoo',
      statement: {
        TotalRevenue: {
          '2024-09-30': 391035000000,
          '2023-09-30': 383285000000,
        },
        NetIncome: {
          '2024-09-30': 100913000000,
        },
      },
      evidenceClass: 'source_derived',
      status: 'normalized',
      provenance: { sourcePayloadShape: 'yahoo_timeseries' },
    });
    expect(result.points).toHaveLength(3);
  });

  test('accepts serialized JSON through the convenience parser', () => {
    const result = parseFinancialStatementJson(JSON.stringify(samplePayload), {
      symbol: 'msft',
      statementType: 'income',
      frequency: 'annual',
    });
    expect(result.symbol).toBe('MSFT');
    expect(result.providerId).toBeNull();
  });

  test('rejects malformed response shapes', () => {
    expect(() => mapProviderNeutralFinancialStatement({}, {
      symbol: 'AAPL',
      statementType: 'income',
      frequency: 'annual',
    })).toThrowError(FinancialStatementParseError);

    expect(() => parseFinancialStatementJson('{bad json', {
      symbol: 'AAPL',
      statementType: 'income',
      frequency: 'annual',
    })).toThrowError(/Invalid financial statement JSON/);
  });

  test('rejects empty and unusable timeseries results', () => {
    const options = { symbol: 'INVALID', statementType: 'income', frequency: 'annual' } as const;
    expect(() => mapProviderNeutralFinancialStatement({ timeseries: { result: [] } }, options)).toThrowError(/No annual income data found/);
    expect(() => mapProviderNeutralFinancialStatement({
      timeseries: {
        result: [{ meta: { type: ['annualRevenue'] }, annualRevenue: [{ asOfDate: '2024-01-01', reportedValue: { raw: 'not numeric' } }] }],
      },
    }, options)).toThrowError(/No annual income data found/);
  });
});
