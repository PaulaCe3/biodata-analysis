from sklearn.pipeline import Pipeline
from sklearn.model_selection import KFold, cross_val_score


def build_model_pipeline(preprocessor, model):
    """
    Construye un pipeline que combina preprocesamiento y modelo.

    Parameters
    ----------
    preprocessor : sklearn transformer
        Preprocesador encargado de transformar las variables.

    model : sklearn estimator
        Modelo de Machine Learning que se desea utilizar.

    Returns
    -------
    sklearn.pipeline.Pipeline
        Pipeline completo de preprocesamiento y modelado.
    """

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    return pipeline

def cross_validate_regression_mae(
    pipeline,
    X_train,
    y_train,
    n_splits=5,
    random_state=42
):
    """
    Evalúa un modelo de regresión mediante validación cruzada
    utilizando MAE como métrica.

    Parameters
    ----------
    pipeline : sklearn.pipeline.Pipeline
        Pipeline que contiene preprocesamiento y modelo.

    X_train : pandas.DataFrame
        Variables predictoras de entrenamiento.

    y_train : pandas.Series
        Variable objetivo de entrenamiento.

    n_splits : int
        Cantidad de folds de la validación cruzada.

    random_state : int
        Semilla para reproducibilidad.

    Returns
    -------
    numpy.ndarray
        Valores de MAE obtenidos en cada fold.
    """

    if n_splits < 2:
        raise ValueError("n_splits debe ser mayor o igual que 2.")

    if len(X_train) < n_splits:
        raise ValueError(
            "No hay suficientes filas de entrenamiento para la cantidad de folds."
        )

    cv = KFold(
        n_splits=n_splits,
        shuffle=True,
        random_state=random_state
    )

    scores = cross_val_score(
        pipeline,
        X_train,
        y_train,
        cv=cv,
        scoring="neg_mean_absolute_error"
    )

    mae_scores = -scores

    return mae_scores


def compare_regression_models(
    preprocessor,
    models,
    X_train,
    y_train,
    n_splits=5,
    random_state=42
):
    """
    Compara varios modelos de regresión mediante validación cruzada.

    Parameters
    ----------
    preprocessor : sklearn transformer
        Preprocesador que se aplicará a los datos.

    models : dict
        Diccionario con nombres de modelos y estimadores de sklearn.

    X_train : pandas.DataFrame
        Variables predictoras de entrenamiento.

    y_train : pandas.Series
        Variable objetivo de entrenamiento.

    n_splits : int
        Cantidad de folds de la validación cruzada.

    random_state : int
        Semilla para reproducibilidad.

    Returns
    -------
    dict
        Resultados de MAE para cada modelo.
    """

    results = {}

    for model_name, model in models.items():

        pipeline = build_model_pipeline(
            preprocessor,
            model
        )

        mae_scores = cross_validate_regression_mae(
            pipeline,
            X_train,
            y_train,
            n_splits=n_splits,
            random_state=random_state
        )

        results[model_name] = {
            "mae_scores": mae_scores,
            "mean_mae": mae_scores.mean()
        }

    return results

def select_best_regression_model(results):
    """
    Selecciona el modelo con menor MAE promedio.

    Parameters
    ----------
    results : dict
        Resultados generados por compare_regression_models.

    Returns
    -------
    str
        Nombre del modelo con menor MAE promedio.
    """

    best_model_name = min(
        results,
        key=lambda model_name: results[model_name]["mean_mae"]
    )

    return best_model_name

def train_regression_model(
    preprocessor,
    model,
    X_train,
    y_train
):
    """
    Entrena un modelo de regresión utilizando todos los datos
    de entrenamiento.

    Parameters
    ----------
    preprocessor : sklearn transformer
        Preprocesador que se aplicará a los datos.

    model : sklearn estimator
        Modelo de regresión que se desea entrenar.

    X_train : pandas.DataFrame
        Variables predictoras de entrenamiento.

    y_train : pandas.Series
        Variable objetivo de entrenamiento.

    Returns
    -------
    sklearn.pipeline.Pipeline
        Pipeline entrenado listo para realizar predicciones.
    """

    pipeline = build_model_pipeline(
        preprocessor,
        model
    )

    pipeline.fit(
        X_train,
        y_train
    )

    return pipeline
