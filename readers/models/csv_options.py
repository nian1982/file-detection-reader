from dataclasses import dataclass, field
from typing import List

@dataclass(slots=True)
class CsvOptions:
    sep: str = "|"
    encoding: str = "latin1"
    skiprows: int = 0
    nrows: int | None = None
    header: int | None = None
    usecols: list[str] = field(
        default_factory=list
    )