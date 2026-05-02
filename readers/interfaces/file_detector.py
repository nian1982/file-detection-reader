from typing import Protocol
from pathlib import Path
from readers.models.detection_result import DetectionResult


class FileDetector(Protocol):
    """Interfaz para detectores de archivos."""
    
    def detect(self, file_path: Path, config_id: str, 
               lines_to_check: int = 5) -> DetectionResult:
        """Detecta si un archivo coincide con una configuración."""
        ...
    
    def detect_in_directory(self, directory: Path, config_id: str,
                           lines_to_check: int = 5) -> list[DetectionResult]:
        """Detecta archivos en un directorio que coincidan con la configuración."""
        ...
