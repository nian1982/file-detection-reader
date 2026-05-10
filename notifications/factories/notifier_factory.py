from notifications.models.enums import NotificationChannel


class NotifierFactory:

    _notifiers: dict[NotificationChannel, type] = {}

    @classmethod
    def create(cls, channel: NotificationChannel):
        notifier_cls = cls._notifiers.get(channel)
        if not notifier_cls:
            raise ValueError(f"Unsupported notification channel: {channel}")
        return notifier_cls()

    @classmethod
    def register(cls, channel: NotificationChannel, notifier_cls: type) -> None:
        cls._notifiers[channel] = notifier_cls
