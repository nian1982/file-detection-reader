from pathlib import Path

import pandas as pd

from readers.interfaces.config_repository import ConfigRepository
from readers.models.detection_result import DetectionResult
from readers.services.column_extractor import ColumnExtractor
from readers.services.column_comparator import ColumnComparator
from readers.services.detection_result_factory import DetectionResultFactory


class DetectionFileService:

    def __init__(
        self,
        repository: ConfigRepository,
        extractor: ColumnExtractor | None = None,
        comparator: ColumnComparator | None = None,
        result_factory: DetectionResultFactory | None = None,
    ):
        self._repository = repository
        self._extractor = extractor or ColumnExtractor()
        self._comparator = comparator or ColumnComparator()
        self._result_factory = result_factory or DetectionResultFactory()

    def detect(self, file_path: Path, df: pd.DataFrame) -> DetectionResult:
        configs = self._repository.get_all()

        for row_index, row in df.iterrows():
            detected_columns = self._extractor.extract(row)
            if not detected_columns:
                continue

            for config in configs:
                if self._comparator.compare(detected_columns, config):
                    row_idx = (
                        int(row_index)
                        if isinstance(row_index, int | float)
                        else 0
                    )
                    return self._result_factory.success(
                        file_path=file_path,
                        config=config,
                        row_index=row_idx,
                        detected_columns=detected_columns,
                    )

        return self._result_factory.not_found(file_path=file_path, df=df)
