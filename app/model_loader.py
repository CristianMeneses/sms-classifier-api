import json
from pathlib import Path
from transformers import pipeline

MODEL_DIR = Path(__file__).parent.parent / "model"

_classifier = None
_categories: list[str] = []


def load_model() -> None:
    global _classifier, _categories

    if not MODEL_DIR.exists() or not (MODEL_DIR / "config.json").exists():
        raise RuntimeError(
            f"No se encontró el modelo en {MODEL_DIR}. "
            "Ejecuta training/train.py primero."
        )

    _classifier = pipeline(
        "text-classification",
        model=str(MODEL_DIR),
        tokenizer=str(MODEL_DIR),
        top_k=3,
        device=-1,
    )

    label_map_path = MODEL_DIR / "label_map.json"
    with open(label_map_path, encoding="utf-8") as f:
        label_map: dict = json.load(f)
    _categories = list(label_map.values())


def get_classifier():
    return _classifier


def get_categories() -> list[str]:
    return _categories
