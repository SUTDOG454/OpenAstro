# AFE Unified Attachment Ingestion

Four user-provided AFE documents were preserved under `raw/` with SHA-256 hashes. The two midpoint-resource attachments are byte-identical and remain separately recorded as an exact duplicate for provenance.

The implementation extracts only explicit, testable contracts from the documents. It adds:

- `tools/afe_arabic_parts.py` for sect-aware Arabic Parts calculations, longitude normalization, sign/house lookup, and ten explicitly described parts.
- `tools/afe_transit_strength.py` for the supplied dignity, dispositor, aspect, orb, avashta, speed-modifier, and house-affinity rules.
- `tools/afe_midpoint_resource.py` for schema-tolerant midpoint-resource loading, indexing, searching, and circular-orb activation matching.
- `data/resources/midpoints_resource.sample.json` containing only the three sample interpretations printed in the attachment.
- `tests/test_afe_integrations.py` covering formulas, provenance, indexing, circular orbs, invalid inputs, and duplicate preservation.

The implementation does **not** claim that the attachments are production-ready. The complete midpoint JSON referenced by the documents was not supplied, so the sample fixture is explicitly incomplete. Transit speed modifiers are source-derived placeholders until actual ephemeris speed inputs are provided. Interpretations and scoring are methodology-bound and must not be treated as verified financial forecasts or causal evidence. No code from the attachments was executed.
