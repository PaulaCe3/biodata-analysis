import matplotlib.pyplot as plt
import pandas as pd

from src.i18n import translate

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

    if numeric_df.empty:
        return numeric_df

    summary = numeric_df.describe()

    return summary

def get_categorical_summary(df, max_categories=50):
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
        include=["object", "string", "category", "bool"]
    )

    summary = {}

    if max_categories < 1:
        raise ValueError("max_categories debe ser mayor o igual que 1.")

    for column in categorical_df.columns:
        summary[column] = (
            categorical_df[column]
            .value_counts(dropna=False)
            .head(max_categories)
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

def plot_numeric_distribution(df, column, bins=30, language="es"):
    """
    Genera un histograma para una variable numérica.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset que contiene la variable.

    column : str
        Nombre de la columna numérica que se desea visualizar.

    bins : int, optional
        Cantidad de intervalos del histograma. Por defecto es 30.

    Returns
    -------
    matplotlib.figure.Figure
        Figura generada.
    """

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.hist(
        df[column].dropna(),
        bins=bins,
        edgecolor="black"
    )

    ax.set_title(translate("Distribución de {column}", language, column=column))
    ax.set_xlabel(column)
    ax.set_ylabel(translate("Frecuencia", language))

    return fig

def plot_categorical_distribution(
    df,
    column,
    max_categories=30,
    language="es"
):
    """
    Genera un gráfico de barras para una variable categórica.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset que contiene la variable.

    column : str
        Nombre de la columna categórica que se desea visualizar.

    Returns
    -------
    matplotlib.figure.Figure
        Figura generada.
    """

    if max_categories < 1:
        raise ValueError("max_categories debe ser mayor o igual que 1.")

    counts = (
        df[column]
        .value_counts(dropna=False)
        .head(max_categories)
    )

    category_labels = [
        translate("Sin dato", language) if pd.isna(value) else str(value)
        for value in counts.index
    ]

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        category_labels,
        counts.values,
        edgecolor="black"
    )

    ax.set_title(translate("Distribución de {column}", language, column=column))
    ax.set_xlabel(column)
    ax.set_ylabel(translate("Frecuencia", language))

    return fig

def plot_correlation_heatmap(df, language="es"):
    """
    Genera un mapa de calor de correlaciones entre variables numéricas.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset que se desea analizar.

    Returns
    -------
    matplotlib.figure.Figure
        Figura generada.
    """

    correlation_matrix = get_correlation_matrix(df)

    fig, ax = plt.subplots(figsize=(10, 8))

    image = ax.imshow(
        correlation_matrix,
        cmap="coolwarm",
        vmin=-1,
        vmax=1
    )

    fig.colorbar(
        image,
        ax=ax,
        label=translate("Correlación", language)
    )

    ax.set_xticks(range(len(correlation_matrix.columns)))
    ax.set_xticklabels(
        correlation_matrix.columns,
        rotation=45,
        ha="right"
    )

    ax.set_yticks(range(len(correlation_matrix.index)))
    ax.set_yticklabels(correlation_matrix.index)

    for i in range(len(correlation_matrix.index)):
        for j in range(len(correlation_matrix.columns)):
            ax.text(
                j,
                i,
                f"{correlation_matrix.iloc[i, j]:.2f}",
                ha="center",
                va="center"
            )

    ax.set_title(translate("Mapa de calor de correlaciones", language))

    fig.tight_layout()

    return fig
