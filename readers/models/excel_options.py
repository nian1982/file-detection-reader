from dataclasses import dataclass
from pathlib import Path


@dataclass
class ExcelOptions:
    sheet_name: str | None = None
    skiprows: int | None = None  
    nrows: int | None = None
    header: int | None = 0    