from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .guardrails import is_leading_content


class Stage(str, Enum):
    I = "I"  # noqa: E741 - Stage labels follow CRV notation
    II = "II"
    III = "III"
    IV = "IV"
    V = "V"
    VI = "VI"

PROMPTS = {
    "OPEN": "Target reference is [ID]. Describe the target.",
    "DESCRIBE": "Describe the target.",
    "SENSORY": "List colors, textures, temperatures, sounds, and smells.",
    "MOV_ABOVE": "From the top of the target, look down and describe.",
    "MOV_NORTH": "Move 20 meters to the north and describe.",
    "MOV_SOUTH": "Move 20 meters to the south and describe.",
    "MOV_EAST": "Move 20 meters to the east and describe.",
    "MOV_WEST": "Move 20 meters to the west and describe.",
    "AOL_BREAK": "AOL—write it, break.",
    "AI_NOTED": "AI noted.",
    "ADVANCE": "Proceed to Stage {stage} and stay in structure.",
}

@dataclass
class MonitorState:
    session_id: str
    stage: Stage = Stage.I
    log: list[dict] = field(default_factory=list)


def next_monitor_output(state: MonitorState, viewer_text: str) -> tuple[str, dict]:
    """Given viewer text, return monitor utterance + a log entry.

    If leading content is detected, force an AOL break.

    Otherwise, return a neutral prompt suitable for the current stage.

    """
    # Detect AOL trigger (object naming etc.)
    if is_leading_content(viewer_text):
        utterance = PROMPTS["AOL_BREAK"]
        entry = {"stage": state.stage.value, "type": "AOL_BREAK", "prompt": utterance}
        state.log.append(entry)
        return utterance, entry

    # Stage-specific neutral prompts
    if state.stage == Stage.I:
        utterance = PROMPTS["DESCRIBE"]
    elif state.stage == Stage.II:
        utterance = PROMPTS["SENSORY"]
    elif state.stage == Stage.III:
        # alternate describe vs movement
        utterance = PROMPTS["MOV_ABOVE"]
    elif state.stage in (Stage.IV, Stage.V, Stage.VI):
        utterance = PROMPTS["DESCRIBE"]
    else:
        utterance = PROMPTS["DESCRIBE"]

    entry = {"stage": state.stage.value, "type": "PROMPT", "prompt": utterance}
    state.log.append(entry)
    return utterance, entry

def advance_stage(state: MonitorState, to_stage: Stage) -> str:
    state.stage = to_stage
    utterance = PROMPTS["ADVANCE"].format(stage=to_stage.value)
    state.log.append({"stage": to_stage.value, "type": "ADVANCE", "prompt": utterance})
    return utterance
