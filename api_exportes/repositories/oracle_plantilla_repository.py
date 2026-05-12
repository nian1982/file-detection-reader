from api_exportes.models.plantilla_notificacion import PlantillaNotificacion
from api_exportes.repositories.database import DatabaseConnection
from api_exportes.repositories.plantilla_repository import PlantillaRepository


class OraclePlantillaRepository(PlantillaRepository):
    def __init__(self, db: DatabaseConnection):
        self._db = db

    def find_by_name(self, nombre_plantilla: str) -> list[PlantillaNotificacion]:
        query = """
            SELECT nq.RECIPIENTS, nq."DATA", mt.SUBJECT,
                   mt.MESSAGE_TEMPLATE, mt.VARIABLES
            FROM DBO_.NOTIFICATION_QUEUE nq
            JOIN DBO_.MESSAGE_TEMPLATES mt ON mt.ID = nq.MESSAGE_TEMPLATE_ID
            WHERE nq.STATUS = 'P'
            AND UPPER(TRIM(mt.NAME)) = UPPER(TRIM(:nombre_plantilla))
        """
        rows = self._db.execute(query, {"nombre_plantilla": nombre_plantilla})
        return [self._row_to_model(row) for row in rows]

    def _row_to_model(self, row: dict) -> PlantillaNotificacion:
        return PlantillaNotificacion(
            recipients=row["RECIPIENTS"],
            data=row["DATA"],
            subject=row["SUBJECT"],
            message_template=row["MESSAGE_TEMPLATE"],
            variables=row["VARIABLES"],
        )
