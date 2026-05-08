from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd


@dataclass
class ProcessResult:
    success: bool
    file_name: str | None = None
    file_size: int | None = None
    extension: str | None = None
    sheet_name: str | None = None
    config_id: str | None = None
    data_start_row: int | None = None
    raw_row_count: int | None = None
    final_row_count: int | None = None
    column_count: int | None = None
    error: str | None = None
    df: pd.DataFrame | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "file_name": self.file_name,
            "file_size": self.file_size,
            "extension": self.extension,
            "sheet_name": self.sheet_name,
            "config_id": self.config_id,
            "data_start_row": self.data_start_row,
            "raw_row_count": self.raw_row_count,
            "final_row_count": self.final_row_count,
            "column_count": self.column_count,
            "error": self.error,
        }
