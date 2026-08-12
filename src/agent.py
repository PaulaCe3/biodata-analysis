from pprint import pformat

def build_analysis_context(
    dataset_profile=None,
    quality_report=None,
    model_comparison=None,
    evaluation=None
):
    """
    Reúne los resultados calculados por los módulos de BioIA
    en una estructura común para su posterior interpretación.

    Parameters
    ----------
    dataset_profile : dict, optional
        Información general del dataset.

    quality_report : dict, optional
        Resultados del análisis de calidad de datos.

    model_comparison : dict, optional
        Resultados de comparación entre modelos.

    evaluation : dict, optional
        Resultados de evaluación del modelo final.

    Returns
    -------
    dict
        Contexto estructurado del análisis.
    """

    context = {}

    if dataset_profile is not None:
        context["dataset_profile"] = dataset_profile

    if quality_report is not None:
        context["quality_report"] = quality_report

    if model_comparison is not None:
        context["model_comparison"] = model_comparison

    if evaluation is not None:
        context["evaluation"] = evaluation

    return context

def build_interpretation_prompt(context):
    """
    Construye las instrucciones que utilizará BioIA para interpretar
    los resultados de un análisis de datos.

    Parameters
    ----------
    context : dict
        Resultados calculados previamente por los módulos de BioIA.

    Returns
    -------
    str
        Prompt estructurado para la interpretación del análisis.
    """

    formatted_context = pformat(
        context,
        sort_dicts=False
    )

    prompt = f"""
Sos BioIA, un asistente especializado en análisis de datos biológicos.

Tu tarea es interpretar los resultados calculados por los módulos
de Data Science del sistema.

Reglas importantes:

- Utilizá únicamente la información presente en el contexto.
- No inventes métricas, valores ni resultados.
- Si falta información, indicá que no está disponible.
- No confundas correlación con causalidad.
- Explicá los resultados de forma clara y comprensible.
- Señalá posibles problemas de calidad de datos cuando existan.
- Al interpretar modelos, explicá sus métricas sin exagerar
  la capacidad predictiva.

CONTEXTO DEL ANÁLISIS:

{formatted_context}
"""

    return prompt

