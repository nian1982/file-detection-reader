import json
import sys
from dataclasses import asdict

from api_exportes.repositories.oracle_database import OracleDatabase
from api_exportes.repositories.oracle_plantilla_repository import (
    OraclePlantillaRepository,
)
from api_exportes.services_impl.export_service_impl import ExportServiceImpl


def main(nombre_plantilla: str):
    db = OracleDatabase()
    repo = OraclePlantillaRepository(db)
    service = ExportServiceImpl(repo)
    resultados = service.export_by_plantilla(nombre_plantilla)
    for r in resultados:
        print(json.dumps(asdict(r), indent=2, default=str))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python -m api_exportes.cli <nombre_plantilla>", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
