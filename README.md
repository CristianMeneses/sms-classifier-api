# SMS Classifier API

API REST para clasificar mensajes SMS en categorías usando **DistilBERT multilingual** con fine-tuning sobre un dataset sintético multilingüe (ES + EN).

**Live demo:** https://cmeneses99-sms-classifier-api.hf.space

## Categorías

| Categoría              | Descripción                                       |
| ---------------------- | ------------------------------------------------- |
| `transaction`          | Confirmaciones de pagos, débitos y transferencias |
| `otp_verification`     | Códigos de un solo uso para verificar identidad   |
| `promotion_offer`      | Descuentos, cupones y ofertas de comercios        |
| `security_alert`       | Accesos no reconocidos y actividad sospechosa     |
| `delivery_logistics`   | Estado de envíos y seguimiento de pedidos         |
| `appointment_reminder` | Recordatorios de citas médicas y dentales         |
| `customer_service`     | Tickets, reclamos y soporte                       |
| `spam_advertising`     | Mensajes fraudulentos y publicidad engañosa       |
| `billing_reminder`     | Facturas pendientes y fechas de vencimiento       |

## Stack tecnológico

- **Python 3.11** + **FastAPI** + **Uvicorn**
- **DistilBERT** (`distilbert-base-multilingual-cased`) vía HuggingFace Transformers
- **PyTorch** (CPU-only en producción)
- **Pydantic v2** para validación
- **Docker** para contenedorización
- **Hugging Face Spaces** para deployment
- **Hugging Face Hub** para hosting del modelo

## Estructura del proyecto

```
app/
├── main.py                      # App entry point
├── utils.py                     # normalize(), read_static()
├── core/                        # Infraestructura compartida
│   ├── cache.py                 # LRU cache thread-safe
│   ├── model_loader.py          # Carga del modelo al startup
│   ├── schemas.py               # Modelos Pydantic
│   └── category_meta.py         # Metadata de categorías
├── services/
│   └── classifier.py            # Lógica de inferencia + caché LRU
├── api/                         # Endpoints JSON
│   ├── inference.py             # POST /classify, POST /classify/batch
│   └── meta.py                  # GET /health, GET /api/categories
├── web/                         # Endpoints HTML
│   └── pages.py                 # Rutas de UI
└── templates/                   # Archivos HTML
    ├── home.html
    ├── index.html
    ├── batch.html
    └── categories.html
training/
├── config.py                    # Hiperparámetros
├── generate_dataset.py          # Genera training/data/sms_dataset.csv
├── train.py                     # Fine-tuning script
└── eval_report.py               # Reporte de métricas por categoría
```

## Correr localmente

### Requisitos

- Python 3.11+
- Modelo entrenado en `./model/` (ver sección de entrenamiento)

```bash
# Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
pip install torch --index-url https://download.pytorch.org/whl/cpu

# Levantar API
uvicorn app.main:app --reload
```

API disponible en `http://localhost:8000`

### Con Docker

```bash
docker compose up --build
```

## Entrenar el modelo

```bash
pip install -r requirements-training.txt

cd training
python generate_dataset.py   # genera training/data/sms_dataset.csv
python train.py              # fine-tuning → guarda modelo en ./model/
python eval_report.py        # reporte de métricas por categoría
```

## Endpoints

| Método | Ruta              | Descripción                          |
| ------ | ----------------- | ------------------------------------ |
| `GET`  | `/`               | Home con descripción de la API       |
| `GET`  | `/classify`       | Clasificador interactivo (UI)        |
| `GET`  | `/classify/batch` | Clasificador por lotes (UI)          |
| `GET`  | `/categories`     | Vista de categorías con ejemplos     |
| `POST` | `/classify`       | Clasificar un texto (JSON)           |
| `POST` | `/classify/batch` | Clasificar múltiples textos (JSON)   |
| `GET`  | `/api/categories` | Lista de categorías (JSON)           |
| `GET`  | `/health`         | Estado del servicio y stats de caché |

### POST /classify

```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "Tu código OTP es 482910. No lo compartas."}'
```

```json
{
  "text": "Tu código OTP es 482910. No lo compartas.",
  "prediction": {
    "category": "otp_verification",
    "confidence": 0.9821
  },
  "top_3": [
    { "category": "otp_verification", "confidence": 0.9821 },
    { "category": "security_alert", "confidence": 0.0091 },
    { "category": "customer_service", "confidence": 0.0044 }
  ],
  "cached": false
}
```

### POST /classify/batch

```bash
curl -X POST http://localhost:8000/classify/batch \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Tu código OTP es 482910.", "Se debitó $45.000 en Falabella."]}'
```

```json
{
  "results": [...],
  "total": 2,
  "from_cache": 0
}
```

## Despliegue en Hugging Face Spaces

1. Crea un Space en [huggingface.co/new-space](https://huggingface.co/new-space) con SDK: **Docker**
2. Sube el código al repo del Space:
   ```bash
   git remote add hfspace https://USER:TOKEN@huggingface.co/spaces/USER/SPACE-NAME
   git push hfspace main
   ```
3. HF Spaces detecta el `Dockerfile` automáticamente y hace el build
4. Al iniciar, el modelo se descarga desde HF Hub (~520MB, solo la primera vez)

El modelo está en [huggingface.co/cmeneses99/sms-classifier](https://huggingface.co/cmeneses99/sms-classifier).
