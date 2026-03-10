# Astrology Chart Analysis Methodology

## Purpose and Scope

This methodology provides a repeatable framework for:

1. Chart delineation (what is present in the chart).
2. Interpretation (what those factors mean in context).
3. Strength calculation (how dominant each factor is).
4. Synthesis (how factors interact as a system).
5. Reporting (how to deliver insights responsibly).

It is designed for natal chart work first, and can be adapted to synastry, transit, and progression analysis by changing the weighting model.

---

## 1) Chart Delineation Workflow

### 1.1 Data Integrity and Inputs

Collect and validate:

- Birth date (YYYY-MM-DD)
- Birth time (with time zone and DST handling)
- Birth location (latitude/longitude)
- House system used
- Zodiac model used (tropical/sidereal)
- Ayanamsa (if sidereal)

If birth time reliability is low, clearly tag all house and angle-based conclusions as provisional.

### 1.2 Core Objects to Delineate

Minimum required bodies and points:

- Luminaries: Sun, Moon
- Personal planets: Mercury, Venus, Mars
- Social planets: Jupiter, Saturn
- Outer planets: Uranus, Neptune, Pluto
- Angles: ASC, MC, DSC, IC
- Nodes: North Node, South Node

Optional modules:

- Chiron, Black Moon Lilith, Part of Fortune
- Major asteroids (context dependent)

### 1.3 Delineation Order

Use a stable order for consistency:

1. Ascendant, chart ruler, and angular planets.
2. Luminaries by sign/house/aspect.
3. Personal planets by sign/house/aspect.
4. Social and outer planets by house and key aspects.
5. Nodal axis and karmic direction indicators.
6. Major aspect patterns and house emphasis.
7. Elemental and modality balance.

---

## 2) Interpretation Protocol

### 2.1 Interpretation Hierarchy

Interpret factors in this precedence order:

1. Angular and ruling factors (ASC ruler, MC ruler, angular planets).
2. Luminary condition and relationship (Sun–Moon dynamics).
3. Sign + house expression of personal planets.
4. Repeated themes across 3+ independent indicators.
5. Modifiers (outer planet overlays, minor factors).

### 2.2 Evidence Rule

No major life statement should be made from a single indicator.

- **Strong claim:** requires at least 3 converging indicators.
- **Moderate claim:** 2 converging indicators.
- **Tentative claim:** 1 indicator, explicitly framed as hypothesis.

### 2.3 Interpretation Style

Use language that is:

- Specific (avoid vague generalities)
- Conditional ("can", "may", "tends to")
- Action-oriented (include growth pathway)
- Non-deterministic (preserves agency)

---

## 3) Strength Calculation Framework

### 3.1 Strength Dimensions

Each planet/point receives scores across four dimensions:

- **Positional strength** (sign dignity, house angularity)
- **Aspect strength** (number, type, and closeness of aspects)
- **Functional strength** (rulership relevance to angles/houses)
- **Pattern strength** (participation in stelliums/configurations)

### 3.2 Suggested Scoring Model (0-100)

Score each factor as:

`Total Strength = Positional (0-35) + Aspect (0-30) + Functional (0-20) + Pattern (0-15)`

#### Positional (0-35)

- Essential dignity bonus (domicile/exaltation): +8 to +12
- Detriment/fall penalty: -5 to -10
- Angular house (1/4/7/10): +8
- Succedent (2/5/8/11): +4
- Cadent (3/6/9/12): +1

#### Aspect (0-30)

For each major aspect, apply:

- Conjunction: up to +8
- Opposition: up to +7
- Trine: up to +6
- Square: up to +6
- Sextile: up to +4

Scale by orb tightness:

- 0-1°: 1.0x
- 1-3°: 0.8x
- 3-5°: 0.6x
- 5-7°: 0.4x

#### Functional (0-20)

- Planet rules ASC sign: +8
- Planet rules MC sign: +6
- Planet rules multiple emphasized houses: +2 to +6

