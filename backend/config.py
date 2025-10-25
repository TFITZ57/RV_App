from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
    RV_TASKER_SECRET: str = os.getenv("RV_TASKER_SECRET", "change-me")
    DB_PATH: str = os.getenv("DB_PATH", "rvmonitor.db")
    USE_CLIP: bool = os.getenv("USE_CLIP", "0") == "1"
    LLM_MONITOR_ENABLED: bool = os.getenv("LLM_MONITOR_ENABLED", "0") == "1"
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    LLM_API_KEY: str | None = os.getenv("LLM_API_KEY")
    LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    LLM_TIMEOUT: float = float(os.getenv("LLM_TIMEOUT", "30"))

    @property
    def llm_configured(self) -> bool:
        return (
            self.LLM_MONITOR_ENABLED
            and bool(self.LLM_API_KEY)
            and bool(self.LLM_MODEL)
        )

settings = Settings()
