def build_evaluation_section(evaluation_summary):
    """
    Genera una sección de texto con los resultados de evaluación
    de un modelo de regresión.

    Parameters
    ----------
    evaluation_summary : dict
        Resumen generado por summarize_regression_evaluation.

    Returns
    -------
    str
        Texto estructurado con los resultados de evaluación.
    """

    lines = [
        "EVALUACIÓN DEL MODELO",
        "",
        f"MAE: {evaluation_summary['mae']:.4f}",
        f"RMSE: {evaluation_summary['rmse']:.4f}",
        f"R²: {evaluation_summary['r2']:.4f}",
        f"Cantidad de predicciones: {evaluation_summary['n_predictions']}",
        f"Residuo promedio: {evaluation_summary['mean_residual']:.4f}",
        f"Residuo mínimo: {evaluation_summary['min_residual']:.4f}",
        f"Residuo máximo: {evaluation_summary['max_residual']:.4f}"
    ]

    return "\n".join(lines)


def build_dataset_profile_section(dataset_profile):
    """
    Genera una sección de texto con la información general
    del dataset.

    Parameters
    ----------
    dataset_profile : dict
        Perfil generado por get_dataset_profile.

    Returns
    -------
    str
        Texto estructurado con la información del dataset.
    """

    columns_text = ", ".join(
        str(column)
        for column in dataset_profile["columns"]
    )

    lines = [
        "PERFIL DEL DATASET",
        "",
        f"Cantidad de filas: {dataset_profile['n_rows']}",
        f"Cantidad de columnas: {dataset_profile['n_columns']}",
        f"Variables: {columns_text}"
    ]

    return "\n".join(lines)

def build_data_quality_section(quality_report):
    """
    Genera una sección de texto con el resumen de calidad
    del dataset.

    Parameters
    ----------
    quality_report : dict
        Reporte generado por get_quality_report.

    Returns
    -------
    str
        Texto estructurado con información de calidad de datos.
    """

    missing_values = quality_report["missing_values"]
    infinite_values = quality_report.get("infinite_values", {})
    duplicate_rows = quality_report["duplicate_rows"]

    total_missing = sum(missing_values.values())
    total_infinite = sum(infinite_values.values())

    lines = [
        "CALIDAD DE DATOS",
        "",
        f"Valores faltantes totales: {total_missing}",
        f"Valores numéricos infinitos: {total_infinite}",
        f"Filas duplicadas: {duplicate_rows}",
        "",
        "Valores faltantes por variable:"
    ]

    for column, count in missing_values.items():
        lines.append(
            f"- {column}: {count}"
        )

    if total_infinite:
        lines.extend(["", "Valores infinitos por variable:"])

        for column, count in infinite_values.items():
            if count:
                lines.append(f"- {column}: {count}")

    return "\n".join(lines)


def build_model_comparison_section(model_comparison):
    """
    Genera una sección de texto con la comparación
    de modelos de regresión.

    Parameters
    ----------
    model_comparison : dict
        Resultados generados por compare_regression_models.

    Returns
    -------
    str
        Texto estructurado con el MAE promedio de cada modelo.
    """

    lines = [
        "COMPARACIÓN DE MODELOS",
        ""
    ]

    for model_name, result in model_comparison.items():
        lines.append(
            f"- {model_name}: MAE promedio = {result['mean_mae']:.4f}"
        )

    best_model = min(
        model_comparison,
        key=lambda name: model_comparison[name]["mean_mae"]
    )

    lines.extend([
        "",
        f"Mejor modelo según MAE: {best_model}"
    ])

    return "\n".join(lines)


