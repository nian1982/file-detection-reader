import psycopg2
from psycopg2.extras import RealDictCursor
from config import get_settings


class PostgresDatabase:
    def __init__(self):
        settings = get_settings()
        self._conn = psycopg2.connect(
            host=settings.postgres_host,
            port=settings.postgres_port,
            user=settings.postgres_user,
            password=settings.postgres_password,
            database=settings.postgres_database,
        )

    def execute(self, query: str, params: dict | tuple | None = None) -> list[dict]:
        if isinstance(params, dict):
            params = tuple(params.values())
        with self._conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            self._conn.commit()
            return [dict(r) for r in cur.fetchall()]
