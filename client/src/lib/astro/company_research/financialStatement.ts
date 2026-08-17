export type StatementType = 'income' | 'balance' | 'cashflow' | (string & {});
export type StatementFrequency = 'annual' | 'quarterly' | 'trailing' | (string & {});

export interface FinancialStatementMappingOptions {
  symbol: string;
  statementType: StatementType;
  frequency: StatementFrequency;
  providerId?: string | null;
}

export interface FinancialStatementPoint {
  date: string;
  value: number;
  rawValue: unknown;
  sourcePath: string;
}

export interface ProviderNeutralFinancialStatement {
  symbol: string;
  statementType: string;
  frequency: string;
  statement: Record<string, Record<string, number>>;
  providerId?: string | null;
  evidenceClass?: 'source_derived';
  status?: 'normalized' | 'unavailable' | 'pending_review';
  points?: FinancialStatementPoint[];
  provenance?: {
    sourcePayloadShape: 'yahoo_timeseries' | 'fmp_statement' | 'generic';
    sourcePaths: string[];
    transformation: string;
  };
  warnings?: string[];
}

export class FinancialStatementParseError extends Error {
  readonly code: 'INVALID_RESPONSE' | 'EMPTY_RESULT' | 'NO_USABLE_DATA';
  readonly symbol: string;

  constructor(code: FinancialStatementParseError['code'], symbol: string, message: string) {
    super(message);
    this.name = 'FinancialStatementParseError';
    this.code = code;
    this.symbol = symbol;
  }
}

