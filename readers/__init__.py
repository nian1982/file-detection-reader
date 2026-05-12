from pathlib import Path

from readers.example_usage import auto_process
from readers.models.process_result import ProcessResult
from readers.services.file_processor import FileProcessor


def process_file(
        file_path: str | Path,
        config_path: Path | None = None,
        preview_rows: int = 5,
        verbose: bool = False,
    ) -> ProcessResult:
    if config_path is None:
        config_path = Path(__file__).parent / "config" / "file_configs.json"
    processor = FileProcessor(config_path)
    return auto_process(
        Path(file_path), processor, preview_rows=preview_rows, verbose=verbose
    )
