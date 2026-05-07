from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class FileConfig:

    id: str
    columns: list[str]
    description: str | None = None
    active: bool = True
    required_columns: list[str] = field(default_factory=list)
    optional_columns: list[str] = field(default_factory=list)
    sheets: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any] ) -> "FileConfig":

        return cls(
            id=data["id"],
            columns=data["columns"],
            description=data.get("description"),
            required_columns=data.get("required_columns",[]),
            optional_columns=data.get("optional_columns",[]),
            sheets=data.get("sheets",[])
        )