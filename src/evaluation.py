import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    root_mean_squared_error,
    r2_score
)


def calculate_regression_metrics(y_true, y_pred):
    """
    Calcula métricas de evaluación para un modelo de regresión.

    Parameters
    ----------
    y_true : array-like
        Valores reales de la variable objetivo.

    y_pred : array-like
        Valores predichos por el modelo.

    Returns
    -------
    dict
        Diccionario con MAE, RMSE y R².
    """

    metrics = {
        "mae": mean_absolute_error(y_true, y_pred),
        "rmse": root_mean_squared_error(y_true, y_pred),
        "r2": r2_score(y_true, y_pred)
    }

    return metrics


def calculate_residuals(y_true, y_pred):
    """
    Calcula los residuos de un modelo de regresión.

    Parameters
    ----------
    y_true : array-like
        Valores reales.

    y_pred : array-like
        Valores predichos.

    Returns
    -------
    numpy.ndarray
        Diferencia entre valores reales y predichos.
    """

    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    residuals = y_true - y_pred

    return residuals


def evaluate_regression_model(model, X_test, y_test):
    """
    Evalúa un modelo de regresión sobre el conjunto de prueba.

    Parameters
    ----------
    model : sklearn estimator
        Modelo o pipeline previamente entrenado.

    X_test : pandas.DataFrame
        Variables predictoras del conjunto de prueba.

    y_test : pandas.Series
        Valores reales de la variable objetivo.

    Returns
    -------
    dict
        Diccionario con predicciones, métricas y residuos.
    """

    y_pred = model.predict(X_test)

    metrics = calculate_regression_metrics(
        y_test,
        y_pred
    )

    residuals = calculate_residuals(
        y_test,
        y_pred
    )

    return {
        "predictions": y_pred,
        "metrics": metrics,
        "residuals": residuals
    }

def summarize_regression_evaluation(evaluation_result):
    """
    Resume los resultados de evaluación de un modelo de regresión.

    Parameters
    ----------
    evaluation_result : dict
        Resultado generado por evaluate_regression_model.

    Returns
    -------
    dict
        Resumen compacto de métricas y residuos.
    """

    metrics = evaluation_result["metrics"]
    predictions = evaluation_result["predictions"]
    residuals = evaluation_result["residuals"]

    summary = {
        "mae": metrics["mae"],
        "rmse": metrics["rmse"],
        "r2": metrics["r2"],
        "n_predictions": len(predictions),
        "mean_residual": float(np.mean(residuals)),
        "min_residual": float(np.min(residuals)),
        "max_residual": float(np.max(residuals))
    }

    return summary

