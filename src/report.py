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


def build_full_report(
    dataset_profile,
    quality_report,
    model_comparison,
    evaluation_summary,
    target_column=None,
    diagnostics_summary=None,
    user_context=None
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

