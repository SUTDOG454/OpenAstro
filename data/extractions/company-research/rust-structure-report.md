# Finance-Query Rust Structure Inspection

## Executive summary

The extracted Rust source is organized as a provider-adapter layer, typed financial DTOs, a provider-neutral normalization layer, and an ancillary research-report metadata layer. The clearest canonical boundary is `FinancialStatement`, which converts Yahoo-style nested timeseries payloads into a symbol/frequency/statement-type record containing `metric -> date -> numeric value` maps. FMP adapters remain provider-specific and expose richer typed DTOs for company profiles, executives, three-statement data, ratios, valuation, ratings, and growth.

The source is useful as a **reference architecture**, not as a drop-in TypeScript module. The extracted files use Rust traits, generic formatting, provider enums, crate-local errors, async HTTP clients, and `serde` attributes that require explicit mapping before use in OpenAstro.

## Layered architecture

| Layer | Extracted artifact | Primary responsibility | OpenAstro relevance |
|---|---|---|---|
| Provider adapter | `finance-query/src/adapters/fmp/quote/company.rs` | FMP company profiles, executives, market cap, outlook, peers, and delisted-company endpoints | Company identity, executive inputs, peers, market-cap history |
| Provider adapter | `finance-query/src/adapters/fmp/fundamentals/core.rs` | Income statement, balance sheet, cash flow, as-reported, and full-statement endpoints | Historical financial facts and filing provenance |
| Provider analysis | `finance-query/src/adapters/fmp/fundamentals/analysis.rs` | Ratios, key metrics, enterprise value, DCF, ratings, and growth endpoints | Derived fundamentals and valuation signals |
| Provider-neutral model | `finance-query/src/models/fundamentals/response.rs` | Flattens nested timeseries into canonical statement maps | Best candidate for a normalized financial-fact contract |
| Provider-neutral model | `finance-query/src/models/fundamentals/financial_data.rs` | Generic formatted/raw/pretty financial data representation | Useful presentation and raw-value separation pattern |
| Discovery metadata | `finance-query/src/models/discovery/search/research.rs` | Search-result report metadata | Ancillary evidence links, not financial facts |

## Company and executive model

`CompanyProfileDTO` is a sparse, provider-shaped profile. Almost every field is optional, including symbol, price, beta, average volume, market capitalization, dividend, company name, identifiers, industry, website, description, CEO, sector, geography, employee count, DCF values, IPO date, and security flags such as ETF, ADR, fund, and active-trading status. JSON names are normalized into Rust snake_case through explicit `serde(rename = ...)` attributes.

`KeyExecutiveDTO` contains title, name, compensation, compensation currency, gender, birth year, and `titleSince`. It does **not** contain a directly supplied tenure in years. Tenure must therefore be derived from `titleSince` and an explicit as-of date, with missing or malformed dates retained as unknown rather than treated as zero. This is important for the OpenAstro `getCLevelTenureScore` integration.

`CompanyOutlookDTO` composes profile, metrics, ratios, insider trades, key executives, stock news, and ratings. Several sections are intentionally left as `serde_json::Value` or vectors of untyped JSON values, indicating that the upstream payload is flexible and not fully normalized at this layer. `StockPeersDTO` provides a symbol and peer list; the adapter converts peers into canonical `SimilarSymbol` records with a default score of `0.0`, then truncates to a requested limit.

## Financial statement model

The FMP core adapter defines separate DTOs for income statement, balance sheet, and cash flow. These are broad financial statement records with optional scalar fields, filing chronology, currency, CIK, fiscal period, and SEC filing links. The income statement includes revenue, cost of revenue, gross profit, operating expenses, EBITDA, operating income, income before tax, net income, EPS, and share counts. The balance sheet includes cash, investments, receivables, inventory, assets, liabilities, equity, total debt, and net debt. The cash-flow model includes operating, investing, and financing flows, working-capital changes, debt repayment, dividends, cash balances, and related items.

The adapter also exposes as-reported and full-statement functions returning raw JSON values rather than imposing typed DTO schemas. This preserves provider data when the typed model is incomplete, but it creates a review boundary: raw payloads should be stored with endpoint, retrieval date, provider, symbol, period, and content hash before any normalization.

## Analysis and valuation model

`FinancialRatiosDTO` covers liquidity, margins, returns, leverage, valuation multiples, dividend yield, and payout ratio. `KeyMetricsDTO` overlaps with ratios but adds per-share metrics, market capitalization, enterprise value, valuation multiples, earnings/free-cash-flow yields, debt ratios, and current ratio. `EnterpriseValueDTO` decomposes enterprise value into stock price, shares, market capitalization, cash subtraction, and debt addition.

