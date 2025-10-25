import uuid

from fastapi import APIRouter
from pydantic import BaseModel

from ..db import get_conn
from ..services.monitor_fsm import MonitorState, Stage, advance_stage, next_monitor_output
from ..services.tasker import choose_target

router = APIRouter()

class StartResponse(BaseModel):
    session_id: str
    target_id: str
    opening_prompt: str

@router.post("/start", response_model=StartResponse)
def start_session():
    session_id = str(uuid.uuid4())
    target_id, _, _ = choose_target()
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO session(id, target_id, stage_plan) VALUES (?,?,?)",
            (session_id, target_id, '["I","II","III","IV","V","VI"]'),
        )
    # Opening prompt
    opening_prompt = f"Target reference is [{target_id}]. Describe the target."
    return StartResponse(session_id=session_id, target_id=target_id, opening_prompt=opening_prompt)

class LogRequest(BaseModel):
    session_id: str
    stage: Stage
    viewer_text: str

class LogResponse(BaseModel):
    monitor_prompt: str

@router.post("/log", response_model=LogResponse)
def log_viewer_input(req: LogRequest):
    # Save transcript
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO transcript_page(session_id, stage, content) VALUES (?,?,?)",
            (req.session_id, req.stage.value, req.viewer_text),
        )
    # Generate monitor output
    state = MonitorState(session_id=req.session_id, stage=req.stage)
    utterance, _ = next_monitor_output(state, req.viewer_text)
    return LogResponse(monitor_prompt=utterance)

class AdvanceRequest(BaseModel):
    session_id: str
    to_stage: Stage

class AdvanceResponse(BaseModel):
    monitor_prompt: str

@router.post("/advance", response_model=AdvanceResponse)
def advance_stage_route(req: AdvanceRequest):
    state = MonitorState(session_id=req.session_id, stage=req.to_stage)
    utterance = advance_stage(state, req.to_stage)
    return AdvanceResponse(monitor_prompt=utterance)

class FinishRequest(BaseModel):
    session_id: str

@router.post("/finish")
def finish_session(req: FinishRequest):
    with get_conn() as conn:
        conn.execute("UPDATE session SET end_ts=CURRENT_TIMESTAMP WHERE id=?", (req.session_id,))
    return {"ok": True}
