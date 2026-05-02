from dataclasses import dataclass
from typing import Any


@dataclass
class FileConfig:
    """Configuración de un tipo de archivo para detección."""
    id: str
    columns: list[str]
    description: str | None = None
    required_columns: list[str] | None = None
    optional_columns: list[str] | None = None
    sheets: list[str] | None = None
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FileConfig":
        return cls(
            id=data["id"],
            columns=data["columns"],
            description=data.get("description"),
            required_columns=data.get("required_columns"),
            optional_columns=data.get("optional_columns"),
            sheets=data.get("sheets")
        )
