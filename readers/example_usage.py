"""
Ejemplo de uso del módulo readers con detección de archivos.
"""
from pathlib import Path
from readers.implementations.csv_reader import CsvReader
from readers.implementations.excel_reader import ExcelReader
from readers.implementations.parquet_reader import ParquetReader
from readers.services.detection_service import DetectionService
from readers.models.detection_result import DetectionResult
import json


def main():

    file_path = Path('/home/nian/Documents/softron/proyectos/dataexpress/docs/varios/2025-04-04 Plantilla de Trabajo para Reconocimiento Ingresos (5) ULT.xlsx')

    config_path = Path('/mnt/mydisc/desarrollo/python/apis/solid/api/readers/config/file_configs.json')

    readers = {
        ".xlsx": ExcelReader(),
        ".csv": CsvReader()
    }

    service = DetectionService(config_path, readers) 

    result = service.detect_file_config(file_path)

    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    

    if result.success:
        df = service.load_full_data(result)

        print("\nDATA REAL:")
        print(df.head())   



if __name__ == "__main__":
    main()
