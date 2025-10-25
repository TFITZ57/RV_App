from __future__ import annotations

import random
import uuid
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from ..db import get_conn
from ..services.clip_ranker import clip_rank
from ..services.scoring import effect_size_from_ranks

router = APIRouter()

class RunJudgingRequest(BaseModel):
    session_id: str
    n_candidates: int = 5
    use_clip: bool = False

class CandidateRank(BaseModel):
    candidate_path: str
    rank: int

class RunJudgingResponse(BaseModel):
    judge_run_id: str
    average_rank: float
    effect_size: float
    ranking: list[CandidateRank]


TARGETS_YAML = Path(__file__).resolve().parents[2] / "targets" / "targets.yaml"

@router.post("/run", response_model=RunJudgingResponse)
def run_judging(req: RunJudgingRequest):
    # Fetch true target
    with get_conn() as conn:
        row_sess = conn.execute(
            "SELECT target_id FROM session WHERE id=?",
            (req.session_id,),
        ).fetchone()
        if not row_sess:
            return {"error": "Invalid session"}
        row_truth = conn.execute(
            "SELECT target_path FROM target_truth WHERE target_id=?",
            (row_sess["target_id"],),
        ).fetchone()
        if not row_truth:
            return {"error": "Truth not found"}
        true_path = row_truth["target_path"]
        # Build pool
        rows_pool = conn.execute(
            "SELECT candidate_path, is_true FROM judging_pool WHERE session_id=?",
            (req.session_id,),
        ).fetchall()
        if not rows_pool:
            # Build pool if not exists
            import yaml

            with open(TARGETS_YAML, encoding="utf-8") as file_handle:
                data = yaml.safe_load(file_handle) or []

            base_dir = TARGETS_YAML.parent
            all_paths = [str((base_dir / entry["target_path"]).resolve()) for entry in data]
            decoys = [path for path in all_paths if path != true_path]
            random.shuffle(decoys)
            pool = [true_path] + decoys[: max(0, req.n_candidates - 1)]
            random.shuffle(pool)
            for candidate in pool:
                conn.execute(
                    "INSERT INTO judging_pool(session_id, candidate_path, is_true) VALUES (?,?,?)",
                    (req.session_id, candidate, 1 if candidate == true_path else 0),
                )
        else:
            pool = [r["candidate_path"] for r in rows_pool]

        # Get transcript text (concatenate pages)
        pages = conn.execute(
            "SELECT content FROM transcript_page WHERE session_id=? ORDER BY id",
            (req.session_id,),
        ).fetchall()
        transcript_text = "\n".join([p["content"] for p in pages])

        # Rank candidates
        if req.use_clip:
            scored = clip_rank(transcript_text, pool)  # list of (path, score)
            # Highest score -> rank 1
            order = [p for p, _ in sorted(scored, key=lambda x: -x[1])]
        else:
            order = pool[:]
            random.shuffle(order)

        ranking = {path: idx + 1 for idx, path in enumerate(order)}

        judge_run_id = str(uuid.uuid4())
        # Persist results
        for path, rank in ranking.items():
            is_true = 1 if path == true_path else 0
            conn.execute(
                """
                INSERT OR REPLACE INTO judging_result(
                    judge_run_id, session_id, candidate_path, rank, is_true
                ) VALUES (?,?,?,?,?)
                """,
                (judge_run_id, req.session_id, path, rank, is_true),
            )

        # Compute stats (true ranks only)
        true_ranks = [ranking[true_path]]
        es, avg = effect_size_from_ranks(true_ranks, req.n_candidates)

        return RunJudgingResponse(
            judge_run_id=judge_run_id,
            average_rank=avg,
            effect_size=es,
            ranking=[
                CandidateRank(candidate_path=path, rank=rank)
                for path, rank in sorted(ranking.items(), key=lambda item: item[1])
            ],
        )

class FeedbackRequest(BaseModel):
    session_id: str

@router.post("/feedback")
def feedback(req: FeedbackRequest):
    with get_conn() as conn:
        sess = conn.execute(
            "SELECT target_id FROM session WHERE id=?",
            (req.session_id,),
        ).fetchone()
        truth = conn.execute(
            "SELECT target_path FROM target_truth WHERE target_id=?",
            (sess["target_id"],),
        ).fetchone()
    return {"target_path": truth["target_path"]}
