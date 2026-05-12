class ReaderError(Exception):
    pass


class UnsupportedFileFormatError(ReaderError):
    def __init__(self, extension: str):
        super().__init__(
            f"Formato no soportado: '{extension}'. Usa: .csv, .xlsx, .xls"
        )


class FileAccessError(ReaderError):
    def __init__(self, file_name: str):
        super().__init__(f"No se encuentra o no se puede leer: '{file_name}'")


class DetectionError(ReaderError):
    def __init__(self, file_name: str, detail: str = ""):
        msg = f"No se encontró configuración que coincida con '{file_name}'"
        if detail:
            msg += f": {detail}"
        super().__init__(msg)
