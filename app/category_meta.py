CATEGORY_META: dict[str, dict] = {
    "transaction": {
        "color": "#3b82f6",
        "description": "Confirmaciones de pagos, débitos, transferencias y compras realizadas.",
        "example_es": "Se debitó $45.000 de tu tarjeta terminada en 4821 en Falabella.",
        "example_en": "Your card ending in 4821 was charged $45 at Amazon.",
    },
    "otp_verification": {
        "color": "#8b5cf6",
        "description": "Códigos de un solo uso para verificar identidad o confirmar acceso.",
        "example_es": "Tu código OTP es 482910. No lo compartas con nadie. Válido 5 min.",
        "example_en": "Your OTP code is 482910. Do not share it with anyone. Valid 5 min.",
    },
    "promotion_offer": {
        "color": "#f59e0b",
        "description": "Descuentos, cupones, cashback y ofertas de comercios.",
        "example_es": "30% de descuento en ropa solo hoy en Ripley. ¡No te lo pierdas!",
        "example_en": "30% off on clothing only today at Target. Don't miss it!",
    },
    "security_alert": {
        "color": "#ef4444",
        "description": "Accesos no reconocidos, intentos fallidos y actividad sospechosa.",
        "example_es": "Detectamos un inicio de sesión desde Berlin. ¿Fuiste tú?",
        "example_en": "We detected a login from Berlin. Was this you?",
    },
    "delivery_logistics": {
        "color": "#10b981",
        "description": "Estado de envíos, despachos, entregas y seguimiento de pedidos.",
        "example_es": "Tu pedido #45231 está en camino. Llega hoy entre 2:00pm y 4:00pm.",
        "example_en": "Your order #45231 is on its way. Arrives today between 2:00pm and 4:00pm.",
    },
    "appointment_reminder": {
        "color": "#06b6d4",
        "description": "Recordatorios de citas médicas, dentales y consultas agendadas.",
        "example_es": "Recordatorio: tienes cita médica el martes a las 10:00am. No faltes.",
        "example_en": "Reminder: you have a medical appointment on Tuesday at 10:00am. Please don't miss it.",
    },
    "customer_service": {
        "color": "#6366f1",
        "description": "Actualizaciones de tickets, reclamos, devoluciones y soporte.",
        "example_es": "Tu caso #3821 fue asignado a un agente. Tiempo estimado: 4 horas.",
        "example_en": "Your case #3821 has been assigned to an agent. Estimated time: 4 hours.",
    },
    "spam_advertising": {
        "color": "#f97316",
        "description": "Mensajes fraudulentos, premios falsos y publicidad engañosa.",
        "example_es": "¡Felicitaciones! Ganaste $500.000. Llama ahora al 300-1234567.",
        "example_en": "Congratulations! You won $500. Call now at 300-1234567.",
    },
    "billing_reminder": {
        "color": "#84cc16",
        "description": "Avisos de facturas pendientes, fechas de vencimiento y cobros próximos.",
        "example_es": "Tu factura de $9.990 vence mañana. Paga para evitar penalidades.",
        "example_en": "Your bill of $9.99 is due tomorrow. Pay now to avoid penalties.",
    },
}
