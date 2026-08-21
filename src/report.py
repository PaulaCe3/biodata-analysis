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
    duplicate_rows = quality_report["duplicate_rows"]

    total_missing = sum(missing_values.values())

    lines = [
        "CALIDAD DE DATOS",
        "",
        f"Valores faltantes totales: {total_missing}",
        f"Filas duplicadas: {duplicate_rows}",
        "",
        "Valores faltantes por variable:"
    ]

    for column, count in missing_values.items():
        lines.append(
            f"- {column}: {count}"
        )

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

def build_full_report(
    dataset_profile,
    quality_report,
    model_comparison,
    evaluation_summary
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

    Returns
    -------
    str
        Reporte completo del análisis.
    """

    sections = [
        build_dataset_profile_section(dataset_profile),
        build_data_quality_section(quality_report),
        build_model_comparison_section(model_comparison),
        build_evaluation_section(evaluation_summary)
    ]

    report = "\n\n" + ("\n\n" + "=" * 50 + "\n\n").join(sections)

    return report

