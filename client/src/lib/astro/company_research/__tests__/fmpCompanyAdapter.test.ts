import {
  mapFmpCompanyOutlook,
  mapFmpCompanyProfile,
  mapFmpKeyExecutives,
} from '../fmpCompanyAdapter';

describe('FMP company profile adapter', () => {
  test('maps provider profile fields into canonical company fields', () => {
    const result = mapFmpCompanyProfile([{
      symbol: 'AAPL',
      price: 178.72,
      beta: 1.286,
      volAvg: 58405568,
      mktCap: 2794000000000,
      companyName: 'Apple Inc.',
      currency: 'USD',
      cik: '0000320193',
      exchange: 'NASDAQ Global Select',
      exchangeShortName: 'NASDAQ',
      industry: 'Consumer Electronics',
      sector: 'Technology',
      country: 'US',
      fullTimeEmployees: '164000',
      ipoDate: '1980-12-12',
      isEtf: false,
      isActivelyTrading: true,
      unknownProviderField: 'preserve me',
    }]);

    expect(result).toMatchObject({
      symbol: 'AAPL',
      companyName: 'Apple Inc.',
      marketCap: 2794000000000,
      averageVolume: 58405568,
      fullTimeEmployees: 164000,
      ipoDate: '1980-12-12',
      isEtf: false,
      isActivelyTrading: true,
    });
    expect(result.extensions).toEqual({ unknownProviderField: 'preserve me' });
  });

  test('returns an empty profile for unsupported payloads', () => {
    expect(mapFmpCompanyProfile(null)).toEqual({});
    expect(mapFmpCompanyProfile({ error: 'not found' })).toEqual({});
  });
});

describe('FMP executive adapter', () => {
  test('maps executive fields and canonicalizes recognized C-level roles', () => {
    const result = mapFmpKeyExecutives([
      {
        title: 'Chief Executive Officer',
        name: 'Tim Cook',
        pay: 16425933,
        currencyPay: 'USD',
        gender: 'male',
        yearBorn: 1960,
        titleSince: '2011-08-24',
      },
      { title: 'Chief Financial Officer', name: 'Luca Maestri', yearBorn: 1963 },
      { title: 'Vice President, Marketing', name: 'Example Person' },
    ]);

    expect(result).toEqual([
      expect.objectContaining({
        title: 'Chief Executive Officer',
        name: 'Tim Cook',
        pay: 16425933,
        isCLevel: true,
        cLevelRole: 'CEO',
      }),
      expect.objectContaining({
        title: 'Chief Financial Officer',
        isCLevel: true,
        cLevelRole: 'CFO',
      }),
      expect.objectContaining({
        title: 'Vice President, Marketing',
        isCLevel: false,
      }),
    ]);
  });

  test('returns no executives for non-array payloads', () => {
    expect(mapFmpKeyExecutives({ keyExecutives: [] })).toEqual([]);
  });
});

describe('FMP company outlook adapter', () => {
  test('composes profile, executives, and untyped provider sections', () => {
    const result = mapFmpCompanyOutlook({
      profile: { symbol: 'MSFT', companyName: 'Microsoft Corporation' },
      keyExecutives: [{ title: 'CEO', name: 'Satya Nadella' }],
      metrics: [{ date: '2024-06-30', revenue: 245000000000 }],
      ratios: [{ currentRatio: 1.2 }],
    });

    expect(result.profile).toMatchObject({ symbol: 'MSFT', companyName: 'Microsoft Corporation' });
    expect(result.executives[0]).toMatchObject({ isCLevel: true, cLevelRole: 'CEO' });
    expect(result.extensions).toEqual({
      metrics: [{ date: '2024-06-30', revenue: 245000000000 }],
      ratios: [{ currentRatio: 1.2 }],
    });
  });
});
