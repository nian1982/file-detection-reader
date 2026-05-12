from typing import Protocol
from api_exportes.models.plantilla_notificacion import PlantillaNotificacion


class PlantillaRepository(Protocol):
    def find_by_name(self, nombre_plantilla: str) -> list[PlantillaNotificacion]: ...
