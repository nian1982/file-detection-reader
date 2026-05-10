# Sistema de Notificaciones

Sistema para enviar notificaciones por **Email**, **SMS** y **Push**. Sigue una arquitectura limpia donde cada canal es independiente y se pueden agregar nuevos sin modificar el código existente.

---

## Canales disponibles

| Canal | Estado | Proveedor |
|---|---|---|
| Email | Funcional | SMTP (Gmail, Outlook, etc.) |
| SMS | Funcional | Twilio |
| Push | Simulado | Log en consola |

---

## Configuración inicial

### 1. Archivo `.env`

Renombrar `.env.example` a `.env` (o editar el existente) y completar:

```ini
# === EMAIL (SMTP) ===
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu_correo@gmail.com
SMTP_PASS=tu_app_password    # Para Gmail: usar App Password (no la contraseña normal)
SMTP_TLS=true

# === ADJUNTOS ===
ATTACHMENT_MAX_SIZE_MB=50
ATTACHMENT_ALLOWED_TYPES=.xlsx,.xls,.csv,.pdf

# === SMS (Twilio) ===
# 1. Crear cuenta en https://twilio.com (dan $15 de crédito)
# 2. Obtener: Account SID, Auth Token
# 3. Comprar un número telefónico con capacidad SMS
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_FROM_NUMBER=+12025551234

# === LISTAS DE CORREO ===
RECIPIENTS_FILE_PATH=notifications/config/recipients.json
```

### 2. Obtener App Password de Gmail (para email)

1. Activar verificación en dos pasos en https://myaccount.google.com/security
2. Ir a https://myaccount.google.com/apppasswords
3. Generar una contraseña de aplicación para "Correo"
4. Copiar esa contraseña en `SMTP_PASS`

### 3. Configurar Twilio (para SMS)

1. Crear cuenta en https://twilio.com (crédito gratuito ~$15)
2. En la consola, copiar **Account SID** y **Auth Token**
3. Comprar un número telefónico (menú: Phone Numbers > Buy a Number)
4. Poner los 3 valores en `.env`

---

## Cómo probar

### Probar conexión SMTP (email)

```bash
cd /ruta/del/proyecto
source .venv/bin/activate
python -m notifications.main
```

Esto ejecuta todos los ejemplos. Para probar solo la conexión email:

```bash
python -c "
from notifications import NotificationService
s = NotificationService()
r = s.test_email_connection()
print(f'Conexión SMTP: {\"OK\" if r.success else \"FALLO: \" + r.error}')
"
```

### Probar envío de email simple

```python
python -c "
from notifications import NotificationService, NotificationRequest, NotificationChannel

s = NotificationService()
r = s.notify(NotificationRequest(
    channel=NotificationChannel.EMAIL,
    recipient='correo@ejemplo.com',
    subject='Hola {{nombre}}',
    template_name='notification_email.html',
    placeholders={
        'notification_type': 'INFO',
        'subject': 'Hola Juan',
        'intro': 'Este es un mensaje de prueba.',
        'cause': 'Motivo del mensaje',
        'job_name': 'tarea_ejemplo',
        'execution_time': '2026-05-09 10:00:00',
        'attachment_msg': '',
        'table': '',
        'nombre': 'Juan',           # placeholders adicionales para el subject
    },
))
print(f'Enviado: {r.success}')
"
```

### Probar envío de SMS

Requiere Twilio configurado en `.env`.

```bash
python -c "
from notifications import NotificationService, NotificationRequest, NotificationChannel

s = NotificationService()
r = s.notify(NotificationRequest(
    channel=NotificationChannel.SMS,
    recipient='+573002345678',         # Número con código de país
    subject='Tu código de verificación es: 123456',
    template_name='notification_email.html',
    placeholders={
        'intro': 'Código de verificación',
        'cause': '',
        'job_name': '',
        'execution_time': '',
        'attachment_msg': '',
        'table': '',
    },
))
print(f'SMS enviado: {r.success}')
"
```

### Probar envío a una lista de correos

Editar `notifications/config/recipients.json` y agregar:

```json
{
  "lists": [
    {
      "id": "facturacion",
      "recipients": ["juan@empresa.com", "maria@empresa.com"],
      "description": "Equipo de facturación"
    }
  ]
}
```

Luego enviar:

