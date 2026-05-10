from datetime import datetime
import sys
from pathlib import Path
from utils.files import print_json_format

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import get_settings
from sftp import (
    SFTPCredentials,
    ParamikoSFTPClient,
    SFTPService,
    FileOrganizationService,
)

from shared.config.settings import settings

creds = SFTPCredentials(
    host=settings.SFTP_HOST,
    port=settings.SFTP_PORT,
    username=settings.SFTP_USER,
    password=settings.SFTP_PASS    
)

client = ParamikoSFTPClient(creds)

sep = f"\n{'=' * 120}\n"

# Cargar archivos
service = SFTPService(client)
local = r'/home/nian/Documents/softron/proyectos/reconociemiento/logistica/datasets/20260422/SR2104000_VIGENCIA_CONTRATOADMIN_SIGLA_20260422163137.csv'
remote_dir = settings.SFTP_UPLOAD_DIR
result = service.upload_file(Path(local), remote_dir)
if result.success:
    print(f"Load response:")
    print_json_format(result)

print(sep)
# listar solo archivos (sin directorios)
service = SFTPService(client)
result = service.list_files_only("/upload")
if result.success:
    print(f"Files found:")
    print_json_format(result)
else:
    print(f"Error al listar: {result.message}")

print(sep)
# organizar archivos en estructura YYYYMMDD/HH
org_service = FileOrganizationService(client)
result = org_service.organize_files("/upload")
if result.success:
    print(f"Organized files:")
    print_json_format(result)
else:
    print(f"Error al organizar: {result.message}")

print(sep)
# descargar archivos
download_dir = r'/home/nian/Downloads/'
if result.data:
    remote_file = result.data[0]
    result = service.download_file(remote_file, download_dir)
    if result.success:
        print(f"Download file:\n")
        print_json_format(result)
