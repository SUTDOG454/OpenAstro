# Interpretation Indicator Dataset and Gap Analysis

The corpus extractor identified **133 source files** and **3011 normalized interpretation indicators**. Exact normalized-text duplicates were merged into the provenance layer; probable semantic duplicates remain separate.

## Indicator layers

| Record type | Count | Evidence class |
|---|---:|---|
| interpretation_field | 42 | source_derived |\n| interpretation_line | 859 | source_derived |\n| interpretation_list | 172 | source_derived |\n| interpretation_text | 1938 | source_derived |\n
The indicators retain raw text, normalized text, subject path, source ID, source path, SHA-256, keywords, Unicode symbols, status, and limitations. They are suitable for retrieval and regression testing, but not for presenting astrology as established evidence.

## Automatically applied improvements

The system added a reusable indicator schema and validator, a stable keyword index, source-hash links, a deduplication register, and a master-package reference. These are reversible metadata and retrieval improvements.

## Review-gated gaps

Semantic blending across traditions, repair of malformed JSON, deterministic implementation of unavailable chart methods, and empirical validation of interpretations remain review-gated. Thin layers are reported rather than filled with invented text.
