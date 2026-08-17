from __future__ import annotations

import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/home/ubuntu/openastro_worktree')
BUNDLE = ROOT / 'data/unified/openastro-user-corpus-integration-bundle.zip'
MANIFEST = ROOT / 'data/ingested-user-corpus/user_corpus_bundle_manifest.json'

paths = [
    ROOT / 'data/ingested-user-corpus',
    ROOT / 'data/sources/2026-08-user-uploads/referenced_task_inventory.json',
    ROOT / 'tools/ingest_user_corpus.py',
    ROOT / 'tools/integrate_user_corpus.py',
    ROOT / 'tools/package_user_corpus_integration.py',
    ROOT / 'tests/test_user_corpus_integration.py',
    ROOT / 'data/unified/unified_astrology_master.json',
    ROOT / 'data/research/signal_indicator_promotion_policy.json',
    ROOT / 'data/research/temporal_leakage_controls.json',
]

exclude_names = {
    'openastro-user-corpus-integration-bundle.zip',
    'user_corpus_bundle_manifest.json',
}

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

files: list[Path] = []
for path in paths:
    if path.is_file():
        files.append(path)
    elif path.is_dir():
        files.extend(candidate for candidate in path.rglob('*') if candidate.is_file() and candidate.name not in exclude_names)
files = sorted(set(files))

with zipfile.ZipFile(BUNDLE, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
    for path in files:
        archive.write(path, path.relative_to(ROOT).as_posix())

manifest = {
    'schema_version': '1.0.0',
    'generated_at': datetime.now(timezone.utc).isoformat(),
    'bundle_path': str(BUNDLE.relative_to(ROOT)),
    'bundle_sha256': sha256(BUNDLE),
    'bundle_size_bytes': BUNDLE.stat().st_size,
    'file_count': len(files),
    'files': [
        {
            'path': str(path.relative_to(ROOT)),
            'sha256': sha256(path),
            'size_bytes': path.stat().st_size,
        }
        for path in files
    ],
    'exclusions': [
        'Raw user-upload source bodies under data/sources/2026-08-user-uploads/raw/',
        'Derived raw PDF text under data/sources/2026-08-user-uploads/derived-pdf-text/',
        'Quarantined sensitive interpretive content and private personalized chart material are represented by metadata and hashes, not copied into this distributable bundle.',
    ],
}
MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'bundle': manifest['bundle_path'], 'file_count': manifest['file_count'], 'sha256': manifest['bundle_sha256'], 'size_bytes': manifest['bundle_size_bytes']}, indent=2))
