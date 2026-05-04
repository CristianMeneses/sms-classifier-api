from pydantic import BaseModel, Field, field_validator


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=512)

    @field_validator("text")
    @classmethod
    def sanitize(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("El texto no puede estar vacío o contener solo espacios")
        # Colapsa whitespace excesivo (tabs, múltiples espacios, newlines)
        v = " ".join(v.split())
        return v


class IntentPrediction(BaseModel):
    category: str
    confidence: float


class PredictResponse(BaseModel):
    text: str
    prediction: IntentPrediction
    top_3: list[IntentPrediction]
    cached: bool = False


class ClassifyBatchRequest(BaseModel):
    texts: list[str] = Field(..., min_length=1, max_length=50)

    @field_validator("texts")
    @classmethod
    def sanitize_texts(cls, v: list[str]) -> list[str]:
        result = []
        for text in v:
            text = " ".join(text.strip().split())
            if not text:
                raise ValueError("Cada texto debe tener al menos un carácter")
            if len(text) > 512:
                raise ValueError("Cada texto debe tener máximo 512 caracteres")
            result.append(text)
        return result


class ClassifyBatchResponse(BaseModel):
    results: list[PredictResponse]
    total: int
    from_cache: int
