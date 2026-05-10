import json
from pathlib import Path

from notifications.models.recipient_list import RecipientList


class JsonRecipientRepository:

    def __init__(self, file_path: Path):
        self._file_path = file_path
        self._lists: dict[str, list[str]] = {}
        self._load()

    def _load(self) -> None:
        if not self._file_path.exists():
            self._lists = {}
            return
        raw = json.loads(self._file_path.read_text(encoding="utf-8"))
        self._lists = {
            entry["id"]: entry["recipients"]
            for entry in raw.get("lists", [])
        }

    def get(self, key: str) -> list[str]:
        recipients = self._lists.get(key)
        if not recipients:
            raise KeyError(f"Recipient list '{key}' not found")
        return recipients

    def get_all_keys(self) -> list[str]:
        return list(self._lists.keys())
