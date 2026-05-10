from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SFTPCredentials:
    host: str
    port: int
    username: str
    password: str
