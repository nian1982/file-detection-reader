from typing import Protocol


class TemplateLoader(Protocol):

    def load(self, template_name: str) -> str: ...
