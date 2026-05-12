from pydantic import BaseModel, ConfigDict


class ExportResponse(BaseModel):
    recipients: str
    data: str
    subject: str
    message_template: str
    variables: str

    model_config = ConfigDict(from_attributes=True)
