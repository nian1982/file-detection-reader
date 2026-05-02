import csv
from pathlib import Path
from typing import Any
from readers.interfaces.file_reader import FileReader


class CsvReader(FileReader):
    """Lector de archivos CSV."""
    
    def __init__(self, delimiter: str = ",", encoding: str = "utf-8"):
        self.delimiter = delimiter
        self.encoding = encoding
    
    def read(self, file_path: Path, **kwargs) -> Any:
        import pandas as pd
        lines = kwargs.get('lines')
        df = pd.read_csv(file_path, delimiter=self.delimiter, 
                        encoding=self.encoding, nrows=lines)
        df.columns = df.columns.str.strip()
        return df
    
    def get_columns(self, file_path: Path, **kwargs) -> list[str]:
        with open(file_path, "r", encoding=self.encoding) as f:
            reader = csv.reader(f, delimiter=self.delimiter)
            
            for row in reader:
                if row and any(cell.strip() for cell in row):
                    return [col.strip() for col in row]
            
            return []
    
    def get_metadata(self, file_path: Path, **kwargs) -> dict[str, Any]:
        return {
            "file_type": "csv",
            "size": file_path.stat().st_size,
            "delimiter": self.delimiter,
            "encoding": self.encoding,
        }
