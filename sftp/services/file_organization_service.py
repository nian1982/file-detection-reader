from datetime import datetime

from sftp.interfaces.client import SFTPClientProtocol
from sftp.models.results import OperationResult
from sftp.exceptions.sftp_exceptions import SFTPError
from sftp.interfaces.validator import FileTypeValidator
from sftp.validators.extension_validator import ExtensionValidator, DATA_EXTENSIONS


class FileOrganizationService:

    def __init__(self, client: SFTPClientProtocol, file_validator: FileTypeValidator | None = None, ) -> None:
        self._client = client
        self._validator = file_validator or ExtensionValidator(DATA_EXTENSIONS)
        

    def organize_files(self, source_dir: str) -> OperationResult:
        try:
            self._client.connect()

            now = datetime.now()
            date_dir = f"system_{now.strftime('%Y%m%d')}"
            hour_dir = now.strftime("%H")
            date_path = f"{source_dir}/{date_dir}"
            hour_path = f"{date_path}/{hour_dir}"

            for path in (date_path, hour_path):
                if not self._client.directory_exists(path):
                    self._client.create_directory(path)

            files = [
                f
                for f in self._client.list_files_only(source_dir)
                if self._validator.is_allowed(f)
            ]

            moved = []
            for file in files:
                full_dest = f"{hour_path}/{file}"
                self._client.move_file(f"{source_dir}/{file}", full_dest)
                moved.append(full_dest)

            return OperationResult(
                success=True,
                message=f"{len(moved)} archivos movido a {date_dir}/{hour_dir}",
                data=moved,
            )
        except SFTPError as e:
            return OperationResult(success=False, message=str(e))
        finally:
            self._client.disconnect()
