# Tools

## normalize_aspects_json.py

Normalizes aspect payloads that are sometimes pasted as escaped JSON text
(for example content beginning with `[\n {` and containing `\"point1\"`).

### Usage

```bash
python tools/normalize_aspects_json.py payload.txt > normalized_aspects.json
```

Use `--summary` to print quick frequency stats for aspect types and points:

```bash
python tools/normalize_aspects_json.py payload.txt --summary > normalized_aspects.json
```
