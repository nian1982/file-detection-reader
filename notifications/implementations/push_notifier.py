from notifications.models.notification_request import NotificationRequest
from notifications.models.notification_result import NotificationResult


class PushNotifier:

    def send(self, request: NotificationRequest) -> NotificationResult:
        try:
            print(f"[PUSH] To: {request.recipient} - {request.subject}")
            return NotificationResult(
                success=True,
                channel="push",
                message_id=None,
                metadata=dict(request.metadata),
            )
        except Exception as e:
            return NotificationResult(
                success=False,
                channel="push",
                error=str(e),
                metadata=dict(request.metadata),
            )
