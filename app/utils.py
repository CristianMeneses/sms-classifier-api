import unicodedata
from pathlib import Path

_TEMPLATES = Path(__file__).parent / "templates"


def normalize(text: str) -> str:
    """Lowercase and strip accents for cache-key normalization."""
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def read_static(filename: str) -> str:
    return (_TEMPLATES / filename).read_text(encoding="utf-8")
