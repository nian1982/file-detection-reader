from typing import Protocol


class RecipientRepository(Protocol):

    def get(self, key: str) -> list[str]: ...

    def get_all_keys(self) -> list[str]: ...
