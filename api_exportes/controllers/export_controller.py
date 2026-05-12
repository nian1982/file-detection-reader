from fastapi import HTTPException, status
from api_exportes.models.plantilla_notificacion import PlantillaNotificacion
from api_exportes.services.export_service import ExportService


class ExportController:
    def __init__(self, service: ExportService):
        self._service = service

    def export_by_plantilla(
        self, nombre_plantilla: str
    ) -> list[PlantillaNotificacion]:
        try:
            return self._service.export_by_plantilla(nombre_plantilla)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )
