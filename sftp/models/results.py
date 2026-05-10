from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class OperationResult:
    success: bool
    message: str
    data: Any = None
