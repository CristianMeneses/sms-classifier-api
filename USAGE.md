# Guía de uso

URL base: `https://cmeneses99-sms-classifier-api.hf.space`

---

## Desde el navegador (UI)

### Home
Abre `https://cmeneses99-sms-classifier-api.hf.space` — vas a ver una descripción de la API con todos los endpoints disponibles y ejemplos de respuesta. Desde ahí puedes navegar al resto de las vistas con los botones.

---

### Clasificar un mensaje
1. Haz click en **"Clasificador Simple"** desde el home (o navega directo a `/classify`)
2. Escribe el mensaje en el campo de texto
3. Haz click en **"Clasificar"** o presiona **Enter**
4. El resultado muestra la categoría detectada, el nivel de confianza y el top 3 de categorías más probables
5. Si el mismo texto ya fue consultado antes, aparece el badge **"caché activo"**

---

### Clasificar múltiples mensajes
1. Haz click en **"Clasificador por Lotes"** desde el home (o navega directo a `/classify/batch`)
2. Escribe un mensaje por línea en el área de texto
3. El contador en tiempo real te muestra cuántos mensajes cargaste (máx. 50)
4. Haz click en **"Clasificar todo"**
5. Los resultados aparecen uno por uno con su categoría y confianza
6. En la barra de resumen inferior puedes ver cuántos vinieron desde caché

---

### Ver categorías disponibles
1. Haz click en **"Categorías"** desde el home (o navega directo a `/categories`)
2. Cada categoría muestra su descripción y un ejemplo en español e inglés

---

## Desde la API (curl)

### Clasificar un mensaje

```bash
curl -X POST https://cmeneses99-sms-classifier-api.hf.space/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "Tu código OTP es 482910. No lo compartas."}'
```

```json
{
  "text": "Tu código OTP es 482910. No lo compartas.",
  "prediction": { "category": "otp_verification", "confidence": 0.9821 },
  "top_3": [
    { "category": "otp_verification", "confidence": 0.9821 },
    { "category": "security_alert",   "confidence": 0.0091 },
    { "category": "customer_service", "confidence": 0.0044 }
  ],
  "cached": false
}
```

**Límite:** máx. 512 caracteres por mensaje.

---

### Clasificar múltiples mensajes

```bash
curl -X POST https://cmeneses99-sms-classifier-api.hf.space/classify/batch \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "Se debitó $45.000 en Falabella.",
      "Your package will arrive tomorrow between 2-4pm.",
      "Pay your bill today and avoid penalties."
    ]
  }'
```

```json
{
  "results": [
    { "text": "Se debitó $45.000 en Falabella.", "prediction": { "category": "transaction", "confidence": 0.97 }, "top_3": [...], "cached": false },
    { "text": "Your package will arrive tomorrow...", "prediction": { "category": "delivery_logistics", "confidence": 0.95 }, "top_3": [...], "cached": false },
    { "text": "Pay your bill today...", "prediction": { "category": "billing_reminder", "confidence": 0.91 }, "top_3": [...], "cached": false }
  ],
  "total": 3,
  "from_cache": 0
}
```

**Límite:** máx. 50 mensajes por request.

---

### Listar categorías

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

## Categorías

| Categoría | Ejemplos |
|---|---|
| `transaction` | "Se debitó $45.000 en Falabella" / "Payment of $120 confirmed" |
| `otp_verification` | "Tu código OTP es 482910" / "Your verification code is 774321" |
| `promotion_offer` | "30% de descuento este fin de semana" / "Exclusive offer just for you" |
| `security_alert` | "Acceso no reconocido desde Berlín" / "Failed login attempt detected" |
| `delivery_logistics` | "Tu pedido está en camino" / "Your package will arrive tomorrow" |
| `appointment_reminder` | "Recordatorio: cita médica mañana a las 10am" / "Dental appointment confirmed" |
| `customer_service` | "Tu ticket #4821 fue resuelto" / "Your case has been escalated" |
| `spam_advertising` | "Ganaste un premio, haz clic aquí" / "You have been selected for a reward" |
| `billing_reminder` | "Tu factura vence el 15 de mayo" / "Pay your bill today and avoid penalties" |
