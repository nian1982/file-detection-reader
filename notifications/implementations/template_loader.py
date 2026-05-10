from pathlib import Path

from notifications.interfaces.template_loader import TemplateLoader


class FileTemplateLoader:

    def __init__(self, templates_dir: Path):
        self._templates_dir = templates_dir

    def load(self, template_name: str) -> str:
        path = self._templates_dir / template_name
        return path.read_text(encoding="utf-8")
