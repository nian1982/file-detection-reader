from pathlib import Path
from typing import Any
from readers.interfaces.file_reader import FileReader


class ParquetReader(FileReader):
    """Lector de archivos Parquet."""
    
    def read(self, file_path: Path, lines: int | None = None) -> Any:
        import pandas as pd
        
        df = pd.read_parquet(file_path)
        if lines:
            df = df.head(lines)
        return df
    
    def get_columns(self, file_path: Path) -> list[str]:
        import pandas as pd
        
        df = pd.read_parquet(file_path, filters=[])
        return list(df.columns)
    
    def get_metadata(self, file_path: Path) -> dict[str, Any]:
        import pandas as pd
        
        metadata = {
            "file_type": "parquet",
            "size": file_path.stat().st_size,
        }
        
        df = pd.read_parquet(file_path, filters=[])
        metadata["columns"] = list(df.columns)
        metadata["row_count"] = len(df)
        
        return metadata
