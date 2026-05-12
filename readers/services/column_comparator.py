from readers.models.file_config import FileConfig


class ColumnComparator:

    def normalize(self, columns: list[str]) -> list[str]:
        return [str(c).strip().upper().replace("\n", " ") for c in columns]

    def compare(self, detected: list[str], config: FileConfig) -> bool:
        detected_normalized = set(self.normalize(detected))
        config_normalized = set(self.normalize(config.columns))
        return config_normalized.issubset(detected_normalized)

    def match_count(self, detected: list[str], config: FileConfig) -> int:
        detected_normalized = self.normalize(detected)
        config_normalized = self.normalize(config.columns)
        return sum(1 for c in detected_normalized if c in config_normalized)
