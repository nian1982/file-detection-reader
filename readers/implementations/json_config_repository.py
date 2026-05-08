import json
from pathlib import Path
from readers.interfaces.config_repository import ConfigRepository
from readers.models.file_config import FileConfig

class JsonConfigRepository(ConfigRepository):

    def __init__(self, file_path: Path):
        self._file_path = file_path

    def get_all(self) -> list[FileConfig]:

        with open(self._file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return [
            FileConfig.from_dict(config)
            for config in data["configs"]
            if config.get("active", True)
        ]

    def get_by_id(self, config_id: str) -> FileConfig | None:
        configs = self.get_all()

        for config in configs:
            if config.id == config_id and config.active:
                return config

        return None