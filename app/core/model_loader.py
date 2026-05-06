import json
from pathlib import Path
from transformers import pipeline
from huggingface_hub import hf_hub_download

HF_REPO = "cmeneses99/sms-classifier"
MODEL_DIR = Path(__file__).parent.parent.parent / "model"

_classifier = None
_categories: list[str] = []


def _ensure_model() -> Path:
    """Download model files from HF Hub if not present locally."""
    if (MODEL_DIR / "config.json").exists():
        return MODEL_DIR

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    for filename in [
        "config.json",
        "model.safetensors",
        "tokenizer.json",
        "tokenizer_config.json",
        "special_tokens_map.json",
        "vocab.txt",
        "label_map.json",
    ]:
        hf_hub_download(repo_id=HF_REPO, filename=filename, local_dir=str(MODEL_DIR))

    return MODEL_DIR


def load_model() -> None:
    """Load the classifier pipeline and category labels into module-level state."""
    global _classifier, _categories

    model_path = _ensure_model()

    _classifier = pipeline(
        "text-classification",
        model=str(model_path),
        tokenizer=str(model_path),
        top_k=3,
        device=-1,
    )

    with open(model_path / "label_map.json", encoding="utf-8") as f:
        label_map: dict = json.load(f)
    _categories = list(label_map.values())


def get_classifier():
    return _classifier


def get_categories() -> list[str]:
    return _categories
