from typing import Protocol


class DatabaseConnection(Protocol):
    def execute(self, query: str, params: dict | tuple | None = None) -> list[dict]: ...
