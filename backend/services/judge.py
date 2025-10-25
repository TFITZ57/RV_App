from __future__ import annotations

import random
from pathlib import Path

import yaml

from ..db import get_conn

TARGETS_YAML = Path(__file__).resolve().parents[2] / "targets" / "targets.yaml"


def build_pool(session_id: str, true_path: str, n_candidates: int = 5) -> list[str]:
    """Build and persist a judging pool (true target + decoys)."""

    with open(TARGETS_YAML, encoding="utf-8") as file_handle:
        data = yaml.safe_load(file_handle) or []

    base_dir = TARGETS_YAML.parent
    all_paths = [str((base_dir / entry["target_path"]).resolve()) for entry in data]
    decoys = [path for path in all_paths if path != true_path]
    random.shuffle(decoys)

    pool = [true_path] + decoys[: max(0, n_candidates - 1)]
    random.shuffle(pool)

    with get_conn() as conn:
        conn.execute("DELETE FROM judging_pool WHERE session_id=?", (session_id,))
        for candidate in pool:
            conn.execute(
                "INSERT INTO judging_pool(session_id, candidate_path, is_true) VALUES (?,?,?)",
                (session_id, candidate, 1 if candidate == true_path else 0),
            )
    return pool