#### Pattern (0-15)

- Stellium membership: +4
- Apex/focal planet in major configuration: +5
- Repeated dispositorship centrality: +3 to +6

### 3.3 Category Bands

- 80-100: Dominant
- 60-79: Strong
- 40-59: Moderate
- 20-39: Background
- 0-19: Latent

### 3.4 Whole-Chart Metrics

Track aggregate metrics:

- Element distribution (Fire/Earth/Air/Water)
- Modality distribution (Cardinal/Fixed/Mutable)
- Hemisphere emphasis (East/West, North/South)
- House concentration (cluster score)
- Aspect density (major aspects per planet)

These metrics provide system-level context and reduce overfocus on isolated placements.

---

## 4) Synthesis Method

### 4.1 Theme Extraction

Convert delineation + scores into thematic clusters:

- Identity and vitality
- Emotional regulation and attachment style
- Communication and cognition
- Relationships and intimacy
- Vocation and contribution
- Growth edge and developmental tasks

A theme enters the final synthesis only when:

- It is supported by 2+ chart factors, and
- At least one supporting factor is Strong or Dominant.

### 4.2 Tension-to-Integration Mapping

For each major tension (e.g., hard aspects):

1. Define the polarity.
2. Identify situational triggers.
3. Identify high-expression and low-expression manifestations.
4. Provide integration practices (behavioral strategies).

### 4.3 Time Layering (Optional)

When using transits/progressions:

- Keep natal themes as baseline.
- Add timing influences as temporary amplifiers.
- Distinguish structural traits (natal) from cyclical weather (transit).

---

## 5) Reporting Standard

### 5.1 Recommended Report Structure

1. **Executive Summary (5-10 bullet points)**
2. **Core Psychological Signature**
3. **Top 5 Dominant Factors (with scores)**
4. **Strengths and Assets**
5. **Likely Friction Patterns**
6. **Relationship Dynamics**
7. **Career / Directional Indicators**
8. **Current Timing Notes** (if included)
9. **Practical Recommendations (30/90-day actions)**
10. **Appendix: Scoring Table + Aspect Matrix**

### 5.2 Quality and Ethics Checklist

Before finalizing a report:

- Confirm data quality and assumptions are disclosed.
- Avoid fatalistic statements.
- Avoid medical/legal/financial certainty claims.
- Mark confidence level for each major section.
- Include a reflective prompt for client agency.

### 5.3 Confidence Labels

Apply confidence tags to key statements:

- **High confidence:** 3+ converging indicators, including 1 Strong/Dominant.
- **Medium confidence:** 2 converging indicators.
- **Exploratory:** single indicator or weak signal.

---

## 6) Implementation Blueprint (for Teams)

### 6.1 Pipeline

1. Ingest birth data.
2. Compute chart placements and aspects.
3. Run strength scoring engine.
4. Build thematic clusters.
5. Generate narrative draft from templates.
6. Human review for nuance and ethics.
7. Deliver report and feedback loop.

### 6.2 Versioning and Consistency

- Lock scoring weights by version (e.g., `methodology-v1.0`).
- Track changes to interpretations separately from calculations.
- Re-score historical charts only when methodology major version changes.

### 6.3 Validation Metrics

Use internal QA metrics:

- Inter-reader agreement rate (theme matching)
- Narrative specificity score
- Client resonance feedback
- Overclaim rate (claims unsupported by evidence rule)

---

## 7) Quick Reference Checklist

- [ ] Birth data verified and reliability tagged
- [ ] Core delineation completed in standard order
- [ ] Strength scores computed for all required factors
- [ ] Top dominant themes extracted from converging evidence
- [ ] Tensions converted into integration guidance
- [ ] Report formatted with confidence labels
- [ ] Ethics and non-determinism review completed

This methodology turns astrology interpretation into a transparent, auditable, and client-centered process while preserving symbolic depth.
