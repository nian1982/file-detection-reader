from pydantic import BaseModel, Field


class Placeholders(BaseModel):
    notification_type: str = ""
    subject: str = ""
    intro: str = ""
    cause: str = ""
    job_name: str = ""
    execution_time: str = ""
    attachment_msg: str = ""
    table: str = ""


class NotificationRequestSchema(BaseModel):
    channel: str
    recipient: str = ""
    recipient_key: str = ""
    subject: str = ""
    template_name: str = "notification_email.html"
    attachments: list[str] = []
    metadata: dict[str, str] = Field(default={})
    placeholders: Placeholders = Placeholders()


class NotificationResultSchema(BaseModel):
    success: bool
    channel: str
    message_id: str | None = None
    error: str | None = None
    timestamp: str
    metadata: dict[str, str] = Field(default={})


class BulkNotificationRequest(BaseModel):
    notifications: list[NotificationRequestSchema]
