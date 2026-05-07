from typing import Protocol, Any
from pathlib import Path


class FileReader(Protocol):
    
    def read(self, file_path: Path, options: Any | None = None) -> Any: ...
    
  
