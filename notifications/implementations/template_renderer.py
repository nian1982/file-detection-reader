from notifications.interfaces.template_renderer import TemplateRenderer


class SimpleTemplateRenderer:

    def render(self, template: str, placeholders: dict[str, str]) -> str:
        result = template
        for key, value in placeholders.items():
            result = result.replace("{{" + key + "}}", value)
        return result
