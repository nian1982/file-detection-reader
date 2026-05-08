from pathlib import Path
from utils.files import print_json_format
from readers.models.csv_options import CsvOptions
from readers.implementations.clean_df import clean_dataframe
from readers.factories.reader_factory import ReaderFactory
from readers.implementations.json_config_repository import JsonConfigRepository
from readers.services.detection_file_service import DetectionFileService
from readers.implementations.excel_reader import ExcelReader

def main():

    # catalogo = Path('/home/nian/Documents/softron/proyectos/reconociemiento/logistica/datasets/20260422/SR2104000_CATALOGO_PARTICULARADMIN_SIGLA_20260422160608.csv') # sep = ;
    # vigencias = Path('/home/nian/Documents/softron/proyectos/reconociemiento/logistica/datasets/20260422/SR2104000_VIGENCIA_CONTRATOADMIN_SIGLA_20260422163137.csv') # sep = |

    # file_path = catalogo

    # options = CsvOptions(sep=';', encoding='latin1', nrows=5)
    # reader = ReaderFactory.create(file_path)
    # df = reader.read(file_path, options)

    # repository = JsonConfigRepository(
    #     Path("/mnt/mydisc/desarrollo/python/apis/solid/api/readers/config/file_configs.json")
    # )

    # service = DetectionFileService(repository)

    # result = service.detect(file_path=file_path, df=df)

    # print_json_format(result)

    # read_options = CsvOptions(
    #     sep=";",
    #     encoding="latin1",
    #     header=result.data_start_row,
    #     usecols=result.required_columns
    # )

    # if not result.success:
    #     print(f"No se encontró configuración activa para {file_path.name}")
    #     print(f"Error: {result.error}")
    #     return

    # df = reader.read(file_path, read_options)

    # df = clean_dataframe(df)
    # print(df.head())


    test = Path('/home/nian/Downloads/tarifas_cliente_MEDELLIN_GLOBAL_20241205.xlsx')
    reader = ExcelReader()
    sheets = reader.get_sheets(test)

    print(sheets)



if __name__ == "__main__":
    main()
