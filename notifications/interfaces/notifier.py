from typing import Protocol

from notifications.models.notification_request import NotificationRequest
from notifications.models.notification_result import NotificationResult


class Notifier(Protocol):

    def send(self, request: NotificationRequest) -> NotificationResult: ...
