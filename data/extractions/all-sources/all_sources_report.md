# All-Source Ingestion Report

## Scope
This package inventories all available source trees in the sandbox: the OpenAstro worktree, cloned repository sources, and preserved artifacts from referenced research tasks. Source contents were not executed. Each record includes a source path, media classification, SHA-256 hash, duplicate status, and promotion/review status.

## Inventory summary
| Metric | Count |
|---|---:|
| Total records | 24668 |
| Text-like records | 24044 |
| Binary records | 624 |
| Exact hash duplicate groups | 888 |
| Inventory errors | 0 |

## Source roots
| Root | Count |
|---|---:|
| `openastro_worktree` | 91 |
| `referenced_task_artifacts` | 585 |
| `repository_sources` | 23992 |

## Class indexes
| Index | Count | Meaning |
|---|---:|---|
| `signal_indicator_index.json` | 496 | Filtered source index; raw content remains at each recorded path. |
| `dataset_index.json` | 8929 | Filtered source index; raw content remains at each recorded path. |
| `framework_method_index.json` | 321 | Filtered source index; raw content remains at each recorded path. |
| `code_schema_index.json` | 1344 | Filtered source index; raw content remains at each recorded path. |
| `document_index.json` | 13042 | Filtered source index; raw content remains at each recorded path. |
| `test_validation_index.json` | 694 | Filtered source index; raw content remains at each recorded path. |
| `financial_company_index.json` | 91 | Filtered source index; raw content remains at each recorded path. |

## Classification notes
A file can belong to multiple classes. Filenames and extensions provide discovery signals, not semantic authority. The package therefore preserves all records, retains probable duplicates, and leaves license, privacy, factuality, methodology, and promotion decisions pending review. Binary documents and large datasets are indexed by hash and path rather than copied into this package a second time.

## High-priority review areas
- Validate licenses and redistribution rights per repository and dataset.
- Separate source-derived signals from computed indicators, methodology-bound scores, and research hypotheses.
- Create dataset manifests with feature definitions, time windows, labels, missingness, leakage controls, and test splits before ML use.
- Review private or client-linked artifacts for consent and minimization.
- Add executable adapters only after schema and failure contracts are approved.
