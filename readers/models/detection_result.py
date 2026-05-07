from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class DetectionResult:
    """Resultado de la detección de un archivo."""
    success: bool
    file_path: Path
    config_id: str | None = None
    required_columns: list[str] = field(default_factory=list)
    match_percentage: float = 0.0
    total_config_columns: int = 0
    
    # Metadata básica
    file_name: str | None = None
    file_size: int | None = None
    extension: str | None = None
    
    # Info de datos
    sheet_name: str | None = None
    data_start_row: int | None = None
    record_count: int | None = None
    column_count: int | None = None
    
    error: str | None = None
    
    def to_dict(self) -> dict[str, Any]:
        """Convierte a diccionario para fácil uso."""
        return {
            "success": self.success,
            "file_path": str(self.file_path),
            "file_name": self.file_name or self.file_path.name,
            "config_id": self.config_id,
            "required_columns": self.required_columns,
            "match_percentage": self.match_percentage,
            "total_config_columns": self.total_config_columns,
            "file_size": self.file_size,
            "extension": self.extension,
            "sheet_name": self.sheet_name,
            "data_start_row": self.data_start_row,
            "record_count": self.record_count,
            "column_count": self.column_count,
            "error": self.error
        }
