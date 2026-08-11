def get_numeric_summary(df):
    """
    Genera un resumen estadístico de las variables numéricas.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset que se desea analizar.

    Returns
    -------
    pandas.DataFrame
        Tabla con estadísticas descriptivas de las variables numéricas.
    """

    numeric_df = df.select_dtypes(include="number")

    summary = numeric_df.describe()

    return summary

def get_categorical_summary(df):
    """
    Genera un resumen de frecuencias para las variables categóricas.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset que se desea analizar.

    Returns
    -------
    dict
        Diccionario con las frecuencias de cada variable categórica.
    """

    categorical_df = df.select_dtypes(
        include=["object", "string", "category"]
    )

    summary = {}

    for column in categorical_df.columns:
        summary[column] = (
            categorical_df[column]
            .value_counts(dropna=False)
            .to_dict()
        )

    return summary

def get_correlation_matrix(df):
    """
    Calcula la matriz de correlación entre las variables numéricas.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset que se desea analizar.

    Returns
    -------
    pandas.DataFrame
        Matriz de correlación entre las variables numéricas.
    """

    numeric_df = df.select_dtypes(include="number")

    correlation_matrix = numeric_df.corr()

    return correlation_matrix
