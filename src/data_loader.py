import pandas as pd


def load_dataset(file_path, header="infer", column_names=None):
    """
    Carga un dataset tabular utilizando pandas.

    Parameters
    ----------
    file_path : str
        Ruta del archivo que se desea cargar.

    header : int, None o "infer"
        Indica si el archivo contiene nombres de columnas.

    column_names : list, optional
        Lista de nombres para asignar manualmente a las columnas.

    Returns
    -------
    pandas.DataFrame
        Dataset cargado como DataFrame.
    """

    df = pd.read_csv(file_path, header=header)

    if column_names is not None:
        df.columns = column_names

    return df