interface RawTimeseriesResult {
  meta?: { type?: unknown };
  [key: string]: unknown;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function asObjectArray(value: unknown): Record<string, unknown>[] {
  return Array.isArray(value) ? value.filter(isRecord) : [];
}

/** Remove provider frequency prefixes while retaining the provider metric name. */
export function stripFrequencyPrefix(name: string): string {
  return name.replace(/^(annual|quarterly|quarter|trailing[_-]?twelve[_-]?months|trailing)[_-]?/i, '');
}

/** Extract finite numeric values from provider reported-value wrappers. */
export function extractReportedValue(reportedValue: unknown): number | undefined {
  if (!isRecord(reportedValue)) return undefined;
  for (const key of ['raw', 'parsedValue']) {
    const candidate = reportedValue[key];
    if (typeof candidate === 'number' && Number.isFinite(candidate)) return candidate;
    if (isRecord(candidate)) {
      const nested = extractReportedValue(candidate);
      if (nested !== undefined) return nested;
    }
  }
  return undefined;
}

function numericValue(value: unknown): number | undefined {
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  if (typeof value === 'string' && value.trim() !== '') {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : undefined;
  }
  return extractReportedValue(value);
}

function readMetricName(result: RawTimeseriesResult): string {
  const meta = isRecord(result.meta) ? result.meta : undefined;
  const types = meta?.type;
  return Array.isArray(types) && typeof types[0] === 'string' ? types[0] : '';
}

function dateFromPoint(point: Record<string, unknown>): string | undefined {
  for (const key of ['asOfDate', 'periodEndDate', 'date', 'fillingDate']) {
    if (typeof point[key] === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(point[key] as string)) return point[key] as string;
  }
  return undefined;
}

function looksLikeFmp(raw: Record<string, unknown>): boolean {
  return Array.isArray(raw.data) || Array.isArray(raw.results);
}

function mapYahoo(raw: Record<string, unknown>, options: FinancialStatementMappingOptions): ProviderNeutralFinancialStatement {
  if (!isRecord(raw.timeseries) || !Array.isArray(raw.timeseries.result)) {
    throw new FinancialStatementParseError('INVALID_RESPONSE', options.symbol.trim(), 'Financial statement response must contain timeseries.result[]');
  }
  const results = asObjectArray(raw.timeseries.result);
  if (results.length === 0) throw new FinancialStatementParseError('EMPTY_RESULT', options.symbol.trim(), `No ${options.frequency} ${options.statementType} data found`);
  const statement: Record<string, Record<string, number>> = {};
  const points: FinancialStatementPoint[] = [];
  for (let index = 0; index < results.length; index += 1) {
    const result = results[index];
    const providerMetricName = readMetricName(result as RawTimeseriesResult);
    if (!providerMetricName) continue;
    const metricName = stripFrequencyPrefix(providerMetricName);
    const dataPoints = asObjectArray(result[providerMetricName]);
    const dateValues: Record<string, number> = {};
    for (let pointIndex = 0; pointIndex < dataPoints.length; pointIndex += 1) {
      const point = dataPoints[pointIndex];
      const asOfDate = dateFromPoint(point);
      if (!asOfDate) continue;
      const value = extractReportedValue(point.reportedValue ?? point.value ?? point);
      if (value === undefined) continue;
      dateValues[asOfDate] = value;
      points.push({ date: asOfDate, value, rawValue: point, sourcePath: `timeseries.result[${index}].${providerMetricName}[${pointIndex}]` });
    }
    if (Object.keys(dateValues).length > 0) statement[metricName] = dateValues;
  }
  if (Object.keys(statement).length === 0) throw new FinancialStatementParseError('NO_USABLE_DATA', options.symbol.trim(), `No ${options.frequency} ${options.statementType} data found`);
  return {
    symbol: options.symbol.trim().toUpperCase(), statementType: options.statementType, frequency: options.frequency, statement,
    providerId: options.providerId ?? null, evidenceClass: 'source_derived', status: 'normalized', points,
    provenance: { sourcePayloadShape: 'yahoo_timeseries', sourcePaths: points.map((point) => point.sourcePath), transformation: 'flatten timeseries, strip frequency prefixes, unwrap finite numeric values' },
    warnings: [],
  };
}

function mapFmp(raw: Record<string, unknown>, options: FinancialStatementMappingOptions): ProviderNeutralFinancialStatement {
  const rows = Array.isArray(raw.data) ? raw.data : Array.isArray(raw.results) ? raw.results : [];
  if (rows.length === 0) throw new FinancialStatementParseError('EMPTY_RESULT', options.symbol.trim(), `No ${options.frequency} ${options.statementType} data found`);
  const statement: Record<string, Record<string, number>> = {};
  const points: FinancialStatementPoint[] = [];
  for (let rowIndex = 0; rowIndex < rows.length; rowIndex += 1) {
    const row = rows[rowIndex];
    if (!isRecord(row)) continue;
    const date = dateFromPoint(row);
    if (!date) continue;
    for (const [key, rawValue] of Object.entries(row)) {
      if (['date', 'fillingDate', 'calendarYear', 'period', 'symbol', 'reportedCurrency'].includes(key)) continue;
      const value = numericValue(rawValue);
      if (value === undefined) continue;
      const metric = stripFrequencyPrefix(key);
      statement[metric] ??= {};
      statement[metric][date] = value;
      points.push({ date, value, rawValue, sourcePath: `data[${rowIndex}].${key}` });
    }
  }
  if (Object.keys(statement).length === 0) throw new FinancialStatementParseError('NO_USABLE_DATA', options.symbol.trim(), `No ${options.frequency} ${options.statementType} data found`);
  return {
    symbol: options.symbol.trim().toUpperCase(), statementType: options.statementType, frequency: options.frequency, statement,
    providerId: options.providerId ?? null, evidenceClass: 'source_derived', status: 'normalized', points,
    provenance: { sourcePayloadShape: 'fmp_statement', sourcePaths: points.map((point) => point.sourcePath), transformation: 'flatten FMP statement rows, normalize dates and metric names, unwrap finite numeric values' },
    warnings: [],
  };
}

function mapGeneric(raw: Record<string, unknown>, options: FinancialStatementMappingOptions): ProviderNeutralFinancialStatement {
  const source = isRecord(raw.statement) ? raw.statement : raw;
  const statement: Record<string, Record<string, number>> = {};
  const points: FinancialStatementPoint[] = [];
  for (const [metric, values] of Object.entries(source)) {
    if (!isRecord(values)) continue;
    for (const [date, rawValue] of Object.entries(values)) {
      if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) continue;
      const value = numericValue(rawValue);
      if (value === undefined) continue;
      const canonicalMetric = stripFrequencyPrefix(metric);
      statement[canonicalMetric] ??= {};
      statement[canonicalMetric][date] = value;
      points.push({ date, value, rawValue, sourcePath: `statement.${metric}.${date}` });
    }
  }
  if (Object.keys(statement).length === 0) throw new FinancialStatementParseError('NO_USABLE_DATA', options.symbol.trim(), 'No dated finite numeric statement values found');
  return {
    symbol: options.symbol.trim().toUpperCase(), statementType: options.statementType, frequency: options.frequency, statement,
    providerId: options.providerId ?? null, evidenceClass: 'source_derived', status: 'normalized', points,
    provenance: { sourcePayloadShape: 'generic', sourcePaths: points.map((point) => point.sourcePath), transformation: 'map generic metric/date object and unwrap finite numeric values' },
    warnings: ['Generic payload shape was accepted; provider-specific field semantics require review.'],
  };
}

export function mapProviderNeutralFinancialStatement(raw: unknown, options: FinancialStatementMappingOptions): ProviderNeutralFinancialStatement {
  let payload = raw;
  if (typeof payload === 'string') {
    try { payload = JSON.parse(payload) as unknown; }
    catch (error) { throw new FinancialStatementParseError('INVALID_RESPONSE', options.symbol.trim(), `Invalid financial statement JSON: ${error instanceof Error ? error.message : String(error)}`); }
  }
  if (!isRecord(payload)) throw new FinancialStatementParseError('INVALID_RESPONSE', options.symbol.trim(), 'Financial statement response must be an object');
  if (isRecord(payload.timeseries)) return mapYahoo(payload, options);
  if (looksLikeFmp(payload)) return mapFmp(payload, options);
  return mapGeneric(payload, options);
}

export const parseFinancialStatement = mapProviderNeutralFinancialStatement;

export function parseFinancialStatementJson(json: string, options: FinancialStatementMappingOptions): ProviderNeutralFinancialStatement {
  return mapProviderNeutralFinancialStatement(json, options);
}
