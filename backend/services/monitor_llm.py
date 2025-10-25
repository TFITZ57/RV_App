from __future__ import annotations

import json
import logging
from typing import Tuple

from .guardrails import is_leading_content
from .llm_client import LLMNotConfiguredError, LLMRequestError, client as llm_client
from .monitor_fsm import MonitorState, PROMPTS

log = logging.getLogger(__name__)

PROMPT_IDS = {
    "DESCRIBE": PROMPTS["DESCRIBE"],
    "SENSORY": PROMPTS["SENSORY"],
    "MOV_ABOVE": PROMPTS["MOV_ABOVE"],
    "MOV_NORTH": PROMPTS["MOV_NORTH"],
    "MOV_SOUTH": PROMPTS["MOV_SOUTH"],
    "MOV_EAST": PROMPTS["MOV_EAST"],
    "MOV_WEST": PROMPTS["MOV_WEST"],
    "AI_NOTED": PROMPTS["AI_NOTED"],
}

SYSTEM_PROMPT = (
    "You are a Controlled Remote Viewing (CRV) monitor. "
    "You see only the stage label and raw viewer text. "
    "Respond with JSON containing a `prompt_id` that maps to one of the allowed utterances. "
    "Never invent new wording; stay on the whitelist. "
    "Guidelines: Stage I focuses on basic description, Stage II on sensory cues, Stage III on movement commands, "
    "Stages IV-VI stay neutral unless viewer asks for movement. If the viewer reports AI (aesthetic impact) acknowledge with AI_NOTED."
)


class MonitorLLMError(RuntimeError):
    """High-level wrapper for monitor-specific LLM failures."""


class MonitorLLM:
    def __init__(self):
        self._client = llm_client

    @property
    def enabled(self) -> bool:
        return self._client.enabled

    def _emit_aol_break(self, state: MonitorState) -> Tuple[str, dict]:
        utterance = PROMPTS["AOL_BREAK"]
        entry = {"stage": state.stage.value, "type": "AOL_BREAK", "prompt": utterance, "source": "guardrail"}
        state.log.append(entry)
        return utterance, entry

    def generate(self, state: MonitorState, viewer_text: str) -> Tuple[str, dict]:
        if not self.enabled:
            raise MonitorLLMError("LLM monitor disabled")

        if is_leading_content(viewer_text):
            return self._emit_aol_break(state)

        user_content = (
            f"Stage: {state.stage.value}\n"
            f"ViewerText: {viewer_text.strip() or '[no input]'}\n"
            "Return JSON: {\"prompt_id\": <ALLOWED_PROMPT_ID>}"
        )
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ]

        try:
            raw = self._client.chat(messages, response_format="json_object")
            payload = json.loads(raw)
            prompt_id = payload["prompt_id"]
            utterance = PROMPT_IDS[prompt_id]
        except (LLMNotConfiguredError, LLMRequestError, json.JSONDecodeError, KeyError) as exc:
            raise MonitorLLMError(str(exc)) from exc

        entry = {
            "stage": state.stage.value,
            "type": "PROMPT",
            "prompt": utterance,
            "source": "llm",
        }
        state.log.append(entry)
        return utterance, entry


llm_monitor = MonitorLLM()
