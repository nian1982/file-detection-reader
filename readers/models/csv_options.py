from dataclasses import dataclass
from pathlib import Path


@dataclass
class CsvOptions:
    sep: str = ","
    encoding: str = "utf-8"
    skiprows: int = 0
    nrows: int = 5