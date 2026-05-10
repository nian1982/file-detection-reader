from config import get_settings
from notifications.models.notification_request import NotificationRequest
from notifications.models.notification_result import NotificationResult


class SmsNotifier:

    def send(self, request: NotificationRequest) -> NotificationResult:
        try:
            settings = get_settings()
            metadata = dict(request.metadata)

            try:
                from twilio.rest import Client
            except ImportError:
                return NotificationResult(
                    success=False,
                    channel="sms",
                    error="twilio package not installed. Run: pip install twilio",
                    metadata=metadata,
                )

            if not all([settings.twilio_account_sid, settings.twilio_auth_token, settings.twilio_from_number]):
                return NotificationResult(
                    success=False,
                    channel="sms",
                    error="Twilio not configured. Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER in .env",
                    metadata=metadata,
                )

            client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
            message = client.messages.create(
                body=request.subject,
                from_=settings.twilio_from_number,
                to=request.recipient,
            )

            metadata["provider"] = "twilio"
            metadata["twilio_status"] = message.status
            metadata["twilio_sid"] = message.sid

            return NotificationResult(
                success=True,
                channel="sms",
                message_id=message.sid,
                metadata=metadata,
            )

        except Exception as e:
            return NotificationResult(
                success=False,
                channel="sms",
                error=str(e),
                metadata=dict(request.metadata),
            )
