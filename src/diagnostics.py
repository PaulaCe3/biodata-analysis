import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.inspection import permutation_importance

from src.i18n import translate


def build_prediction_table(X_test, y_true, y_pred):
    """Construye una tabla auditable con valores reales y predichos."""

    y_true_array = np.asarray(y_true)
    y_pred_array = np.asarray(y_pred)

    if len(X_test) != len(y_true_array) or len(y_true_array) != len(y_pred_array):
        raise ValueError(
            "X_test, y_true e y_pred deben tener la misma cantidad de filas."
        )

    prediction_table = X_test.reset_index(drop=False).copy()
    index_column = prediction_table.columns[0]
    prediction_table = prediction_table.rename(
        columns={index_column: "fila_original"}
    )

    prediction_table["valor_real"] = y_true_array
    prediction_table["prediccion"] = y_pred_array
    prediction_table["residuo"] = y_true_array - y_pred_array
    prediction_table["error_absoluto"] = np.abs(
        prediction_table["residuo"]
    )

    return prediction_table


def get_largest_errors(prediction_table, n=10):
    """Devuelve los casos con mayor error absoluto."""

    if n < 1:
        raise ValueError("n debe ser mayor o igual que 1.")

    return (
        prediction_table
        .nlargest(n, "error_absoluto")
        .reset_index(drop=True)
    )


def calculate_permutation_feature_importance(
    model,
    X_test,
    y_test,
    n_repeats=8,
    random_state=42
):
    """
    Calcula importancia predictiva sobre las variables originales.

    La importancia representa cuánto empeora el MAE al permutar cada variable.
    No implica causalidad.
    """

    result = permutation_importance(
        model,
        X_test,
        y_test,
        scoring="neg_mean_absolute_error",
        n_repeats=n_repeats,
        random_state=random_state,
        n_jobs=1
    )

    importance_table = pd.DataFrame(
        {
            "variable": X_test.columns,
            "importancia": result.importances_mean,
            "desviacion": result.importances_std
        }
    )

    return (
        importance_table
        .sort_values("importancia", ascending=False)
        .reset_index(drop=True)
    )


def calculate_subgroup_errors(
    prediction_table,
    categorical_features,
    min_group_size=10
):
    """Calcula MAE y sesgo promedio para grupos categóricos con datos suficientes."""

    rows = []

    for feature in categorical_features:
        if feature not in prediction_table.columns:
            continue

        grouped = prediction_table.groupby(
            feature,
            dropna=False,
            observed=False
        )

        for group_value, group_data in grouped:
            if len(group_data) < min_group_size:
                continue

            rows.append(
                {
                    "variable": feature,
                    "grupo": str(group_value),
                    "casos": len(group_data),
                    "mae": group_data["error_absoluto"].mean(),
                    "residuo_promedio": group_data["residuo"].mean()
                }
            )

    return pd.DataFrame(
        rows,
        columns=[
            "variable",
            "grupo",
            "casos",
            "mae",
            "residuo_promedio"
        ]
    )


def build_diagnostic_warnings(
    evaluation_summary,
    prediction_table,
    subgroup_errors=None,
    language="es"
):
    """Genera advertencias explicables a partir de reglas transparentes."""

    warnings = []
    mae = float(evaluation_summary["mae"])
    mean_residual = float(evaluation_summary["mean_residual"])
    p90_error = float(prediction_table["error_absoluto"].quantile(0.90))

    if mae > 0 and abs(mean_residual) > mae * 0.10:
        direction = translate(
            "subestimar" if mean_residual > 0 else "sobreestimar",
            language
        )
        warnings.append(
            {
                "title": translate("Posible sesgo sistemático", language),
                "message": translate(
                    "El residuo promedio es {residual:.3f}. El modelo muestra una tendencia general a {direction} los valores.",
                    language,
                    residual=mean_residual,
                    direction=direction
                )
            }
        )

    if mae > 0 and p90_error > mae * 2:
        warnings.append(
            {
                "title": translate("Errores extremos relevantes", language),
                "message": translate(
                    "El 10 % de los casos con mayor error supera aproximadamente {error:.3f} unidades. Conviene revisarlos antes de tomar decisiones de alto impacto.",
                    language,
                    error=p90_error
                )
            }
        )

    if subgroup_errors is not None and not subgroup_errors.empty:
        for feature, feature_data in subgroup_errors.groupby("variable"):
            minimum_mae = feature_data["mae"].min()
            maximum_mae = feature_data["mae"].max()

            if minimum_mae > 0 and maximum_mae / minimum_mae >= 1.5:
                worst_group = feature_data.loc[feature_data["mae"].idxmax()]
                warnings.append(
                    {
                        "title": translate(
                            "Diferencia de rendimiento en {feature}",
                            language,
                            feature=feature
                        ),
                        "message": translate(
                            "El grupo {group} presenta el mayor MAE ({mae:.3f}). Revisá si esta diferencia es aceptable para el uso previsto.",
                            language,
                            group=worst_group["grupo"],
                            mae=worst_group["mae"]
                        )
                    }
                )

    return warnings


