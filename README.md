# OpenAstro

OpenAstro is an open-source collection of astrological frameworks, definitions, calculation references, delineation material, React examples, and normalization utilities. The repository is organized so that data assets, documentation, components, SVG assets, and utilities have distinct locations.

## Repository layout

| Location | Purpose |
|---|---|
| `data/frameworks/` | Validated high-level astrological reference and delineation frameworks. |
| `data/definitions/` | Structured definitions, rulership data, and canonical terminology. |
| `data/calculations/` | Structured chart-type and calculation references. |
| `data/methodologies/` | Structured methodology and scoring protocols. |
| `data/delineations/` | Structured interpretation and delineation material. |
| `data/charts/` | Saved chart data. Treat personal chart information as sensitive. |
| `data/extractions/` | Machine-readable extracts from source material. |
| `data/sources/` | Curated source text retained for reference. |
| `data/drafts/` | Preserved source files that are not currently valid JSON or contain unfinished material. These files are intentionally not used as machine-readable data until validated. |
| `mfw/definitions/` | Generated karmic-framework definitions maintained by the normalization utility. |
| `docs/` | Human-readable methodology and repository documentation. |
| `components/` | Stand-alone React/JSX component examples. |
| `assets/svg/` | Asteroid SVG assets. |
| `tools/` | Deterministic data-normalization utilities. |

## Data conventions

Use lowercase kebab-case filenames and explicit extensions for data, documentation, and assets. React component source files use PascalCase, Python tools use snake_case, and `README.md` retains its conventional uppercase name. Validated JSON belongs in the appropriate `data/` category. Preserve unfinished, malformed, or placeholder-bearing material under `data/drafts/` rather than presenting it as production-ready JSON. The guide in [`docs/repository-data-map.md`](docs/repository-data-map.md) records the current status of preserved draft files.

## Utilities

The normalization scripts are documented in [`tools/README.md`](tools/README.md). `tools/normalize_karmic_data.py` reads the unified delineation framework and regenerates the karmic-system definition under `mfw/definitions/`.

## Contribution guidance

Keep prose in Markdown, data in valid JSON, UI examples in `components/`, and assets in `assets/`. Before moving or deleting an asset, check for in-repository references and validate JSON with `jq empty <file>` where applicable.


## Optional DeepSeek utility

`deepseek_client.py` and `examples/deepseek_example.py` provide an optional HTTP client example. They require a `DEEPSEEK_API_KEY` supplied through the environment or a repository secret; keys must never be committed to the repository.

```bash
export DEEPSEEK_API_KEY="your_key_here"
python examples/deepseek_example.py
```

The optional client should be reviewed for provider compatibility, data-handling requirements, and dependency policy before use with non-public information.
