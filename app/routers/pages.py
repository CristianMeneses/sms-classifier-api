from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from ..utils import read_static

router = APIRouter(include_in_schema=False)


@router.get("/", response_class=HTMLResponse)
def home():
    return read_static("home.html")


@router.get("/classify", response_class=HTMLResponse)
def classify_ui():
    return read_static("index.html")


@router.get("/classify/batch", response_class=HTMLResponse)
def batch_ui():
    return read_static("batch.html")


@router.get("/categories", response_class=HTMLResponse)
def categories_view():
    return read_static("categories.html")