def build_interpretation_section(
    evaluation_summary,
    model_comparison=None,
    target_column=None,
    user_context=None
):
    """
    Genera una interpretación clara, prudente y orientada a decisiones.

    Parameters
    ----------
    evaluation_summary : dict
        Resumen generado por summarize_regression_evaluation.

    model_comparison : dict, optional
        Resultados de comparación entre modelos.

    target_column : str, optional
        Nombre de la variable objetivo.

    user_context : dict, optional
        Contexto y tolerancia indicados por la persona usuaria.

    Returns
    -------
    str
        Interpretación y limitaciones principales del modelo.
    """

    mae = evaluation_summary["mae"]
    rmse = evaluation_summary["rmse"]
    r2 = evaluation_summary["r2"]
    target_name = (
        str(target_column)
        if target_column is not None
        else "la variable objetivo"
    )

    if model_comparison:
        best_model = min(
            model_comparison,
            key=lambda name: model_comparison[name]["mean_mae"]
        )
        model_text = f"El modelo seleccionado fue {best_model}."
    else:
        model_text = "Se evaluó el modelo final seleccionado."

    if 0 <= r2 <= 1:
        r2_text = (
            f"El modelo logra explicar aproximadamente el {r2 * 100:.1f} % "
            f"de las diferencias observadas en {target_name}. El "
            f"{(1 - r2) * 100:.1f} % restante depende de información que "
            "el modelo no captura o de variabilidad difícil de predecir."
        )
    else:
        r2_text = (
            "El R² es negativo: en este conjunto de prueba, el modelo "
            "rinde peor que una predicción basada en el valor promedio."
        )

    if rmse > mae * 1.25:
        rmse_text = (
            f"El RMSE ({rmse:.4f}) es mayor que el MAE. Esto sugiere que, "
            "aunque muchas predicciones pueden estar relativamente cerca, "
            "existen algunos errores más grandes que merecen revisión."
        )
    else:
        rmse_text = (
            f"El RMSE ({rmse:.4f}) se mantiene relativamente cerca del MAE, "
            "lo que sugiere que los errores grandes no dominan el resultado."
        )

    tolerance_text = (
        f"Definí primero qué error es aceptable para tu caso. Si una "
        f"diferencia de {mae:.4f} unidades en {target_name} puede cambiar "
        "una decisión importante, el modelo todavía no debería decidir "
        "por sí solo."
    )

    if user_context:
        acceptable_error = user_context.get("acceptable_error")

        if acceptable_error is not None and acceptable_error > 0:
            if mae <= acceptable_error:
                tolerance_text = (
                    f"El MAE ({mae:.4f}) está dentro del error tolerable "
                    f"declarado ({acceptable_error:.4f}). Aun así, revisá los "
                    "errores extremos y los subgrupos antes de usar el modelo."
                )
            else:
                tolerance_text = (
                    f"El MAE ({mae:.4f}) supera el error tolerable declarado "
                    f"({acceptable_error:.4f}). El modelo necesita mejoras o "
                    "un uso más limitado antes de apoyar esa decisión."
                )

    lines = [
        "INTERPRETACIÓN EN LENGUAJE CLARO",
        "",
        model_text,
        "",
        "¿Qué significan los resultados?",
        (
            f"- En promedio, la predicción se aleja {mae:.4f} unidades del "
            f"valor real de {target_name}. Ese es el significado práctico "
            "del MAE."
        ),
        f"- {rmse_text}",
        f"- {r2_text}",
        "",
        "¿Cómo usar esta información para decidir?",
        f"- {tolerance_text}",
        (
            "- El modelo puede utilizarse como apoyo para ordenar, priorizar "
            "o revisar casos, siempre que una persona confirme las decisiones "
            "de mayor impacto."
        ),
        (
            "- Antes de ponerlo en uso, revisá los errores por grupos relevantes "
            "y comprobá que ningún grupo reciba predicciones sistemáticamente "
            "peores."
        ),
        (
            "- Validalo con datos nuevos, obtenidos en otro momento o contexto. "
            "Si el rendimiento cae, será necesario actualizar los datos o el modelo."
        ),
        "",
        "LIMITACIONES IMPORTANTES",
        (
            "- Las métricas son promedios: pueden ocultar casos extremos o "
            "diferencias entre subgrupos."
        ),
        (
            "- La evaluación utiliza una partición interna de prueba. No garantiza "
            "el mismo resultado con otra población, laboratorio, región o período."
        ),
        (
            "- El modelo encuentra patrones predictivos, pero no demuestra que "
            "una variable sea la causa de otra."
        ),
        (
            "- La importancia global de variables no explica por sí sola cada "
            "predicción individual ni demuestra causalidad."
        )
    ]

    return "\n".join(lines)


