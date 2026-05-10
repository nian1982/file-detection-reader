from dataclasses import dataclass, field
from typing import Any

from notifications.models.enums import NotificationChannel


@dataclass
class NotificationRequest:
    channel: NotificationChannel
    recipient: str = ""
    recipient_key: str = ""
    subject: str = ""
    template_name: str = ""
    placeholders: dict[str, str] = field(default_factory=dict)
    attachments: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
