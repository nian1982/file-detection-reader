from pathlib import Path

from readers.models.csv_options import CsvOptions
from readers.models.excel_options import ExcelOptions
from readers.models.process_result import ProcessResult
from readers.services.file_processor import FileProcessor


CONFIG_PATH = Path(
    "/mnt/mydisc/desarrollo/python/apis/solid/api/readers/config/file_configs.json"
)


def auto_process(
            file_path: Path,
            processor: FileProcessor,
            preview_rows: int = 5,
            verbose: bool = False,
        ) -> ProcessResult:
    ext = file_path.suffix.lower()
    if ext == ".csv":
        options = CsvOptions(nrows=preview_rows, sep=";", encoding="latin1")
    elif ext in (".xlsx", ".xls"):
        options = ExcelOptions(nrows=preview_rows)
    else:
        return ProcessResult(
            success=False,
            file_name=file_path.name,
            extension=ext,
            error=f"Formato no soportado: '{ext}'. Permitidos: .csv, .xlsx, .xls",
        )

    return processor.process(file_path, options, preview_rows=preview_rows, verbose=verbose)


def main():
    processor = FileProcessor(CONFIG_PATH)

    xls_path = Path(
        "/home/nian/Documents/desarrollo/softron/proyectos/dataexpress/"
        "docs/varios/2025-04-04 Plantilla de Trabajo para Reconocimiento Ingresos (5) ULT.xlsx"
    )

    csv_path = Path(
        "/home/nian/Downloads/SR2104000_VIGENCIA_CONTRATOADMIN_SIGLA_20260422163137.csv"
    )

    filepath = csv_path

    result = auto_process(filepath, processor, preview_rows=15, verbose=False)

    if result.success and result.df is not None:
        print(f"Archivo procesado: {result.file_name}")
        print(f"hoja: {result.sheet_name or 'N/A'}")
        print(f"df:\n {result.df}")
        print(f"COLUMNAS:\n {result.df.columns}")
    else:
        print(f"Error: {result.error}")

    # archivos = [
    #     Path("datos.csv"),
    #     Path("reporte.xlsx"),
    #     Path("desconocido.xyz"),
    #     Path("archivo.xlsxs"),
    # ]

    # for ruta in archivos:
    #     result = auto_process(ruta, processor)
    #     estado = "OK" if result.success else "ERROR"
    #     print(f"[{estado}] {result.file_name}: {result.error or 'Procesado correctamente'}")


if __name__ == "__main__":
    main()