The DCF models are intentionally small: current DCF has symbol, date, DCF value, and stock price; historical DCF has symbol, date, DCF value, and price. `CompanyRatingDTO` combines an overall rating and score with component scores/recommendations for DCF, ROE, ROA, debt-to-equity, PE, and PB. `FinancialGrowthDTO` provides growth rates for revenue, gross profit, EBIT, operating income, net income, EPS, dividends, cash flow, working capital, assets, book value, debt, R&D, and SG&A.

The analysis adapter uses provider-specific endpoint defaults: ratios, key metrics, enterprise value, and growth default to four records; historical DCF defaults to ten; historical ratings and historical market capitalization use one hundred. These defaults must be represented as ingestion settings, not hidden assumptions in a canonical scoring layer.

## Canonical normalization behavior

`FinancialStatement` is the most important normalization structure. Its fields are `symbol`, `statementType`, `frequency`, `statement`, and optional `providerId`. The `statement` map has the shape:

```json
{
  "TotalRevenue": {
    "2024-09-30": 391035000000
  },
  "NetIncome": {
    "2024-09-30": 100913000000
  }
}
```

The parser reads `timeseries.result[]`, uses `meta.type[0]` to identify the metric, strips `annual`, `quarterly`, or `trailing` prefixes, reads the matching array from the result object, ignores null points and missing dates, and extracts either a direct numeric `reportedValue.raw` or a nested `reportedValue.raw.parsedValue`. It uppercases the symbol and returns a structured error when no result or no usable statement values remain.

`FinancialData<F>` separates numeric representation from semantic fields through a generic `Format` parameter. The default representation retains formatted values containing raw and display forms; `Raw` yields direct numeric values; `Pretty` yields human-readable strings. This is a strong pattern for separating calculation inputs from presentation output without duplicating the field schema.

## Research-report model

`ResearchReports` is a transparent wrapper around `Vec<ResearchReport>` with dereferencing and iteration support, plus optional dataframe conversion. `ResearchReport` contains only headline, author, publication timestamp, ID, and provider. It is an evidence-discovery record rather than a financial-data record. In OpenAstro it should be linked to source citations or filings, not merged into numeric company fundamentals.

## Recommended OpenAstro mapping

| Source concept | Proposed canonical field group | Required provenance |
|---|---|---|
| Company profile | `company.identity`, `company.security`, `company.location`, `company.lifecycle` | Provider, endpoint, symbol, retrieval time, raw hash |
| Key executive | `company.executives[]` | Name, title, title-since, as-of date, provider, privacy status |
| Income/balance/cash flow | `company.financial_statements[]` | Statement type, period, currency, filing/accepted dates, source link |
| Ratios/key metrics | `company.fundamentals.ratios` and `company.fundamentals.metrics` | Period, calculation basis, provider, raw record hash |
| DCF/enterprise value/ratings | `company.valuation` and `company.ratings` | Valuation date, methodology/provider, input assumptions, raw hash |
| Growth | `company.growth[]` | Period-over-period basis, fiscal period, provider |
| Research reports | `company.evidence.research_reports[]` | Provider, publication date, report ID, URL if available |

## Important implementation cautions

The source uses many `Option<T>` fields, so missing data is a first-class state and must not be converted to zero. A few provider field names are irregular or misspelled in the source contract, such as `fillingDate` and `otherInvestingActivites`; mappings should preserve the original JSON key while exposing a corrected canonical name with an audit note. Financial values may have currencies and different period frequencies, so normalization must not mix annual and quarterly values without explicit period metadata.

Executive tenure is not directly available in `KeyExecutiveDTO`. The OpenAstro C-level scoring layer should derive tenure from `titleSince` only when the date is valid and should retain `tenureYears: null` otherwise. The current C-level detector can classify titles, but a future adapter should map provider titles such as `Chief Executive Officer` and `Chief Financial Officer` into canonical `CEO` and `CFO` roles before scoring.

## References

[1]: https://github.com/SUTDOG454/finance-query "SUTDOG454/finance-query repository"
[2]: ./finance-query/src/adapters/fmp/quote/company.rs "FMP company and executive adapter extract"
[3]: ./finance-query/src/adapters/fmp/fundamentals/core.rs "FMP core financial statement adapter extract"
[4]: ./finance-query/src/adapters/fmp/fundamentals/analysis.rs "FMP financial analysis adapter extract"
[5]: ./finance-query/src/models/fundamentals/response.rs "Canonical financial statement response extract"
[6]: ./finance-query/src/models/fundamentals/financial_data.rs "Generic formatted/raw/pretty financial data extract"
[7]: ./finance-query/src/models/discovery/search/research.rs "Research-report metadata extract"
