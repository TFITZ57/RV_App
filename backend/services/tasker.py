from __future__ import annotations

import base64
import hashlib
import hmac
import random
from pathlib import Path

import yaml

from ..config import settings
from ..db import get_conn

TARGETS_YAML = Path(__file__).resolve().parents[2] / "targets" / "targets.yaml"


def _hmac_tag(hex_digest: str) -> str:
    mac = hmac.new(settings.RV_TASKER_SECRET.encode(), hex_digest.encode(), hashlib.sha256).digest()
    return base64.urlsafe_b64encode(mac)[:16].decode()


def choose_target() -> tuple[str, str, str]:
    """Return (target_id, target_path, sha256). Also persists mapping in DB."""
    if not TARGETS_YAML.exists():
        raise FileNotFoundError("targets.yaml not found. Run scripts/package_targets.py")
    with open(TARGETS_YAML, encoding="utf-8") as file_handle:
        data = yaml.safe_load(file_handle) or []
    if not data:
        raise RuntimeError("No targets in targets.yaml. Add images and run package_targets.py")
    entry = random.choice(data)
    target_path = str((TARGETS_YAML.parent / entry["target_path"]).resolve())
    sha256 = entry["sha256"]
    target_id = _hmac_tag(sha256)
    # persist mapping (upsert)
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO target_truth(target_id, target_path, sha256)
            VALUES (?,?,?)
            ON CONFLICT(target_id)
            DO UPDATE SET target_path=excluded.target_path, sha256=excluded.sha256
            """,
            (target_id, target_path, sha256),
        )
    return target_id, target_path, sha256
