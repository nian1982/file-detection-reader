import pandas as pd


class ColumnExtractor:

    def extract(self, row: pd.Series) -> list[str]:
        values = []
        for value in row.tolist():
            normalized = str(value).strip().upper()
            if not normalized:
                continue
            if normalized == "NAN":
                continue
            values.append(normalized)
        return values
