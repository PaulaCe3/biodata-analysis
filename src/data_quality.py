import numpy as np


def get_missing_values(df):
    """
    Cuenta los valores faltantes de cada columna.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset que se desea analizar.

    Returns
    -------
    dict
        Diccionario con la cantidad de valores faltantes por columna.
    """

    missing_values = df.isna().sum().to_dict()

    return missing_values

def get_duplicate_count(df):
    """
    Cuenta la cantidad de filas duplicadas en un dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset que se desea analizar.

    Returns
    -------
    int
        Cantidad de filas duplicadas.
    """

    duplicate_count = int(df.duplicated().sum())

    return duplicate_count


def get_infinite_values(df):
    """Cuenta valores infinitos en las columnas numéricas."""

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        return {}

    return {
        column: int(np.isinf(numeric_df[column]).sum())
        for column in numeric_df.columns
    }

def get_quality_report(df):
    """
    Genera un resumen básico de calidad del dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset que se desea analizar.

    Returns
    -------
    dict
        Resumen con valores faltantes y filas duplicadas.
    """

    report = {
        "missing_values": get_missing_values(df),
        "infinite_values": get_infinite_values(df),
        "duplicate_rows": get_duplicate_count(df)
    }

    return report