def summarize_diagnostics(
    prediction_table,
    feature_importance,
    warnings
):
    """Resume los diagnósticos para el informe y la lectura de resultados."""

    absolute_errors = prediction_table["error_absoluto"]
    positive_importance = feature_importance[
        feature_importance["importancia"] > 0
    ]

    return {
        "median_absolute_error": float(absolute_errors.median()),
        "p90_absolute_error": float(absolute_errors.quantile(0.90)),
        "max_absolute_error": float(absolute_errors.max()),
        "top_features": positive_importance.head(5)[
            ["variable", "importancia"]
        ].to_dict(orient="records"),
        "warnings": warnings
    }


def plot_actual_vs_predicted(prediction_table, target_name, language="es"):
    """Grafica valores reales frente a valores predichos."""

    real = prediction_table["valor_real"]
    predicted = prediction_table["prediccion"]
    lower = min(real.min(), predicted.min())
    upper = max(real.max(), predicted.max())

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(real, predicted, alpha=0.55, edgecolors="none")
    ax.plot([lower, upper], [lower, upper], linestyle="--", color="tab:red")
    ax.set_xlabel(translate(
        "Valor real de {target}", language, target=target_name
    ))
    ax.set_ylabel(translate(
        "Predicción de {target}", language, target=target_name
    ))
    ax.set_title(translate("Valores reales frente a predicciones", language))
    ax.grid(alpha=0.2)
    fig.tight_layout()

    return fig


def plot_residuals(prediction_table, language="es"):
    """Grafica residuos frente a predicciones."""

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(
        prediction_table["prediccion"],
        prediction_table["residuo"],
        alpha=0.55,
        edgecolors="none"
    )
    ax.axhline(0, linestyle="--", color="tab:red")
    ax.set_xlabel(translate("Valor predicho", language))
    ax.set_ylabel(translate("Residuo (real − predicción)", language))
    ax.set_title(translate("Errores a lo largo de las predicciones", language))
    ax.grid(alpha=0.2)
    fig.tight_layout()

    return fig


def plot_residual_distribution(prediction_table, language="es"):
    """Grafica la distribución de los residuos."""

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.hist(
        prediction_table["residuo"],
        bins=30,
        color="tab:blue",
        alpha=0.8,
        edgecolor="white"
    )
    ax.axvline(0, linestyle="--", color="tab:red")
    ax.set_xlabel(translate("Residuo (real − predicción)", language))
    ax.set_ylabel(translate("Cantidad de casos", language))
    ax.set_title(translate("Distribución de errores", language))
    fig.tight_layout()

    return fig


def plot_feature_importance(feature_importance, top_n=12, language="es"):
    """Grafica las variables con mayor importancia predictiva."""

    plot_data = (
        feature_importance
        .head(top_n)
        .sort_values("importancia", ascending=True)
    )

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.barh(
        plot_data["variable"],
        plot_data["importancia"],
        xerr=plot_data["desviacion"],
        color="tab:green",
        alpha=0.8
    )
    ax.axvline(0, color="gray", linewidth=0.8)
    ax.set_xlabel(translate("Aumento del MAE al alterar la variable", language))
    ax.set_ylabel(translate("Variable", language))
    ax.set_title(translate("Importancia predictiva por permutación", language))
    fig.tight_layout()

    return fig
