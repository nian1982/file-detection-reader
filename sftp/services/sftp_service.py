from pathlib import Path

from sftp.interfaces.client import SFTPClientProtocol
from sftp.models.results import OperationResult
from sftp.exceptions.sftp_exceptions import SFTPError


class SFTPService:

    def __init__(self, client: SFTPClientProtocol) -> None:
        self._client = client

    def test_connection(self) -> OperationResult:
        try:
            self._client.connect()
            return OperationResult(success=True, message="Conexión SFTP exitosa")
        except SFTPError as e:
            return OperationResult(success=False, message=str(e))
        finally:
            self._client.disconnect()

    def list_files(self, remote_path: str) -> OperationResult:
        try:
            self._client.connect()
            files = self._client.list_files(remote_path)
            return OperationResult(
                success=True,
                message=f"Archivos encontrados: {len(files)}",
                data=files,
            )
        except SFTPError as e:
            return OperationResult(success=False, message=str(e))
        finally:
            self._client.disconnect()

    def list_files_only(self, remote_path: str) -> OperationResult:
        try:
            self._client.connect()
            files = self._client.list_files_only(remote_path)
            return OperationResult(
                success=True,
                message=f"Archivos encontrados: {len(files)}",
                data=files,
            )
        except SFTPError as e:
            return OperationResult(success=False, message=str(e))
        finally:
            self._client.disconnect()

    def download_file(self, remote_path: str, local_path: Path | str) -> OperationResult:
        try:
            local_path = Path(local_path)
            self._client.connect()
            self._client.download_file(remote_path, local_path)
            full_local = str(local_path / Path(remote_path).name) if local_path.is_dir() else str(local_path)
            return OperationResult(
                success=True,
                message="Archivo descargado correctamente",
                data=full_local,
            )
        except (SFTPError, OSError) as e:
            return OperationResult(success=False, message=str(e))
        finally:
            self._client.disconnect()

    def upload_file(self, local_path: Path, remote_path: str) -> OperationResult:
        try:
            self._client.connect()
            self._client.upload_file(local_path, remote_path)
            full_remote = f"{remote_path.rstrip('/')}/{local_path.name}"
            return OperationResult(
                success=True,
                message="Archivo cargado correctamente",
                data=full_remote,
            )
        except (SFTPError, OSError) as e:
            return OperationResult(success=False, message=str(e))
        finally:
            self._client.disconnect()

    def delete_file(self, remote_path: str) -> OperationResult:
        try:
            self._client.connect()
            self._client.delete_file(remote_path)
            return OperationResult(success=True, message="Archivo eliminado correctamente")
        except SFTPError as e:
            return OperationResult(success=False, message=str(e))
        finally:
            self._client.disconnect()

    def move_file(self, source: str, target: str) -> OperationResult:
        try:
            self._client.connect()
            self._client.move_file(source, target)
            return OperationResult(success=True, message="Archivo movido correctamente")
        except SFTPError as e:
            return OperationResult(success=False, message=str(e))
        finally:
            self._client.disconnect()
