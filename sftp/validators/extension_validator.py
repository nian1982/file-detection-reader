from pathlib import Path


DATA_EXTENSIONS = {".csv", ".xlsx", ".xls"}


class ExtensionValidator:

    def __init__(self, extensions: set[str]) -> None:
        if not extensions:
            raise ValueError("Debe proporcionar al menos una extensión")
        self._extensions = {e.lower().lstrip(".") for e in extensions}

    def is_allowed(self, filename: str) -> bool:
        ext = Path(filename).suffix.lstrip(".").lower()
        return ext in self._extensions
