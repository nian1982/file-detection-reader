from typing import Protocol, Any, runtime_checkable
from pathlib import Path
from readers.interfaces.file_reader import FileReader




@runtime_checkable
class SheetableReader(FileReader, Protocol):
    """Interfaz para lectores que soportan hojas múltiples."""

    def get_sheets(self, file_path: Path) -> list[str]: ...