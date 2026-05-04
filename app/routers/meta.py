from fastapi import APIRouter
from ..model_loader import get_categories
from ..category_meta import CATEGORY_META
from ..services.classifier import get_cache

router = APIRouter(tags=["meta"])

_FALLBACK = {"color": "#94a3b8", "description": "", "example_es": "", "example_en": ""}


@router.get("/health")
def health():
    return {
        "status": "ok",
        "model": "distilbert-multilingual-sms",
        "version": "2.0.0",
        "cache": get_cache().stats(),
    }


@router.get("/api/categories")
def categories_api():
    cats = get_categories()
    return {
        "categories": [{"name": c, **CATEGORY_META.get(c, _FALLBACK)} for c in cats],
        "total": len(cats),
    }
