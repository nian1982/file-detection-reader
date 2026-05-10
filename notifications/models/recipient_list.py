from dataclasses import dataclass, field


@dataclass
class RecipientList:
    id: str
    recipients: list[str]
    description: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "RecipientList":
        return cls(
            id=data["id"],
            recipients=data["recipients"],
            description=data.get("description", ""),
        )