def build_user_context_section(user_context):
    """Documenta el objetivo y los criterios definidos para el análisis."""

    labels = {
        "goal": "Objetivo",
        "audience": "Audiencia",
        "decision": "Decisión que se desea apoyar",
        "acceptable_error": "Error tolerable",
        "impact": "Impacto de la decisión"
    }

    lines = ["CONTEXTO DEL ANÁLISIS", ""]

    for key, label in labels.items():
        value = user_context.get(key)

        if value not in (None, "", 0, 0.0):
            lines.append(f"{label}: {value}")

    if len(lines) == 2:
        lines.append("No se proporcionó contexto adicional.")

    return "\n".join(lines)


def build_diagnostics_section(diagnostics_summary):
    """Resume errores extremos, variables importantes y advertencias."""

    lines = [
        "DIAGNÓSTICO DEL MODELO",
        "",
        (
            "Error absoluto mediano: "
            f"{diagnostics_summary['median_absolute_error']:.4f}"
        ),
        (
            "Error absoluto del percentil 90: "
            f"{diagnostics_summary['p90_absolute_error']:.4f}"
        ),
        (
            "Mayor error absoluto observado: "
            f"{diagnostics_summary['max_absolute_error']:.4f}"
        ),
        "",
        "Variables con mayor importancia predictiva:"
    ]

    top_features = diagnostics_summary.get("top_features", [])

    if top_features:
        for feature in top_features:
            lines.append(
                f"- {feature['variable']}: {feature['importancia']:.4f}"
            )
    else:
        lines.append("- No se identificaron importancias positivas.")

    lines.extend(["", "Advertencias automáticas:"])
    warnings = diagnostics_summary.get("warnings", [])

    if warnings:
        for warning in warnings:
            lines.append(
                f"- {warning['title']}: {warning['message']}"
            )
    else:
        lines.append("- No se activaron advertencias con las reglas actuales.")

    lines.extend([
        "",
        (
            "La importancia por permutación mide utilidad predictiva. "
            "No implica causalidad."
        )
    ])

    return "\n".join(lines)


