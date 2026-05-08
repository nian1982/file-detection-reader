from pathlib import Path

import pandas as pd

from readers.models.detection_result import DetectionResult
from readers.models.file_config import FileConfig


class DetectionResultFactory:

    def success(
        self,
        file_path: Path,
        config: FileConfig,
        row_index: int,
        detected_columns: list[str],
        record_count: int | None = None,
    ) -> DetectionResult:
        return DetectionResult(
            success=True,
            file_path=file_path,
            config_id=config.id,
            required_columns=config.required_columns,
            match_percentage=100.0,
            total_config_columns=len(config.columns),
            file_name=file_path.name,
            file_size=file_path.stat().st_size,
            extension=file_path.suffix,
            data_start_row=row_index,
            record_count=record_count,
            column_count=len(detected_columns),
        )

    def not_found(self, file_path: Path, df: pd.DataFrame) -> DetectionResult:
        return DetectionResult(
            success=False,
            file_path=file_path,
            file_name=file_path.name,
            file_size=file_path.stat().st_size,
            extension=file_path.suffix,
            column_count=len(df.columns),
            error="No matching configuration found",
        )
