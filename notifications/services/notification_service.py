from dataclasses import replace as dc_replace

from notifications.factories.notifier_factory import NotifierFactory
from notifications.interfaces.recipient_repository import RecipientRepository
from notifications.models.enums import NotificationChannel
from notifications.models.notification_request import NotificationRequest
from notifications.models.notification_result import NotificationResult


class NotificationService:

    def __init__(self, factory: NotifierFactory | None = None, recipient_repository: RecipientRepository | None = None):
        self._factory = factory or NotifierFactory()
        self._recipient_repo = recipient_repository

    def notify(self, request: NotificationRequest) -> NotificationResult:
        notifier = self._factory.create(request.channel)
        return notifier.send(request)

    def notify_by_key(self, request: NotificationRequest) -> list[NotificationResult]:
        if not request.recipient_key or not self._recipient_repo:
            return [self.notify(request)]

        recipients = self._recipient_repo.get(request.recipient_key)
        results = []
        for recipient in recipients:
            single = dc_replace(
                request,
                recipient=recipient,
                recipient_key="",
            )
            results.append(self.notify(single))
        return results

    def test_email_connection(self) -> NotificationResult:
        notifier = self._factory.create(NotificationChannel.EMAIL)
        return notifier.test_connection()

    def notify_multiple(
        self, requests: list[NotificationRequest]
    ) -> list[NotificationResult]:
        return [self.notify(r) for r in requests]

    def notify_multiple_by_key(
        self, requests: list[NotificationRequest]
    ) -> list[NotificationResult]:
        results = []
        for req in requests:
            results.extend(self.notify_by_key(req))
        return results
