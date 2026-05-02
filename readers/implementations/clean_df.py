import pandas as pd

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # limpiar nombres de columnas
    df.columns = [str(col).strip() if not isinstance(col, int) else col for col in df.columns]

    # limpiar espacios en columnas tipo texto
    obj_cols = df.select_dtypes(include=["object"]).columns
    df[obj_cols] = df[obj_cols].apply(lambda col: col.str.strip())

    # convertir vacíos a NA
    df.replace(r'^\s*$', pd.NA, regex=True, inplace=True)

    # eliminar columnas completamente vacías
    df.dropna(axis=1, how='all', inplace=True)

    # eliminar filas completamente vacías
    df.dropna(axis=0, how='all', inplace=True)

    # eliminar filas con muchos nulos (menos del 50% de datos)
    min_non_null = df.shape[1] * 0.5
    df = df.dropna(thresh=min_non_null)

    # reset index
    df.reset_index(drop=True, inplace=True)

    # convertir NaN a None
    df = df.astype(object).where(pd.notna(df), None)

    return df