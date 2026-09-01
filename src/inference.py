import math

import numpy as np
import pandas as pd


def _python_scalar(value):
    """Convierte escalares de NumPy a tipos simples cuando es posible."""

    return value.item() if isinstance(value, np.generic) else value


def _suggest_numeric_step(minimum, maximum, integer_like):
    """Propone un paso de entrada legible según la escala observada."""

    if integer_like:
        return 1

    span = abs(float(maximum) - float(minimum))

    if not np.isfinite(span) or span == 0:
        reference = max(abs(float(minimum)), 1.0)
        span = reference

    exponent = math.floor(math.log10(span)) - 2
    return float(max(10 ** exponent, 1e-9))


def build_feature_profiles(
    dataframe,
    numeric_features,
    categorical_features
):
    """Resume los valores necesarios para construir un caso nuevo."""

    profiles = {}

    for feature in numeric_features:
        values = (
            pd.to_numeric(dataframe[feature], errors="coerce")
            .replace([np.inf, -np.inf], np.nan)
            .dropna()
        )

        if values.empty:
            raise ValueError(
                f"La variable numérica {feature} no tiene valores válidos."
            )

        minimum = float(values.min())
        maximum = float(values.max())
        median = float(values.median())
        integer_like = bool(
            np.all(np.isclose(values.to_numpy(dtype=float), np.round(values)))
        )

        profiles[feature] = {
            "kind": "numeric",
            "minimum": minimum,
            "maximum": maximum,
            "median": median,
            "integer_like": integer_like,
            "step": _suggest_numeric_step(minimum, maximum, integer_like)
        }

    for feature in categorical_features:
        categories = [
            _python_scalar(value)
            for value in dataframe[feature].dropna().drop_duplicates().tolist()
        ]
        categories = sorted(categories, key=lambda value: str(value).casefold())

        if not categories:
            raise ValueError(
                f"La variable categórica {feature} no tiene valores válidos."
            )

        profiles[feature] = {
            "kind": "categorical",
            "categories": categories
        }

    missing_profiles = [
        feature
        for feature in dataframe.columns
        if feature not in profiles
    ]

    if missing_profiles:
        raise ValueError(
            "No se pudo describir una o más variables predictoras: "
            + ", ".join(map(str, missing_profiles))
        )

    return profiles


def build_observation(feature_order, values):
    """Construye una fila con el mismo orden usado durante el entrenamiento."""

    record = {}

    for feature in feature_order:
        value = values.get(feature)

        if value is None or (isinstance(value, str) and not value.strip()):
            value = np.nan

        record[feature] = value

    return pd.DataFrame([record], columns=list(feature_order))


def assess_observation(observation, feature_profiles):
    """Detecta faltantes y valores alejados de la referencia de entrenamiento."""

    if len(observation) != 1:
        raise ValueError("La evaluación requiere exactamente una observación.")

    missing_features = []
    out_of_range_features = []
    unseen_categories = []
    provided_count = 0

    for feature, profile in feature_profiles.items():
        value = observation.iloc[0][feature]

        if pd.isna(value):
            missing_features.append(feature)
            continue

        provided_count += 1

        if profile["kind"] == "numeric":
            numeric_value = float(value)

            if not np.isfinite(numeric_value):
                missing_features.append(feature)
                provided_count -= 1
            elif (
                numeric_value < profile["minimum"]
                or numeric_value > profile["maximum"]
            ):
                out_of_range_features.append(feature)
        elif value not in profile["categories"]:
            unseen_categories.append(feature)

    return {
        "provided_count": provided_count,
        "missing_features": missing_features,
        "out_of_range_features": out_of_range_features,
        "unseen_categories": unseen_categories
    }


def predict_observation(model, observation):
    """Genera una única predicción numérica y valida el resultado."""

    predictions = np.asarray(model.predict(observation), dtype=float)

    if predictions.size != 1 or not np.isfinite(predictions[0]):
        raise ValueError("El modelo no devolvió una predicción numérica válida.")

    return float(predictions[0])
