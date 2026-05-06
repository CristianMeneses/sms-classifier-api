# SMS Classifier API

REST API that classifies SMS messages into operational categories using **multilingual DistilBERT** fine-tuned on a synthetic bilingual dataset (ES + EN).

**Live demo:** https://cmeneses99-sms-classifier-api.hf.space

## Categories

| Category               | Description                                          |
| ---------------------- | ---------------------------------------------------- |
| `transaction`          | Payment confirmations, debits and transfers          |
| `otp_verification`     | One-time codes for identity verification             |
| `promotion_offer`      | Discounts, coupons and merchant offers               |
| `security_alert`       | Unrecognized access and suspicious activity          |
| `delivery_logistics`   | Shipment status and order tracking                   |
| `appointment_reminder` | Medical and dental appointment reminders             |
| `customer_service`     | Tickets, claims and support updates                  |
| `spam_advertising`     | Fraudulent messages and misleading advertising       |
| `billing_reminder`     | Pending invoices and payment due dates               |

## Tech stack

- **Python 3.11** + **FastAPI** + **Uvicorn**
- **DistilBERT** (`distilbert-base-multilingual-cased`) via HuggingFace Transformers
- **PyTorch** (CPU-only in production)
- **Pydantic v2** for validation
- **Docker** for containerization
- **Hugging Face Spaces** for deployment
- **Hugging Face Hub** for model hosting

## Project structure

```
app/
├── main.py                      # App entry point
├── utils.py                     # normalize(), read_static()
├── core/                        # Shared infrastructure
│   ├── cache.py                 # Thread-safe LRU cache
│   ├── model_loader.py          # Downloads and loads the model at startup
│   ├── schemas.py               # Pydantic models
│   └── category_meta.py         # Category metadata
├── services/
│   └── classifier.py            # Inference logic + LRU cache integration
├── api/                         # JSON endpoints
│   ├── inference.py             # POST /classify, POST /classify/batch
│   └── meta.py                  # GET /health, GET /api/categories
├── web/                         # HTML endpoints
│   └── pages.py                 # UI routes
└── templates/                   # HTML files
    ├── home.html
    ├── index.html
    ├── batch.html
    └── categories.html
training/
├── config.py                    # Hyperparameters
├── generate_dataset.py          # Generates training/data/sms_dataset.csv
├── train.py                     # Fine-tuning script
└── eval_report.py               # Per-category metrics report
```

## Run locally

### Requirements

- Python 3.11+
- Trained model in `./model/` (see training section)

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac

# Install dependencies
pip install -r requirements.txt
pip install torch --index-url https://download.pytorch.org/whl/cpu

# Start API
uvicorn app.main:app --reload
```

API available at `http://localhost:8000`

### With Docker

```bash
docker compose up --build
```

## Train the model

```bash
pip install -r requirements-training.txt

cd training
python generate_dataset.py   # generates training/data/sms_dataset.csv
python train.py              # fine-tuning → saves model to ./model/
python eval_report.py        # per-category metrics report
```

## Endpoints

| Method | Route             | Description                        |
| ------ | ----------------- | ---------------------------------- |
| `GET`  | `/`               | Home with API description          |
| `GET`  | `/classify`       | Interactive single classifier (UI) |
| `GET`  | `/classify/batch` | Batch classifier (UI)              |
| `GET`  | `/categories`     | Categories view with examples      |
| `POST` | `/classify`       | Classify one message (JSON)        |
| `POST` | `/classify/batch` | Classify multiple messages (JSON)  |
| `GET`  | `/api/categories` | List categories (JSON)             |
| `GET`  | `/health`         | Service status and cache stats     |

### POST /classify

```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "Your OTP code is 482910. Do not share it."}'
```

```json
{
  "text": "Your OTP code is 482910. Do not share it.",
  "prediction": {
    "category": "otp_verification",
    "confidence": 0.9821
  },
  "top_3": [
    { "category": "otp_verification", "confidence": 0.9821 },
    { "category": "security_alert",   "confidence": 0.0091 },
    { "category": "customer_service", "confidence": 0.0044 }
  ],
  "cached": false
}
```

### POST /classify/batch

```bash
curl -X POST http://localhost:8000/classify/batch \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Your OTP code is 482910.", "Your card was charged $45 at Amazon."]}'
```

```json
{
  "results": [...],
  "total": 2,
  "from_cache": 0
}
```

## Deploy on Hugging Face Spaces

1. Create a Space at [huggingface.co/new-space](https://huggingface.co/new-space) with SDK: **Docker**
2. Push the code to the Space repo:
   ```bash
   git remote add hfspace https://USER:TOKEN@huggingface.co/spaces/USER/SPACE-NAME
   git push hfspace main
   ```
3. HF Spaces detects the `Dockerfile` automatically and builds the image
4. On startup, the model is downloaded from HF Hub (~520MB, first time only)

Model hosted at [huggingface.co/cmeneses99/sms-classifier](https://huggingface.co/cmeneses99/sms-classifier).
