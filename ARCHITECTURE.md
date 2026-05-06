# Architecture

## Deployment

```
GitHub (source code)
    │
    └─► Hugging Face Spaces (Docker runtime)
            │  builds and runs the FastAPI container
            │
            ├─► on startup: downloads model from HF Hub
            │       huggingface.co/cmeneses99/sms-classifier
            │       (model.safetensors, tokenizer, config — ~520MB)
            │
            └─► serves API on port 7860
                    https://cmeneses99-sms-classifier-api.hf.space

cron-job.org ──GET /health every 10min──► HF Spaces (keep-alive)
```

## Request flow

```
Client
  │
  ▼
FastAPI
  │
  ├── web/pages.py      → HTML responses (/, /classify, /classify/batch, /categories)
  ├── api/inference.py  → POST /classify, POST /classify/batch
  └── api/meta.py       → GET /health, GET /api/categories
        │
        ▼
services/classifier.py
  │
  ├── LRU Cache (core/cache.py) ──hit──► return cached response
  │
  └── miss ──► core/model_loader.py (HuggingFace pipeline)
                    └── distilbert-base-multilingual-cased (fine-tuned)
                            └── top_k=3 predictions → PredictResponse
```

## Model

| Detail           | Value                                                  |
|------------------|--------------------------------------------------------|
| Base model       | `distilbert-base-multilingual-cased`                   |
| Task             | Sequence classification                                |
| Categories       | 9                                                      |
| Training data    | 3,150 synthetic examples (350/category, ES + EN)       |
| Training         | 5 epochs, fine-tuned with HuggingFace Trainer API      |
| Runtime          | CPU-only (PyTorch CPU build)                           |
| Cache            | LRU, max 512 entries, thread-safe                      |

## Project structure

```
app/
├── main.py                      # Lifespan + router registration
├── utils.py                     # normalize(), read_static()
├── core/                        # Shared infrastructure
│   ├── cache.py                 # Thread-safe LRU cache
│   ├── model_loader.py          # Downloads model from HF Hub on startup
│   ├── schemas.py               # Pydantic v2 request/response models
│   └── category_meta.py         # Labels, colors and examples per category
├── services/
│   └── classifier.py            # Inference logic with cache integration
├── api/                         # JSON endpoints
│   ├── inference.py             # POST /classify, POST /classify/batch
│   └── meta.py                  # GET /health, GET /api/categories
├── web/                         # HTML endpoints
│   └── pages.py                 # UI routes
└── templates/                   # HTML files
    ├── home.html
    ├── index.html                # Single classifier UI
    ├── batch.html                # Batch classifier UI
    └── categories.html
training/
├── config.py
├── generate_dataset.py
├── train.py
└── eval_report.py
```
