from pathlib import Path

from readers.models.csv_options import CsvOptions
from readers.services.file_processor import FileProcessor
from utils.files import print_json_format

CONFIG_PATH = Path(__file__).parent / "config" / "file_configs.json"


def main():
    processor = FileProcessor(CONFIG_PATH)

    csv_path = Path(
        "/home/nian/Documents/softron/proyectos/reconociemiento/logistica/datasets/20260422/SR2104000_CATALOGO_PARTICULARADMIN_SIGLA_20260422160608.csv"
    )
    csv_opts = CsvOptions(sep=";", encoding="latin1")

    result = processor.process(csv_path, csv_opts, preview_rows=5)
    if result.success and result.df is not None:
        print("CSV procesado:")
        print_json_format(result)
        print(result.df)
    else:
        print(f"CSV: {result.error}")


if __name__ == "__main__":
    main()
