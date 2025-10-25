from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

import httpx

from ..config import settings


class LLMNotConfiguredError(RuntimeError):
    """Raised when the monitor tries to call an LLM without credentials."""


class LLMRequestError(RuntimeError):
    """Raised when the LLM provider fails or returns malformed data."""


@dataclass
class LLMClient:
    provider: str = settings.LLM_PROVIDER.lower().strip()
    base_url: str = settings.LLM_BASE_URL.rstrip("/")
    model: str = settings.LLM_MODEL
    api_key: str | None = settings.LLM_API_KEY
    timeout: float = settings.LLM_TIMEOUT

    @property
    def enabled(self) -> bool:
        return settings.llm_configured

    def chat(self, messages: List[Dict[str, Any]], response_format: str | None = None) -> str:
        if not self.enabled:
            raise LLMNotConfiguredError("LLM monitor is not configured.")

        if self.provider != "openai":
            raise LLMRequestError(f"Unsupported LLM provider: {self.provider}")

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": 0,
        }
        if response_format:
            payload["response_format"] = {"type": response_format}

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, headers=headers, json=payload)
                response.raise_for_status()
        except httpx.HTTPError as exc:  # pragma: no cover - network failures
            raise LLMRequestError(f"LLM request failed: {exc}") from exc

        data = response.json()
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as exc:  # pragma: no cover - provider drift
            raise LLMRequestError("LLM response missing choices content") from exc


client = LLMClient()
