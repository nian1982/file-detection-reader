import json
from pathlib import Path
from typing import Any, Mapping
from readers.interfaces.file_detector import FileDetector
from readers.interfaces.file_reader import FileReader
from readers.interfaces.sheetable_reader import SheetableReader
from readers.implementations.csv_reader import CsvReader
from readers.models.detection_result import DetectionResult
from readers.models.file_config import FileConfig
from readers.implementations.clean_df import clean_dataframe



class DetectionService(FileDetector):
    """Servicio para detectar archivos basado en configuración."""
    
    def __init__(self, config_path: Path, readers: Mapping[str, FileReader]):
        self.config_path = config_path
        self.readers = readers
        self._configs: dict[str, FileConfig] = {}
        self._load_configs()
    
    def _load_configs(self) -> None:
        with open(self.config_path, "r") as f:
            configs_data = json.load(f)
        
        for config_data in configs_data.get("configs", []):
            config = FileConfig.from_dict(config_data)
            self._configs[config.id] = config


    def _resolve_reader(self, file_path: Path) -> FileReader:
        suffix = file_path.suffix.lower()
        print(suffix)
        try:
            return self.readers[suffix]
        except KeyError:
            raise ValueError(f"No hay reader para: {suffix}")


    def detect_file_config(self, file_path: Path, match_threshold: float = 100.0):

        reader = self._resolve_reader(file_path)

        try:
            for sheet, df in self._iterate_sources(reader, file_path):

                result = self._detect_in_dataframe(
                    df=df,
                    file_path=file_path,
                    sheet=sheet,
                    match_threshold=match_threshold
                )

                if result.success:
                    return result

            return DetectionResult(
                success=False,
                file_path=file_path,
                error="No se encontró coincidencia"
            )

        except Exception as e:
            return DetectionResult(
                success=False,
                file_path=file_path,
                error=str(e)
            )


    def _iterate_sources(self, reader, file_path: Path):
        from readers.models.excel_options import ExcelOptions

        if isinstance(reader, SheetableReader):
            sheets = reader.get_sheets(file_path)

            for sheet in sheets:
                df = reader.read(
                    file_path,
                    ExcelOptions(sheet_name=sheet, nrows=10)
                )
                yield sheet, df
        else:
            df = reader.read(file_path) 
            yield None, df


    def _detect_in_dataframe(
            self,
            df,
            file_path: Path,
            sheet: str | None,
            match_threshold: float
        ) -> DetectionResult:

        # preprocesar configs UNA sola vez
        configs_prepared = [
            (
                config,
                set(col.strip().upper() for col in config.columns)
            )
            for config in self._configs.values()
        ]

        # convertir df a lista (MUCHO más rápido que iterrows)
        rows = df.values.tolist()

        for idx, row in enumerate(rows):

            # limpiar fila una sola vez
            row_set = {
                str(v).strip().upper()
                for v in row
                if v is not None and str(v).strip() != ""
            }

            if not row_set:
                continue

            for config, expected_set in configs_prepared:

                matches = row_set & expected_set  # intersección rápida

                if not matches:
                    continue

                percentage = (len(matches) / len(expected_set)) * 100

                if percentage >= match_threshold:

                    # SOLO aquí lees metadata pesada
                    file_stat = file_path.stat()

                    return DetectionResult(
                        success=True,
                        file_path=file_path,
                        config_id=config.id,
                        columns_matched=list(matches),
                        match_percentage=percentage,
                        total_config_columns=len(expected_set),

                        file_name=file_path.name,
                        file_size=file_stat.st_size,
                        extension=file_path.suffix,

                        sheet_name=sheet,
                        data_start_row=idx + 1,
                        record_count=None,  # evitar lectura completa
                        column_count=len(df.columns),

                    )

        return DetectionResult(success=False, file_path=file_path)
   
    
    def load_full_data(self, result: DetectionResult):
        reader = self._resolve_reader(result.file_path)

        if not result.success:
            raise ValueError("No se puede cargar archivo sin detección exitosa")

        if isinstance(reader, SheetableReader):
            from readers.models.excel_options import ExcelOptions

            options = ExcelOptions(
                sheet_name=result.sheet_name,
                skiprows=result.data_start_row
            )
            print(f"options.nrows: {options.nrows}")

            df = reader.read(result.file_path, options)

        else:
            from readers.models.csv_options import CsvOptions

            options = CsvOptions(
                skiprows=result.data_start_row
            )

            df = reader.read(result.file_path, options)

        return clean_dataframe(df)