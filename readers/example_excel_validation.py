"""
Ejemplo de validación de archivo Excel usando DetectionService.
Reutiliza la ruta del archivo Excel definida en example_usage.py.
"""
from pathlib import Path
from readers.implementations.csv_reader import CsvReader
from readers.implementations.excel_reader import ExcelReader
from readers.services.detection_service import DetectionService


def example_excel_detection():
    # Misma ruta del archivo Excel que en example_usage.py::main()
    excel_file = Path(
        '/home/nian/Documents/softron/proyectos/dataexpress/docs/varios/'
        '2025-04-04 Plantilla de Trabajo para Reconocimiento Ingresos (5) ULT.xlsx'
    )
    
    if not excel_file.exists():
        print(f"El archivo {excel_file} no existe")
        return
    
    # Configuración
    config_path = Path('/mnt/mydisc/desarrollo/python/apis/solid/api/readers/config/file_configs.json')
    readers = {
        "csv": CsvReader(),
        "excel": ExcelReader()
    }
    
    # Crear servicio de detección
    service = DetectionService(config_path, readers)
    
    # 1. Detectar automáticamente qué configuración coincide
    print("=== Detección automática (sin config_id) ===")
    result = service.detect(excel_file)
    _print_result(result)
    
    # 2. Detectar con un config_id específico (ej. EXCEL_CATALOGO)
    # print("\n=== Detección con config_id específico ===")
    # result = service.detect(excel_file, "EXCEL_CATALOGO")
    # _print_result(result)
    
    # 3. Listar hojas del archivo Excel
    print("\n=== Hojas del archivo Excel ===")
    excel_reader = readers["excel"]
    sheets = excel_reader.get_sheets(excel_file)
    print(f"Hojas disponibles: {sheets}")


def _print_result(result):
    """Imprime el resultado de detección de forma legible."""
    if result.success:
        print(f"✓ Éxito: {result.file_name}")
        print(f"  Config ID: {result.config_id}")
        print(f"  Hoja detectada: {result.sheet_name or 'N/A'}")
        print(f"  Columnas coincidentes: {result.columns_matched}")
        print(f"  Match: {len(result.columns_matched)}/{result.total_config_columns} ({result.match_percentage:.1f}%)")
        print(f"  Registros: {result.record_count}")
        print(f"  Fila inicio datos: {result.data_start_row}")
    else:
        print(f"✗ Fallo: {result.error or 'No hay coincidencia'}")


if __name__ == "__main__":
    example_excel_detection()
