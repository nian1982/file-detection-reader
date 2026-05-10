import stat
from pathlib import Path

import paramiko

from sftp.models.credentials import SFTPCredentials
from sftp.exceptions.sftp_exceptions import (
    SFTPError,
    SFTPConnectionError,
    SFTPAuthenticationError,
    RemoteFileNotFoundError,
    RemoteDirectoryCreateError,
)


class ParamikoSFTPClient:

    def __init__(self, credentials: SFTPCredentials) -> None:
        self._credentials = credentials
        self._transport: paramiko.Transport | None = None
        self._client: paramiko.SFTPClient | None = None

    def connect(self) -> None:
        host = self._credentials.host
        port = self._credentials.port
        try:
            self._transport = paramiko.Transport((host, port))
            self._transport.connect(
                username=self._credentials.username,
                password=self._credentials.password,
            )
            self._client = paramiko.SFTPClient.from_transport(self._transport)
        except paramiko.AuthenticationException as e:
            raise SFTPAuthenticationError("Credenciales SFTP inválidas.") from e
        except paramiko.SSHException as e:
            raise SFTPConnectionError(
                f"No se pudo conectar a {host}:{port}. "
                "Verifica que el servidor SFTP esté disponible."
            ) from e
        except OSError as e:
            raise SFTPConnectionError(
                f"Error de red al conectar a {host}:{port}: {e.strerror}"
            ) from e
        except Exception as e:
            raise SFTPConnectionError(
                f"Error inesperado al conectar a {host}:{port}: {e}"
            ) from e

    def disconnect(self) -> None:
        if self._client:
            self._client.close()
        if self._transport:
            self._transport.close()

    def list_files(self, remote_path: str) -> list[str]:
        self._ensure_connected()
        return self._client.listdir(remote_path)

    def list_files_only(self, remote_path: str) -> list[str]:
        self._ensure_connected()
        items = self._client.listdir(remote_path)
        return [
            f
            for f in items
            if not stat.S_ISDIR(self._client.stat(f"{remote_path}/{f}").st_mode)
        ]

    def download_file(self, remote_path: str, local_path: Path | str) -> None:
        self._ensure_connected()
        local_path = Path(local_path)
        if local_path.is_dir():
            local_path = local_path / Path(remote_path).name
        try:
            self._client.get(remote_path, str(local_path))
        except FileNotFoundError as e:
            raise RemoteFileNotFoundError(
                f"No se encontró el archivo remoto: {remote_path}"
            ) from e
        except OSError as e:
            raise SFTPError(f"Error al descargar archivo: {e}") from e

    def upload_file(self, local_path: Path, remote_path: str) -> None:
        self._ensure_connected()
        full_remote = f"{remote_path.rstrip('/')}/{local_path.name}"
        try:
            self._client.put(str(local_path), full_remote)
        except OSError as e:
            raise SFTPError(f"Error al subir archivo: {e}") from e

    def delete_file(self, remote_path: str) -> None:
        self._ensure_connected()
        self._client.remove(remote_path)

    def move_file(self, source: str, target: str) -> None:
        self._ensure_connected()
        try:
            self._client.remove(target)
        except FileNotFoundError:
            pass
        self._client.rename(source, target)

    def directory_exists(self, remote_path: str) -> bool:
        self._ensure_connected()
        try:
            return stat.S_ISDIR(self._client.stat(remote_path).st_mode)
        except FileNotFoundError:
            return False

    def create_directory(self, remote_path: str) -> None:
        self._ensure_connected()
        try:
            self._client.mkdir(remote_path)
        except OSError as e:
            raise RemoteDirectoryCreateError(
                f"No se pudo crear el directorio {remote_path}: {e.strerror}"
            ) from e

    def _ensure_connected(self) -> None:
        if not self._client:
            raise SFTPConnectionError(
                "No hay conexión activa. Debes llamar a connect() antes de realizar operaciones."
            )
