from ..cache import LRUCache
from ..model_loader import get_classifier
from ..schemas import PredictResponse, IntentPrediction

_cache = LRUCache(max_size=512)


def get_cache() -> LRUCache:
    return _cache


def run_inference(texts: list[str]) -> list[PredictResponse]:
    classifier = get_classifier()
    raw = classifier(texts, batch_size=16)
    responses = []
    for text, result in zip(texts, raw):
        preds = result if isinstance(result, list) else [result]
        top_3 = [
            IntentPrediction(category=r["label"], confidence=round(r["score"], 4))
            for r in preds
        ]
        responses.append(PredictResponse(text=text, prediction=top_3[0], top_3=top_3))
    return responses


def classify_one(normalized_text: str, original_text: str) -> PredictResponse:
    cached = _cache.get(normalized_text)
    if cached:
        return cached.model_copy(update={"cached": True})
    response = run_inference([normalized_text])[0]
    response.text = original_text
    _cache.set(normalized_text, response)
    return response


def classify_many(normalized_texts: list[str], original_texts: list[str]) -> tuple[list[PredictResponse], int]:
    """Returns (results, from_cache_count)."""
    results: list[PredictResponse | None] = [None] * len(normalized_texts)
    from_cache = 0
    pending = []

    for i, key in enumerate(normalized_texts):
        cached = _cache.get(key)
        if cached:
            results[i] = cached
            from_cache += 1
        else:
            pending.append(i)

    if pending:
        inferred = run_inference([normalized_texts[i] for i in pending])
        for i, response in zip(pending, inferred):
            response.text = original_texts[i]
            _cache.set(normalized_texts[i], response)
            results[i] = response

    return results, from_cache
