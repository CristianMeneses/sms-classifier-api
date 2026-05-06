# Usage Guide

Base URL: `https://cmeneses99-sms-classifier-api.hf.space`

---

## Via Browser (UI)

### Home
Open `https://cmeneses99-sms-classifier-api.hf.space` to see a description of the API with all available endpoints and response examples. From there you can navigate to any view using the buttons.

---

### Classify a single message
1. Click **"Clasificador Simple"** from the home (or navigate directly to `/classify`)
2. Type the message in the text field
3. Click **"Clasificar"** or press **Enter**
4. The result shows the detected category, confidence score and the top 3 most likely categories
5. If the same text was already classified before, a **"caché activo"** badge appears

---

### Classify multiple messages
1. Click **"Clasificador por Lotes"** from the home (or navigate directly to `/classify/batch`)
2. Type one message per line in the text area
3. A real-time counter shows how many messages you have loaded (max 50)
4. Click **"Clasificar todo"**
5. Results appear one by one with their category and confidence
6. The summary bar at the bottom shows how many results came from cache

---

### Browse available categories
1. Click **"Categorías"** from the home (or navigate directly to `/categories`)
2. Each category shows its description and an example in Spanish and English

---

## Via API (curl)

### Classify one message

```bash
curl -X POST https://cmeneses99-sms-classifier-api.hf.space/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "Your OTP code is 482910. Do not share it."}'
```

```json
{
  "text": "Your OTP code is 482910. Do not share it.",
  "prediction": { "category": "otp_verification", "confidence": 0.9821 },
  "top_3": [
    { "category": "otp_verification", "confidence": 0.9821 },
    { "category": "security_alert",   "confidence": 0.0091 },
    { "category": "customer_service", "confidence": 0.0044 }
  ],
  "cached": false
}
```

**Limit:** max 512 characters per message.

---

### Classify multiple messages

```bash
curl -X POST https://cmeneses99-sms-classifier-api.hf.space/classify/batch \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "Your card was charged $45 at Amazon.",
      "Your package will arrive tomorrow between 2-4pm.",
      "Pay your bill today and avoid penalties."
    ]
  }'
```

```json
{
  "results": [
    { "text": "Your card was charged $45 at Amazon.", "prediction": { "category": "transaction", "confidence": 0.97 }, "top_3": [...], "cached": false },
    { "text": "Your package will arrive tomorrow...", "prediction": { "category": "delivery_logistics", "confidence": 0.95 }, "top_3": [...], "cached": false },
    { "text": "Pay your bill today...", "prediction": { "category": "billing_reminder", "confidence": 0.91 }, "top_3": [...], "cached": false }
  ],
  "total": 3,
  "from_cache": 0
}
```

**Limit:** max 50 messages per request.

---

### List categories

```bash
curl https://cmeneses99-sms-classifier-api.hf.space/api/categories
```

```json
["transaction", "otp_verification", "promotion_offer", "security_alert",
 "delivery_logistics", "appointment_reminder", "customer_service",
 "spam_advertising", "billing_reminder"]
```

---

### Health check

```bash
curl https://cmeneses99-sms-classifier-api.hf.space/health
```

```json
{
  "status": "ok",
  "model_loaded": true,
  "cache": { "hits": 12, "misses": 5, "hit_rate": 0.71, "size": 5 }
}
```

---

## Categories

| Category               | Examples                                                                          |
|------------------------|-----------------------------------------------------------------------------------|
| `transaction`          | "Your card was charged $45 at Amazon" / "Se debitó $45.000 en Falabella"         |
| `otp_verification`     | "Your OTP code is 482910" / "Tu código OTP es 482910"                            |
| `promotion_offer`      | "Exclusive offer just for you" / "30% de descuento este fin de semana"           |
| `security_alert`       | "Failed login attempt detected" / "Acceso no reconocido desde Berlín"            |
| `delivery_logistics`   | "Your package will arrive tomorrow" / "Tu pedido está en camino"                 |
| `appointment_reminder` | "Dental appointment confirmed" / "Recordatorio: cita médica mañana a las 10am"  |
| `customer_service`     | "Your case has been escalated" / "Tu ticket #4821 fue resuelto"                  |
| `spam_advertising`     | "You have been selected for a reward" / "Ganaste un premio, haz clic aquí"       |
| `billing_reminder`     | "Pay your bill today and avoid penalties" / "Tu factura vence el 15 de mayo"     |
