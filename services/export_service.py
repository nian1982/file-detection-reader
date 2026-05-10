"""
Exportador de datos a múltiples formatos
Soporta: Excel, CSV, TXT, Parquet
"""
from typing import List
from enum import Enum


class FormatoExport(Enum):
    EXCEL = "excel"
    CSV = "csv"
    TXT = "txt"
    PARQUET = "parquet"


class CSVDummy:
    """Exportador CSV"""
    content_type = "text/csv"
    extension = "csv"
    
    def __init__(self, headers: List[str]):
        self.headers = headers
    
    def get_content_type(self) -> str:
        return self.content_type
    
    def get_extension(self) -> str:
        return self.extension
    
    def get_filename(self, nombre_base: str) -> str:
        return f"{nombre_base}.{self.extension}"
    
    def get_headers(self) -> List[str]:
        return self.headers
    
    def format_row(self, row: dict) -> str:
        values = [self.format_value(row.get(h, "")) for h in self.headers]
        return ",".join(values)
    
    def format_value(self, value) -> str:
        if value is None:
            return ""
        return str(value).replace(",", ";")


class TxtDummy:
    """Exportador TXT"""
    content_type = "text/plain"
    extension = "txt"
    
    def __init__(self, headers: List[str]):
        self.headers = headers
    
    def get_content_type(self) -> str:
        return self.content_type
    
    def get_extension(self) -> str:
        return self.extension
    
    def get_filename(self, nombre_base: str) -> str:
        return f"{nombre_base}.{self.extension}"
    
    def get_headers(self) -> List[str]:
        return self.headers
    
    def format_row(self, row: dict) -> str:
        values = [self.format_value(row.get(h, "")) for h in self.headers]
        return "|".join(values)
    
    def format_value(self, value) -> str:
        if value is None:
            return ""
        return str(value).ljust(20)[:20]


def get_exportador(formato: str, headers: List[str]):
    """Factory para obtener exportador"""
    forma = FormatoExport(formato.lower()) if formato.lower() in [e.value for e in FormatoExport] else FormatoExport.CSV
    
    if forma == FormatoExport.CSV:
        return CSVDummy(headers)
    elif forma == FormatoExport.TXT:
        return TxtDummy(headers)
    else:
        return CSVDummy(headers)


def exportar_a_csv(data: List[dict], headers: List[str]) -> str:
    """Exporta a CSV"""
    exp = CSVDummy(headers)
    lineas = [exp.format_row(r) for r in data]
    return "\n".join([",".join(headers)] + lineas)


def exportar_a_txt(data: List[dict], headers: List[str]) -> str:
    """Exporta a TXT delimitado por pipes"""
    exp = TxtDummy(headers)
    lineas = [exp.format_row(r) for r in data]
    header_line = exp.format_row(dict(zip(headers, headers)))
    return "\n".join([header_line] + lineas)


def exportar_a_excel(data: List[dict], headers: List[str]) -> bytes:
    """Exporta a Excel (necesita openpyxl)"""
    try:
        import openpyxl
        from io import BytesIO
        
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Data"
        
        ws.append(headers)
        for row in data:
            ws.append([row.get(h, "") for h in headers])
        
        buffer = BytesIO()
        wb.save(buffer)
        return buffer.getvalue()
    except ImportError:
        raise ImportError("openpyxl no está instalado. Ejecuta: pip install openpyxl")


def exportar_a_parquet(data: List[dict], headers: List[str]) -> bytes:
    """Exporta a Parquet (necesita pyarrow)"""
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
        from io import BytesIO
        
        table = pa.Table.from_pylist([row for row in data])
        buffer = BytesIO()
        writer = pq.NewFileWriter(buffer, table.schema)
        writer.write_table(table)
        writer.close()
        return buffer.getvalue()
    except ImportError:
        raise ImportError("pyarrow no está instalado. Ejecuta: pip install pyarrow")