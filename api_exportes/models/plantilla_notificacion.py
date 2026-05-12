from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PlantillaNotificacion:
    recipients: str
    data: str
    subject: str
    message_template: str
    variables: str
