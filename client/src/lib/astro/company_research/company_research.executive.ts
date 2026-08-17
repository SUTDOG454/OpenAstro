export interface Executive {
  title: string;
  tenureYears?: number;
  isCLevel?: boolean;
  cLevelRole?: CLevelRole;
}

export type CLevelRole =
  | 'CEO'
  | 'CFO'
  | 'COO'
  | 'CTO'
  | 'CMO'
  | 'CIO'
  | 'CHRO'
  | 'General Counsel';

export interface CLevelDetection {
  isCLevel: true;
  role: CLevelRole;
}

export interface NonCLevelDetection {
  isCLevel: false;
}

const ABBREVIATION_ROLES: readonly CLevelRole[] = [
  'CEO',
  'CFO',
  'COO',
  'CTO',
  'CMO',
  'CIO',
  'CHRO',
];

const CHIEF_ROLE_PATTERNS: readonly [RegExp, CLevelRole][] = [
  [/\bchief executive officer\b/i, 'CEO'],
  [/\bchief financial officer\b/i, 'CFO'],
  [/\bchief operating officer\b/i, 'COO'],
  [/\bchief technology officer\b/i, 'CTO'],
  [/\bchief marketing officer\b/i, 'CMO'],
  [/\bchief information officer\b/i, 'CIO'],
  [/\bchief human resources officer\b/i, 'CHRO'],
  [/\bgeneral counsel\b/i, 'General Counsel'],
];

/** Detects the canonical C-level role represented by an executive title. */
export function detectCLevel(title: string): CLevelDetection | NonCLevelDetection {
  const normalized = title.trim();
  if (!normalized) return { isCLevel: false };

  const abbreviation = normalized.toUpperCase().match(/\bC(?:EO|FO|OO|TO|MO|IO|HRO)\b/)?.[0];
  if (abbreviation && ABBREVIATION_ROLES.includes(abbreviation as CLevelRole)) {
    return { isCLevel: true, role: abbreviation as CLevelRole };
  }

  for (const [pattern, role] of CHIEF_ROLE_PATTERNS) {
    if (pattern.test(normalized)) return { isCLevel: true, role };
  }

  return { isCLevel: false };
}

export const C_LEVEL_TENURE_MIN_YEARS = 1;
export const C_LEVEL_TENURE_MAX_YEARS = 20;

/** Normalize a C-level tenure average to the executive engine's 0–1 score range. */
export function normalizeCLevelTenure(averageTenureYears: number): number {
  if (!Number.isFinite(averageTenureYears)) return 0;

  const normalized =
    (averageTenureYears - C_LEVEL_TENURE_MIN_YEARS) /
    (C_LEVEL_TENURE_MAX_YEARS - C_LEVEL_TENURE_MIN_YEARS);

  return Math.max(0, Math.min(1, normalized));
}

/**
 * Returns the normalized average tenure of C-level executives.
 * The executive engine contract normalizes tenure from 1 year to 20 years.
 */
export function getCLevelTenureScore(executives: Executive[]): number {
  const cLevelTenures = executives
    .filter((executive) => executive.isCLevel === true)
    .map((executive) => executive.tenureYears)
    .filter((tenure): tenure is number => Number.isFinite(tenure));

  if (cLevelTenures.length === 0) return 0;

  const averageTenure = cLevelTenures.reduce((sum, tenure) => sum + tenure, 0) / cLevelTenures.length;
  return normalizeCLevelTenure(averageTenure);
}
