from pathlib import Path

class ReaderFactory:

    @staticmethod
    def get_reader(file_path: Path) -> FileReader:
        suffix = file_path.suffix.lower()

        if suffix in [".xlsx", ".xls"]:
            return ExcelReader()
        elif suffix == ".csv":
            return CsvReader()
        else:
            raise ValueError(f"Tipo de archivo no soportado: {suffix}")