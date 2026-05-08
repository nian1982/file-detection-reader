import dataclasses
from pathlib import Path

import pandas as pd

from readers.factories.reader_factory import ReaderFactory
from readers.implementations.json_config_repository import JsonConfigRepository
from readers.services.detection_file_service import DetectionFileService
from readers.services.detection_result_factory import DetectionResultFactory
from readers.implementations.clean_df import clean_dataframe
from readers.models.csv_options import CsvOptions
from readers.models.process_result import ProcessResult


class FileProcessor:

    def __init__(self, config_path: Path):
        self._repository = JsonConfigRepository(config_path)
        self._service = DetectionFileService(self._repository)
        self._result_factory = DetectionResultFactory()

    def process(
            self,
            file_path: Path,
            preview_options=None,
            preview_rows: int = 5,
        ) -> ProcessResult:
        reader = ReaderFactory.create(file_path)

        if preview_options is None:
            preview_options = CsvOptions(nrows=preview_rows)

        preview_opts = self._preview_options(preview_options, preview_rows)
        preview_df = reader.read(file_path, preview_opts)
        result = self._service.detect(file_path, preview_df)

        if not result.success:
            return ProcessResult(
                success=False,
                file_name=file_path.name,
                file_size=result.file_size,
                extension=file_path.suffix,
                column_count=result.column_count,
                error=result.error,
            )

        return self._read_and_build(reader, file_path, preview_options, result)

    def _read_and_build(
            self,
            reader,
            file_path: Path,
            preview_options,
            result,
        ) -> ProcessResult:
        read_options = self._build_read_options(preview_options, result)

        df = reader.read(file_path, read_options)
        cleaned = clean_dataframe(df)

        return ProcessResult(
            success=True,
            file_name=file_path.name,
            file_size=result.file_size,
            extension=file_path.suffix,
            config_id=result.config_id,
            data_start_row=result.data_start_row,
            raw_row_count=len(df),
            final_row_count=len(cleaned),
            column_count=len(cleaned.columns),
            df=cleaned,
        )

    def _preview_options(self, options, preview_rows: int):
        kwargs = {f.name: getattr(options, f.name) for f in dataclasses.fields(options)}
        kwargs["header"] = None
        kwargs["nrows"] = preview_rows
        return options.__class__(**kwargs)

    def _build_read_options(self, preview_options, result):
        field_names = [f.name for f in dataclasses.fields(preview_options)]
        read_kwargs = {
            name: getattr(preview_options, name)
            for name in field_names
            if name not in ("header", "nrows")
        }
        read_kwargs["header"] = result.data_start_row
        read_kwargs["nrows"] = None

        if hasattr(preview_options, "usecols") and result.required_columns:
            read_kwargs["usecols"] = result.required_columns

        return preview_options.__class__(**read_kwargs)
