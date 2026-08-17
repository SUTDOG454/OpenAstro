import { detectCLevel, getCLevelTenureScore, type Executive } from '../company_research.executive';

describe('C-Level Detection', () => {
  test('identifies CEO, CFO, and chief-officer titles', () => {
    expect(detectCLevel('CEO')).toEqual({ isCLevel: true, role: 'CEO' });
    expect(detectCLevel('CFO')).toEqual({ isCLevel: true, role: 'CFO' });
    expect(detectCLevel('Chief Technology Officer')).toEqual({ isCLevel: true, role: 'CTO' });
    expect(detectCLevel('Vice President')).toEqual({ isCLevel: false });
  });

  test('does not classify unrecognized executive titles as C-level', () => {
    expect(detectCLevel('Chief Revenue Officer')).toEqual({ isCLevel: false });
    expect(detectCLevel('Chief of Staff')).toEqual({ isCLevel: false });
    expect(detectCLevel('Director of Finance')).toEqual({ isCLevel: false });
    expect(detectCLevel('')).toEqual({ isCLevel: false });
  });
});

describe('C-Level Tenure Score', () => {
  test('computes normalized average tenure of C-level executives', () => {
    const executives: Executive[] = [
      { title: 'CEO', tenureYears: 5, isCLevel: true, cLevelRole: 'CEO' },
      { title: 'CFO', tenureYears: 3, isCLevel: true, cLevelRole: 'CFO' },
      { title: 'VP Marketing', tenureYears: 2, isCLevel: false },
    ];

    // Average tenure = 4; normalize(4, 1, 20) = 3 / 19 ≈ 0.1579.
    expect(getCLevelTenureScore(executives)).toBeCloseTo(3 / 19, 2);
  });

  test('returns zero when no C-level executives have valid tenure', () => {
    expect(getCLevelTenureScore([{ title: 'VP Marketing', isCLevel: false }])).toBe(0);
    expect(getCLevelTenureScore([{ title: 'CEO', isCLevel: true, tenureYears: Number.NaN }])).toBe(0);
  });

  test('clamps extreme tenure values to the normalization bounds', () => {
    expect(getCLevelTenureScore([{ title: 'CEO', isCLevel: true, tenureYears: 1 }])).toBe(0);
    expect(getCLevelTenureScore([{ title: 'CEO', isCLevel: true, tenureYears: 20 }])).toBe(1);
    expect(getCLevelTenureScore([{ title: 'CEO', isCLevel: true, tenureYears: 0 }])).toBe(0);
    expect(getCLevelTenureScore([{ title: 'CEO', isCLevel: true, tenureYears: 25 }])).toBe(1);
  });
});
