from pathlib import Path

from readers.implementations.csv_reader import CsvReader
from readers.implementations.excel_reader import ExcelReader
from readers.exceptions import UnsupportedFileFormatError


class ReaderFactory:

    READERS = {
        ".csv": CsvReader,
        ".xlsx": ExcelReader,
        ".xls": ExcelReader,
    }

    @classmethod
    def create(cls, file_path: Path):
        suffix = file_path.suffix.lower()

        reader_class = cls.READERS.get(suffix)

        if not reader_class:
            raise UnsupportedFileFormatError(suffix)

        return reader_class()
