from __future__ import annotations

import os
from pathlib import Path

import yaml
from fastapi import APIRouter, UploadFile

router = APIRouter()

TARGETS_DIR = Path(__file__).resolve().parents[2] / "targets"
TARGETS_YAML = TARGETS_DIR / "targets.yaml"

@router.post("/upload")
async def upload_target(files: list[UploadFile]):
    os.makedirs(TARGETS_DIR, exist_ok=True)
    for upload in files:
        destination = TARGETS_DIR / upload.filename
        with open(destination, "wb") as out_file:
            out_file.write(await upload.read())
    return {"ok": True}

@router.get("/list")
def list_targets():
    if not TARGETS_YAML.exists():
        return {"count": 0, "items": []}
    with open(TARGETS_YAML, encoding="utf-8") as file_handle:
        data = yaml.safe_load(file_handle) or []
    return {"count": len(data), "items": data}
