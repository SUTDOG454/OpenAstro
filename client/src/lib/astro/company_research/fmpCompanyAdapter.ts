import { detectCLevel, type CLevelRole } from './company_research.executive';

export interface NormalizedCompanyProfile {
  symbol?: string;
  companyName?: string;
  price?: number;
  beta?: number;
  averageVolume?: number;
  marketCap?: number;
  lastDividend?: number;
  range?: string;
  changes?: number;
  currency?: string;
  cik?: string;
  isin?: string;
  cusip?: string;
  exchange?: string;
  exchangeShortName?: string;
  industry?: string;
  website?: string;
  description?: string;
  ceo?: string;
  sector?: string;
  country?: string;
  fullTimeEmployees?: number;
  phone?: string;
  address?: string;
  city?: string;
  state?: string;
  zip?: string;
  dcfDiff?: number;
  dcf?: number;
  image?: string;
  ipoDate?: string;
  defaultImage?: boolean;
  isEtf?: boolean;
  isActivelyTrading?: boolean;
  isAdr?: boolean;
  isFund?: boolean;
  extensions?: Record<string, unknown>;
}

export interface NormalizedExecutive {
  title?: string;
  name?: string;
  pay?: number;
  currencyPay?: string;
  gender?: string;
  yearBorn?: number;
  titleSince?: string;
  isCLevel: boolean;
  cLevelRole?: CLevelRole;
  tenureYears?: number;
}

export interface NormalizedCompanyResearch {
  profile?: NormalizedCompanyProfile;
  executives: NormalizedExecutive[];
  extensions?: Record<string, unknown>;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

const PROFILE_KEYS = new Set([
  'symbol', 'companyName', 'price', 'beta', 'volAvg', 'mktCap', 'lastDiv', 'range', 'changes',
  'currency', 'cik', 'isin', 'cusip', 'exchange', 'exchangeShortName', 'industry', 'website',
  'description', 'ceo', 'sector', 'country', 'fullTimeEmployees', 'phone', 'address', 'city',
  'state', 'zip', 'dcfDiff', 'dcf', 'image', 'ipoDate', 'defaultImage', 'isEtf',
  'isActivelyTrading', 'isAdr', 'isFund',
]);

function firstRecord(payload: unknown): Record<string, unknown> | undefined {
  if (Array.isArray(payload)) return payload.find((item) => isRecord(item) && Object.keys(item).some((key) => PROFILE_KEYS.has(key)));
  if (isRecord(payload) && Object.keys(payload).some((key) => PROFILE_KEYS.has(key))) return payload;
  return undefined;
}

function optionalString(value: unknown): string | undefined {
  return typeof value === 'string' && value.length > 0 ? value : undefined;
}

function optionalNumber(value: unknown): number | undefined {
  return typeof value === 'number' && Number.isFinite(value) ? value : undefined;
}

function optionalBoolean(value: unknown): boolean | undefined {
  return typeof value === 'boolean' ? value : undefined;
}

function optionalInteger(value: unknown): number | undefined {
  return typeof value === 'number' && Number.isInteger(value) ? value : undefined;
}

function mapProfile(raw: Record<string, unknown>): NormalizedCompanyProfile {
  const knownKeys = new Set([
    'symbol', 'companyName', 'price', 'beta', 'volAvg', 'mktCap', 'lastDiv', 'range', 'changes',
    'currency', 'cik', 'isin', 'cusip', 'exchange', 'exchangeShortName', 'industry', 'website',
    'description', 'ceo', 'sector', 'country', 'fullTimeEmployees', 'phone', 'address', 'city',
    'state', 'zip', 'dcfDiff', 'dcf', 'image', 'ipoDate', 'defaultImage', 'isEtf',
    'isActivelyTrading', 'isAdr', 'isFund',
  ]);
  const extensions = Object.fromEntries(Object.entries(raw).filter(([key]) => !knownKeys.has(key)));

  const employeesRaw = raw.fullTimeEmployees;
  const employees = typeof employeesRaw === 'string' ? Number(employeesRaw) : employeesRaw;

  return {
    symbol: optionalString(raw.symbol),
    companyName: optionalString(raw.companyName),
    price: optionalNumber(raw.price),
    beta: optionalNumber(raw.beta),
    averageVolume: optionalNumber(raw.volAvg),
    marketCap: optionalNumber(raw.mktCap),
    lastDividend: optionalNumber(raw.lastDiv),
    range: optionalString(raw.range),
    changes: optionalNumber(raw.changes),
    currency: optionalString(raw.currency),
    cik: optionalString(raw.cik),
    isin: optionalString(raw.isin),
    cusip: optionalString(raw.cusip),
    exchange: optionalString(raw.exchange),
    exchangeShortName: optionalString(raw.exchangeShortName),
    industry: optionalString(raw.industry),
    website: optionalString(raw.website),
    description: optionalString(raw.description),
    ceo: optionalString(raw.ceo),
    sector: optionalString(raw.sector),
    country: optionalString(raw.country),
    fullTimeEmployees: optionalNumber(employees),
    phone: optionalString(raw.phone),
    address: optionalString(raw.address),
    city: optionalString(raw.city),
    state: optionalString(raw.state),
    zip: optionalString(raw.zip),
    dcfDiff: optionalNumber(raw.dcfDiff),
    dcf: optionalNumber(raw.dcf),
    image: optionalString(raw.image),
    ipoDate: optionalString(raw.ipoDate),
    defaultImage: optionalBoolean(raw.defaultImage),
    isEtf: optionalBoolean(raw.isEtf),
    isActivelyTrading: optionalBoolean(raw.isActivelyTrading),
    isAdr: optionalBoolean(raw.isAdr),
    isFund: optionalBoolean(raw.isFund),
    ...(Object.keys(extensions).length > 0 ? { extensions } : {}),
  };
}

export function mapFmpCompanyProfile(payload: unknown): NormalizedCompanyProfile {
  const profile = firstRecord(payload);
  return profile ? mapProfile(profile) : {};
}

export function mapFmpKeyExecutives(payload: unknown): NormalizedExecutive[] {
  if (!Array.isArray(payload)) return [];

  return payload.filter(isRecord).map((raw) => {
    const title = optionalString(raw.title);
    const detection = title ? detectCLevel(title) : { isCLevel: false as const };
    return {
      title,
      name: optionalString(raw.name),
      pay: optionalNumber(raw.pay),
      currencyPay: optionalString(raw.currencyPay),
      gender: optionalString(raw.gender),
      yearBorn: optionalInteger(raw.yearBorn),
      titleSince: optionalString(raw.titleSince),
      isCLevel: detection.isCLevel,
      ...(detection.isCLevel ? { cLevelRole: detection.role } : {}),
    };
  });
}

export function mapFmpCompanyOutlook(payload: unknown): NormalizedCompanyResearch {
  const outlook = isRecord(payload) ? payload : {};
  const profile = outlook.profile === undefined ? undefined : mapFmpCompanyProfile(outlook.profile);
  const executives = mapFmpKeyExecutives(outlook.keyExecutives);
  const extensions = Object.fromEntries(
    Object.entries(outlook).filter(([key]) => !['profile', 'keyExecutives'].includes(key)),
  );

  return {
    ...(profile ? { profile } : {}),
    executives,
    ...(Object.keys(extensions).length > 0 ? { extensions } : {}),
  };
}
