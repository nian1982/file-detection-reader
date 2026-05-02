from pathlib import Path
from typing import Any
from readers.interfaces import SheetableReader
import pandas as pd
from readers.models.excel_options import ExcelOptions


class ExcelReader(SheetableReader):
    """Lector de archivos Excel."""
    
    def read(self, file_path: Path, options: ExcelOptions | None = None):
        options = options or ExcelOptions()

        sheet = options.sheet_name if options.sheet_name is not None else 0

        df = pd.read_excel(
            file_path,
            sheet_name=sheet,
            skiprows=options.skiprows,
            nrows=options.nrows,
            header=options.header
        )        
        return df

    def get_columns(self, file_path: Path, options: ExcelOptions | None = None) -> list[str]:
        options = options or ExcelOptions()

        df = pd.read_excel(
            file_path,
            sheet_name=options.sheet_name if options.sheet_name is not None else 0,
            nrows=0
        )
        return list(df.columns)

    def get_sheets(self, file_path: Path) -> list[str]:
        return pd.ExcelFile(file_path).sheet_names

    def get_metadata(self, file_path: Path, options: ExcelOptions | None = None) -> dict[str, Any]:
        options = options or ExcelOptions()

        metadata = {
            "file_type": "excel",
            "size": file_path.stat().st_size,
            "sheets": self.get_sheets(file_path),
        }

        if options.sheet_name:
            df = pd.read_excel(file_path, sheet_name=options.sheet_name)
            metadata["columns"] = list(df.columns)
            metadata["row_count"] = len(df)

        return metadata
