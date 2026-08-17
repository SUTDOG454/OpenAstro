# Company Research TypeScript Layer

This directory contains the provider-neutral company-research helpers added from the inspected finance-query architecture.

`financialStatement.ts` maps Yahoo-style fundamentals-timeseries responses into a canonical statement shape:

```ts
{
  symbol: 'AAPL',
  statementType: 'income',
  frequency: 'annual',
  statement: {
    TotalRevenue: { '2024-09-30': 391035000000 },
    NetIncome: { '2024-09-30': 100913000000 }
  },
  providerId: 'yahoo'
}
```

The mapper strips `annual`, `quarterly`, and `trailing` metric prefixes, ignores null or undated points, extracts direct or nested numeric values, uppercases symbols, and throws typed parse errors for malformed, empty, or unusable responses.

`fmpCompanyAdapter.ts` maps FMP profile, executive, and company-outlook payloads into canonical records. Provider-specific names such as `mktCap`, `volAvg`, `companyName`, and `fullTimeEmployees` are converted to stable application names. Unknown profile fields and untyped outlook sections remain under `extensions` instead of being discarded. Executive titles are passed through the canonical C-level detector.

The source extracts remain preserved under `data/extractions/company-research/` and are not treated as executable authority. The TypeScript layer is an explicitly implemented adapter with tests, not a claim that the source provider data is complete or current.

Run the tests from this directory with:

```bash
npm install
npm test
npm run typecheck
```
