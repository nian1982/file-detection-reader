from functools import lru_cache
from config import get_settings
from models.product import Product
from repositories.product_repository import ProductRepository
from repositories.product_repository_json import JsonProductRepository
from services.product_service import ProductService
from services_impl.product_service_impl import ProductServiceImpl
from controllers.product_controller import ProductController


def create_repository() -> ProductRepository:
    settings = get_settings()
    if settings.storage_type == "postgres":
        from repositories.product_repository_postgres import PostgresProductRepository
        return PostgresProductRepository()
    return JsonProductRepository(settings.json_file_path)


@lru_cache
def get_repository() -> ProductRepository:
    return create_repository()


def get_service() -> ProductService:
    return ProductServiceImpl(get_repository())


def get_controller() -> ProductController:
    return ProductController(get_service())


from sftp.models.credentials import SFTPCredentials
from sftp.implementations.paramiko_client import ParamikoSFTPClient
from sftp.services.sftp_service import SFTPService


def get_sftp_service() -> SFTPService:
    settings = get_settings()
    creds = SFTPCredentials(
        host=settings.sftp_host,
        port=settings.sftp_port,
        username=settings.sftp_username,
        password=settings.sftp_password,
    )
    client = ParamikoSFTPClient(creds)
    return SFTPService(client)


from pathlib import Path

from notifications.services.notification_service import NotificationService
from notifications.implementations.json_recipient_repository import JsonRecipientRepository


@lru_cache
def get_recipient_repository() -> JsonRecipientRepository:
    settings = get_settings()
    return JsonRecipientRepository(Path(settings.recipients_file_path))


@lru_cache
def get_notification_service() -> NotificationService:
    return NotificationService(
        recipient_repository=get_recipient_repository(),
    )