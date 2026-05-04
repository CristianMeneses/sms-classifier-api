import csv
import random
from pathlib import Path

random.seed(42)

STORES_ES = ["Falabella", "Ripley", "Lider", "Jumbo", "Amazon", "Uber", "Netflix", "Paris", "Easy", "Rappi", "Shell", "Farmacia Cruz Verde"]
STORES_EN = ["Walmart", "Amazon", "Target", "Uber", "Netflix", "Best Buy", "Walgreens", "Apple Store", "Shell", "CVS"]
TIMES = ["8:00am", "8:30am", "9:00am", "9:30am", "10:00am", "10:30am", "11:00am", "11:30am",
         "2:00pm", "2:30pm", "3:00pm", "3:30pm", "4:00pm", "4:30pm", "5:00pm"]
DAYS_ES = ["lunes", "martes", "miercoles", "jueves", "viernes"]
DAYS_EN = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
SPECIALTIES_ES = ["medica", "odontologica", "oftalmologica", "dermatologica", "de control"]
SPECIALTIES_EN = ["medical", "dental", "ophthalmology", "dermatology", "follow-up"]
CITIES_ES = ["Santiago", "Valparaiso", "Concepcion", "Bogota", "Medellin", "Lima", "Buenos Aires"]
CITIES_EN = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
DEVICES = ["iPhone", "Samsung Galaxy", "Huawei", "PC Windows", "Mac"]
LOCATIONS_ES = ["Colombia", "Argentina", "Peru", "Chile", "Mexico", "Espana", "Berlin", "Paris", "Tokyo", "Londres", "Rusia", "China", "Italia", "Canada", "Australia"]
LOCATIONS_EN = ["USA", "Mexico", "Brazil", "Spain", "Colombia", "Berlin", "Paris", "Tokyo", "Russia", "China", "Italy", "Canada", "Australia", "India", "Nigeria"]
DISCOUNTS = [10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70]
PRODUCTS_ES = ["ropa", "electrodomesticos", "calzado", "tecnologia", "muebles", "perfumes", "deportes", "libros"]
PRODUCTS_EN = ["clothing", "electronics", "shoes", "furniture", "perfumes", "sports gear", "books"]


def amount_es():
    return f"${random.randint(1, 500) * 1000:,}".replace(",", ".")


def amount_small_es():
    return f"${random.randint(500, 9990)}"


def amount_en():
    return f"${random.randint(5, 3000)}"


def order_num():
    return f"#{random.randint(10000, 99999)}"


def ticket_num():
    return f"#{random.randint(1000, 9999)}"


def code():
    return str(random.randint(100000, 999999))


def card_last():
    return str(random.randint(1000, 9999))


def hours():
    return random.randint(1, 48)


def pct():
    return random.choice(DISCOUNTS)


# ── Templates ────────────────────────────────────────────────────────────────

