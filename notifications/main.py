from pathlib import Path

from config import get_settings
from notifications.implementations.json_recipient_repository import JsonRecipientRepository
from notifications.models.enums import NotificationChannel
from notifications.models.notification_request import NotificationRequest
from notifications.models.notification_result import NotificationResult
from notifications.services.notification_service import NotificationService
from utils.files import print_json_format
from datetime import datetime

now = datetime.now()
month = now.month


def _build_service() -> NotificationService:
    repo = JsonRecipientRepository(
        Path(get_settings().recipients_file_path)
    )
    return NotificationService(recipient_repository=repo)


def example_single_push():
    service = _build_service()

    result: NotificationResult = service.notify(
        NotificationRequest(
            channel=NotificationChannel.PUSH,
            recipient="user-device-token",
            subject="Notificación de prueba",
            template_name="notification_email.html",
            placeholders={
                "notification_type": "INFO",
                "subject": "Notificación de prueba",
                "intro": "Este es un mensaje de prueba.",
                "cause": "Verificación del sistema",
                "job_name": "test_job",
                "execution_time": "2026-05-08 19:00:00",
                "attachment_msg": "",
                "table": "",
            },
        )
    )
    print(f"[PUSH] Result: success={result.success}, msg_id={result.message_id}")


def example_email_with_attachments():
    service = _build_service()

    result: NotificationResult = service.notify(
        NotificationRequest(
            channel=NotificationChannel.EMAIL,
            recipient="dataexpress.pruebas@gmail.com",
            subject="Reporte {{MES}} - {{CIUDAD}}",
            template_name="notification_email.html",
            placeholders={
                "MES":str(month),
                "CIUDAD": "BOGOTA",
                "notification_type": "REPORTE",
                "subject": "Reporte MENSUAL - BOGOTA",
                "intro": "Se adjunta el reporte de reconocimiento de ingresos.",
                "cause": "Cierre mensual del período Mayo 2026",
                "job_name": "reconocimiento_ingresos_mensual",
                "execution_time": "2026-05-08 19:00:00",
                "attachment_msg": "Adjunto encontrará los archivos con el detalle.",
                "table": (
                    "<table>"
                    "<tr><th>Concepto</th><th>Valor</th></tr>"
                    "<tr><td>Ingresos reconocidos</td><td>$12,500,000</td></tr>"
                    "<tr><td>Contratos procesados</td><td>45</td></tr>"
                    "</table>"
                ),
            },
            attachments=[
                "/home/nian/Downloads/autorización kiko.pdf",
                "/tmp/detalle_contratos.csv",
            ],
        )
    )
    print(f"[EMAIL] Result: success={result.success}, msg_id={result.message_id}")
    print_json_format(result)


def example_sms():
    service = _build_service()

    result: NotificationResult = service.notify(
        NotificationRequest(
            channel=NotificationChannel.SMS,
            recipient="+573023243413",
            subject="Código: {{CODIGO}}",
            template_name="notification_email.html",
            placeholders={
                "CODIGO": "123456",
                "intro": "Tu código de verificación es: 123456",
                "cause": "Autenticación de dos factores",
                "job_name": "",
                "execution_time": "",
                "attachment_msg": "",
                "table": "",
            },
        )
    )
    print(f"[SMS] Result: success={result.success}, msg_id={result.message_id}")
    print_json_format(result)


def example_notify_by_key():
    service = _build_service()

    results = service.notify_by_key(
        NotificationRequest(
            channel=NotificationChannel.EMAIL,
            recipient_key="facturacion",
            subject="Reporte mensual {{MES}}",
            template_name="notification_email.html",
            placeholders={
                "MES": "MAYO",
                "notification_type": "REPORTE",
                "subject": "Reporte mensual MAYO",
                "intro": "Se adjunta el reporte mensual de facturación.",
                "cause": "Cierre del mes de Mayo 2026",
                "job_name": "reporte_facturacion_mensual",
                "execution_time": "2026-05-08 19:00:00",
                "attachment_msg": "",
                "table": (
                    "<table>"
                    "<tr><th>Cliente</th><th>Monto</th></tr>"
                    "<tr><td>Cliente A</td><td>$5,000,000</td></tr>"
                    "<tr><td>Cliente B</td><td>$3,200,000</td></tr>"
                    "</table>"
                ),
            },
        )
    )
    for r in results:
        print(f"[{r.channel}] To: ..., success={r.success}, msg_id={r.message_id}")


def example_bulk_by_key():
    service = _build_service()

    results = service.notify_multiple_by_key([
        NotificationRequest(
            channel=NotificationChannel.EMAIL,
            recipient_key="soporte",
            subject="Incidencia #{{ID}} reportada",
            template_name="notification_email.html",
            placeholders={
                "intro": "Se ha reportado una nueva incidencia.",
                "cause": "Fallo en el servidor de producción",
                "job_name": "incidencia_1234",
                "execution_time": "2026-05-08 20:00:00",
                "attachment_msg": "",
                "table": "",
            },
        ),
        NotificationRequest(
            channel=NotificationChannel.EMAIL,
            recipient_key="gerencia",
            subject="Alerta crítica en producción",
            template_name="notification_email.html",
            placeholders={
                "intro": "Se ha detectado una anomalía crítica.",
                "cause": "Latencia superior a 5s en APIs críticas",
                "job_name": "alerta_produccion",
                "execution_time": "2026-05-08 20:05:00",
                "attachment_msg": "",
                "table": "",
            },
        ),
    ])
    for r in results:
        print(f"[{r.channel}] success={r.success}, error={r.error}")


def example_bulk_notifications():
    service = _build_service()

    requests = [
        NotificationRequest(
            channel=NotificationChannel.EMAIL,
            recipient="admin@example.com",
            subject="Alerta del sistema",
            template_name="notification_email.html",
            placeholders={
                "intro": "Se detectó un error crítico en el servidor.",
                "cause": "CPU al 100% durante 5 minutos",
                "job_name": "monitoreo_servidor",
                "execution_time": "2026-05-08 19:00:00",
                "attachment_msg": "",
                "table": "",
            },
        ),
        NotificationRequest(
            channel=NotificationChannel.PUSH,
            recipient="device-token-123",
            subject="Notificación push de prueba",
            template_name="notification_email.html",
            placeholders={
                "intro": "Tienes una nueva alerta.",
            },
        ),
    ]

    results = service.notify_multiple(requests)
    for r in results:
        print(f"[{r.channel}] success={r.success}, error={r.error}")


def example_test_email_connection():
    service = _build_service()
    result = service.test_email_connection()
    print(f"[EMAIL CONNECTION] success={result.success}, error={result.error}")


if __name__ == "__main__":
    print("=== Ejemplo Push ===")
    example_single_push()

    print("\n=== Ejemplo Email con adjuntos ===")
    example_email_with_attachments()

    print("\n=== Ejemplo SMS ===")
    example_sms()

    print("\n=== Ejemplo Notificar por clave (lista facturacion) ===")
    example_notify_by_key()

    print("\n=== Ejemplo Múltiples notificaciones por clave ===")
    example_bulk_by_key()

    print("\n=== Test conexión SMTP ===")
    example_test_email_connection()

    print("\n=== Ejemplo Múltiples notificaciones directas ===")
    example_bulk_notifications()
