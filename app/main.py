from contextlib import asynccontextmanager
from fastapi import FastAPI
from .core.model_loader import load_model
from .api import inference, meta
from .web import pages


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()
    yield


app = FastAPI(
    title="SMS Classifier API",
    description="Classifies SMS messages into categories using fine-tuned DistilBERT.",
    version="2.0.0",
    lifespan=lifespan,
)

app.include_router(pages.router)
app.include_router(inference.router)
app.include_router(meta.router)