```bash
python -c "
from notifications import NotificationService, NotificationRequest, NotificationChannel

s = NotificationService()
resultados = s.notify_by_key(NotificationRequest(
    channel=NotificationChannel.EMAIL,
    recipient_key='facturacion',
    subject='Reporte {{MES}}',
    template_name='notification_email.html',
    placeholders={
        'MES': 'MAYO',
        'intro': 'Reporte mensual adjunto.',
        'cause': 'Cierre mensual',
        'job_name': 'reporte_mensual',
        'execution_time': '2026-05-09',
        'attachment_msg': '',
        'table': '',
    },
))
for r in resultados:
    print(f'Para: {r.channel} -> OK: {r.success}')
"
```

---

## Consumo desde la API (FastAPI)

El sistema de notificaciones también se expone como API REST. Los endpoints son:

### 1. Probar conexión SMTP

```
GET /notifications/test-email
```

Respuesta:
```json
{
  "success": true,
  "channel": "email",
  "error": null
}
```

### 2. Enviar una notificación

```
POST /notifications/send
```

**Body (JSON):**

| Campo | Requerido | Descripción |
|---|---|---|
| `channel` | Sí | Medio: `"email"`, `"sms"` o `"push"` |
| `recipient` | No | Destinatario (email o número de teléfono). Obligatorio si no se usa `recipient_key` |
| `recipient_key` | No | Clave de lista de destinatarios (ver sección de listas) |
| `subject` | Sí | Asunto del mensaje. Puede tener `{{placeholders}}` |
| `template_name` | No | Plantilla (default: `"notification_email.html"`) |
| `attachments` | No | Lista de rutas de archivos a adjuntar. Ej: `["/tmp/reporte.xlsx"]` |
| `metadata` | No | Datos adicionales para auditoría. Ej: `{"origen": "cron"}` |
| `placeholders` | No | Valores que reemplazan los `{{variables}}` en el subject y la plantilla |

**Ejemplo completo con curl:**

```bash
curl -X POST http://localhost:8000/notifications/send \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "email",
    "recipient": "correo@ejemplo.com",
    "subject": "Reporte {{MES}} - {{CIUDAD}}",
    "template_name": "notification_email.html",
    "attachments": ["/tmp/reporte_mensual.xlsx"],
    "metadata": {
      "origen": "cron_job",
      "usuario": "admin"
    },
    "placeholders": {
      "MES": "MAYO",
      "CIUDAD": "BOGOTA",
      "intro": "Se adjunta el reporte de ingresos.",
      "cause": "Cierre mensual Mayo 2026",
      "job_name": "reconocimiento_ingresos",
      "execution_time": "2026-05-09 19:00:00",
      "attachment_msg": "Adjunto encontrarás el detalle.",
      "table": "<table><tr><th>Concepto</th><th>Valor</th></tr><tr><td>Total</td><td>$10,000</td></tr></table>"
    }
  }'
```

**Respuesta:**
```json
{
  "success": true,
  "channel": "email",
  "message_id": "<abc123@mail.gmail.com>",
  "error": null,
  "timestamp": "2026-05-09T19:00:00",
  "metadata": {
    "origen": "cron_job",
    "usuario": "admin",
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "attachments_count": 1
  }
}
```

### 3. Enviar a una lista de destinatarios

```
POST /notifications/send-by-key
```

Envía el mismo mensaje a todos los correos de una lista definida en `recipients.json`.

```bash
curl -X POST http://localhost:8000/notifications/send-by-key \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "email",
    "recipient_key": "facturacion",
    "subject": "Reporte mensual",
    "placeholders": {
      "intro": "Reporte adjunto",
      "cause": "Cierre mensual",
      "job_name": "reporte",
      "execution_time": "2026-05-09",
      "attachment_msg": "",
      "table": ""
    }
  }'
```

Respuesta: lista de resultados, uno por cada destinatario.

### 4. Enviar múltiples notificaciones

```
POST /notifications/send-multiple
```

```bash
curl -X POST http://localhost:8000/notifications/send-multiple \
  -H "Content-Type: application/json" \
  -d '{
    "notifications": [
      {
        "channel": "email",
        "recipient": "correo1@ejemplo.com",
        "subject": "Primera notificación"
      },
      {
        "channel": "sms",
        "recipient": "+573001234567",
        "subject": "Mensaje SMS"
      }
    ]
  }'
```

### 5. Enviar múltiples por clave

```
POST /notifications/send-multiple-by-key
```

Igual que `send-multiple` pero cada notificación puede usar `recipient_key`.

---

## Placeholders (variables en plantillas)

La plantilla `notification_email.html` tiene estos placeholders:

