import oracledb
from shared.config.settings import settings


class OracleDatabase:
    def __init__(self):
        self._pool = oracledb.create_pool(
            host=settings.ORACLE_HOST,
            port=settings.ORACLE_PORT,
            service_name=settings.ORACLE_SERVICE_NAME,
            user=settings.ORACLE_USER,
            password=settings.ORACLE_PASSWORD,
            min=settings.ORACLE_MIN_POOL,
            max=settings.ORACLE_MAX_POOL,
        )

    @staticmethod
    def _lobs_to_str(value):
        if isinstance(value, oracledb.LOB):
            return value.read()
        return value

    def execute(self, query: str, params: dict | tuple | None = None) -> list[dict]:
        with self._pool.acquire() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params or {})
                if cur.description is None:
                    return []
                columns = [col[0] for col in cur.description]
                return [
                    {col: self._lobs_to_str(val) for col, val in zip(columns, row)}
                    for row in cur.fetchall()
                ]
