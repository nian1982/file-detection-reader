from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class NotificationResult:
    success: bool
    channel: str
    message_id: str | None = None
    error: str | None = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)