def build_full_report_english(
    dataset_profile,
    quality_report,
    model_comparison,
    evaluation_summary,
    target_column=None,
    diagnostics_summary=None,
    user_context=None
):
    """Builds the downloadable report in English."""

    target_name = str(target_column or "the target variable")
    missing_values = quality_report["missing_values"]
    infinite_values = quality_report.get("infinite_values", {})
    total_missing = sum(missing_values.values())
    total_infinite = sum(infinite_values.values())
    columns_text = ", ".join(str(column) for column in dataset_profile["columns"])

    profile_lines = [
        "DATASET PROFILE",
        "",
        f"Rows: {dataset_profile['n_rows']}",
        f"Columns: {dataset_profile['n_columns']}",
        f"Variables: {columns_text}"
    ]

    quality_lines = [
        "DATA QUALITY",
        "",
        f"Total missing values: {total_missing}",
        f"Infinite numeric values: {total_infinite}",
        f"Duplicate rows: {quality_report['duplicate_rows']}",
        "",
        "Missing values by variable:"
    ]
    quality_lines.extend(
        f"- {column}: {count}" for column, count in missing_values.items()
    )
    if total_infinite:
        quality_lines.extend(["", "Infinite values by variable:"])
        quality_lines.extend(
            f"- {column}: {count}"
            for column, count in infinite_values.items()
            if count
        )

    sections = ["\n".join(profile_lines), "\n".join(quality_lines)]

    if user_context:
        context_labels = {
            "goal": "Goal",
            "audience": "Audience",
            "decision": "Decision to support",
            "acceptable_error": "Tolerable error",
            "impact": "Decision impact"
        }
        context_lines = ["ANALYSIS CONTEXT", ""]
        for key, label in context_labels.items():
            value = user_context.get(key)
            if value not in (None, "", 0, 0.0):
                context_lines.append(
                    f"{label}: {translate(str(value), 'en')}"
                )
        if len(context_lines) == 2:
            context_lines.append("No additional context was provided.")
        sections.append("\n".join(context_lines))

    comparison_lines = ["MODEL COMPARISON", ""]
    for name, result in model_comparison.items():
        comparison_lines.append(
            f"- {model_label(name, 'en')}: mean MAE = {result['mean_mae']:.4f}"
        )
    best_model = min(
        model_comparison,
        key=lambda name: model_comparison[name]["mean_mae"]
    )
    comparison_lines.extend([
        "",
        f"Best model by MAE: {model_label(best_model, 'en')}"
    ])
    sections.append("\n".join(comparison_lines))

    evaluation_lines = [
        "MODEL EVALUATION",
        "",
        f"MAE: {evaluation_summary['mae']:.4f}",
        f"RMSE: {evaluation_summary['rmse']:.4f}",
        f"R²: {evaluation_summary['r2']:.4f}",
        f"Number of predictions: {evaluation_summary['n_predictions']}",
        f"Mean residual: {evaluation_summary['mean_residual']:.4f}",
        f"Minimum residual: {evaluation_summary['min_residual']:.4f}",
        f"Maximum residual: {evaluation_summary['max_residual']:.4f}"
    ]
    sections.append("\n".join(evaluation_lines))

    if diagnostics_summary:
        diagnostic_lines = [
            "MODEL DIAGNOSTICS",
            "",
            (
                "Median absolute error: "
                f"{diagnostics_summary['median_absolute_error']:.4f}"
            ),
            (
                "90th percentile absolute error: "
                f"{diagnostics_summary['p90_absolute_error']:.4f}"
            ),
            (
                "Largest observed absolute error: "
                f"{diagnostics_summary['max_absolute_error']:.4f}"
            ),
            "",
            "Variables with the highest predictive importance:"
        ]
        top_features = diagnostics_summary.get("top_features", [])
        if top_features:
            diagnostic_lines.extend(
                f"- {feature['variable']}: {feature['importancia']:.4f}"
                for feature in top_features
            )
        else:
            diagnostic_lines.append("- No positive importance values were identified.")
        diagnostic_lines.extend(["", "Automatic warnings:"])
        warnings = diagnostics_summary.get("warnings", [])
        if warnings:
            diagnostic_lines.extend(
                f"- {warning['title']}: {warning['message']}"
                for warning in warnings
            )
        else:
            diagnostic_lines.append("- No warnings were triggered by the current rules.")
        diagnostic_lines.extend([
            "",
            "Permutation importance measures predictive usefulness. It does not imply causality."
        ])
        sections.append("\n".join(diagnostic_lines))

    mae = evaluation_summary["mae"]
    rmse = evaluation_summary["rmse"]
    r2 = evaluation_summary["r2"]

    if 0 <= r2 <= 1:
        r2_text = (
            f"The model explains approximately {r2 * 100:.1f}% of the observed "
            f"variation in {target_name}. The remaining {(1 - r2) * 100:.1f}% "
            "depends on information unavailable to the model or variation that "
            "is difficult to predict."
        )
    else:
        r2_text = (
            "R² is negative: on this test set, the model performs worse than a "
            "prediction based on the mean value."
        )

    if rmse > mae * 1.25:
        rmse_text = (
            f"RMSE ({rmse:.4f}) is higher than MAE, suggesting that some large "
            "errors deserve specific review."
        )
    else:
        rmse_text = (
            f"RMSE ({rmse:.4f}) remains relatively close to MAE, suggesting "
            "that large errors do not dominate the result."
        )

    tolerance_text = (
        f"First define what error is acceptable. If a difference of {mae:.4f} "
        f"units in {target_name} can change an important decision, the model "
        "should not make that decision on its own."
    )
    if user_context:
        acceptable_error = user_context.get("acceptable_error")
        if acceptable_error is not None and acceptable_error > 0:
            if mae <= acceptable_error:
                tolerance_text = (
                    f"MAE ({mae:.4f}) is within the declared tolerable error "
                    f"({acceptable_error:.4f}). Even so, review extreme errors "
                    "and subgroups before using the model."
                )
            else:
                tolerance_text = (
                    f"MAE ({mae:.4f}) exceeds the declared tolerable error "
                    f"({acceptable_error:.4f}). Improve the model or limit its "
                    "use before it supports this decision."
                )

    interpretation_lines = [
        "PLAIN-LANGUAGE INTERPRETATION",
        "",
        f"The selected model was {model_label(best_model, 'en')}.",
        "",
        "What do the results mean?",
        (
            f"- On average, predictions differ from the actual {target_name} "
            f"by {mae:.4f} units. This is the practical meaning of MAE."
        ),
        f"- {rmse_text}",
        f"- {r2_text}",
        "",
        "How should this information support decisions?",
        f"- {tolerance_text}",
        (
            "- Use the model to help rank, prioritize or review cases. A person "
            "should confirm high-impact decisions."
        ),
        (
            "- Review errors across relevant groups and verify that no group "
            "systematically receives worse predictions."
        ),
        (
            "- Validate performance with new data from another time or context. "
            "Update the data or model if performance declines."
        ),
        "",
        "IMPORTANT LIMITATIONS",
        "- Average metrics can hide extreme cases or subgroup differences.",
        (
            "- This is an internal test split and does not guarantee the same "
            "performance in another population, laboratory, region or period."
        ),
        "- Predictive patterns do not establish causality.",
        (
            "- Global feature importance does not explain each individual "
            "prediction or establish causality."
        )
    ]
    sections.append("\n".join(interpretation_lines))

    return ("\n\n" + "=" * 50 + "\n\n").join(sections)


