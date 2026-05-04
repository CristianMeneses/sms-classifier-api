from contextlib import asynccontextmanager
from fastapi import FastAPI
from .model_loader import load_model
from .routers import pages, inference, meta


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()
    yield


app = FastAPI(
    title="SMS Classifier API",
    description="Clasifica mensajes SMS en categorías usando DistilBERT fine-tuned.",
    version="2.0.0",
    lifespan=lifespan,
)

app.include_router(pages.router)
app.include_router(inference.router)
app.include_router(meta.router)
