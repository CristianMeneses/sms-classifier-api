# Architecture

## Deployment Overview

```
GitHub (source code)
    │
    └─► Hugging Face Spaces (Docker runtime)
            │  builds & runs the FastAPI container
            │
            ├─► on startup: pulls model from HF Hub
            │       huggingface.co/cmeneses99/sms-classifier
            │       (model.safetensors, tokenizer, config — ~520MB)
            │
            └─► serves API on port 7860
                    https://cmeneses99-sms-classifier-api.hf.space

cron-job.org ──GET /health every 10min──► HF Spaces (keep-alive)
```

## Request Flow

```
Client
  │
  ▼
FastAPI (routers/)
  │
  ├── pages.py      → HTML responses (/, /classify, /classify/batch, /categories)
  ├── inference.py  → POST /classify, POST /classify/batch
  └── meta.py       → GET /health, GET /api/categories
        │
        ▼
services/classifier.py
  │
  ├── LRU Cache (cache.py) ──hit──► return cached response
  │
  └── miss ──► model_loader.py (HuggingFace pipeline)
                    └── distilbert-base-multilingual-cased (fine-tuned)
                            └── top_k=3 predictions → PredictResponse
```

## Model

| Detail | Value |
|---|---|
| Base model | `distilbert-base-multilingual-cased` |
| Task | Sequence classification |
| Categories | 9 |
| Training data | 3,150 synthetic examples (350/category, ES + EN) |
| Training | 5 epochs, fine-tuned with HuggingFace Trainer API |
| Runtime | CPU-only (PyTorch CPU build) |
| Cache | LRU, max 512 entries, thread-safe |

## Project Structure

```
app/
├── main.py                  # Lifespan + router registration
├── model_loader.py          # Downloads model from HF Hub on startup
├── schemas.py               # Pydantic v2 request/response models
├── category_meta.py         # Labels, colors, examples per category
├── cache.py                 # Thread-safe LRU cache
├── utils.py                 # normalize(), read_static()
├── routers/
│   ├── pages.py             # HTML routes
│   ├── inference.py         # Classification endpoints
│   └── meta.py              # Health + categories endpoints
├── services/
│   └── classifier.py        # Inference logic with cache integration
└── static/
    ├── home.html
    ├── index.html            # Single classifier UI
    ├── batch.html            # Batch classifier UI
    └── categories.html
training/
├── config.py
├── generate_dataset.py
├── train.py
└── eval_report.py
```
