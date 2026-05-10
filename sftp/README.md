


Opción 1: Usando dependencies.py (recomendado, estilo producción)
from dependencies import get_sftp_service
service = get_sftp_service()
local = Path("/ruta/local/archivo.csv")
remote_dir = "/upload"
result = service.upload_file(local, remote_dir)
Esto usa la fábrica ya armada en dependencies.py:37-46, que lee las credenciales de las variables de entorno (SFTP_HOST, SFTP_PORT, etc.).

# Módulo SFTP

Cliente SFTP con arquitectura limpia: interfaz, implementación (paramiko), servicios de alto nivel y validación de tipos de archivo.

## Índice

- [Instalación](#instalación)
- [Configuración](#configuración)
- [Estructura](#estructura)
- [Flujo: conexión](#flujo-conexión)
- [Flujo: listar archivos](#flujo-listar-archivos)
- [Flujo: listar solo archivos (sin directorios)](#flujo-listar-solo-archivos-sin-directorios)
- [Flujo: descargar](#flujo-descargar)
- [Flujo: subir](#flujo-subir)
- [Flujo: eliminar](#flujo-eliminar)
- [Flujo: mover / renombrar](#flujo-mover--renombrar)
- [Flujo: organizar archivos en YYYYMMDD/HH](#flujo-organizar-archivos-en-yyyymmddhh)
- [Inyección de dependencias (FastAPI)](#inyección-de-dependencias-fastapi)
- [Validación de tipos de archivo](#validación-de-tipos-de-archivo)
- [Tests](#tests)

---

## Instalación

```bash
pip install paramiko python-dotenv
```

## Configuración

Variables de entorno (`.env`):

```env
SFTP_HOST=127.0.0.1
SFTP_PORT=22
SFTP_USERNAME=usuario
SFTP_PASSWORD=contraseña
```

Se cargan automáticamente vía `config.py`:

```python
from config import get_settings
settings = get_settings()
# settings.sftp_host, settings.sftp_port, ...
```

## Estructura

```
sftp/
├── interfaces/
│   ├── client.py          # SFTPClientProtocol
│   └── validator.py       # FileTypeValidator (Protocol)
├── models/
│   ├── credentials.py     # SFTPCredentials (dataclass frozen)
│   └── results.py         # OperationResult
├── exceptions/
│   └── sftp_exceptions.py # Jerarquía: SFTPError → ...
├── implementations/
│   └── paramiko_client.py # ParamikoSFTPClient
├── services/
│   ├── sftp_service.py    # SFTPService (operaciones individuales)
│   └── file_organization_service.py  # FileOrganizationService
├── validators/
│   └── extension_validator.py  # ExtensionValidator + DATA_EXTENSIONS
├── tests/
│   └── test_sftp_service.py
├── sftp_main.py           # Script de ejemplo
└── __init__.py
```

## Flujo: conexión

Solo es necesaria si usas `ParamikoSFTPClient` directamente. Con `SFTPService` o `FileOrganizationService` el ciclo connect/disconnect es automático.

```python
from sftp import SFTPCredentials, ParamikoSFTPClient

creds = SFTPCredentials(host="127.0.0.1", port=22, username="user", password="pass")
client = ParamikoSFTPClient(creds)
client.connect()
# ... operaciones ...
client.disconnect()
```

## Flujo: listar archivos

Retorna TODO (archivos + directorios):

```python
from sftp import SFTPCredentials, ParamikoSFTPClient, SFTPService

creds = SFTPCredentials(host="...", port=22, username="...", password="...")
service = SFTPService(ParamikoSFTPClient(creds))

result = service.list_files("/ruta/remota")
if result.success:
    print(f"Contenido: {result.data}")
else:
    print(f"Error: {result.message}")
```

## Flujo: listar solo archivos (sin directorios)

```python
result = service.list_files_only("/ruta/remota")
if result.success:
    print(f"Archivos: {result.data}")  # solo .csv, .xlsx, .pdf, etc.
```

## Flujo: descargar

```python
from pathlib import Path

result = service.download_file("/ruta/remota/reporte.csv", Path("/local/reporte.csv"))
if result.success:
    print("Archivo descargado")
```

## Flujo: subir

```python
from pathlib import Path

result = service.upload_file(Path("/local/datos.xlsx"), "/ruta/remota/datos.xlsx")
if result.success:
    print("Archivo subido")
```

## Flujo: eliminar

```python
result = service.delete_file("/ruta/remota/obsoleto.csv")
if result.success:
    print("Archivo eliminado")
```

## Flujo: mover / renombrar

Si el destino existe, lo sobrescribe automáticamente:

```python
result = service.move_file("/ruta/viejo.csv", "/ruta/nuevo.csv")
if result.success:
    print("Archivo movido")
```

## Flujo: organizar archivos en YYYYMMDD/HH

Toma los archivos de un directorio, los clasifica por fecha/hora actual y los mueve a `{fecha}/{hora}/`. Por defecto solo procesa `.csv`, `.xlsx`, `.xls`.

```python
from sftp import SFTPCredentials, ParamikoSFTPClient, FileOrganizationService

creds = SFTPCredentials(host="...", port=22, username="...", password="...")
client = ParamikoSFTPClient(creds)
org = FileOrganizationService(client)

result = org.organize_files("/upload")
if result.success:
    print(f"Archivos archivados: {result.data}")
    # → ["data.csv", "reporte.xlsx"]
else:
    print(f"Error: {result.message}")
```

Usa `list_files_only` internamente, así que los subdirectorios no se mueven.

### Validación de tipos de archivo

`FileOrganizationService` acepta un validador personalizado:

```python
from sftp import ExtensionValidator

# Solo CSV y Excel
org = FileOrganizationService(client)

# Agregar más extensiones
org = FileOrganizationService(
    client,
    file_validator=ExtensionValidator({".csv", ".xlsx", ".json", ".parquet"}),
)

# Lógica completamente distinta
class MiValidador:
    def is_allowed(self, filename: str) -> bool:
        return filename.endswith(".csv") or "reporte" in filename

org = FileOrganizationService(client, file_validator=MiValidador())
```

## Inyección de dependencias (FastAPI)

```python
# dependencies.py
from config import get_settings
from sftp import SFTPCredentials, ParamikoSFTPClient, SFTPService, FileOrganizationService

def get_sftp_service() -> SFTPService:
    settings = get_settings()
    creds = SFTPCredentials(
        host=settings.sftp_host, port=settings.sftp_port,
        username=settings.sftp_username, password=settings.sftp_password,
    )
    return SFTPService(ParamikoSFTPClient(creds))

def get_organization_service() -> FileOrganizationService:
    settings = get_settings()
    creds = SFTPCredentials(...)
    return FileOrganizationService(ParamikoSFTPClient(creds))
```

```python
# routes/sftp.py
from fastapi import APIRouter, Depends
from dependencies import get_sftp_service
from sftp import SFTPService

router = APIRouter()

@router.get("/sftp/files")
def list_files(service: SFTPService = Depends(get_sftp_service)):
    result = service.list_files_only("/upload")
    if not result.success:
        return {"error": result.message}, 502
    return {"files": result.data}
```

## Mock para tests

```python
from unittest.mock import MagicMock
from sftp import SFTPService, FileOrganizationService, ExtensionValidator

# SFTPService
mock = MagicMock()
mock.list_files_only.return_value = ["a.csv", "b.xlsx"]
service = SFTPService(mock)
result = service.list_files_only("/x")
assert result.data == ["a.csv", "b.xlsx"]

# FileOrganizationService
mock = MagicMock()
mock.list_files_only.return_value = ["a.csv", "b.txt"]
org = FileOrganizationService(mock)
result = org.organize_files("/x")
assert result.data == ["a.csv"]  # .txt filtrado por default
```

## Tests

```bash
python -m pytest sftp/tests/ -v
```
