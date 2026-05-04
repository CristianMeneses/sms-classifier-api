from fastapi import APIRouter, HTTPException
from ..model_loader import get_classifier
from ..schemas import PredictRequest, PredictResponse, ClassifyBatchRequest, ClassifyBatchResponse
from ..services.classifier import classify_one, classify_many
from ..utils import normalize

router = APIRouter(tags=["inference"])


@router.post("/classify", response_model=PredictResponse)
def classify(request: PredictRequest):
    if get_classifier() is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    return classify_one(normalize(request.text), request.text)


@router.post("/classify/batch", response_model=ClassifyBatchResponse)
def classify_batch(request: ClassifyBatchRequest):
    if get_classifier() is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    normalized = [normalize(t) for t in request.texts]
    results, from_cache = classify_many(normalized, request.texts)
    return ClassifyBatchResponse(results=results, total=len(results), from_cache=from_cache)