TEMPLATES = {
    "transaction": [
        # Spanish
        lambda: f"debito automatico de {amount_es()} procesado en tu cuenta",
        lambda: f"compra aprobada por {amount_es()} en {random.choice(STORES_ES)}",
        lambda: f"transferencia exitosa de {amount_es()} a cuenta terminada en {card_last()}",
        lambda: f"pago de {amount_es()} a {random.choice(STORES_ES)} completado",
        lambda: f"retiro de {amount_es()} en cajero automatico fue exitoso",
        lambda: f"cargo de {amount_small_es()} aplicado a tu tarjeta terminada en {card_last()}",
        lambda: f"recibiste una transferencia de {amount_es()} en tu cuenta",
        lambda: f"tu compra de {amount_es()} en {random.choice(STORES_ES)} fue autorizada",
        lambda: f"pago de servicios por {amount_small_es()} completado exitosamente",
        lambda: f"suscripcion mensual de {amount_small_es()} cobrada a tarjeta {card_last()}",
        lambda: f"se debito {amount_es()} de tu cuenta corriente terminada en {card_last()}",
        lambda: f"pago exitoso de {amount_small_es()} en comercio {random.choice(STORES_ES)}",
        lambda: f"realizaste una compra de {amount_es()} con tu tarjeta de credito",
        lambda: f"abono de {amount_es()} recibido en tu cuenta de ahorros",
        lambda: f"tu pago de {amount_es()} en {random.choice(STORES_ES)} fue confirmado",
        lambda: f"pagaste {amount_es()} en {random.choice(STORES_ES)}",
        lambda: f"transaccion de {amount_es()} aprobada en {random.choice(STORES_ES)}",
        lambda: f"tu tarjeta fue usada por {amount_es()} en {random.choice(STORES_ES)}",
        lambda: f"operacion bancaria: debito de {amount_es()} procesado correctamente",
        lambda: f"confirmacion: pago de {amount_small_es()} realizado con exito en {random.choice(STORES_ES)}",
        lambda: f"se acredito {amount_es()} en tu cuenta",
        lambda: f"cargo exitoso de {amount_small_es()} a tarjeta terminada en {card_last()}",
        lambda: f"tu compra en {random.choice(STORES_ES)} por {amount_es()} fue procesada",
        # English
        lambda: f"debit of {amount_en()} processed on your account",
        lambda: f"purchase of {amount_en()} approved at {random.choice(STORES_EN)}",
        lambda: f"transfer of {amount_en()} to account ending in {card_last()} completed",
        lambda: f"payment of {amount_en()} to {random.choice(STORES_EN)} confirmed",
        lambda: f"atm withdrawal of {amount_en()} was successful",
        lambda: f"your card ending in {card_last()} was charged {amount_en()} at {random.choice(STORES_EN)}",
        lambda: f"you received a transfer of {amount_en()} to your account",
        lambda: f"monthly subscription of {amount_en()} charged to card {card_last()}",
        lambda: f"transaction of {amount_en()} at {random.choice(STORES_EN)} approved",
        lambda: f"your {amount_en()} payment to {random.choice(STORES_EN)} was processed",
        lambda: f"you spent {amount_en()} at {random.choice(STORES_EN)}",
        lambda: f"card transaction: {amount_en()} debited from your account",
        lambda: f"successful transfer of {amount_en()} to account {card_last()}",
        lambda: f"your purchase of {amount_en()} at {random.choice(STORES_EN)} is confirmed",
    ],

    "otp_verification": [
        # Spanish
        lambda: f"tu codigo otp es {code()}. no lo compartas con nadie",
        lambda: f"codigo de verificacion: {code()}. valido por 5 minutos",
        lambda: f"ingresa {code()} para confirmar tu acceso",
        lambda: f"usa {code()} para verificar tu identidad en nuestra app",
        lambda: f"tu codigo de seguridad es {code()}. expira en 10 minutos",
        lambda: f"{code()} es tu clave temporal de ingreso. no la compartas",
        lambda: f"codigo de autenticacion: {code()}. si no fuiste tu, ignora este mensaje",
        lambda: f"para continuar ingresa el codigo {code()} en la aplicacion",
        lambda: f"tu pin de un solo uso es {code()}. valido solo por esta sesion",
        lambda: f"verificacion en 2 pasos: usa el codigo {code()}",
        lambda: f"codigo de acceso: {code()}. caduca en 3 minutos",
        lambda: f"confirmacion de identidad requerida. tu codigo: {code()}",
        lambda: f"tu token de verificacion es {code()}. no lo reenvies",
        lambda: f"para recuperar tu contrasena usa el codigo {code()}",
        lambda: f"codigo de confirmacion de transaccion: {code()}",
        lambda: f"clave de un solo uso: {code()}. expira en 2 minutos",
        lambda: f"autenticacion de dos factores: {code()} es tu codigo",
        lambda: f"no compartas este codigo: {code()}. nadie te lo pedira",
        lambda: f"tu verificacion telefonica: {code()}",
        lambda: f"codigo temporal {code()} para completar tu registro",
        # English
        lambda: f"your otp code is {code()}. do not share it with anyone",
        lambda: f"verification code: {code()}. valid for 5 minutes",
        lambda: f"enter {code()} to confirm your access",
        lambda: f"use {code()} to verify your identity in our app",
        lambda: f"your security code is {code()}. expires in 10 minutes",
        lambda: f"{code()} is your one-time password. keep it safe",
        lambda: f"authentication code: {code()}. if this was not you, ignore this message",
        lambda: f"2-step verification: use code {code()}",
        lambda: f"your access token is {code()}. expires in 3 minutes",
        lambda: f"transaction confirmation code: {code()}. do not share it",
        lambda: f"one-time pin: {code()}. valid for this session only",
        lambda: f"two-factor authentication code: {code()}",
        lambda: f"never share this code: {code()}. we will never ask for it",
        lambda: f"your login verification code is {code()}",
        lambda: f"complete your sign-in with code {code()}",
    ],

    "promotion_offer": [
        # Spanish
        lambda: f"{pct()}% de descuento en {random.choice(PRODUCTS_ES)} solo por hoy en {random.choice(STORES_ES)}",
        lambda: f"aprovecha {pct()}% off en toda la tienda {random.choice(STORES_ES)} este fin de semana",
        lambda: f"oferta exclusiva: {pct()}% de rebaja en tu proxima compra en {random.choice(STORES_ES)}",
        lambda: f"tienes un cupon de {pct()}% dcto valido hasta el {random.randint(1,28)}/{random.randint(1,12)}",
        lambda: f"2x1 en {random.choice(PRODUCTS_ES)} en {random.choice(STORES_ES)}. solo hoy!",
        lambda: f"descuento especial del {pct()}% para clientes frecuentes de {random.choice(STORES_ES)}",
        lambda: f"ultimas horas: {pct()}% de descuento en {random.choice(PRODUCTS_ES)}. no te lo pierdas",
        lambda: f"tu cashback de {amount_small_es()} esta disponible para usar en {random.choice(STORES_ES)}",
        lambda: f"acumula puntos dobles este fin de semana en {random.choice(STORES_ES)}",
        lambda: f"oferta flash: {pct()}% off en {random.choice(PRODUCTS_ES)} por las proximas 24 horas",
        lambda: f"comprando {amount_es()} o mas en {random.choice(STORES_ES)} obtenes {pct()}% de descuento",
        lambda: f"promo especial: lleva 3 y paga 2 en {random.choice(PRODUCTS_ES)}",
        lambda: f"liquidacion de {random.choice(PRODUCTS_ES)}: hasta {pct()}% de descuento en {random.choice(STORES_ES)}",
        lambda: f"envio gratis en tu proxima compra en {random.choice(STORES_ES)}. valido esta semana",
        lambda: f"regalo de {amount_small_es()} en puntos por tu compra en {random.choice(STORES_ES)}",
        lambda: f"rebaja de {pct()}% en {random.choice(PRODUCTS_ES)} en {random.choice(STORES_ES)} solo este mes",
        lambda: f"oferta de temporada: {pct()}% menos en {random.choice(PRODUCTS_ES)}",
        lambda: f"promocion exclusiva: {pct()}% de descuento en tu siguiente compra en {random.choice(STORES_ES)}",
        lambda: f"sale: todos los {random.choice(PRODUCTS_ES)} a {pct()}% de descuento en {random.choice(STORES_ES)}",
        lambda: f"aprovecha nuestra promo: 3x2 en {random.choice(PRODUCTS_ES)} hasta agotar stock",
        # English
        lambda: f"{pct()}% off on {random.choice(PRODUCTS_EN)} only today at {random.choice(STORES_EN)}",
        lambda: f"exclusive offer: {pct()}% discount on your next purchase at {random.choice(STORES_EN)}",
        lambda: f"flash sale: {pct()}% off {random.choice(PRODUCTS_EN)} for the next 24 hours",
        lambda: f"your {amount_en()} cashback is ready to use at {random.choice(STORES_EN)}",
        lambda: f"double points this weekend at {random.choice(STORES_EN)}",
        lambda: f"buy 2 get 1 free on {random.choice(PRODUCTS_EN)} at {random.choice(STORES_EN)}",
        lambda: f"limited time: {pct()}% off {random.choice(PRODUCTS_EN)} ends tonight",
        lambda: f"free shipping on orders over {amount_en()} at {random.choice(STORES_EN)}",
        lambda: f"members only: {pct()}% discount at {random.choice(STORES_EN)} this week",
        lambda: f"clearance sale: up to {pct()}% off {random.choice(PRODUCTS_EN)} at {random.choice(STORES_EN)}",
        lambda: f"seasonal promo: {pct()}% off all {random.choice(PRODUCTS_EN)} at {random.choice(STORES_EN)}",
        lambda: f"special deal: buy one get one {pct()}% off at {random.choice(STORES_EN)}",
        lambda: f"weekend offer: {pct()}% discount on {random.choice(PRODUCTS_EN)} at {random.choice(STORES_EN)}",
    ],

    "security_alert": [
        # Spanish
        lambda: f"detectamos un inicio de sesion inusual desde {random.choice(LOCATIONS_ES)}. fuiste tu?",
        lambda: f"nuevo dispositivo {random.choice(DEVICES)} accedio a tu cuenta. si no fuiste tu cambia tu contrasena ya",
        lambda: f"intento de acceso fallido {random.randint(2,5)} veces en tu cuenta. la bloqueamos por seguridad",
        lambda: f"alerta: cambio de contrasena realizado. si no lo hiciste contactanos de inmediato",
        lambda: f"actividad sospechosa detectada en tu cuenta. accede y revisa tus movimientos",
        lambda: f"compra de {amount_es()} en {random.choice(STORES_ES)} fue marcada como sospechosa. la rechazamos?",
        lambda: f"tu sesion fue cerrada por seguridad desde ip desconocida. ingresa nuevamente",
        lambda: f"alerta: acceso desde {random.choice(LOCATIONS_ES)} detectado en tu cuenta",
        lambda: f"contrasena incorrecta ingresada {random.randint(3,5)} veces. cuenta bloqueada temporalmente",
        lambda: f"se agrego un nuevo metodo de pago a tu cuenta. si no fuiste tu actua de inmediato",
        lambda: f"alerta de seguridad: tu correo asociado fue cambiado. si no fuiste tu contactanos",
        lambda: f"detectamos un intento de phishing en tu cuenta. no compartas tus datos",
        lambda: f"tu cuenta fue accedida desde {random.choice(DEVICES)} no reconocido. revisa ahora",
        lambda: f"transferencia inusual de {amount_es()} fue bloqueada. confirma si la autorizas",
        lambda: f"verificacion requerida: acceso sospechoso desde {random.choice(LOCATIONS_ES)}",
        lambda: f"detectamos un acceso desde {random.choice(LOCATIONS_ES)}. si no fuiste tu bloquea tu cuenta",
        lambda: f"alguien ingreso a tu cuenta desde {random.choice(LOCATIONS_ES)} a las {random.randint(0,23)}:{random.choice(['00','15','30','45'])}",
        lambda: f"inicio de sesion desde {random.choice(LOCATIONS_ES)} en tu cuenta. reconoces este acceso?",
        lambda: f"acceso no reconocido desde {random.choice(LOCATIONS_ES)} a las {random.randint(0,23)}h. cambia tu contrasena",
        lambda: f"alerta: login desde {random.choice(LOCATIONS_ES)} registrado. si no fuiste tu actua ahora",
        # English
        lambda: f"unusual login detected from {random.choice(LOCATIONS_EN)}. was this you?",
        lambda: f"new device {random.choice(DEVICES)} accessed your account. if this was not you, change your password now",
        lambda: f"failed login attempt {random.randint(2,5)} times. your account has been locked",
        lambda: f"alert: password was changed. if you did not do this, contact us immediately",
        lambda: f"suspicious activity detected on your account. please review your recent activity",
        lambda: f"purchase of {amount_en()} at {random.choice(STORES_EN)} flagged as suspicious. was this you?",
        lambda: f"your session was closed due to suspicious activity. please log in again",
        lambda: f"security alert: access from {random.choice(LOCATIONS_EN)} detected on your account",
        lambda: f"wrong password entered {random.randint(3,5)} times. account temporarily locked",
        lambda: f"a new payment method was added to your account. if this was not you, act now",
        lambda: f"we detected access from {random.choice(LOCATIONS_EN)} at {random.randint(0,23)}:{random.choice(['00','15','30','45'])}. was this you?",
        lambda: f"someone logged into your account from {random.choice(LOCATIONS_EN)}. do you recognize this?",
        lambda: f"login from {random.choice(LOCATIONS_EN)} detected. if this was not you, secure your account now",
        lambda: f"unauthorized access attempt from {random.choice(LOCATIONS_EN)}. your account may be at risk",
        lambda: f"alert: sign in from {random.choice(LOCATIONS_EN)} at {random.randint(0,23)}h. not you? change password",
    ],

    "delivery_logistics": [
        # Spanish
        lambda: f"tu pedido {order_num()} esta en camino. llega hoy entre {random.choice(TIMES)} y {random.choice(TIMES)}",
        lambda: f"paquete {order_num()} fue despachado desde {random.choice(CITIES_ES)}. llega en {random.randint(1,5)} dias habiles",
        lambda: f"entrega programada para manana entre {random.choice(TIMES)} y {random.choice(TIMES)}. alguien debe estar en casa",
        lambda: f"tu pedido llego al centro de distribucion de {random.choice(CITIES_ES)}",
        lambda: f"el repartidor esta a {random.randint(2,15)} paradas de tu direccion. prepara tu entrega",
        lambda: f"intento de entrega fallido para pedido {order_num()}. reagenda en nuestra app",
        lambda: f"tu paquete {order_num()} esta disponible para retiro en sucursal {random.choice(CITIES_ES)}",
        lambda: f"pedido {order_num()} entregado exitosamente. como fue tu experiencia?",
        lambda: f"pedido {order_num()} retrasado por clima. nueva fecha estimada: manana",
        lambda: f"tu compra de {random.choice(STORES_ES)} salio del almacen y va en camino",
        lambda: f"seguimiento actualizado: tu paquete {order_num()} esta en aduana",
        lambda: f"tu envio {order_num()} de {random.choice(STORES_ES)} fue confirmado y esta en preparacion",
        lambda: f"segundo intento de entrega para {order_num()} sera manana a las {random.choice(TIMES)}",
        lambda: f"tu pedido {order_num()} llega manana. descarga la app para seguirlo en tiempo real",
        lambda: f"paquete {order_num()} en camino. firma requerida en la entrega",
        lambda: f"tu envio salio del deposito. numero de seguimiento: {order_num()}",
        lambda: f"entrega exitosa del pedido {order_num()}. recibiste tu paquete?",
        lambda: f"tu pedido {order_num()} esta siendo preparado para despacho",
        lambda: f"aviso de despacho: paquete {order_num()} en camino desde {random.choice(CITIES_ES)}",
        lambda: f"no habia nadie en casa. reprogramamos la entrega de {order_num()} para manana",
        # English
        lambda: f"your order {order_num()} is on its way. arrives today between {random.choice(TIMES)} and {random.choice(TIMES)}",
        lambda: f"package {order_num()} was shipped from {random.choice(CITIES_EN)}. arrives in {random.randint(1,5)} business days",
        lambda: f"delivery scheduled for tomorrow between {random.choice(TIMES)} and {random.choice(TIMES)}",
        lambda: f"your order reached the {random.choice(CITIES_EN)} distribution center",
        lambda: f"your driver is {random.randint(2,15)} stops away. get ready for your delivery",
        lambda: f"delivery attempt failed for order {order_num()}. reschedule in our app",
        lambda: f"order {order_num()} delivered successfully. how was your experience?",
        lambda: f"order {order_num()} delayed due to weather. new estimate: tomorrow",
        lambda: f"your {random.choice(STORES_EN)} purchase has left the warehouse",
        lambda: f"package {order_num()} is out for delivery. signature required",
        lambda: f"shipment {order_num()} is now in transit from {random.choice(CITIES_EN)}",
        lambda: f"we could not deliver your package {order_num()} today. rescheduling for tomorrow",
        lambda: f"tracking update: your parcel {order_num()} is at the sorting facility",
    ],

    "appointment_reminder": [
        # Spanish
        lambda: f"recordatorio: tienes cita {random.choice(SPECIALTIES_ES)} el {random.choice(DAYS_ES)} a las {random.choice(TIMES)}",
        lambda: f"confirmacion de cita medica: {random.choice(DAYS_ES)} {random.randint(1,28)}/{random.randint(1,12)} a las {random.choice(TIMES)}",
        lambda: f"tu turno {random.choice(SPECIALTIES_ES)} es manana a las {random.choice(TIMES)}. no faltes",
        lambda: f"cita medica agendada para el {random.randint(1,28)}/{random.randint(1,12)} a las {random.choice(TIMES)} en clinica central",
        lambda: f"recuerda tu consulta medica manana a las {random.choice(TIMES)} en policlinico norte",
        lambda: f"tu cita en la clinica es en 24 horas, a las {random.choice(TIMES)}. lleva tu carnet",
        lambda: f"para cancelar tu cita {random.choice(SPECIALTIES_ES)} del {random.choice(DAYS_ES)} responde CANCELAR",
        lambda: f"confirmamos tu cita medica para el {random.randint(1,28)}/{random.randint(1,12)} a las {random.choice(TIMES)}",
        lambda: f"recordatorio de cita {random.choice(SPECIALTIES_ES)}: {random.choice(DAYS_ES)} a las {random.choice(TIMES)}",
        lambda: f"tu reserva en clinica dental es manana {random.randint(1,28)}/{random.randint(1,12)} a las {random.choice(TIMES)}",
        lambda: f"tienes una consulta medica programada para manana. presentate en recepcion a las {random.choice(TIMES)}",
        lambda: f"te esperamos el {random.choice(DAYS_ES)} a las {random.choice(TIMES)} para tu control medico. trae resultados previos",
        lambda: f"aviso: tu hora {random.choice(SPECIALTIES_ES)} fue confirmada para el {random.randint(1,28)}/{random.randint(1,12)}",
        lambda: f"recordatorio: manana tienes cita con el doctor a las {random.choice(TIMES)}. llega 10 min antes",
        lambda: f"tu cita {random.choice(SPECIALTIES_ES)} fue reagendada para el {random.choice(DAYS_ES)}. confirma respondiendo SI",
        lambda: f"clinica central: tu consulta del {random.randint(1,28)}/{random.randint(1,12)} esta confirmada",
        lambda: f"no olvides tu cita con el medico el {random.choice(DAYS_ES)} a las {random.choice(TIMES)}",
        lambda: f"hospital norte: recordatorio de tu turno {random.choice(SPECIALTIES_ES)} manana",
        # English
        lambda: f"reminder: you have a {random.choice(SPECIALTIES_EN)} appointment on {random.choice(DAYS_EN)} at {random.choice(TIMES)}",
        lambda: f"your {random.choice(SPECIALTIES_EN)} appointment is confirmed for {random.randint(1,28)}/{random.randint(1,12)} at central clinic",
        lambda: f"your {random.choice(SPECIALTIES_EN)} appointment is tomorrow at {random.choice(TIMES)}. please do not miss it",
        lambda: f"to cancel your {random.choice(SPECIALTIES_EN)} appointment on {random.choice(DAYS_EN)}, reply CANCEL",
        lambda: f"your dental clinic appointment is scheduled for tomorrow at {random.choice(TIMES)}",
        lambda: f"we confirm your medical appointment for {random.randint(1,28)}/{random.randint(1,12)}. bring your id",
        lambda: f"appointment reminder: {random.choice(SPECIALTIES_EN)} checkup on {random.choice(DAYS_EN)}. please arrive 10 minutes early",
        lambda: f"your doctor appointment has been rescheduled to {random.choice(DAYS_EN)} at {random.choice(TIMES)}",
        lambda: f"see you on {random.choice(DAYS_EN)} at {random.choice(TIMES)} for your {random.choice(SPECIALTIES_EN)} visit",
        lambda: f"please confirm your medical appointment for tomorrow by replying YES",
        lambda: f"health clinic: your {random.choice(SPECIALTIES_EN)} checkup is confirmed for {random.choice(DAYS_EN)}",
        lambda: f"do not forget your doctor appointment on {random.choice(DAYS_EN)} at {random.choice(TIMES)}",
    ],

    "customer_service": [
        # Spanish
        lambda: f"tu caso {ticket_num()} fue asignado a un agente. tiempo estimado: {hours()} horas",
        lambda: f"tu solicitud ha sido recibida. te contactaremos en {random.randint(1,5)} dias habiles",
        lambda: f"gracias por contactarnos. tu ticket {ticket_num()} esta en proceso",
        lambda: f"tu devolucion de {amount_small_es()} fue aprobada. acreditaremos en {random.randint(3,10)} dias habiles",
        lambda: f"resolvimos tu caso {ticket_num()}. como calificarias la atencion?",
        lambda: f"un agente te contactara en los proximos {random.randint(10,60)} minutos",
        lambda: f"tu reclamo {ticket_num()} fue escalado a nivel 2. te informaremos pronto",
        lambda: f"actualizamos tu ticket {ticket_num()} con nueva informacion. revisa tu email",
        lambda: f"tu contrato fue renovado exitosamente hasta {random.randint(1,12)}/{random.randint(2025,2026)}",
        lambda: f"encuesta: como fue tu experiencia con nuestro servicio al cliente?",
        lambda: f"tu solicitud de cambio de plan fue procesada exitosamente",
        lambda: f"hemos recibido tu pago. tu servicio fue reactivado",
        lambda: f"tu caso esta siendo revisado por nuestro equipo. respuesta en {random.randint(1,72)} horas",
        lambda: f"cerramos tu ticket {ticket_num()} por resolucion exitosa. gracias por contactarnos",
        lambda: f"notificacion: tu solicitud {ticket_num()} paso a estado en revision",
        lambda: f"reembolso de {amount_small_es()} procesado. veras el credito en {random.randint(3,7)} dias",
        lambda: f"tu queja fue registrada bajo el numero {ticket_num()}. te responderemos pronto",
        lambda: f"soporte tecnico: tu incidencia {ticket_num()} esta siendo atendida",
        lambda: f"tu solicitud de baja fue recibida. procesaremos en {random.randint(1,5)} dias habiles",
        lambda: f"actualizacion de tu caso {ticket_num()}: en revision por equipo especializado",
        # English
        lambda: f"your case {ticket_num()} has been assigned to an agent. estimated time: {hours()} hours",
        lambda: f"your request has been received. we will contact you within {random.randint(1,5)} business days",
        lambda: f"thank you for contacting us. your ticket {ticket_num()} is being processed",
        lambda: f"your refund of {amount_en()} has been approved. it will be credited in {random.randint(3,10)} business days",
        lambda: f"we resolved your case {ticket_num()}. how would you rate our service?",
        lambda: f"an agent will contact you within the next {random.randint(10,60)} minutes",
        lambda: f"your complaint {ticket_num()} has been escalated to level 2. we will keep you updated",
        lambda: f"we updated your ticket {ticket_num()} with new information. check your email",
        lambda: f"your plan change request has been processed successfully",
        lambda: f"survey: how was your experience with our customer service team?",
        lambda: f"your cancellation request {ticket_num()} has been received and is being processed",
        lambda: f"support ticket {ticket_num()} opened. our team will respond within {hours()} hours",
        lambda: f"your refund request is under review. we will notify you within {random.randint(1,5)} business days",
    ],

    "billing_reminder": [
        # Spanish
        lambda: f"tienes una factura pendiente de {amount_small_es()}. paga antes del {random.randint(1,28)}/{random.randint(1,12)} para evitar recargos",
        lambda: f"recordatorio: tu pago de {amount_small_es()} vence manana. evita penalidades",
        lambda: f"tu factura del mes esta disponible. monto a pagar: {amount_small_es()}",
        lambda: f"aviso de cobro: debes {amount_small_es()} con vencimiento el {random.randint(1,28)}/{random.randint(1,12)}",
        lambda: f"paga tu servicio antes del {random.randint(1,28)} para evitar la suspension",
        lambda: f"tu cuenta tiene un saldo pendiente de {amount_small_es()}. regulariza tu situacion",
        lambda: f"ultimo aviso: factura de {amount_small_es()} vence hoy. paga ahora para evitar corte",
        lambda: f"recordatorio de pago: {amount_small_es()} con vencimiento el {random.randint(1,28)}/{random.randint(1,12)}",
        lambda: f"tu plan vence en {random.randint(1,7)} dias. renueva para no perder el servicio",
        lambda: f"deuda pendiente de {amount_small_es()}. paga antes del {random.randint(1,28)} para evitar intereses",
        lambda: f"factura mensual generada por {amount_small_es()}. fecha limite de pago: {random.randint(1,28)}/{random.randint(1,12)}",
        lambda: f"tu servicio sera suspendido en {random.randint(1,5)} dias por falta de pago. regulariza ya",
        lambda: f"aviso: tienes {random.randint(1,3)} facturas sin pagar. total adeudado: {amount_small_es()}",
        lambda: f"paga tu factura hoy y evita penalidades. monto: {amount_small_es()}",
        lambda: f"recordatorio: el debito automatico de {amount_small_es()} se ejecutara el {random.randint(1,28)}/{random.randint(1,12)}",
        lambda: f"tu suscripcion de {amount_small_es()} se renueva en {random.randint(1,7)} dias",
        lambda: f"segundo aviso: factura vencida de {amount_small_es()}. evita el corte del servicio",
        lambda: f"notificacion de cobro: se intentara debitar {amount_small_es()} de tu cuenta el {random.randint(1,28)}/{random.randint(1,12)}",
        # English
        lambda: f"your bill of {amount_en()} is due on {random.randint(1,28)}/{random.randint(1,12)}. pay now to avoid penalties",
        lambda: f"reminder: your payment of {amount_en()} is due tomorrow. avoid late fees",
        lambda: f"your monthly invoice is ready. amount due: {amount_en()}",
        lambda: f"payment notice: you owe {amount_en()} due on {random.randint(1,28)}/{random.randint(1,12)}",
        lambda: f"pay your bill today and avoid penalties",
        lambda: f"your account has an outstanding balance of {amount_en()}. please settle it",
        lambda: f"final notice: invoice of {amount_en()} due today. pay now to avoid service interruption",
        lambda: f"your subscription of {amount_en()} renews in {random.randint(1,7)} days",
        lambda: f"overdue balance: {amount_en()}. pay before {random.randint(1,28)}/{random.randint(1,12)} to avoid interest",
        lambda: f"your service will be suspended in {random.randint(1,5)} days due to non-payment",
        lambda: f"payment reminder: {amount_en()} due on {random.randint(1,28)}/{random.randint(1,12)}",
        lambda: f"second notice: overdue invoice of {amount_en()}. avoid service interruption",
    ],

    "spam_advertising": [
        # Spanish
        lambda: f"felicitaciones! ganaste un premio de {amount_es()}. llama ahora al {random.randint(300,399)}-{random.randint(1000000,9999999)}",
        lambda: f"gana {amount_es()} desde casa. sin experiencia necesaria. registrate ya!",
        lambda: f"oferta unica! accede ahora antes de que expire: bit.ly/{random.randint(10000,99999)}",
        lambda: f"invierte {amount_small_es()} hoy y gana {amount_es()} en 48 horas garantizado",
        lambda: f"eres el ganador seleccionado de {amount_es()}! reclama tu premio antes de manana",
        lambda: f"trabajo desde casa ganando {amount_es()} al mes. cupos limitados! entra ya",
        lambda: f"promo exclusiva solo para ti! no te lo pierdas: www.oferta{random.randint(1,999)}.com",
        lambda: f"alerta! tu cuenta tiene un bono de {amount_small_es()} pendiente. activalo en 24h",
        lambda: f"replica este metodo secreto y gana {amount_es()} sin salir de casa. mira como",
        lambda: f"te regalamos {amount_small_es()} en creditos. canjealos antes de que expiren hoy",
        lambda: f"sistema automatico de ganancias! genera {amount_es()} mientras duermes",
        lambda: f"urgente: ultimo cupo para ganar {amount_es()}. llama ahora al {random.randint(300,399)}-{random.randint(1000000,9999999)}",
        lambda: f"has sido preseleccionado para ganar {amount_es()}. confirma tus datos ya",
        lambda: f"oferta de inversion: duplica tu dinero en {random.randint(7,30)} dias. 100% garantizado",
        lambda: f"gana puntos canjeables por {amount_es()}. solo hoy! ingresa tu numero",
        lambda: f"haz clic aqui y reclama tu regalo de {amount_es()}: www.premio{random.randint(1,999)}.com",
        lambda: f"eres uno de los {random.randint(5,20)} ganadores seleccionados. actua ahora!",
        lambda: f"metodo probado para ganar {amount_es()} por semana. sin inversion inicial",
        lambda: f"tu numero fue sorteado! llama gratis al {random.randint(300,399)}-{random.randint(1000000,9999999)} para reclamar",
        lambda: f"consigue {amount_es()} adicionales al mes trabajando solo {random.randint(1,4)} horas al dia",
        # English
        lambda: f"congratulations! you won {amount_en()}. call now {random.randint(300,399)}-{random.randint(1000000,9999999)}",
        lambda: f"earn {amount_en()} from home. no experience needed. sign up now!",
        lambda: f"exclusive offer just for you! do not miss it: bit.ly/{random.randint(10000,99999)}",
        lambda: f"invest {amount_en()} today and earn {amount_en()} in 48 hours guaranteed",
        lambda: f"you have been selected to win {amount_en()}! claim your prize before tomorrow",
        lambda: f"work from home earning {amount_en()} per month. limited spots! join now",
        lambda: f"secret method to earn {amount_en()} without leaving home. see how",
        lambda: f"alert! you have a pending bonus of {amount_en()}. activate it within 24h",
        lambda: f"automated profit system! generate {amount_en()} while you sleep",
        lambda: f"urgent: last spot to win {amount_en()}. call now {random.randint(300,399)}-{random.randint(1000000,9999999)}",
        lambda: f"click here to claim your {amount_en()} reward: www.prize{random.randint(1,999)}.com",
        lambda: f"you are one of {random.randint(5,20)} winners selected. act now!",
        lambda: f"proven method to earn {amount_en()} per week. no upfront investment",
        lambda: f"your number was drawn! call free {random.randint(300,399)}-{random.randint(1000000,9999999)} to claim",
    ],
}

EXAMPLES_PER_CATEGORY = 350


def generate():
    rows = []
    for label, templates in TEMPLATES.items():
        for _ in range(EXAMPLES_PER_CATEGORY):
            fn = random.choice(templates)
            rows.append({"text": fn(), "category": label})

    random.shuffle(rows)

    output_path = Path(__file__).parent / "data" / "sms_dataset.csv"
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "category"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Dataset generado: {output_path}")
    print(f"Total ejemplos: {len(rows)}")
    for label in TEMPLATES:
        count = sum(1 for r in rows if r["category"] == label)
        print(f"  {label}: {count}")


if __name__ == "__main__":
    generate()
