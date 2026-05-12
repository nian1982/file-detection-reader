from api_exportes.models.plantilla_notificacion import PlantillaNotificacion
from api_exportes.repositories.plantilla_repository import PlantillaRepository
from api_exportes.services.export_service import ExportService


class ExportServiceImpl(ExportService):
    def __init__(self, repository: PlantillaRepository):
        self._repository = repository

    def export_by_plantilla(self, nombre_plantilla: str) -> list[PlantillaNotificacion]:
        resultados = self._repository.find_by_name(nombre_plantilla)
        if not resultados:
            raise ValueError(
                f"No hay notificaciones pendientes para la plantilla "
                f"'{nombre_plantilla}'"
            )
        return resultados
