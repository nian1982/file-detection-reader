import mimetypes
import smtplib
import warnings
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from config import get_settings
from notifications.implementations.template_loader import FileTemplateLoader
from notifications.implementations.template_renderer import SimpleTemplateRenderer
from notifications.models.notification_request import NotificationRequest
from notifications.models.notification_result import NotificationResult


class EmailNotifier:

    def __init__(self, template_loader=None, template_renderer=None):
        self._loader = template_loader or FileTemplateLoader(
            Path(__file__).parent.parent / "templates"
        )
        self._renderer = template_renderer or SimpleTemplateRenderer()

    def test_connection(self) -> NotificationResult:
        try:
            settings = get_settings()
            with smtplib.SMTP(
                settings.smtp_host, settings.smtp_port, timeout=30
            ) as server:
                if settings.smtp_tls:
                    server.starttls()
                server.login(settings.smtp_user, settings.smtp_pass)
                server.quit()
            return NotificationResult(
                success=True,
                channel="email",
                message_id=None,
            )
        except Exception as e:
            return NotificationResult(
                success=False,
                channel="email",
                error=str(e),
            )

    def send(self, request: NotificationRequest) -> NotificationResult:
        try:
            settings = get_settings()

            template = self._loader.load(request.template_name)
            body = self._renderer.render(template, request.placeholders)
            subject = self._renderer.render(request.subject, request.placeholders)

            recipient = request.recipient.strip().rstrip(",").strip()
            if not recipient:
                raise ValueError("Recipient email is empty")

            msg = MIMEMultipart()
            msg["From"] = settings.smtp_user
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "html"))

            max_bytes = settings.attachment_max_size_mb * 1024 * 1024
            allowed_extensions = settings.attachment_allowed_types

            for filepath in request.attachments:
                path = Path(filepath)
                if not path.exists():
                    warnings.warn(f"Attachment not found: {filepath}")
                    continue

                if path.suffix.lower() not in allowed_extensions:
                    warnings.warn(
                        f"Attachment type not allowed: {filepath} "
                        f"(allowed: {allowed_extensions})"
                    )
                    continue

                if path.stat().st_size > max_bytes:
                    warnings.warn(
                        f"Attachment too large: {filepath} "
                        f"({path.stat().st_size} bytes > {max_bytes} bytes)"
                    )
                    continue

                with path.open("rb") as f:
                    ctype, _ = mimetypes.guess_type(path.name)
                    if ctype is None:
                        ctype = "application/octet-stream"
                    maintype, subtype = ctype.split("/", 1)
                    part = MIMEBase(maintype, subtype, name=path.name)
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        "attachment",
                        filename=path.name,
                    )
                    msg.attach(part)

            with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=30) as server:
                if settings.smtp_tls:
                    server.starttls()
                server.login(settings.smtp_user, settings.smtp_pass)
                server.send_message(msg)

            metadata = dict(request.metadata)
            metadata.update({
                "smtp_host": settings.smtp_host,
                "smtp_port": settings.smtp_port,
                "attachments_count": len(request.attachments),
            })

            return NotificationResult(
                success=True,
                channel="email",
                message_id=msg["Message-ID"],
                metadata=metadata,
            )

        except Exception as e:
            return NotificationResult(
                success=False,
                channel="email",
                error=str(e),
                metadata=dict(request.metadata),
            )
