import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split

def detect_feature_types(df, target_column=None):
    """
    Detecta las variables numéricas y categóricas de un dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset que se desea analizar.

    target_column : str, optional
        Nombre de la variable objetivo. Si se proporciona,
        se excluye de las variables predictoras.

    Returns
    -------
    dict
        Diccionario con las variables numéricas y categóricas.
    """

    features_df = df.copy()

    if target_column is not None:
        features_df = features_df.drop(columns=[target_column])

    numeric_features = (
        features_df
        .select_dtypes(include="number")
        .columns
        .tolist()
    )

    categorical_features = (
        features_df
        .select_dtypes(include=["object", "string", "category", "bool"])
        .columns
        .tolist()
    )

    return {
        "numeric_features": numeric_features,
        "categorical_features": categorical_features
    }

def build_preprocessor(numeric_features, categorical_features):
    """
    Construye un preprocesador para variables numéricas y categóricas.

    Parameters
    ----------
    numeric_features : list
        Lista de columnas numéricas.

    categorical_features : list
        Lista de columnas categóricas.

    Returns
    -------
    sklearn.compose.ColumnTransformer
        Preprocesador listo para utilizar dentro de un pipeline.
    """

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="infrequent_if_exist",
                    min_frequency=2
                )
            )
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features)
        ]
    )

    return preprocessor

def split_features_target(df, target_column):
    """
    Separa las variables predictoras de la variable objetivo.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset completo.

    target_column : str
        Nombre de la variable objetivo.

    Returns
    -------
    tuple
        X contiene las variables predictoras.
        y contiene la variable objetivo.
    """

    X = df.drop(columns=[target_column])
    y = df[target_column]

    return X, y


def prepare_regression_dataset(
    df,
    target_column,
    min_samples=10
):
    """Limpia y valida los datos mínimos para un problema de regresión."""

    if target_column not in df.columns:
        raise ValueError("La variable objetivo no existe en el dataset.")

    if target_column not in df.select_dtypes(include="number").columns:
        raise ValueError("La variable objetivo debe ser numérica.")

    cleaned_df = df.copy()
    numeric_columns = cleaned_df.select_dtypes(include="number").columns
    cleaned_df[numeric_columns] = cleaned_df[numeric_columns].replace(
        [np.inf, -np.inf],
        np.nan
    )

    initial_rows = len(cleaned_df)
    cleaned_df = cleaned_df.dropna(subset=[target_column])
    dropped_target_rows = initial_rows - len(cleaned_df)

    if len(cleaned_df) < min_samples:
        raise ValueError(
            f"Se necesitan al menos {min_samples} filas con un objetivo válido."
        )

    if cleaned_df[target_column].nunique(dropna=True) < 2:
        raise ValueError(
            "La variable objetivo necesita al menos dos valores diferentes."
        )

    X, y = split_features_target(cleaned_df, target_column)

    if X.shape[1] == 0:
        raise ValueError(
            "El dataset necesita al menos una variable predictora."
        )

    feature_types = detect_feature_types(X)

    if not (
        feature_types["numeric_features"]
        or feature_types["categorical_features"]
    ):
        raise ValueError(
            "No se detectaron variables predictoras numéricas o categóricas."
        )

    return X, y, dropped_target_rows


def get_valid_regression_targets(df, min_samples=10):
    """Devuelve targets numéricos con datos suficientes y variación real."""

    valid_targets = []

    for column in df.select_dtypes(include="number").columns:
        clean_target = (
            df[column]
            .replace([np.inf, -np.inf], np.nan)
            .dropna()
        )

        if (
            len(clean_target) >= min_samples
            and clean_target.nunique() >= 2
        ):
            valid_targets.append(column)

    return valid_targets

def split_train_test(
    X,
    y,
    test_size=0.2,
    random_state=42
):
    """
    Divide los datos en conjuntos de entrenamiento y prueba.

    Parameters
    ----------
    X : pandas.DataFrame
        Variables predictoras.

    y : pandas.Series
        Variable objetivo.

    test_size : float
        Proporción de datos reservada para prueba.

    random_state : int
        Semilla para reproducibilidad.

    Returns
    -------
    tuple
        X_train, X_test, y_train, y_test
    """

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state
    )

    return X_train, X_test, y_train, y_test

