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
        .select_dtypes(include=["object", "string", "category"])
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
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
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