| Placeholder | Dónde se usa | Descripción |
|---|---|---|
| `{{notification_type}}` | Subject / Body | Tipo de notificación (INFO, REPORTE, ALERTA) |
| `{{subject}}` | Subject / Body | Asunto del mensaje |
| `{{intro}}` | Body | Texto de introducción del mensaje |
| `{{cause}}` | Body | Causa o motivo de la notificación |
| `{{job_name}}` | Body | Nombre del proceso que generó la notificación |
| `{{execution_time}}` | Body | Fecha y hora de ejecución |
| `{{attachment_msg}}` | Body | Mensaje sobre archivos adjuntos |
| `{{table}}` | Body | Tabla HTML con datos |

Además, en el **subject** se pueden usar placeholders adicionales como:
```
Asunto: "Reporte {{MES}}_{{CIUDAD}}_{{UNIDAD}}"
```
Y pasar los valores en `placeholders`:
```json
{
  "MES": "MAYO",
  "CIUDAD": "BOGOTA",
  "UNIDAD": "NEGOCIO1"
}
```

---

## Listas de destinatarios

Las listas se definen en `notifications/config/recipients.json`:

```json
{
  "lists": [
    {
      "id": "facturacion",
      "recipients": ["juan@empresa.com", "maria@empresa.com"],
      "description": "Equipo de facturación"
    },
    {
      "id": "soporte",
      "recipients": ["soporte1@empresa.com", "soporte2@empresa.com"],
      "description": "Mesa de ayuda"
    }
  ]
}
```

Se envía usando `recipient_key` en lugar de `recipient`.

---

## Adjuntos

| Propiedad | Valor |
|---|---|
| Formatos permitidos | `.xlsx`, `.xls`, `.csv`, `.pdf` |
| Tamaño máximo | 50 MB (configurable en `.env`) |
| Nombre del archivo | Se usa el nombre real del archivo en disco |

Si un archivo no existe o supera el límite, se muestra una advertencia pero el resto de adjuntos se envían igual.

Para configurar:

```ini
ATTACHMENT_MAX_SIZE_MB=50
ATTACHMENT_ALLOWED_TYPES=.xlsx,.xls,.csv,.pdf
```

---

## Solución de problemas

### El email no llega

1. Probar conexión SMTP:
```bash
curl http://localhost:8000/notifications/test-email
```
2. Verificar credenciales en `.env`
3. Para Gmail: usar App Password, no la contraseña normal
4. Revisar carpeta Spam

### El SMS no llega

1. Verificar que Twilio está configurado en `.env`
2. Verificar saldo en https://console.twilio.com
3. El número destino debe tener formato internacional: `+573001234567`

### Error "noname" en adjuntos

Actualizado. El sistema ahora envía el nombre real del archivo en el `Content-Type` y `Content-Disposition`.

### Error "535 Username and Password not accepted"

Las credenciales SMTP son incorrectas. Para Gmail:
1. Activar verificación en 2 pasos
2. Generar App Password en https://myaccount.google.com/apppasswords
3. Usar ese password en `SMTP_PASS`

---

## Estructura del proyecto

```
notifications/
├── __init__.py                    # Registra los notificadores en la factory
├── main.py                        # Ejemplos de uso (python -m notifications.main)
├── README.md                      # Este archivo
├── config/recipients.json         # Listas de destinatarios
├── templates/
│   └── notification_email.html    # Plantilla HTML del correo
├── models/
│   ├── enums.py                   # NotificationChannel (EMAIL, SMS, PUSH)
│   ├── notification_request.py    # Datos de la solicitud
│   ├── notification_result.py     # Resultado del envío
│   └── recipient_list.py          # Modelo de lista de destinatarios
├── interfaces/
│   ├── notifier.py                # Protocolo que todo notificador debe implementar
│   ├── template_renderer.py       # Protocolo para renderizar plantillas
│   ├── template_loader.py         # Protocolo para cargar plantillas
│   └── recipient_repository.py    # Protocolo para obtener listas de correos
├── implementations/
│   ├── email_notifier.py          # Envío de email vía SMTP
│   ├── sms_notifier.py            # Envío de SMS vía Twilio
│   ├── push_notifier.py           # Push (simulado)
│   ├── template_renderer.py       # Reemplazo de {{placeholders}}
│   ├── template_loader.py         # Carga de archivos HTML
│   └── json_recipient_repository.py # Lee recipients.json
├── factories/
│   └── notifier_factory.py        # Registry: asocia canal con su implementación
└── services/
    └── notification_service.py    # Orquestador: recibe request, elige notifier, envía
```
