from functools import lru_cache

from api_exportes.controllers.export_controller import ExportController
from api_exportes.repositories.oracle_database import OracleDatabase
from api_exportes.repositories.oracle_plantilla_repository import (
    OraclePlantillaRepository,
)
from api_exportes.services.export_service import ExportService
from api_exportes.services_impl.export_service_impl import ExportServiceImpl


def create_database() -> OracleDatabase:
    return OracleDatabase()


def create_repository() -> OraclePlantillaRepository:
    return OraclePlantillaRepository(create_database())


def create_service() -> ExportService:
    return ExportServiceImpl(create_repository())


def create_controller() -> ExportController:
    return ExportController(create_service())


@lru_cache
def get_export_controller() -> ExportController:
    return create_controller()
