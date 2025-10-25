from __future__ import annotations

import re
from pathlib import Path

LEXICON_PATH = Path(__file__).resolve().parents[1] / "lexicon" / "nouns_en_basic.txt"

# Load a coarse noun list (user should expand over time)
with open(LEXICON_PATH, encoding="utf-8") as file_handle:
    NOUNS = {
        word.strip().lower()
        for word in file_handle
        if word.strip() and not word.startswith("#")
    }

pattern = "|".join(re.escape(word) for word in sorted(NOUNS) if word)
if pattern:
    LEADING_PAT = re.compile(rf"\b({pattern})\b", re.IGNORECASE)
else:  # pragma: no cover - lexicon should never be empty
    LEADING_PAT = re.compile(r"^$")

def is_leading_content(text: str) -> bool:
    if not text:
        return False
    return bool(LEADING_PAT.search(text))
