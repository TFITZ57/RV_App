from __future__ import annotations

import hashlib
import os
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TARGETS_DIR = ROOT / "targets"
OUT = TARGETS_DIR / "targets.yaml"


def sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with open(path, "rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


if __name__ == "__main__":
    os.makedirs(TARGETS_DIR, exist_ok=True)
    items: list[dict] = []
    for filename in sorted(os.listdir(TARGETS_DIR)):
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            rel_path = Path("targets") / filename
            full_path = TARGETS_DIR / filename
            items.append(
                {
                    "target_path": str(rel_path),
                    "notes": "",
                    "categories": [],
                    "distinctiveness": None,
                    "sha256": sha256(full_path),
                }
            )
    with open(OUT, "w", encoding="utf-8") as file_handle:
        yaml.safe_dump(items, file_handle, sort_keys=False, indent=2, allow_unicode=True)
    print(f"Wrote {OUT} with {len(items)} entries.")
