from notifications.factories.notifier_factory import NotifierFactory
from notifications.implementations.email_notifier import EmailNotifier
from notifications.implementations.sms_notifier import SmsNotifier
from notifications.implementations.push_notifier import PushNotifier
from notifications.models.enums import NotificationChannel
from notifications.models.recipient_list import RecipientList
from notifications.services.notification_service import NotificationService
from notifications.models.notification_request import NotificationRequest
from notifications.models.notification_result import NotificationResult

NotifierFactory.register(NotificationChannel.EMAIL, EmailNotifier)
NotifierFactory.register(NotificationChannel.SMS, SmsNotifier)
NotifierFactory.register(NotificationChannel.PUSH, PushNotifier)

__all__ = [
    "NotifierFactory",
    "NotificationService",
    "NotificationRequest",
    "NotificationResult",
    "NotificationChannel",
    "RecipientList",
]
