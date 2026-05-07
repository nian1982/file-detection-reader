from pathlib import Path
from typing import Any
import pandas as pd
from readers.interfaces.file_reader import FileReader
from readers.models.csv_options import CsvOptions


class CsvReader(FileReader):

    def read(self, file_path: Path, options: CsvOptions | None = None) -> pd.DataFrame:
        options = options or CsvOptions()

        df = pd.read_csv(
            file_path,
            sep=options.sep,
            encoding=options.encoding,
            skiprows=options.skiprows,
            nrows=options.nrows,
            header=options.header,
            usecols=(
                lambda column: str(column).strip() in options.usecols
            )
            if options.usecols
            else None,
            keep_default_na=False,
            skip_blank_lines=False,
            dtype=str
        )

        if options.header is not None:
            df.columns = df.columns.str.strip()

        return df
