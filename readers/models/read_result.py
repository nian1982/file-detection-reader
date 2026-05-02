from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ReadResult:
    """Resultado de la lectura de un archivo."""
    success: bool
    data: list[dict[str, Any]]
    columns: list[str]
    file_path: Path
    sheet_name: str | None = None
    metadata: dict[str, Any] | None = None
    error: str | None = None
