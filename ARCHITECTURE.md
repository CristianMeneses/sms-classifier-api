# Arquitectura

## Despliegue

```
GitHub (código fuente)
    │
    └─► Hugging Face Spaces (runtime Docker)
            │  construye y ejecuta el contenedor FastAPI
            │
            ├─► al iniciar: descarga el modelo desde HF Hub
            │       huggingface.co/cmeneses99/sms-classifier
            │       (model.safetensors, tokenizer, config — ~520MB)
            │
            └─► expone la API en el puerto 7860
                    https://cmeneses99-sms-classifier-api.hf.space

cron-job.org ──GET /health cada 10min──► HF Spaces (keep-alive)
```

## Flujo de una solicitud

```
Cliente
  │
  ▼
FastAPI (routers/)
  │
  ├── pages.py      → respuestas HTML (/, /classify, /classify/batch, /categories)
  ├── inference.py  → POST /classify, POST /classify/batch
  └── meta.py       → GET /health, GET /api/categories
        │
        ▼
services/classifier.py
  │
  ├── Cache LRU (cache.py) ──hit──► retorna respuesta en caché
  │
  └── miss ──► model_loader.py (pipeline de HuggingFace)
                    └── distilbert-base-multilingual-cased (fine-tuned)
                            └── top_k=3 predicciones → PredictResponse
```

## Modelo

| Detalle | Valor |
|---|---|
| Modelo base | `distilbert-base-multilingual-cased` |
| Tarea | Clasificación de secuencias |
| Categorías | 9 |
| Datos de entrenamiento | 3.150 ejemplos sintéticos (350/categoría, ES + EN) |
| Entrenamiento | 5 épocas, fine-tuning con HuggingFace Trainer API |
| Runtime | Solo CPU (build CPU de PyTorch) |
| Cache | LRU, máx. 512 entradas, thread-safe |

## Estructura del proyecto

```
app/
├── main.py                      # Lifespan + registro de routers
├── utils.py                     # normalize(), read_static()
├── core/                        # Infraestructura compartida
│   ├── cache.py                 # Cache LRU thread-safe
│   ├── model_loader.py          # Descarga el modelo desde HF Hub al iniciar
│   ├── schemas.py               # Modelos Pydantic v2 para request/response
│   └── category_meta.py         # Labels, colores y ejemplos por categoría
├── services/
│   └── classifier.py            # Lógica de inferencia con integración de caché
├── api/                         # Endpoints JSON
│   ├── inference.py             # POST /classify, POST /classify/batch
│   └── meta.py                  # GET /health, GET /api/categories
├── web/                         # Endpoints HTML
│   └── pages.py                 # Rutas de UI
└── templates/                   # Archivos HTML
    ├── home.html
    ├── index.html                # UI clasificador simple
    ├── batch.html                # UI clasificador por lotes
    └── categories.html
training/
├── config.py
├── generate_dataset.py
├── train.py
└── eval_report.py
```
