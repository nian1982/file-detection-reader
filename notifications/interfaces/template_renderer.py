from typing import Protocol


class TemplateRenderer(Protocol):

    def render(self, template: str, placeholders: dict[str, str]) -> str: ...
