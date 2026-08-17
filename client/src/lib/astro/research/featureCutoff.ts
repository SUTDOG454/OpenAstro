export interface ResearchFeature {
  name: string;
  value: number | string | null;
  availableAt: string;
  sourceId: string;
}

export interface ResearchRow {
  rowId: string;
  featureCutoff: string;
  outcomeWindowStart?: string;
  features: ResearchFeature[];
}

export interface FeatureCutoffViolation {
  rowId: string;
  featureName: string;
  availableAt: string;
  featureCutoff: string;
  code: 'FEATURE_AFTER_CUTOFF' | 'INVALID_TIMESTAMP' | 'OUTCOME_OVERLAP';
}

export interface FeatureCutoffReport {
  valid: boolean;
  rowCount: number;
  missingValueCount: number;
  violations: FeatureCutoffViolation[];
  policy: {
    featureAvailabilityRule: 'available_at_or_before_feature_cutoff';
    outcomeLeakageRule: 'outcome_window_must_start_after_feature_cutoff';
  };
}

function parseTimestamp(value: string): number | undefined {
  const parsed = Date.parse(value);
  return Number.isFinite(parsed) ? parsed : undefined;
}

export function validateFeatureCutoffs(rows: ResearchRow[]): FeatureCutoffReport {
  const violations: FeatureCutoffViolation[] = [];
  let missingValueCount = 0;
  for (const row of rows) {
    const cutoff = parseTimestamp(row.featureCutoff);
    if (cutoff === undefined) {
      violations.push({ rowId: row.rowId, featureName: '__row__', availableAt: row.featureCutoff, featureCutoff: row.featureCutoff, code: 'INVALID_TIMESTAMP' });
      continue;
    }
    if (row.outcomeWindowStart) {
      const outcomeStart = parseTimestamp(row.outcomeWindowStart);
      if (outcomeStart === undefined) {
        violations.push({ rowId: row.rowId, featureName: '__outcome__', availableAt: row.outcomeWindowStart, featureCutoff: row.featureCutoff, code: 'INVALID_TIMESTAMP' });
      } else if (outcomeStart <= cutoff) {
        violations.push({ rowId: row.rowId, featureName: '__outcome__', availableAt: row.outcomeWindowStart, featureCutoff: row.featureCutoff, code: 'OUTCOME_OVERLAP' });
      }
    }
    for (const feature of row.features) {
      if (feature.value === null || feature.value === '') {
        missingValueCount += 1;
        continue;
      }
      const availableAt = parseTimestamp(feature.availableAt);
      if (availableAt === undefined) {
        violations.push({ rowId: row.rowId, featureName: feature.name, availableAt: feature.availableAt, featureCutoff: row.featureCutoff, code: 'INVALID_TIMESTAMP' });
      } else if (availableAt > cutoff) {
        violations.push({ rowId: row.rowId, featureName: feature.name, availableAt: feature.availableAt, featureCutoff: row.featureCutoff, code: 'FEATURE_AFTER_CUTOFF' });
      }
    }
  }
  return {
    valid: violations.length === 0,
    rowCount: rows.length,
    missingValueCount,
    violations,
    policy: { featureAvailabilityRule: 'available_at_or_before_feature_cutoff', outcomeLeakageRule: 'outcome_window_must_start_after_feature_cutoff' },
  };
}
