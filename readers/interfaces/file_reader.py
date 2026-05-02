from typing import Protocol, Any
from pathlib import Path


class FileReader(Protocol):
    """Interfaz base para lectores de archivos estructurados."""
    
    def read(self, file_path: Path, options: Any = None) -> Any:
        """Lee un archivo y retorna un DataFrame."""
        ...
    
    def get_columns(self, file_path: Path, options: Any = None) -> list[str]:
        """Obtiene las columnas del archivo."""
        ...
    
    def get_metadata(self, file_path: Path, options: Any = None) -> dict[str, Any]:
        """Obtiene metadatos del archivo."""
        ...
