import dataclasses
from pathlib import Path

import pandas as pd

from readers.exceptions import FileAccessError, UnsupportedFileFormatError
from readers.factories.reader_factory import ReaderFactory
from readers.implementations.json_config_repository import JsonConfigRepository
from readers.services.detection_file_service import DetectionFileService
from readers.implementations.clean_df import clean_dataframe
from readers.models.csv_options import CsvOptions
from readers.models.process_result import ProcessResult


class FileProcessor:

    def __init__(self, config_path: Path):
        self._repository = JsonConfigRepository(config_path)
        self._service = DetectionFileService(self._repository)

    def process(
        self,
        file_path: Path,
        preview_options=None,
        preview_rows: int = 5,
        verbose: bool = False,
    ) -> ProcessResult:
        try:
            reader = ReaderFactory.create(file_path)

            if preview_options is None:
                preview_options = CsvOptions(nrows=preview_rows)

            if hasattr(reader, "get_sheets"):
                return self._process_sheets(reader, file_path, preview_options, preview_rows, verbose)

            return self._process_single(reader, file_path, preview_options, preview_rows, verbose)
        except (FileNotFoundError, FileAccessError):
            return ProcessResult(
                success=False,
                file_name=file_path.name,
                extension=file_path.suffix,
                error=f"No se encuentra o no se puede leer: {file_path.name}",
            )
        except UnsupportedFileFormatError as e:
            return ProcessResult(
                success=False,
                file_name=file_path.name,
                extension=file_path.suffix,
                error=str(e),
            )

    def _process_single(
        self,
        reader,
        file_path: Path,
        preview_options,
        preview_rows: int,
        verbose: bool = False,
    ) -> ProcessResult:
        preview_opts = self._preview_options(preview_options, preview_rows)
        preview_df = reader.read(file_path, preview_opts)
        result = self._service.detect(file_path, preview_df)

        if not result.success:
            if verbose:
                self._log_preview(file_path, preview_df, self._repository.get_all())
            return ProcessResult(
                success=False,
                file_name=file_path.name,
                file_size=result.file_size,
                extension=file_path.suffix,
                column_count=result.column_count,
                error=result.error,
            )

        return self._read_and_build(reader, file_path, preview_options, result)

    def _process_sheets(
        self,
        reader,
        file_path: Path,
        preview_options,
        preview_rows: int,
        verbose: bool = False,
    ) -> ProcessResult:
        configs = self._repository.get_all() if verbose else None

        for sheet_name in reader.get_sheets(file_path):
            sheet_opts = self._sheet_preview(preview_options, sheet_name, preview_rows)
            preview_df = reader.read(file_path, sheet_opts)
            result = self._service.detect(file_path, preview_df)

            if verbose:
                self._log_preview(file_path, preview_df, configs, sheet_name)

            if result.success:
                read_opts = self._build_read_options(preview_options, result)
                if hasattr(read_opts, "sheet_name"):
                    read_opts.sheet_name = sheet_name

                df = reader.read(file_path, read_opts)
                df = self._filter_required_columns(df, result)
                cleaned = clean_dataframe(df)

                return ProcessResult(
                    success=True,
                    file_name=file_path.name,
                    file_size=result.file_size,
                    extension=file_path.suffix,
                    sheet_name=sheet_name,
                    config_id=result.config_id,
                    data_start_row=result.data_start_row,
                    raw_row_count=len(df),
                    final_row_count=len(cleaned),
                    column_count=len(cleaned.columns),
                    df=cleaned,
                )

        return ProcessResult(
            success=False,
            file_name=file_path.name,
            extension=file_path.suffix,
            error="No matching sheet found",
        )

    def _read_and_build(
        self,
        reader,
        file_path: Path,
        preview_options,
        result,
    ) -> ProcessResult:
        read_options = self._build_read_options(preview_options, result)

        df = reader.read(file_path, read_options)
        df = self._filter_required_columns(df, result)
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
        kwargs["nrows"] = preview_rows if options.nrows is None else options.nrows
        return options.__class__(**kwargs)

    def _sheet_preview(self, options, sheet_name: str, preview_rows: int):
        kwargs = {f.name: getattr(options, f.name) for f in dataclasses.fields(options)}
        kwargs["header"] = None
        kwargs["nrows"] = preview_rows if options.nrows is None else options.nrows
        kwargs["sheet_name"] = sheet_name
        return options.__class__(**kwargs)

    @staticmethod
    def _normalize_column_name(name: str) -> str:
        return str(name).strip().upper().replace("\n", " ").replace(" ", "_")

    @staticmethod
    def _column_base_name(name: str) -> str:
        parts = name.rsplit(".", 1)
        return parts[0] if len(parts) == 2 and parts[1].isdigit() else name

    def _filter_required_columns(self, df: pd.DataFrame, result) -> pd.DataFrame:
        if not result.required_columns:
            return df
        norm_req = [self._normalize_column_name(c) for c in result.required_columns]
        selected = set()
        keep = []
        for req in norm_req:
            req_base = self._column_base_name(req)
            for idx, col in enumerate(df.columns):
                if idx in selected:
                    continue
                col_base = self._column_base_name(self._normalize_column_name(col))
                if col_base == req_base:
                    selected.add(idx)
                    keep.append(col)
                    break
        return df[keep] if keep else df

    def _log_preview(self, file_path, preview_df, configs, sheet_name=None):
        print(f"\n--- {file_path.name} {'[' + sheet_name + ']' if sheet_name else ''} ---")
        print(f"Preview ({len(preview_df)} rows, {len(preview_df.columns)} cols):")
        print(preview_df.to_string())
        print("\nValores por fila (normalizados):")
        for i in range(len(preview_df)):
            row = preview_df.iloc[i]
            values = [str(v).strip().upper() for v in row.tolist() if str(v).strip().upper() not in ("", "NAN", "NAN")]
            print(f"  Row {i}: {values}")
        if configs:
            print("\nConfig columns esperadas:")
            for config in configs:
                norm = [str(c).strip().upper() for c in config.columns]
                print(f"  [{config.id}]: {norm}")
        print()

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
