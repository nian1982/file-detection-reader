from typing import Protocol


class FileTypeValidator(Protocol):
    def is_allowed(self, filename: str) -> bool: ...
