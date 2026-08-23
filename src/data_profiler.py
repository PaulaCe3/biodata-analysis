import hashlib

import pandas as pd


def get_dataset_profile(df):
    """
    Obtiene información básica sobre la estructura de un dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset que se desea analizar.

    Returns
    -------
    dict
        Diccionario con información básica del dataset.
    """

    profile = {
        "n_rows": df.shape[0],
        "n_columns": df.shape[1],
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.astype(str).to_dict()
    }

    return profile


def get_dataset_fingerprint(df):
    """Genera una huella estable para no reutilizar análisis de otros datos."""

    hashed_values = pd.util.hash_pandas_object(
        df,
        index=True,
        categorize=True
    ).values
    schema = repr(
        list(zip(df.columns.astype(str), df.dtypes.astype(str)))
    ).encode("utf-8")

    digest = hashlib.sha256()
    digest.update(hashed_values.tobytes())
    digest.update(schema)

    return digest.hexdigest()
