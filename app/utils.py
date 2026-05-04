import unicodedata
from pathlib import Path

_STATIC = Path(__file__).parent / "static"


def normalize(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def read_static(filename: str) -> str:
    return (_STATIC / filename).read_text(encoding="utf-8")
