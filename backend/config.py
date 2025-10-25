import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
    RV_TASKER_SECRET: str = os.getenv("RV_TASKER_SECRET", "change-me")
    DB_PATH: str = os.getenv("DB_PATH", "rvmonitor.db")
    USE_CLIP: bool = os.getenv("USE_CLIP", "0") == "1"

settings = Settings()