def build_full_report(
    dataset_profile,
    quality_report,
    model_comparison,
    evaluation_summary,
    target_column=None,
    diagnostics_summary=None,
    user_context=None,
    language="es"
):
    """
    Genera un reporte completo con los principales resultados
    del análisis de datos y modelado.

    Parameters
    ----------
    dataset_profile : dict
        Perfil general del dataset.

    quality_report : dict
        Resumen de calidad de datos.

    model_comparison : dict
        Resultados de comparación de modelos.

    evaluation_summary : dict
        Resumen de evaluación del modelo final.

    target_column : str, optional
        Nombre de la variable objetivo.

    diagnostics_summary : dict, optional
        Resumen de diagnóstico, importancia y advertencias.

    user_context : dict, optional
        Objetivo y criterios de decisión proporcionados por la persona.

    Returns
    -------
    str
        Reporte completo del análisis.
    """

    if language == "en":
        return build_full_report_english(
            dataset_profile,
            quality_report,
            model_comparison,
            evaluation_summary,
            target_column=target_column,
            diagnostics_summary=diagnostics_summary,
            user_context=user_context
        )

    sections = [
        build_dataset_profile_section(dataset_profile),
        build_data_quality_section(quality_report),
    ]

    if user_context:
        sections.append(build_user_context_section(user_context))

    sections.extend([
        build_model_comparison_section(model_comparison),
        build_evaluation_section(evaluation_summary)
    ])

    if diagnostics_summary:
        sections.append(build_diagnostics_section(diagnostics_summary))

    sections.append(
        build_interpretation_section(
            evaluation_summary,
            model_comparison=model_comparison,
            target_column=target_column,
            user_context=user_context
        )
    )

    report = ("\n\n" + "=" * 50 + "\n\n").join(sections)

    return report

from src.i18n import model_label, translate

