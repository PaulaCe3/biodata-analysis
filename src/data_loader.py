import pandas as pd


def load_dataset(
    file_path,
    header="infer",
    column_names=None,
    separator=None
):
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

    separator : str, optional
        Separador explícito. Si no se proporciona, pandas intentará detectarlo.

    Returns
    -------
    pandas.DataFrame
        Dataset cargado como DataFrame.
    """

    try:
        df = pd.read_csv(
            file_path,
            header=header,
            sep=separator,
            engine="python" if separator is None else "c"
        )
    except (
        pd.errors.EmptyDataError,
        pd.errors.ParserError,
        UnicodeDecodeError
    ) as error:
        raise ValueError(
            "No se pudo leer el archivo. Revisá el separador, la codificación "
            "y que el contenido sea tabular."
        ) from error

    if df.empty or df.shape[1] == 0:
        raise ValueError("El archivo no contiene datos utilizables.")

    if column_names is not None:
        if len(column_names) != df.shape[1]:
            raise ValueError(
                "La cantidad de nombres no coincide con las columnas del archivo."
            )

        df.columns = column_names

    return df


def validate_column_names(columns):
    """Normaliza nombres de columnas y rechaza vacíos o duplicados."""

    normalized = [str(column).strip() for column in columns]

    if any(not column for column in normalized):
        raise ValueError("Todas las columnas deben tener un nombre.")

    duplicated = sorted(
        {
            column
            for column in normalized
            if normalized.count(column) > 1
        }
    )

    if duplicated:
        duplicated_text = ", ".join(duplicated)
        raise ValueError(
            f"Los nombres de columnas deben ser únicos. Repetidos: "
            f"{duplicated_text}."
        )

    return normalized
