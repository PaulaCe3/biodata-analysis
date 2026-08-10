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