from typing import Protocol
from api_exportes.models.plantilla_notificacion import PlantillaNotificacion


class ExportService(Protocol):
    def export_by_plantilla(self, nombre_plantilla: str) -> list[PlantillaNotificacion]: ...
