from typing import Protocol
from readers.models.file_config import FileConfig


class ConfigRepository(Protocol):

    def get_all(self) -> list[FileConfig]: ...

    def get_by_id(self, config_id: str) -> FileConfig | None: ...