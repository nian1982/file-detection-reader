from fastapi import APIRouter, Depends

from dependencies import get_notification_service
from notifications.models.enums import NotificationChannel
from notifications.models.notification_request import NotificationRequest
from notifications.services.notification_service import NotificationService
from schemas.notification_schema import (
    BulkNotificationRequest,
    NotificationRequestSchema,
    NotificationResultSchema,
)


router = APIRouter(prefix="/notifications", tags=["notifications"])


def _to_domain(schema: NotificationRequestSchema) -> NotificationRequest:
    return NotificationRequest(
        channel=NotificationChannel(schema.channel),
        recipient=schema.recipient,
        recipient_key=schema.recipient_key,
        subject=schema.subject,
        template_name=schema.template_name,
        attachments=schema.attachments,
        metadata=schema.metadata,
        placeholders=schema.placeholders.model_dump(),
    )


def _to_response(result) -> NotificationResultSchema:
    return NotificationResultSchema(
        success=result.success,
        channel=result.channel,
        message_id=result.message_id,
        error=result.error,
        timestamp=result.timestamp.isoformat(),
        metadata=result.metadata,
    )


def _to_responses(results: list) -> list[NotificationResultSchema]:
    return [_to_response(r) for r in results]


@router.post("/send")
def send_notification(
    request: NotificationRequestSchema,
    service: NotificationService = Depends(get_notification_service),
):
    domain = _to_domain(request)
    if domain.recipient_key:
        results = service.notify_by_key(domain)
        return _to_responses(results)
    result = service.notify(domain)
    return _to_response(result)


@router.post("/send-by-key")
def send_by_key(
    request: NotificationRequestSchema,
    service: NotificationService = Depends(get_notification_service),
):
    domain = _to_domain(request)
    results = service.notify_by_key(domain)
    return _to_responses(results)


@router.post("/send-multiple")
def send_multiple_notifications(
    request: BulkNotificationRequest,
    service: NotificationService = Depends(get_notification_service),
):
    domains = [_to_domain(s) for s in request.notifications]
    results = service.notify_multiple(domains)
    return _to_responses(results)


@router.post("/send-multiple-by-key")
def send_multiple_by_key(
    request: BulkNotificationRequest,
    service: NotificationService = Depends(get_notification_service),
):
    domains = [_to_domain(s) for s in request.notifications]
    results = service.notify_multiple_by_key(domains)
    return _to_responses(results)


@router.get("/test-email")
def test_email_connection(
    service: NotificationService = Depends(get_notification_service),
):
    return _to_response(service.test_email_connection())
