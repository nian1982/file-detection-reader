from typing import Any
import json
from dataclasses import is_dataclass, asdict


def _object_to_dict(data: Any) -> Any:
    if hasattr(data, "to_dict"):
        return data.to_dict()
    if isinstance(data, dict):
        return data
    if is_dataclass(data):
        return asdict(data)
    if hasattr(data, "__dict__"):
        return vars(data)
    return {"value": str(data)}


def print_json_format(data: Any = None) -> None:

    if data is None:
        print('{"error": "No se encontraron datos para procesar"}')
        return

    data = _object_to_dict(data)

    try:
        result = json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
            default=str,
        )
        print(f"\n{result}\n")
    except TypeError as e:
        print(f'{{"error": "Error serializando JSON: {e}"}}')