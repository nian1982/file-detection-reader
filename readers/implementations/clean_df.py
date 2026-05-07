import pandas as pd


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.columns = [
        str(col).strip() if not isinstance(col, int) else col
        for col in df.columns
    ]

    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].str.strip()

    df.replace(r'^\s*$', pd.NA, regex=True, inplace=True)

    df.dropna(axis=1, how='all', inplace=True)

    df.dropna(axis=0, how='all', inplace=True)

    min_non_null = int(df.shape[1] * 0.5)
    df = df.dropna(thresh=min_non_null)

    df.reset_index(drop=True, inplace=True)

    df = df.astype(object).where(pd.notna(df), None)

    return df
