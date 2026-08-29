from html import escape
from importlib import reload
from inspect import signature
from pathlib import Path

import streamlit as st

# Se configura y reemplaza el indicador de carga antes de importar las
# librerías de análisis, que son la parte más costosa del arranque.
st.set_page_config(
    page_title="Biodata",
    layout="wide",
    initial_sidebar_state="expanded"
)

_startup_loader = st.empty()

_startup_loader.markdown(
    """
    <style>
    @keyframes biodata-early-nature-loader {
        0%, 38% {
            opacity: 1;
            transform: scale(1) rotate(0deg);
        }
        50%, 88% {
            opacity: 0;
            transform: scale(0.78) rotate(-6deg);
        }
        100% {
            opacity: 1;
            transform: scale(1) rotate(0deg);
        }
    }
    [data-testid="stStatusWidgetRunningIcon"] {
        color: transparent !important;
        display: grid !important;
        font-size: 0 !important;
        height: 1.7rem;
        place-items: center;
        position: relative;
        width: 1.7rem;
    }
    [data-testid="stStatusWidgetRunningIcon"] > * {
        display: none !important;
        visibility: hidden !important;
    }
    [data-testid="stStatusWidgetRunningManIcon"],
    [data-testid="stStatusWidgetNewYearsIcon"] {
        display: none !important;
        visibility: hidden !important;
    }
    [data-testid="stStatusWidgetRunningIcon"]::before,
    [data-testid="stStatusWidgetRunningIcon"]::after {
        animation: biodata-early-nature-loader 2.4s ease-in-out infinite;
        background-position: center;
        background-repeat: no-repeat;
        background-size: contain;
        content: "";
        height: 1.6rem;
        pointer-events: none;
        position: absolute;
        visibility: visible !important;
        width: 1.6rem;
    }
    [data-testid="stStatusWidgetRunningIcon"]::before {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%233ddc84' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 4C12 4 6 8 6 14c0 3 2 5 5 5 6 0 9-7 9-15Z'/%3E%3Cpath d='M4 20c3-5 7-9 12-11'/%3E%3C/svg%3E");
    }
    [data-testid="stStatusWidgetRunningIcon"]::after {
        animation-delay: -1.2s;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%233ddc84' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cellipse cx='7' cy='8' rx='2' ry='2.7'/%3E%3Cellipse cx='17' cy='8' rx='2' ry='2.7'/%3E%3Cellipse cx='11' cy='5.5' rx='2' ry='2.7'/%3E%3Cellipse cx='14.5' cy='5.8' rx='2' ry='2.7'/%3E%3Cpath d='M6.5 16.2c0-3.1 2.5-5.4 5.5-5.4s5.5 2.3 5.5 5.4c0 2-1.5 3.3-3.3 3.3-.9 0-1.5-.5-2.2-.5s-1.3.5-2.2.5c-1.8 0-3.3-1.3-3.3-3.3Z'/%3E%3C/svg%3E");
    }
    @media (prefers-reduced-motion: reduce) {
        [data-testid="stStatusWidgetRunningIcon"]::before {
            animation: none !important;
            opacity: 1 !important;
            transform: none !important;
        }
        [data-testid="stStatusWidgetRunningIcon"]::after {
            animation: none !important;
            opacity: 0 !important;
        }
    }
    .biodata-startup-loader {
        align-items: center;
        background:
            radial-gradient(circle at 50% 42%, rgba(61, 220, 132, 0.09), transparent 18rem),
            #0b1015;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        inset: 0;
        justify-content: center;
        position: fixed;
        z-index: 2147483647;
    }
    .biodata-startup-loader-visual {
        align-items: center;
        background: rgba(61, 220, 132, 0.06);
        border: 1px solid rgba(101, 230, 160, 0.22);
        border-radius: 20px;
        box-shadow: 0 18px 55px rgba(0, 0, 0, 0.28);
        display: flex;
        height: 72px;
        justify-content: center;
        position: relative;
        width: 72px;
    }
    .biodata-startup-loader-icon {
        animation: biodata-early-nature-loader 2.4s ease-in-out infinite;
        color: #3ddc84;
        height: 34px;
        position: absolute;
        width: 34px;
    }
    .biodata-startup-loader-icon.animal {
        animation-delay: -1.2s;
    }
    .biodata-startup-loader strong {
        color: #f5f8f6;
        font-family: "Inter", "Segoe UI", sans-serif;
        font-size: 1rem;
        font-weight: 650;
        letter-spacing: -0.01em;
    }
    .biodata-startup-loader small {
        color: rgba(231, 239, 235, 0.6);
        font-family: "Inter", "Segoe UI", sans-serif;
        font-size: 0.78rem;
    }
    @media (prefers-reduced-motion: reduce) {
        .biodata-startup-loader-icon {
            animation: none !important;
        }
        .biodata-startup-loader-icon.animal {
            display: none;
        }
    }
    </style>
    <div class="biodata-startup-loader" role="status" aria-live="polite">
        <div class="biodata-startup-loader-visual" aria-hidden="true">
            <svg class="biodata-startup-loader-icon plant" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="1.7"
                stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 4C12 4 6 8 6 14c0 3 2 5 5 5 6 0 9-7 9-15Z" />
                <path d="M4 20c3-5 7-9 12-11" />
            </svg>
            <svg class="biodata-startup-loader-icon animal" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="1.7"
                stroke-linecap="round" stroke-linejoin="round">
                <ellipse cx="7" cy="8" rx="2" ry="2.7" />
                <ellipse cx="17" cy="8" rx="2" ry="2.7" />
                <ellipse cx="11" cy="5.5" rx="2" ry="2.7" />
                <ellipse cx="14.5" cy="5.8" rx="2" ry="2.7" />
                <path d="M6.5 16.2c0-3.1 2.5-5.4 5.5-5.4s5.5 2.3 5.5 5.4c0 2-1.5 3.3-3.3 3.3-.9 0-1.5-.5-2.2-.5s-1.3.5-2.2.5c-1.8 0-3.3-1.3-3.3-3.3Z" />
            </svg>
        </div>
        <strong>Biodata</strong>
        <small>Análisis de datos · Data analysis</small>
    </div>
    """,
    unsafe_allow_html=True
)

from src.data_loader import load_dataset, validate_column_names
from src.data_profiler import get_dataset_fingerprint, get_dataset_profile
from src.data_quality import get_quality_report

import src.eda as eda_module

# Streamlit puede conservar módulos importados entre dos despliegues consecutivos.
# Si app.py ya espera la interfaz bilingüe pero el proceso mantiene una versión
# anterior, se recarga el módulo antes de enlazar sus funciones.
if "language" not in signature(eda_module.plot_numeric_distribution).parameters:
    reload(eda_module)

from src.eda import (
    get_numeric_summary,
    get_categorical_summary,
    plot_numeric_distribution,
    plot_categorical_distribution,
    plot_correlation_heatmap
)

from src.preprocessing import (
    detect_feature_types,
    build_preprocessor,
    get_valid_regression_targets,
    prepare_regression_dataset,
    split_train_test
)
from src.modeling import (
    compare_regression_models,
    select_best_regression_model,
    train_regression_model
)
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)
from src.evaluation import (
    evaluate_regression_model,
    summarize_regression_evaluation
)

import src.diagnostics as diagnostics_module

if "language" not in signature(diagnostics_module.build_diagnostic_warnings).parameters:
    reload(diagnostics_module)

from src.diagnostics import (
    build_diagnostic_warnings,
    build_prediction_table,
    calculate_permutation_feature_importance,
    calculate_subgroup_errors,
    get_largest_errors,
    plot_actual_vs_predicted,
    plot_feature_importance,
    plot_residual_distribution,
    plot_residuals,
    summarize_diagnostics
)

import src.report as report_module

if "language" not in signature(report_module.build_full_report).parameters:
    reload(report_module)

from src.report import build_full_report
from src.i18n import model_label, translate
from src.plot_style import apply_figure_theme


def current_language():
    """Devuelve el idioma activo de la interfaz."""

    return st.session_state.get("biodata_language", "es")


def tr(text, **values):
    """Atajo para localizar textos visibles de la aplicación."""

    return translate(text, current_language(), **values)


def localize_generated_table(table):
    """Traduce solo columnas generadas por Biodata, no las del dataset."""

    if current_language() != "en":
        return table

    return table.rename(
        columns={
            "fila_original": "original_row",
            "valor_real": "actual_value",
            "prediccion": "prediction",
            "residuo": "residual",
            "error_absoluto": "absolute_error",
            "variable": "variable",
            "importancia": "importance",
            "desviacion": "std_deviation",
            "grupo": "group",
            "casos": "cases",
            "mae": "mae",
            "residuo_promedio": "mean_residual"
        }
    )


def effective_theme():
    """Resuelve el tema visual efectivo, incluido el modo automático."""

    selected_theme = st.session_state.get("biodata_theme", "system")
    if selected_theme != "system":
        return selected_theme

    context_theme = st.context.theme.get("type")
    return context_theme if context_theme in ("light", "dark") else "dark"


def themed_figure(figure):
    """Aplica el tema activo a una figura antes de mostrarla."""

    return apply_figure_theme(figure, effective_theme())


def format_variable_label(column_name, language_code=None):
    """Convierte nombres técnicos en etiquetas legibles sin alterar los datos."""

    original_name = str(column_name).strip()
    language_code = language_code or current_language()
    known_labels = {
        "es": {
            "sex": "Sexo",
            "length": "Longitud",
            "diameter": "Diámetro",
            "height": "Altura",
            "whole_weight": "Peso total",
            "shucked_weight": "Peso sin concha",
            "viscera_weight": "Peso de vísceras",
            "shell_weight": "Peso de la concha",
            "rings": "Anillos"
        },
        "en": {
            "sex": "Sex",
            "length": "Length",
            "diameter": "Diameter",
            "height": "Height",
            "whole_weight": "Total weight",
            "shucked_weight": "Shucked weight",
            "viscera_weight": "Viscera weight",
            "shell_weight": "Shell weight",
            "rings": "Rings"
        }
    }

    return known_labels[language_code].get(
        original_name.lower(),
        original_name.replace("_", " ").strip().capitalize()
    )


def format_spanish_number(value, decimals=2):
    """Formatea números según el idioma activo."""

    formatted = f"{value:.{decimals}f}"
    return formatted.replace(".", ",") if current_language() == "es" else formatted


def render_preferences():
    """Muestra preferencias globales y conserva su estado en la sesión."""

    st.session_state.setdefault("biodata_language", "es")
    st.session_state.setdefault("biodata_theme", "system")

    with st.sidebar.expander(tr("Preferencias"), expanded=False):
        st.caption(
            tr(
                "Personalizá Biodata sin perder el archivo ni los resultados de la sesión."
            )
        )

        st.segmented_control(
            "Idioma / Language",
            options=["es", "en"],
            format_func=lambda value: "Español" if value == "es" else "English",
            key="biodata_language"
        )

        theme_labels = {
            "system": tr("Automático"),
            "dark": tr("Oscuro"),
            "light": tr("Claro")
        }

        st.segmented_control(
            tr("Apariencia"),
            options=["system", "dark", "light"],
            format_func=lambda value: theme_labels[value],
            key="biodata_theme"
        )

        if st.session_state["biodata_theme"] == "system":
            st.caption(tr("Sigue la configuración visual de tu dispositivo."))

    return (
        st.session_state["biodata_language"],
        st.session_state["biodata_theme"]
    )


def render_global_styles():
    """Aplica el sistema visual principal de Biodata."""

    st.markdown(
        """
        <style>
        :root {
            --biodata-bg: #0b1015;
            --biodata-surface: #111820;
            --biodata-surface-raised: #151e27;
            --biodata-border: rgba(236, 245, 240, 0.11);
            --biodata-border-strong: rgba(101, 230, 160, 0.28);
            --biodata-green: #3ddc84;
            --biodata-green-soft: #76e9aa;
            --biodata-text: #f5f8f6;
            --biodata-muted: rgba(231, 239, 235, 0.66);
            --biodata-shadow: 0 22px 60px rgba(0, 0, 0, 0.28);
        }
        html {
            scroll-behavior: smooth;
        }
        ::selection {
            background: rgba(61, 220, 132, 0.28);
            color: #ffffff;
        }
        @keyframes biodata-fade-up {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        @keyframes biodata-nature-loader {
            0%, 38% {
                opacity: 1;
                transform: scale(1) rotate(0deg);
            }
            50%, 88% {
                opacity: 0;
                transform: scale(0.78) rotate(-6deg);
            }
            100% {
                opacity: 1;
                transform: scale(1) rotate(0deg);
            }
        }
        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(
                    circle at 86% -8%,
                    rgba(61, 220, 132, 0.10),
                    transparent 32rem
                ),
                radial-gradient(
                    circle at 22% 92%,
                    rgba(38, 113, 83, 0.08),
                    transparent 30rem
                ),
                linear-gradient(180deg, #0b1015 0%, #0d1218 100%);
        }
        [data-testid="stHeader"] {
            backdrop-filter: blur(18px);
            background: rgba(11, 16, 21, 0.72);
            border-bottom: 1px solid rgba(236, 245, 240, 0.055);
        }
        [data-testid="stAppDeployButton"] {
            display: none;
        }
        [data-testid="stStatusWidgetRunningIcon"] {
            color: transparent !important;
            display: grid !important;
            font-size: 0 !important;
            height: 1.7rem;
            place-items: center;
            position: relative;
            width: 1.7rem;
        }
        [data-testid="stStatusWidgetRunningIcon"] > * {
            visibility: hidden !important;
        }
        [data-testid="stStatusWidgetRunningManIcon"],
        [data-testid="stStatusWidgetNewYearsIcon"] {
            display: none !important;
        }
        [data-testid="stStatusWidgetRunningIcon"]::before,
        [data-testid="stStatusWidgetRunningIcon"]::after {
            animation: biodata-nature-loader 2.4s ease-in-out infinite;
            background-position: center;
            background-repeat: no-repeat;
            background-size: contain;
            content: "";
            height: 1.6rem;
            pointer-events: none;
            position: absolute;
            visibility: visible !important;
            width: 1.6rem;
        }
        [data-testid="stStatusWidgetRunningIcon"]::before {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%233ddc84' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 4C12 4 6 8 6 14c0 3 2 5 5 5 6 0 9-7 9-15Z'/%3E%3Cpath d='M4 20c3-5 7-9 12-11'/%3E%3C/svg%3E");
        }
        [data-testid="stStatusWidgetRunningIcon"]::after {
            animation-delay: -1.2s;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%233ddc84' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cellipse cx='7' cy='8' rx='2' ry='2.7'/%3E%3Cellipse cx='17' cy='8' rx='2' ry='2.7'/%3E%3Cellipse cx='11' cy='5.5' rx='2' ry='2.7'/%3E%3Cellipse cx='14.5' cy='5.8' rx='2' ry='2.7'/%3E%3Cpath d='M6.5 16.2c0-3.1 2.5-5.4 5.5-5.4s5.5 2.3 5.5 5.4c0 2-1.5 3.3-3.3 3.3-.9 0-1.5-.5-2.2-.5s-1.3.5-2.2.5c-1.8 0-3.3-1.3-3.3-3.3Z'/%3E%3C/svg%3E");
        }
        [data-testid="stSidebar"] {
            background:
                radial-gradient(
                    circle at 10% 4%,
                    rgba(61, 220, 132, 0.075),
                    transparent 15rem
                ),
                linear-gradient(180deg, #111820 0%, #0e141a 100%);
            border-right: 1px solid var(--biodata-border);
            box-shadow: 18px 0 48px rgba(0, 0, 0, 0.16);
        }
        .biodata-sidebar-kicker {
            color: var(--biodata-green-soft);
            font-size: 0.72rem;
            font-weight: 750;
            letter-spacing: 0.11em;
            margin-bottom: 0.3rem;
            text-transform: uppercase;
        }
        [data-testid="stSidebar"] h3 {
            color: var(--biodata-text);
            letter-spacing: -0.025em;
        }
        [data-testid="stSidebar"] hr {
            border-color: rgba(236, 245, 240, 0.08);
            margin: 1.6rem 0;
        }
        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
            background:
                linear-gradient(
                    145deg,
                    rgba(255, 255, 255, 0.045),
                    rgba(255, 255, 255, 0.018)
                );
            border: 1px dashed rgba(101, 230, 160, 0.44);
            border-radius: 14px;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.035);
            padding: 0.95rem 0.75rem;
            transition:
                background-color 180ms ease,
                border-color 180ms ease,
                box-shadow 180ms ease,
                transform 180ms ease;
        }
        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"]:hover {
            background: rgba(61, 220, 132, 0.055);
            border-color: rgba(101, 230, 160, 0.78);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.18);
            transform: translateY(-1px);
        }
        [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {
            background: rgba(61, 220, 132, 0.12);
            border-color: rgba(101, 230, 160, 0.36);
            min-height: 2.75rem;
        }
        .block-container {
            max-width: 1180px;
            padding-bottom: 5rem;
            /* Mantiene la identidad visual debajo de la barra superior fija. */
            padding-top: 3.65rem;
        }
        .biodata-brand {
            align-items: center;
            animation: biodata-fade-up 360ms ease-out both;
            display: flex;
            gap: 0.9rem;
            margin-bottom: 2rem;
            min-height: 48px;
        }
        .biodata-brand-mark {
            align-items: center;
            background:
                radial-gradient(
                    circle at 30% 24%,
                    rgba(118, 233, 170, 0.22),
                    transparent 58%
                ),
                rgba(61, 220, 132, 0.07);
            border: 1px solid rgba(101, 230, 160, 0.35);
            border-radius: 14px;
            box-shadow:
                inset 0 1px 0 rgba(255, 255, 255, 0.07),
                0 10px 26px rgba(0, 0, 0, 0.18);
            display: flex;
            height: 44px;
            justify-content: center;
            width: 44px;
        }
        .biodata-brand-mark svg {
            color: var(--biodata-green-soft);
            height: 1.45rem;
            width: 1.45rem;
        }
        .biodata-brand h1 {
            color: var(--biodata-text);
            font-size: 1.62rem;
            letter-spacing: -0.045em;
            line-height: 1.05;
            margin: 0;
            padding: 0;
        }
        .biodata-brand p {
            color: rgba(250, 250, 250, 0.62);
            font-size: 0.9rem;
            line-height: 1.4;
            margin: 0.3rem 0 0;
        }
        .biodata-brand-badge {
            align-items: center;
            background: rgba(255, 255, 255, 0.025);
            border: 1px solid rgba(236, 245, 240, 0.09);
            border-radius: 999px;
            color: rgba(231, 239, 235, 0.68);
            display: flex;
            font-size: 0.76rem;
            gap: 0.5rem;
            margin-left: auto;
            padding: 0.45rem 0.75rem;
            white-space: nowrap;
        }
        .biodata-brand-badge span {
            background: var(--biodata-green);
            border-radius: 50%;
            box-shadow: 0 0 0 4px rgba(61, 220, 132, 0.10);
            height: 6px;
            width: 6px;
        }
        .biodata-hero {
            animation: biodata-fade-up 480ms 50ms ease-out both;
            background:
                linear-gradient(
                    135deg,
                    rgba(22, 31, 40, 0.98),
                    rgba(15, 23, 30, 0.96)
                );
            border: 1px solid var(--biodata-border);
            border-radius: 20px;
            box-shadow: var(--biodata-shadow);
            display: grid;
            gap: clamp(1.5rem, 4vw, 3.3rem);
            grid-template-columns: minmax(0, 1.35fr) minmax(250px, 0.65fr);
            overflow: hidden;
            padding: clamp(1.7rem, 4vw, 3.2rem);
            position: relative;
            transition:
                border-color 220ms ease,
                box-shadow 220ms ease,
                transform 220ms ease;
        }
        .biodata-hero::before {
            background: radial-gradient(
                circle,
                rgba(61, 220, 132, 0.14),
                transparent 68%
            );
            content: "";
            height: 20rem;
            pointer-events: none;
            position: absolute;
            right: -7rem;
            top: -10rem;
            width: 20rem;
        }
        .biodata-hero > * {
            position: relative;
            z-index: 1;
        }
        .biodata-kicker {
            color: var(--biodata-green-soft);
            font-size: 0.76rem;
            font-weight: 750;
            letter-spacing: 0.10em;
            text-transform: uppercase;
        }
        .biodata-hero h2 {
            color: var(--biodata-text);
            font-size: clamp(2.1rem, 5vw, 3.65rem);
            letter-spacing: -0.055em;
            line-height: 1.02;
            margin: 1.2rem 0 1.1rem;
            max-width: 760px;
            text-wrap: balance;
        }
        .biodata-hero-copy > p {
            color: rgba(231, 239, 235, 0.74);
            font-size: clamp(1rem, 2vw, 1.15rem);
            line-height: 1.7;
            margin: 0;
            max-width: 680px;
        }
        .biodata-hero-capabilities {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-top: 1.5rem;
        }
        .biodata-hero-capabilities span {
            background: rgba(255, 255, 255, 0.028);
            border: 1px solid rgba(236, 245, 240, 0.10);
            border-radius: 999px;
            color: rgba(240, 246, 243, 0.80);
            font-size: 0.78rem;
            padding: 0.46rem 0.7rem;
        }
        .biodata-hero-trust {
            align-self: stretch;
            background: rgba(7, 13, 17, 0.34);
            border: 1px solid rgba(236, 245, 240, 0.085);
            border-radius: 16px;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.035);
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 1.1rem;
        }
        .biodata-trust-label {
            color: rgba(231, 239, 235, 0.72);
            font-size: 0.74rem;
            font-weight: 750;
            letter-spacing: 0.09em;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
        }
        .biodata-trust-item {
            align-items: flex-start;
            border-bottom: 1px solid rgba(236, 245, 240, 0.07);
            display: grid;
            gap: 0.7rem;
            grid-template-columns: 1.75rem 1fr;
            padding: 0.8rem 0;
        }
        .biodata-trust-item:last-child {
            border-bottom: none;
            padding-bottom: 0;
        }
        .biodata-trust-item > span {
            color: var(--biodata-green-soft);
            font-size: 0.72rem;
            font-weight: 750;
            padding-top: 0.12rem;
        }
        .biodata-trust-item strong,
        .biodata-trust-item small {
            display: block;
        }
        .biodata-trust-item strong {
            color: rgba(245, 248, 246, 0.92);
            font-size: 0.86rem;
            line-height: 1.35;
        }
        .biodata-trust-item small {
            color: rgba(231, 239, 235, 0.70);
            font-size: 0.78rem;
            line-height: 1.45;
            margin-top: 0.18rem;
        }
        .biodata-journey-heading {
            align-items: center;
            background: rgba(255, 255, 255, 0.015);
            border: 1px solid rgba(236, 245, 240, 0.08);
            border-radius: 15px;
            display: grid;
            gap: 1.4rem;
            grid-template-columns: minmax(0, 1.15fr) minmax(260px, 0.85fr);
            margin: 1.35rem 0 0.85rem;
            padding: 1.2rem 1.3rem;
        }
        .biodata-journey-heading h3 {
            color: var(--biodata-text);
            font-size: clamp(1.3rem, 2.5vw, 1.75rem);
            letter-spacing: -0.035em;
            line-height: 1.16;
            margin: 0;
        }
        .biodata-journey-heading p {
            color: var(--biodata-muted);
            font-size: 0.88rem;
            line-height: 1.6;
            margin: 0;
        }
        .biodata-steps {
            display: grid;
            gap: 0.85rem;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            margin: 1rem 0;
        }
        .biodata-step {
            animation: biodata-fade-up 420ms ease-out both;
            background: rgba(255, 255, 255, 0.018);
            border: 1px solid rgba(236, 245, 240, 0.085);
            border-radius: 15px;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.025);
            min-height: 192px;
            padding: 1.15rem;
            transition:
                background-color 180ms ease,
                border-color 180ms ease,
                box-shadow 180ms ease,
                transform 180ms ease;
        }
        .biodata-step:nth-child(1) {
            animation-delay: 100ms;
        }
        .biodata-step:nth-child(2) {
            animation-delay: 150ms;
            background:
                linear-gradient(
                    145deg,
                    rgba(61, 220, 132, 0.075),
                    rgba(255, 255, 255, 0.018)
                );
            border-color: rgba(101, 230, 160, 0.24);
        }
        .biodata-step:nth-child(3) {
            animation-delay: 200ms;
        }
        .biodata-step:hover {
            background: rgba(61, 220, 132, 0.035);
            border-color: rgba(101, 230, 160, 0.30);
            box-shadow: 0 14px 34px rgba(0, 0, 0, 0.18);
            transform: translateY(-3px);
        }
        .biodata-step-number {
            align-items: center;
            background: rgba(61, 220, 132, 0.085);
            border: 1px solid rgba(101, 230, 160, 0.22);
            border-radius: 10px;
            color: var(--biodata-green-soft);
            display: inline-flex;
            font-size: 0.76rem;
            font-weight: 750;
            height: 2rem;
            justify-content: center;
            width: 2rem;
        }
        .biodata-step-top {
            align-items: center;
            display: flex;
            justify-content: space-between;
        }
        .biodata-step-icon {
            align-items: center;
            background: rgba(61, 220, 132, 0.06);
            border: 1px solid rgba(101, 230, 160, 0.18);
            border-radius: 10px;
            color: rgba(118, 233, 170, 0.62);
            display: flex;
            height: 2.3rem;
            justify-content: center;
            width: 2.3rem;
        }
        .biodata-step-icon svg {
            height: 1.2rem;
            width: 1.2rem;
        }
        .biodata-step-tag {
            background: rgba(61, 220, 132, 0.065);
            border: 1px solid rgba(101, 230, 160, 0.14);
            border-radius: 999px;
            color: rgba(168, 241, 199, 0.88);
            display: inline-flex;
            font-size: 0.75rem;
            font-weight: 650;
            letter-spacing: 0;
            margin-top: 1rem;
            padding: 0.3rem 0.55rem;
            text-transform: none;
        }
        .biodata-step h3 {
            color: var(--biodata-text);
            font-size: 1.05rem;
            letter-spacing: -0.02em;
            margin: 0.45rem 0 0.55rem;
        }
        .biodata-step p {
            color: rgba(250, 250, 250, 0.66);
            font-size: 0.9rem;
            line-height: 1.58;
            margin: 0;
        }
        .biodata-start-note {
            align-items: center;
            background: rgba(61, 220, 132, 0.045);
            border: 1px solid rgba(101, 230, 160, 0.16);
            border-radius: 13px;
            color: rgba(240, 246, 243, 0.86);
            display: flex;
            font-size: 0.9rem;
            gap: 0.75rem;
            line-height: 1.5;
            padding: 0.85rem 1rem;
        }
        .biodata-start-note > span {
            background: var(--biodata-green);
            border-radius: 50%;
            box-shadow: 0 0 0 5px rgba(61, 220, 132, 0.09);
            flex: 0 0 auto;
            height: 7px;
            width: 7px;
        }
        .biodata-model-flow {
            animation: biodata-fade-up 360ms ease-out both;
            border-bottom: 1px solid rgba(250, 250, 250, 0.10);
            border-top: 1px solid rgba(250, 250, 250, 0.10);
            display: grid;
            gap: 0.5rem;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            margin: 1rem 0 1.8rem;
            padding: 0.8rem 0;
        }
        .biodata-model-flow-item {
            align-items: center;
            color: rgba(250, 250, 250, 0.72);
            display: flex;
            font-size: 0.86rem;
            gap: 0.55rem;
            transition: color 160ms ease;
        }
        .biodata-model-flow-item:hover {
            color: rgba(250, 250, 250, 0.96);
        }
        .biodata-model-flow-item span {
            align-items: center;
            border: 1px solid rgba(61, 220, 132, 0.45);
            border-radius: 50%;
            color: #65e6a0;
            display: inline-flex;
            font-size: 0.75rem;
            height: 1.6rem;
            justify-content: center;
            transition: background-color 160ms ease, border-color 160ms ease;
            width: 1.6rem;
        }
        .biodata-model-flow-item:hover span {
            background: rgba(61, 220, 132, 0.10);
            border-color: rgba(61, 220, 132, 0.78);
        }
        .biodata-result-overview {
            display: grid;
            gap: 0.8rem;
            grid-template-columns: 1.5fr 1fr 1fr;
            margin: 0.9rem 0 1rem;
        }
        .biodata-result-overview-card {
            background: rgba(255, 255, 255, 0.025);
            border: 1px solid rgba(250, 250, 250, 0.10);
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            min-height: 126px;
            padding: 1rem;
            transition:
                background-color 180ms ease,
                border-color 180ms ease,
                transform 180ms ease;
        }
        .biodata-result-overview-card:hover {
            background: rgba(61, 220, 132, 0.035);
            border-color: rgba(61, 220, 132, 0.34);
            transform: translateY(-2px);
        }
        .biodata-summary-card,
        .biodata-reading-card {
            animation: biodata-fade-up 420ms ease-out both;
            transition:
                background-color 180ms ease,
                border-color 180ms ease,
                transform 180ms ease;
        }
        .biodata-summary-card:hover,
        .biodata-reading-card:hover {
            background: rgba(61, 220, 132, 0.032);
            border-color: rgba(61, 220, 132, 0.30);
            transform: translateY(-2px);
        }
        .biodata-result-overview-card span,
        .biodata-test-metric span {
            color: rgba(250, 250, 250, 0.58);
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.045em;
            text-transform: uppercase;
        }
        .biodata-result-overview-card strong {
            color: #ffffff;
            font-size: 1.35rem;
            line-height: 1.2;
            margin: 0.6rem 0 0.4rem;
            overflow-wrap: anywhere;
        }
        .biodata-result-overview-card small,
        .biodata-test-metric small {
            color: rgba(250, 250, 250, 0.58);
            font-size: 0.79rem;
            line-height: 1.4;
        }
        .biodata-test-metrics {
            display: grid;
            gap: 0.7rem;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            margin: 0.8rem 0 0.7rem;
        }
        .biodata-test-metric {
            border-left: 2px solid rgba(61, 220, 132, 0.55);
            min-height: 104px;
            padding: 0.45rem 0.8rem;
            transition: background-color 180ms ease, border-color 180ms ease;
        }
        .biodata-test-metric:hover {
            background: rgba(61, 220, 132, 0.035);
            border-color: #3ddc84;
        }
        .biodata-test-metric strong {
            color: #ffffff;
            display: block;
            font-size: 1.55rem;
            line-height: 1.15;
            margin: 0.55rem 0 0.35rem;
            overflow-wrap: anywhere;
        }
        .stButton > button,
        .stDownloadButton > button {
            border-radius: 11px;
            font-weight: 650;
            min-height: 2.75rem;
            transition:
                border-color 160ms ease,
                box-shadow 160ms ease,
                transform 160ms ease;
        }
        .stButton > button[kind="primary"],
        .stDownloadButton > button[kind="primary"] {
            background: linear-gradient(135deg, #4be18e 0%, #2fc878 100%);
            border: 1px solid rgba(118, 233, 170, 0.62);
            box-shadow:
                inset 0 1px 0 rgba(255, 255, 255, 0.22),
                0 10px 24px rgba(36, 171, 100, 0.16);
            color: #07150d;
        }
        .stButton > button[kind="primary"]:hover,
        .stDownloadButton > button[kind="primary"]:hover {
            border-color: rgba(151, 245, 191, 0.92);
            box-shadow:
                inset 0 1px 0 rgba(255, 255, 255, 0.28),
                0 14px 32px rgba(36, 171, 100, 0.25);
        }
        .stButton > button:hover,
        .stDownloadButton > button:hover {
            box-shadow: 0 8px 22px rgba(61, 220, 132, 0.15);
            transform: translateY(-1px);
        }
        .stButton > button:active,
        .stDownloadButton > button:active {
            box-shadow: none;
            transform: translateY(0);
        }
        .stButton > button:focus-visible,
        .stDownloadButton > button:focus-visible,
        [data-baseweb="tab"]:focus-visible,
        [data-testid="stExpander"] summary:focus-visible,
        [data-testid="stFileUploaderDropzone"]:focus-within,
        [data-baseweb="select"]:focus-within,
        div[role="radiogroup"] [role="radio"]:focus-visible {
            outline: 2px solid #65e6a0;
            outline-offset: 2px;
        }
        [data-baseweb="tab-list"] {
            background: rgba(255, 255, 255, 0.022);
            border: 1px solid rgba(236, 245, 240, 0.085);
            border-radius: 13px;
            gap: 0.2rem;
            padding: 0.28rem;
            width: fit-content;
        }
        [data-baseweb="tab"] {
            border-radius: 9px;
            min-height: 2.75rem;
            padding-left: 1rem;
            padding-right: 1rem;
            transition: background-color 160ms ease, color 160ms ease;
        }
        [data-baseweb="tab"]:hover {
            background: rgba(61, 220, 132, 0.05);
        }
        [data-baseweb="tab"][aria-selected="true"] {
            background: rgba(61, 220, 132, 0.10);
            color: var(--biodata-text);
        }
        [data-baseweb="tab-highlight"] {
            background-color: var(--biodata-green) !important;
            border-radius: 999px;
            height: 2px;
        }
        [data-testid="stExpander"] {
            background: rgba(255, 255, 255, 0.014);
            border-color: rgba(236, 245, 240, 0.095);
            border-radius: 12px;
            overflow: hidden;
            transition:
                border-color 180ms ease,
                background-color 180ms ease,
                box-shadow 180ms ease;
        }
        [data-testid="stExpander"]:hover {
            background: rgba(61, 220, 132, 0.022);
            border-color: rgba(61, 220, 132, 0.24);
            box-shadow: 0 10px 28px rgba(0, 0, 0, 0.12);
        }
        [data-testid="stDialog"] [role="dialog"] {
            border: 1px solid rgba(101, 230, 160, 0.22);
            border-radius: 18px;
        }
        [data-testid="stDialog"] [data-testid="stMarkdownContainer"] {
            line-height: 1.65;
        }
        [data-testid="stDialog"] [data-testid="stMarkdownContainer"] h2 {
            border-top: 1px solid rgba(236, 245, 240, 0.09);
            margin-top: 2rem;
            padding-top: 1.25rem;
        }
        [data-testid="stDialog"] [data-testid="stMarkdownContainer"] table {
            font-size: 0.92rem;
        }
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(255, 255, 255, 0.012);
            border-radius: 14px;
            transition:
                background-color 180ms ease,
                border-color 180ms ease,
                box-shadow 180ms ease;
        }
        [data-testid="stVerticalBlockBorderWrapper"]:hover {
            background: rgba(255, 255, 255, 0.018);
            border-color: rgba(61, 220, 132, 0.20);
            box-shadow: 0 14px 36px rgba(0, 0, 0, 0.11);
        }
        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.018);
            border: 1px solid rgba(236, 245, 240, 0.08);
            border-radius: 13px;
            min-height: 112px;
            padding: 0.85rem 0.95rem;
            transition:
                background-color 180ms ease,
                border-color 180ms ease,
                box-shadow 180ms ease,
                transform 180ms ease;
        }
        [data-testid="stMetric"]:hover {
            background: rgba(61, 220, 132, 0.028);
            border-color: rgba(61, 220, 132, 0.25);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
            transform: translateY(-2px);
        }
        [data-testid="stDataFrame"] {
            border: 1px solid rgba(236, 245, 240, 0.09);
            border-radius: 13px;
            overflow: hidden;
        }
        [data-testid="stAlert"] {
            border-radius: 12px;
        }
        [data-baseweb="select"] > div,
        [data-testid="stNumberInputContainer"],
        [data-testid="stTextArea"] textarea {
            background-color: rgba(255, 255, 255, 0.025) !important;
            border-color: rgba(236, 245, 240, 0.11) !important;
            border-radius: 10px !important;
        }
        [data-baseweb="select"] > div:hover,
        [data-testid="stNumberInputContainer"]:hover,
        [data-testid="stTextArea"] textarea:hover {
            border-color: rgba(101, 230, 160, 0.34) !important;
        }
        @media (max-width: 1050px) {
            .biodata-hero {
                grid-template-columns: 1fr;
            }
            .biodata-hero-trust {
                display: grid;
                gap: 0 1rem;
                grid-template-columns: repeat(3, minmax(0, 1fr));
            }
            .biodata-trust-label {
                grid-column: 1 / -1;
            }
            .biodata-trust-item {
                border-bottom: none;
                border-right: 1px solid rgba(236, 245, 240, 0.07);
                padding: 0.75rem 0.75rem 0.3rem 0;
            }
            .biodata-trust-item:last-child {
                border-right: none;
            }
        }
        @media (max-width: 760px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
                padding-top: 4rem;
            }
            .biodata-brand {
                margin-bottom: 1.2rem;
            }
            .biodata-brand-badge {
                display: none;
            }
            .biodata-hero {
                border-radius: 16px;
                padding: 1.35rem;
            }
            .biodata-hero h2 {
                font-size: clamp(2rem, 11vw, 2.7rem);
            }
            .biodata-hero-trust {
                display: block;
            }
            .biodata-trust-item {
                border-bottom: 1px solid rgba(236, 245, 240, 0.07);
                border-right: none;
            }
            .biodata-steps {
                grid-template-columns: 1fr;
            }
            .biodata-journey-heading {
                align-items: start;
                grid-template-columns: 1fr;
                margin-top: 1.4rem;
            }
            .biodata-step {
                min-height: auto;
            }
            .biodata-model-flow,
            .biodata-test-metrics {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
            .biodata-result-overview {
                grid-template-columns: 1fr;
            }
            .biodata-result-overview-card {
                min-height: auto;
            }
            [data-baseweb="tab-list"] {
                width: 100%;
            }
            [data-baseweb="tab"] {
                flex: 1;
                justify-content: center;
                padding-left: 0.55rem;
                padding-right: 0.55rem;
            }
        }
        @media (prefers-reduced-motion: reduce) {
            [data-testid="stStatusWidgetRunningIcon"]::before {
                animation: none !important;
                opacity: 1 !important;
                transform: none !important;
            }
            [data-testid="stStatusWidgetRunningIcon"]::after {
                animation: none !important;
                opacity: 0 !important;
            }
            .biodata-brand,
            .biodata-hero,
            .biodata-step,
            .biodata-model-flow,
            .biodata-summary-card,
            .biodata-reading-card {
                animation: none !important;
                opacity: 1 !important;
                transform: none !important;
            }
            .biodata-hero,
            .biodata-step,
            .biodata-model-flow-item,
            .biodata-model-flow-item span,
            .biodata-result-overview-card,
            .biodata-summary-card,
            .biodata-reading-card,
            .biodata-test-metric,
            .stButton > button,
            .stDownloadButton > button,
            [data-baseweb="tab"],
            [data-testid="stExpander"],
            [data-testid="stVerticalBlockBorderWrapper"] {
                transition: none;
            }
            .biodata-step:hover,
            [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"]:hover,
            .biodata-result-overview-card:hover,
            .biodata-summary-card:hover,
            .biodata-reading-card:hover,
            .stButton > button:hover,
            .stDownloadButton > button:hover {
                transform: none;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_theme_overrides(theme_mode):
    """Aplica un tema claro fijo o adaptado al dispositivo."""

    light_rules = """
        :root {
            color-scheme: light;
            --background-color: #f4f7f5;
            --secondary-background-color: #eaf0ec;
            --text-color: #18221c;
            --primary-color: #168a4f;
            --biodata-bg: #f4f7f5;
            --biodata-surface: #ffffff;
            --biodata-surface-raised: #f8fbf9;
            --biodata-border: rgba(26, 51, 37, 0.13);
            --biodata-border-strong: rgba(22, 138, 79, 0.30);
            --biodata-green: #168a4f;
            --biodata-green-soft: #137645;
            --biodata-text: #162019;
            --biodata-muted: rgba(27, 45, 35, 0.68);
            --biodata-shadow: 0 22px 54px rgba(30, 64, 45, 0.11);
        }
        body,
        [data-testid="stAppViewContainer"] {
            color: #18221c;
        }
        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 86% -8%, rgba(22, 138, 79, 0.11), transparent 32rem),
                radial-gradient(circle at 18% 94%, rgba(73, 151, 105, 0.09), transparent 30rem),
                linear-gradient(180deg, #f7faf8 0%, #eef4f0 100%);
        }
        [data-testid="stHeader"] {
            background: rgba(247, 250, 248, 0.82);
            border-bottom-color: rgba(26, 51, 37, 0.08);
        }
        [data-testid="stSidebar"] {
            background:
                radial-gradient(circle at 10% 4%, rgba(22, 138, 79, 0.10), transparent 15rem),
                linear-gradient(180deg, #f7faf8 0%, #edf3ef 100%);
            border-right-color: rgba(26, 51, 37, 0.12);
            box-shadow: 18px 0 48px rgba(30, 64, 45, 0.08);
        }
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] small {
            color: #1b2b21;
        }
        details > summary,
        details > summary:hover {
            background: rgba(255, 255, 255, 0.76) !important;
            color: #1b2b21 !important;
        }
        details > summary p,
        details > summary span {
            color: #1b2b21 !important;
        }
        div[role="radiogroup"] {
            background: #e8efea !important;
            border-color: rgba(26, 51, 37, 0.14) !important;
        }
        div[role="radiogroup"] [role="radio"],
        div[role="radiogroup"] [role="radio"] p,
        div[role="radiogroup"] [role="radio"] span {
            background: #edf3ef !important;
            color: #244033 !important;
        }
        div[role="radiogroup"] [role="radio"][aria-checked="true"],
        div[role="radiogroup"] [role="radio"][aria-checked="true"] p,
        div[role="radiogroup"] [role="radio"][aria-checked="true"] span {
            background: rgba(22, 138, 79, 0.13) !important;
            color: #0f6638 !important;
        }
        .biodata-brand p,
        .biodata-hero-copy > p,
        .biodata-step p,
        .biodata-result-overview-card span,
        .biodata-result-overview-card small,
        .biodata-test-metric span,
        .biodata-test-metric small {
            color: rgba(27, 45, 35, 0.68);
        }
        .biodata-brand-badge,
        .biodata-hero-capabilities span {
            background: rgba(22, 138, 79, 0.045);
            border-color: rgba(26, 51, 37, 0.12);
            color: rgba(27, 45, 35, 0.78);
        }
        .biodata-hero {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(244, 249, 246, 0.97));
            border-color: rgba(26, 51, 37, 0.13);
        }
        .biodata-hero-trust,
        .biodata-journey-heading,
        .biodata-step,
        .biodata-result-overview-card,
        .biodata-summary-card,
        .biodata-reading-card,
        [data-testid="stVerticalBlockBorderWrapper"],
        [data-testid="stMetric"],
        [data-testid="stExpander"],
        [data-testid="stDialog"] [role="dialog"] {
            background: #ffffff !important;
            border-color: rgba(26, 51, 37, 0.12);
            box-shadow: 0 10px 30px rgba(30, 64, 45, 0.055);
        }
        [data-testid="stDialog"] h1,
        [data-testid="stDialog"] h2,
        [data-testid="stDialog"] h3,
        [data-testid="stDialog"] h4,
        [data-testid="stDialog"] h5,
        [data-testid="stDialog"] h6,
        [data-testid="stDialog"] p,
        [data-testid="stDialog"] li,
        [data-testid="stDialog"] strong {
            color: #18221c !important;
        }
        [data-testid="stDialog"] hr,
        [data-testid="stDialog"] [data-testid="stMarkdownContainer"] h2 {
            border-color: rgba(26, 51, 37, 0.12) !important;
        }
        .stButton > button:focus-visible,
        .stDownloadButton > button:focus-visible,
        [data-baseweb="tab"]:focus-visible,
        [data-testid="stExpander"] summary:focus-visible,
        [data-testid="stFileUploaderDropzone"]:focus-within,
        [data-baseweb="select"]:focus-within,
        div[role="radiogroup"] [role="radio"]:focus-visible {
            outline-color: #0f6638;
        }
        .biodata-step:nth-child(2) {
            background: linear-gradient(145deg, rgba(22, 138, 79, 0.09), rgba(255, 255, 255, 0.84));
            border-color: rgba(22, 138, 79, 0.24);
        }
        .biodata-trust-label,
        .biodata-trust-item small,
        .biodata-card-label,
        .biodata-card-helper {
            color: rgba(27, 45, 35, 0.70) !important;
        }
        .biodata-trust-item strong,
        .biodata-result-overview-card strong,
        .biodata-test-metric strong,
        .biodata-card-value,
        .biodata-reading-card h5,
        .biodata-reading-card p {
            color: #18221c !important;
        }
        .biodata-start-note {
            background: rgba(22, 138, 79, 0.07);
            border-color: rgba(22, 138, 79, 0.18);
            color: #20352a;
        }
        .biodata-model-flow {
            border-color: rgba(26, 51, 37, 0.12);
        }
        .biodata-model-flow-item,
        .biodata-model-flow-item:hover {
            color: rgba(27, 45, 35, 0.82);
        }
        [data-baseweb="tab-list"] {
            background: rgba(255, 255, 255, 0.70);
            border-color: rgba(26, 51, 37, 0.12);
        }
        [data-baseweb="tab"] {
            color: rgba(27, 45, 35, 0.76);
        }
        [data-baseweb="tab"][aria-selected="true"] {
            background: rgba(22, 138, 79, 0.10);
            color: #14251b;
        }
        [data-baseweb="select"] > div,
        [data-testid="stNumberInputContainer"],
        [data-testid="stTextArea"] textarea,
        [data-testid="stFileUploaderDropzone"] {
            background-color: rgba(255, 255, 255, 0.82) !important;
            border-color: rgba(26, 51, 37, 0.14) !important;
            color: #18221c !important;
        }
        [data-testid="stDataFrame"] {
            background: #ffffff;
            border-color: rgba(26, 51, 37, 0.12);
        }
        .stButton > button:not([kind="primary"]),
        .stDownloadButton > button:not([kind="primary"]) {
            background: rgba(255, 255, 255, 0.84);
            border-color: rgba(26, 51, 37, 0.16);
            color: #18221c;
        }
    """

    if theme_mode == "light":
        rules = light_rules
    elif theme_mode == "system":
        rules = f"@media (prefers-color-scheme: light) {{{light_rules}}}"
    else:
        rules = ""

    st.markdown(f"<style>{rules}</style>", unsafe_allow_html=True)


def render_brand_header():
    """Muestra el encabezado compacto de la aplicación."""

    st.markdown(
        f"""
        <div class="biodata-brand">
            <div class="biodata-brand-mark" aria-hidden="true">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                    stroke-width="1.7" stroke-linecap="round"
                    stroke-linejoin="round">
                    <path d="M20 4c-7.2.1-12.8 2.8-14.2 7.4-1 3.5 1.1 6.7 4.7 7.2C16 19.4 19.6 13.2 20 4Z" />
                    <path d="M4 20c2.5-4.8 6.2-8.3 11.1-10.8" />
                </svg>
            </div>
            <div>
                <h1>Biodata</h1>
                <p>{tr("Análisis de datos y modelos predictivos")}</p>
            </div>
            <div class="biodata-brand-badge">
                <span aria-hidden="true"></span>
                {tr("Modelos predictivos integrados")}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_landing_page():
    """Muestra una portada útil mientras todavía no hay un dataset cargado."""

    st.markdown(
        f"""
        <section class="biodata-hero">
            <div class="biodata-hero-copy">
                <div class="biodata-kicker">{tr("Análisis de datos y predicción")}</div>
                <h2>{tr("Entendé tus datos antes de tomar decisiones.")}</h2>
                <p>
                    {tr("Biodata combina el análisis exploratorio con modelos predictivos. Estos modelos usan aprendizaje automático (machine learning) para detectar patrones y estimar resultados con datos nuevos.")}
                </p>
                <div class="biodata-hero-capabilities" aria-label="{tr('Etapas disponibles')}">
                    <span>{tr("Calidad de datos")}</span>
                    <span>{tr("Exploración visual")}</span>
                    <span>{tr("Modelos predictivos")}</span>
                </div>
            </div>
            <aside class="biodata-hero-trust">
                <div class="biodata-trust-label">{tr("Diseñado para trabajar con criterio")}</div>
                <div class="biodata-trust-item">
                    <span>01</span>
                    <div>
                        <strong>{tr("Prueba separada")}</strong>
                        <small>{tr("El resultado final se evalúa con datos reservados.")}</small>
                    </div>
                </div>
                <div class="biodata-trust-item">
                    <span>02</span>
                    <div>
                        <strong>{tr("Errores visibles")}</strong>
                        <small>{tr("Las métricas se traducen a una lectura práctica.")}</small>
                    </div>
                </div>
                <div class="biodata-trust-item">
                    <span>03</span>
                    <div>
                        <strong>{tr("Límites explícitos")}</strong>
                        <small>{tr("El informe aclara qué no puede concluir el modelo.")}</small>
                    </div>
                </div>
            </aside>
        </section>
        <div class="biodata-journey-heading">
            <h3>{tr("Un proceso claro, desde los datos hasta la decisión.")}</h3>
            <p>
                {tr("Primero se comprenden los datos, después se comparan modelos y al final se traducen sus resultados, errores y limitaciones.")}
            </p>
        </div>
        <div class="biodata-steps">
            <article class="biodata-step">
                <div class="biodata-step-top">
                    <div class="biodata-step-number">1</div>
                    <div class="biodata-step-icon" aria-hidden="true">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                            stroke-width="1.8" stroke-linecap="round"
                            stroke-linejoin="round">
                            <rect x="3" y="3" width="18" height="18" rx="4" />
                            <path d="M7 16v-3M12 16V8M17 16v-6" />
                        </svg>
                    </div>
                </div>
                <div class="biodata-step-tag">{tr("Análisis de datos")}</div>
                <h3>{tr("Prepará y comprendé")}</h3>
                <p>
                    {tr("Revisá faltantes, duplicados, tipos de variables y distribuciones antes de entrenar un modelo.")}
                </p>
            </article>
            <article class="biodata-step">
                <div class="biodata-step-top">
                    <div class="biodata-step-number">2</div>
                    <div class="biodata-step-icon" aria-hidden="true">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                            stroke-width="1.8" stroke-linecap="round"
                            stroke-linejoin="round">
                            <circle cx="6" cy="12" r="2.3" />
                            <circle cx="18" cy="7" r="2.3" />
                            <circle cx="18" cy="17" r="2.3" />
                            <path d="m8.2 11 7.5-3.1M8.2 13l7.5 3.1" />
                        </svg>
                    </div>
                </div>
                <div class="biodata-step-tag">{tr("Modelos predictivos")}</div>
                <h3>{tr("Entrená y compará")}</h3>
                <p>
                    {tr("Biodata prueba varias alternativas para aprender patrones. Las compara de forma justa y evalúa la mejor con datos que no vio.")}
                </p>
            </article>
            <article class="biodata-step">
                <div class="biodata-step-top">
                    <div class="biodata-step-number">3</div>
                    <div class="biodata-step-icon" aria-hidden="true">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                            stroke-width="1.8" stroke-linecap="round"
                            stroke-linejoin="round">
                            <rect x="4" y="3" width="16" height="18" rx="3" />
                            <path d="m8 12 2 2 5-5M8 17h8M8 7h5" />
                        </svg>
                    </div>
                </div>
                <div class="biodata-step-tag">{tr("Evaluación e informe")}</div>
                <h3>{tr("Interpretá y decidí")}</h3>
                <p>
                    {tr("Entendé el error, revisá los casos difíciles y descargá un informe que explique resultados, controles y limitaciones.")}
                </p>
            </article>
        </div>
        <div class="biodata-start-note">
            <span aria-hidden="true"></span>
            <div>
                <strong>{tr("Para comenzar:")}</strong>
                {tr("si es tu primera vez, abrí el manual de uso. Después seleccioná un archivo desde la barra lateral para iniciar el análisis.")}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def get_user_manual():
    """Lee el manual correspondiente al idioma activo."""

    filename = (
        "USER_GUIDE.md"
        if current_language() == "en"
        else "MANUAL_DE_USO.md"
    )
    manual_path = Path(__file__).resolve().parent / "docs" / filename
    return manual_path.read_text(encoding="utf-8")


@st.dialog(tr("Manual de uso"), width="large")
def render_user_manual_dialog():
    """Muestra y permite descargar la guía sin abandonar el análisis."""

    st.caption(tr("El contenido se adapta al idioma seleccionado."))

    try:
        manual_content = get_user_manual()
    except OSError:
        st.error(
            tr(
                "No se pudo cargar el manual. Volvé a intentarlo en unos minutos."
            )
        )
        return

    st.download_button(
        tr("Descargar manual (.md)"),
        data=manual_content,
        file_name=(
            "biodata_user_guide.md"
            if current_language() == "en"
            else "manual_biodata.md"
        ),
        mime="text/markdown",
        key="download_biodata_manual",
        width="stretch"
    )
    st.divider()
    st.markdown(manual_content)

language, theme_mode = render_preferences()
render_global_styles()
render_theme_overrides(theme_mode)
render_brand_header()
_startup_loader.empty()


# =========================================================
# BARRA LATERAL
# =========================================================

with st.sidebar:

    st.markdown(
        f'<div class="biodata-sidebar-kicker">{tr("Espacio de trabajo")}</div>',
        unsafe_allow_html=True
    )

    st.subheader(tr("Nuevo análisis"))

    st.caption(tr("Cargá un dataset biológico tabular para iniciar el análisis."))

    uploaded_file = st.file_uploader(
        tr("Archivo de datos"),
        type=["csv", "data", "txt"],
        key="biodata_uploaded_file",
        help=(
            tr("Formatos admitidos: CSV, DATA y TXT. Tamaño máximo: 25 MB.")
        )
    )

    st.caption(tr("Usá datos públicos o de prueba. No subas información personal, clínica, confidencial o regulada."))

    has_header = st.checkbox(
        tr("El archivo tiene nombres de columnas"),
        value=True,
        key="biodata_has_header",
        help=(
            tr("Desactivá esta opción si la primera fila contiene datos y no los nombres de las variables.")
        )
    )

    st.divider()

    st.markdown(f"**{tr('Manual de uso')}**")
    st.caption(
        tr(
            "Guía para cargar, explorar, modelar e interpretar datos con criterio."
        )
    )

    if st.button(
        tr("Abrir manual de uso"),
        key="open_biodata_manual",
        width="stretch"
    ):
        render_user_manual_dialog()

    st.divider()

    st.markdown(f"**{tr('Procesamiento y privacidad')}**")

    st.caption(tr("El archivo se transfiere a los servidores de Streamlit Community Cloud en Estados Unidos y se procesa temporalmente en memoria. Biodata no guarda una copia permanente ni lo envía a otros servicios. Al cerrar la pestaña, reemplazar o quitar el archivo, deja de estar disponible."))

    st.caption(tr("Versión 1 · Análisis y modelos predictivos"))


# =========================================================
# ESPERAR ARCHIVO
# =========================================================

if uploaded_file is None:
    render_landing_page()
    st.stop()


# =========================================================
# CARGA DEL DATASET
# =========================================================

abalone_columns = [
    "sex",
    "length",
    "diameter",
    "height",
    "whole_weight",
    "shucked_weight",
    "viscera_weight",
    "shell_weight",
    "rings"
]


is_abalone = uploaded_file.name.lower() == "abalone.data"

try:
    if is_abalone:
        df = load_dataset(
            uploaded_file,
            header=None,
            column_names=abalone_columns
        )
    else:
        header = "infer" if has_header else None
        df = load_dataset(
            uploaded_file,
            header=header
        )

        if not has_header:
            df.columns = [
                f"Variable_{i + 1}"
                for i in range(df.shape[1])
            ]
except ValueError as error:
    st.error(str(error))
    st.stop()

# =========================================================
# NOMBRES DE COLUMNAS
# =========================================================

# Si el archivo no tiene encabezado, evitamos mostrar
# columnas como 0, 1, 2, 3...
# y generamos nombres neutros y comprensibles.

# =========================================================
# NOMBRES DE VARIABLES
# =========================================================

if not has_header and not is_abalone:

    st.subheader(tr("Nombres de las variables"))

    st.info(tr("Este archivo no contiene encabezados. Asigná un nombre a cada columna antes de continuar."))

    new_column_names = []

    for i in range(df.shape[1]):

        column_name = st.text_input(
            tr("Columna {number}", number=i + 1),
            value=tr("Variable_{number}", number=i + 1),
            key=f"column_name_{i}"
        )

        new_column_names.append(column_name)

    df.columns = new_column_names

try:
    df.columns = validate_column_names(df.columns)
except ValueError as error:
    st.error(str(error))
    st.stop()


# =========================================================
# ANÁLISIS GENERAL
# =========================================================

profile = get_dataset_profile(df)

dataset_fingerprint = get_dataset_fingerprint(df)

quality_report = get_quality_report(df)

numeric_summary = get_numeric_summary(df)

categorical_summary = get_categorical_summary(df)


# =========================================================
# DATASET ACTUAL
# =========================================================

st.success(
    tr("Dataset cargado correctamente: {filename}", filename=uploaded_file.name)
)

st.caption(
    tr(
        "{rows} observaciones · {columns} variables",
        rows=profile["n_rows"],
        columns=profile["n_columns"]
    )
)


# =========================================================
# PESTAÑAS
# =========================================================

tab_summary, tab_eda, tab_model = st.tabs(
    [
        tr("Resumen"),
        tr("Exploración"),
        tr("Modelos")
    ]
)


# =========================================================
# TAB 1 — RESUMEN
# =========================================================

with tab_summary:

    # -----------------------------------------------------
    # MÉTRICAS GENERALES
    # -----------------------------------------------------

    st.header(tr("Resumen del dataset"))

    total_missing = sum(
        quality_report["missing_values"].values()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        tr("Observaciones"),
        profile["n_rows"]
    )

    col2.metric(
        tr("Variables"),
        profile["n_columns"]
    )

    col3.metric(
        tr("Valores faltantes"),
        total_missing
    )

    col4.metric(
        tr("Filas duplicadas"),
        quality_report["duplicate_rows"]
    )

    st.divider()


    # -----------------------------------------------------
    # VISTA PREVIA
    # -----------------------------------------------------

    st.subheader(tr("Vista previa de datos"))

    st.caption(
        tr("Primeras 10 observaciones del dataset.")
    )

    st.dataframe(
        df.head(10),
        width="stretch",
        hide_index=True
    )

    st.divider()


    # -----------------------------------------------------
    # CALIDAD
    # -----------------------------------------------------

    st.subheader(tr("Calidad de los datos"))

    quality_col1, quality_col2, quality_col3 = st.columns(3)

    missing_with_values = {
        column: count
        for column, count
        in quality_report["missing_values"].items()
        if count > 0
    }

    infinite_with_values = {
        column: count
        for column, count
        in quality_report["infinite_values"].items()
        if count > 0
    }

    with quality_col1:

        st.markdown(f"**{tr('Valores faltantes')}**")

        if missing_with_values:

            missing_table = {
                tr("Variable"): list(
                    missing_with_values.keys()
                ),
                tr("Cantidad de faltantes"): list(
                    missing_with_values.values()
                )
            }

            st.dataframe(
                missing_table,
                width="stretch",
                hide_index=True
            )

        else:

            st.write(
                tr("No se detectaron valores faltantes.")
            )

    with quality_col2:

        st.markdown(f"**{tr('Valores infinitos')}**")

        if infinite_with_values:
            infinite_table = {
                tr("Variable"): list(infinite_with_values.keys()),
                tr("Cantidad"): list(infinite_with_values.values())
            }

            st.dataframe(
                infinite_table,
                width="stretch",
                hide_index=True
            )

            st.caption(
                tr("En el modelado se tratarán como valores faltantes.")
            )
        else:
            st.write(tr("No se detectaron valores infinitos."))

    with quality_col3:

        st.markdown(f"**{tr('Filas duplicadas')}**")

        if quality_report["duplicate_rows"] > 0:

            st.write(tr(
                "Se detectaron {count} filas duplicadas.",
                count=quality_report["duplicate_rows"]
            ))

        else:

            st.write(
                tr("No se detectaron filas duplicadas.")
            )

    st.divider()


    # -----------------------------------------------------
    # ESTADÍSTICAS DESCRIPTIVAS
    # -----------------------------------------------------

    st.subheader(tr("Estadísticas descriptivas"))

    st.caption(
        tr("Resumen de las variables numéricas del dataset.")
    )

    if not numeric_summary.empty:

        # describe() originalmente devuelve:
        #
        #           Variable 1 | Variable 2
        # count
        # mean
        # std
        # ...
        #
        # La transponemos para obtener una tabla
        # mucho más clara:
        #
        # Variable | N | Media | Desv. estándar | ...

        descriptive_table = (
            numeric_summary
            .T
            .reset_index()
        )

        descriptive_table.columns = [
            tr("Variable"),
            "N",
            tr("Media"),
            tr("Desv. estándar"),
            tr("Mínimo"),
            "25 %",
            tr("Mediana"),
            "75 %",
            tr("Máximo")
        ]

        descriptive_table = (
            descriptive_table.round(4)
        )

        descriptive_table["N"] = (
            descriptive_table["N"]
            .astype(int)
        )

        st.dataframe(
            descriptive_table,
            width="stretch",
            hide_index=True
        )

    else:

        st.info(
            tr("No se detectaron variables numéricas.")
        )

    st.divider()


    # -----------------------------------------------------
    # VARIABLES CATEGÓRICAS
    # -----------------------------------------------------

    st.subheader(tr("Variables categóricas"))

    if categorical_summary:

        for column, counts in categorical_summary.items():

            with st.expander(
                f"{column}"
            ):

                categorical_table = {
                    tr("Categoría"): list(
                        counts.keys()
                    ),
                    tr("Frecuencia"): list(
                        counts.values()
                    )
                }

                st.dataframe(
                    categorical_table,
                    width="stretch",
                    hide_index=True
                )

                total_categories = df[column].nunique(dropna=False)

                if total_categories > len(counts):
                    st.caption(tr(
                        "Se muestran las {shown} categorías más frecuentes de {total}.",
                        shown=len(counts),
                        total=total_categories
                    ))

    else:

        st.info(
            tr("No se detectaron variables categóricas.")
        )


# =========================================================
# TAB 2 — EXPLORACIÓN
# =========================================================

with tab_eda:

    st.header(tr("Exploración de datos"))

    numeric_columns = (
        numeric_summary.columns.tolist()
        if not numeric_summary.empty
        else []
    )

    categorical_columns = list(
        categorical_summary.keys()
    )


    # -----------------------------------------------------
    # DISTRIBUCIÓN NUMÉRICA
    # -----------------------------------------------------

    st.subheader(tr("Distribución de variable numérica"))

    if numeric_columns:

        selected_numeric_column = st.selectbox(
            tr("Elegí una variable numérica"),
            numeric_columns,
            key="numeric_distribution"
        )

        numeric_fig = themed_figure(
            plot_numeric_distribution(
                df,
                selected_numeric_column,
                language=current_language()
            )
        )

        st.pyplot(
            numeric_fig,
            width="stretch"
        )

    else:

        st.info(
            tr("No hay variables numéricas para visualizar.")
        )

    st.divider()


    # -----------------------------------------------------
    # DISTRIBUCIÓN CATEGÓRICA
    # -----------------------------------------------------

    st.subheader(tr("Distribución de variable categórica"))

    if categorical_columns:

        selected_categorical_column = st.selectbox(
            tr("Elegí una variable categórica"),
            categorical_columns,
            key="categorical_distribution"
        )

        categorical_fig = themed_figure(
            plot_categorical_distribution(
                df,
                selected_categorical_column,
                language=current_language()
            )
        )

        st.pyplot(
            categorical_fig,
            width="stretch"
        )

    else:

        st.info(
            tr("No hay variables categóricas para visualizar.")
        )

    st.divider()


    # -----------------------------------------------------
    # CORRELACIONES
    # -----------------------------------------------------

    st.subheader(tr("Mapa de correlaciones"))

    if len(numeric_columns) >= 2:

        default_correlation_columns = numeric_columns[:10]

        selected_correlation_columns = st.multiselect(
            tr("Variables incluidas en el mapa"),
            numeric_columns,
            default=default_correlation_columns,
            max_selections=20,
            key=f"biodata_correlation_{dataset_fingerprint}",
            help=(
                tr("Elegí entre 2 y 20 variables. Limitar el mapa ayuda a mantenerlo legible en datasets grandes.")
            )
        )

        if len(selected_correlation_columns) >= 2:
            correlation_fig = themed_figure(
                plot_correlation_heatmap(
                    df[selected_correlation_columns],
                    language=current_language()
                )
            )

            st.pyplot(
                correlation_fig,
                width="stretch"
            )
        else:
            st.info(
                tr("Seleccioná al menos dos variables para construir el mapa.")
            )

    else:

        st.info(
            tr("Se necesitan al menos dos variables numéricas para calcular correlaciones.")
        )


# =========================================================
# TAB 3 — MODELADO
# =========================================================

with tab_model:

    st.header(tr("Modelos predictivos"))

    st.caption(
        tr("Estos modelos usan aprendizaje automático (machine learning) para aprender patrones y estimar un resultado numérico. Configurá el problema, compará alternativas y revisá su desempeño antes de utilizarlo.")
    )

    st.markdown(
        f"""
        <div class="biodata-model-flow">
            <div class="biodata-model-flow-item">
                <span>1</span><strong>{tr("Objetivo")}</strong>
            </div>
            <div class="biodata-model-flow-item">
                <span>2</span><strong>{tr("Predictores")}</strong>
            </div>
            <div class="biodata-model-flow-item">
                <span>3</span><strong>{tr("Contexto")}</strong>
            </div>
            <div class="biodata-model-flow-item">
                <span>4</span><strong>{tr("Comparación")}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # VARIABLES OBJETIVO VÁLIDAS
    # -----------------------------------------------------

    # Como todavía trabajamos solamente con regresión,
    # permitimos seleccionar únicamente targets numéricos.

    target_options = get_valid_regression_targets(df)


    if not target_options:

        st.warning(
            tr("No hay una variable objetivo numérica con al menos 10 valores válidos y dos valores diferentes.")
        )


    else:
        st.markdown(f"### {tr('Configuración')}")

        with st.container(border=True):
            target_col, target_data_col = st.columns(
                [1.8, 1],
                vertical_alignment="center"
            )

            with target_col:
                st.markdown(f"#### {tr('1. Variable objetivo')}")
                st.caption(
                    tr("Es la medida numérica que querés que el modelo estime.")
                )

                target_column = st.selectbox(
                    tr("Variable a predecir"),
                    target_options,
                    index=len(target_options) - 1,
                    key=f"biodata_target_{dataset_fingerprint}",
                    format_func=format_variable_label
                )

            try:
                X, y, dropped_target_rows = prepare_regression_dataset(
                    df,
                    target_column
                )
            except ValueError as error:
                st.error(str(error))
                st.stop()

            with target_data_col:
                st.markdown(f"#### {tr('Datos disponibles')}")
                st.metric(tr("Filas con objetivo válido"), len(y))
                st.caption(
                    tr(
                        "Objetivo seleccionado: {target}",
                        target=format_variable_label(target_column)
                    )
                )

            if dropped_target_rows:
                st.warning(tr(
                    "Se excluyeron {count} filas porque la variable objetivo no tenía un valor numérico válido.",
                    count=dropped_target_rows
                ))

            st.divider()
            st.markdown(f"#### {tr('2. Variables predictoras')}")

            target_display_name = format_variable_label(target_column).lower()

            predictor_intro = tr(
                "Las variables predictoras son las pistas que usará el modelo para estimar {target}. Podés mantener todas o quitar las que no correspondan al uso real.",
                target=target_display_name
            )
            if current_language() == "es":
                predictor_intro = predictor_intro.replace(
                    "las pistas que usará el modelo para estimar",
                    "las **pistas que usará el modelo para estimar"
                ).replace(
                    f"{target_display_name}.",
                    f"{target_display_name}**."
                )
            else:
                predictor_intro = predictor_intro.replace(
                    "the information the model will use to estimate",
                    "the **information the model will use to estimate"
                ).replace(
                    f"{target_display_name}.",
                    f"{target_display_name}**."
                )
            st.write(predictor_intro)

            if current_language() == "es":
                st.markdown(
                    """
- **Mantené** mediciones y características que conocerías antes de hacer la predicción.
- **Quitá** identificadores, números de fila, datos obtenidos después del resultado o variables que revelen directamente la respuesta.
                    """
                )
            else:
                st.markdown(
                    """
- **Keep** measurements and characteristics available before making the prediction.
- **Remove** identifiers, row numbers, information collected after the outcome or variables that directly reveal the answer.
                    """
                )

            st.caption(
                tr("¿Por qué importa? Si el modelo recibe información que no existiría en una situación real, puede mostrar resultados demasiado buenos que después no se repiten.")
            )

            available_feature_types = detect_feature_types(X)
            available_features = (
                available_feature_types["numeric_features"]
                + available_feature_types["categorical_features"]
            )
            usable_features = [
                column
                for column in available_features
                if X[column].notna().any()
            ]
            ignored_features = [
                column
                for column in X.columns
                if column not in usable_features
            ]

            selected_features = st.multiselect(
                tr("Variables incluidas"),
                usable_features,
                default=usable_features,
                key=f"biodata_features_{dataset_fingerprint}_{target_column}",
                format_func=format_variable_label,
                help=(
                    tr("Usá la X de cada etiqueta para quitar una variable. Esto no borra la columna del archivo: solo evita que el modelo la utilice.")
                )
            )

            if ignored_features:
                ignored_text = ", ".join(
                    format_variable_label(column)
                    for column in ignored_features
                )
                st.caption(tr(
                    "Biodata excluyó variables vacías o no compatibles: {variables}",
                    variables=ignored_text
                ))

            if not selected_features:
                st.warning(tr("Seleccioná al menos una variable predictora."))
                st.stop()

            X = X[selected_features].copy()
            feature_types = detect_feature_types(X)
            numeric_features = feature_types["numeric_features"]
            categorical_features = feature_types["categorical_features"]

            high_cardinality_features = [
                column
                for column in categorical_features
                if X[column].nunique(dropna=True) > 50
            ]

            if high_cardinality_features:
                high_cardinality_text = ", ".join(
                    format_variable_label(column)
                    for column in high_cardinality_features
                )
                st.warning(tr(
                    "Revisá estas variables: tienen muchas categorías y podrían ser identificadores: {variables}.",
                    variables=high_cardinality_text
                ))

            st.caption(tr(
                "{selected} variables seleccionadas · {numeric} numéricas · {categorical} categóricas",
                selected=len(selected_features),
                numeric=len(numeric_features),
                categorical=len(categorical_features)
            ))

            with st.expander(tr("Ver detalle de las variables seleccionadas")):
                numeric_text = (
                    ", ".join(
                        format_variable_label(column)
                        for column in numeric_features
                    )
                    if numeric_features
                    else tr("Ninguna")
                )
                categorical_text = (
                    ", ".join(
                        format_variable_label(column)
                        for column in categorical_features
                    )
                    if categorical_features
                    else tr("Ninguna")
                )

                st.markdown(f"**{tr('Numéricas')}:** {numeric_text}")
                st.markdown(f"**{tr('Categóricas')}:** {categorical_text}")

        with st.expander(tr("3. Contexto de uso (recomendado)")):
            st.caption(
                tr("Ayuda a convertir las métricas en recomendaciones útiles. No modifica el entrenamiento.")
            )

            context_goal = st.text_area(
                tr("¿Cuál es el objetivo del análisis?"),
                placeholder=(
                    tr("Ejemplo: estimar la edad para priorizar muestras que necesitan una revisión especializada.")
                ),
                key="biodata_context_goal"
            )

            context_decision = st.text_area(
                tr("¿Qué decisión querés apoyar con el resultado?"),
                placeholder=(
                    tr("Ejemplo: decidir qué casos revisar primero, sin reemplazar la evaluación de una persona especialista.")
                ),
                key="biodata_context_decision"
            )

            context_col1, context_col2 = st.columns(2)

            context_audience = context_col1.selectbox(
                tr("Audiencia del informe"),
                [
                    "Público general",
                    "Equipo técnico",
                    "Equipo científico",
                    "Responsables de decisión"
                ],
                format_func=tr,
                key="biodata_context_audience"
            )

            context_impact = context_col2.selectbox(
                tr("Impacto de la decisión"),
                ["Bajo", "Medio", "Alto", "Crítico"],
                index=1,
                format_func=tr,
                key="biodata_context_impact"
            )

            acceptable_error = st.number_input(
                tr("Error máximo tolerable"),
                min_value=0.0,
                value=0.0,
                step=0.1,
                help=tr("Usá 0 si todavía no fue definido."),
                key="biodata_acceptable_error"
            )

        user_context = {
            "goal": context_goal.strip(),
            "decision": context_decision.strip(),
            "audience": context_audience,
            "acceptable_error": float(acceptable_error),
            "impact": context_impact
        }

        analysis_id = (
            dataset_fingerprint,
            target_column,
            tuple(selected_features)
        )

        with st.container(border=True):
            run_text_col, run_button_col = st.columns(
                [2, 1],
                vertical_alignment="center"
            )

            with run_text_col:
                st.markdown(f"#### {tr('4. Ejecutar análisis')}")
                st.caption(
                    tr("Biodata reservará 20 % de los datos para la prueba final y comparará los modelos solo con el conjunto de entrenamiento.")
                )

            analyze_clicked = run_button_col.button(
                tr("Analizar y comparar modelos"),
                type="primary",
                width="stretch"
            )

        if analyze_clicked:
            with st.spinner(
                tr("Preparando datos, comparando modelos y generando diagnósticos...")
            ):
                X_train, X_test, y_train, y_test = split_train_test(X, y)

                preprocessor = build_preprocessor(
                    numeric_features,
                    categorical_features
                )

                models = {
                    "Dummy": DummyRegressor(strategy="mean"),
                    "Regresión lineal": LinearRegression(),
                    "Random Forest": RandomForestRegressor(
                        random_state=42
                    ),
                    "Gradient Boosting": GradientBoostingRegressor(
                        random_state=42
                    )
                }

                model_results = compare_regression_models(
                    preprocessor,
                    models,
                    X_train,
                    y_train
                )

                best_model_name = select_best_regression_model(
                    model_results
                )

                trained_model = train_regression_model(
                    preprocessor,
                    models[best_model_name],
                    X_train,
                    y_train
                )

                evaluation_result = evaluate_regression_model(
                    trained_model,
                    X_test,
                    y_test
                )

                evaluation_summary = summarize_regression_evaluation(
                    evaluation_result
                )

                prediction_table = build_prediction_table(
                    X_test,
                    y_test,
                    evaluation_result["predictions"]
                )

                feature_importance = calculate_permutation_feature_importance(
                    trained_model,
                    X_test,
                    y_test
                )

                subgroup_errors = calculate_subgroup_errors(
                    prediction_table,
                    categorical_features
                )

                diagnostic_warnings = build_diagnostic_warnings(
                    evaluation_summary,
                    prediction_table,
                    subgroup_errors,
                    language=current_language()
                )

                diagnostics_summary = summarize_diagnostics(
                    prediction_table,
                    feature_importance,
                    diagnostic_warnings
                )

                processed_feature_count = len(
                    trained_model
                    .named_steps["preprocessor"]
                    .get_feature_names_out()
                )

            st.session_state["biodata_modeling_result"] = {
                "analysis_id": analysis_id,
                "model_results": model_results,
                "best_model_name": best_model_name,
                "evaluation_summary": evaluation_summary,
                "prediction_table": prediction_table,
                "feature_importance": feature_importance,
                "subgroup_errors": subgroup_errors,
                "diagnostics_summary": diagnostics_summary,
                "language": current_language(),
                "n_train": len(X_train),
                "n_test": len(X_test),
                "processed_feature_count": processed_feature_count
            }

        analysis_result = st.session_state.get("biodata_modeling_result")

        if (
            analysis_result is None
            or analysis_result.get("analysis_id") != analysis_id
        ):
            st.info(
                tr("Ejecutá el análisis para ver la comparación, los diagnósticos y el informe final.")
            )

        else:
            model_results = analysis_result["model_results"]
            best_model_name = analysis_result["best_model_name"]
            evaluation_summary = analysis_result["evaluation_summary"]
            prediction_table = analysis_result["prediction_table"]
            feature_importance = analysis_result["feature_importance"]
            subgroup_errors = analysis_result["subgroup_errors"]
            diagnostics_summary = analysis_result["diagnostics_summary"]

            if analysis_result.get("language") != current_language():
                localized_warnings = build_diagnostic_warnings(
                    evaluation_summary,
                    prediction_table,
                    subgroup_errors,
                    language=current_language()
                )
                diagnostics_summary = {
                    **diagnostics_summary,
                    "warnings": localized_warnings
                }

            st.divider()
            st.markdown(f"### {tr('Resultados')}")

            localized_model_name = model_label(
                best_model_name,
                current_language()
            )

            st.markdown(
                f"""
                <div class="biodata-result-overview">
                    <div class="biodata-result-overview-card">
                        <span>{tr("Modelo seleccionado")}</span>
                        <strong>{escape(localized_model_name)}</strong>
                        <small>{tr("Menor MAE en la validación cruzada")}</small>
                    </div>
                    <div class="biodata-result-overview-card">
                        <span>{tr("División de los datos")}</span>
                        <strong>{analysis_result['n_train']} / {analysis_result['n_test']}</strong>
                        <small>{tr("Entrenamiento / prueba")}</small>
                    </div>
                    <div class="biodata-result-overview-card">
                        <span>{tr("Variables procesadas")}</span>
                        <strong>{analysis_result['processed_feature_count']}</strong>
                        <small>{tr("Después del preprocesamiento")}</small>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            comparison_table = {
                tr("Modelo"): [],
                tr("MAE promedio (CV)"): []
            }

            for model_name, result in model_results.items():
                comparison_table[tr("Modelo")].append(
                    model_label(model_name, current_language())
                )
                comparison_table[tr("MAE promedio (CV)")].append(
                    round(float(result["mean_mae"]), 4)
                )

            with st.expander(tr("Ver comparación de los cuatro modelos")):
                st.dataframe(
                    comparison_table,
                    width="stretch",
                    hide_index=True
                )

                st.caption(
                    tr("La comparación usa únicamente el entrenamiento. Un MAE menor representa un error promedio menor.")
                )

            # -------------------------------------------------
            # EVALUACIÓN Y DIAGNÓSTICOS
            # -------------------------------------------------

            st.markdown(f"#### {tr('Rendimiento en datos de prueba')}")

            st.markdown(
                f"""
                <div class="biodata-test-metrics">
                    <div class="biodata-test-metric">
                        <span>MAE</span>
                        <strong>{format_spanish_number(evaluation_summary['mae'], 3)}</strong>
                        <small>{tr("Error promedio")}</small>
                    </div>
                    <div class="biodata-test-metric">
                        <span>RMSE</span>
                        <strong>{format_spanish_number(evaluation_summary['rmse'], 3)}</strong>
                        <small>{tr("Penaliza errores grandes")}</small>
                    </div>
                    <div class="biodata-test-metric">
                        <span>R²</span>
                        <strong>{format_spanish_number(evaluation_summary['r2'], 3)}</strong>
                        <small>{tr("Ajuste global")}</small>
                    </div>
                    <div class="biodata-test-metric">
                        <span>Error P90</span>
                        <strong>{format_spanish_number(diagnostics_summary['p90_absolute_error'], 3)}</strong>
                        <small>{tr("El 90 % queda por debajo")}</small>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.caption(
                tr("Las métricas y los gráficos siguientes se calcularon sobre el conjunto de prueba reservado. El preprocesador se ajustó solo con entrenamiento para evitar filtraciones.")
            )

            for warning in diagnostics_summary["warnings"]:
                st.warning(
                    f"**{warning['title']}.** {warning['message']}"
                )

            if not diagnostics_summary["warnings"]:
                st.success(
                    tr("No se activaron advertencias con las reglas diagnósticas actuales.")
                )

            st.markdown(f"#### {tr('Diagnóstico del modelo')}")
            st.caption(
                tr("Explorá cómo se distribuyen los errores, qué variables aportan información y qué casos conviene revisar.")
            )

            (
                predictions_tab,
                residuals_tab,
                importance_tab,
                review_tab
            ) = st.tabs(
                [
                    tr("Predicciones"),
                    tr("Residuos"),
                    tr("Variables importantes"),
                    tr("Casos a revisar")
                ]
            )

            with predictions_tab:
                st.pyplot(
                    themed_figure(
                        plot_actual_vs_predicted(
                            prediction_table,
                            target_column,
                            language=current_language()
                        )
                    ),
                    width="stretch"
                )

                st.caption(
                    tr("Cuanto más cerca esté un punto de la línea diagonal, más cercana fue la predicción al valor real.")
                )

            with residuals_tab:
                residual_col1, residual_col2 = st.columns(2)

                with residual_col1:
                    st.pyplot(
                        themed_figure(
                            plot_residuals(
                                prediction_table,
                                language=current_language()
                            )
                        ),
                        width="stretch"
                    )

                with residual_col2:
                    st.pyplot(
                        themed_figure(
                            plot_residual_distribution(
                                prediction_table,
                                language=current_language()
                            )
                        ),
                        width="stretch"
                    )

                st.caption(
                    tr("Un patrón aleatorio alrededor de cero es deseable. Patrones o desplazamientos persistentes pueden indicar sesgo o relaciones que el modelo no aprendió.")
                )

            with importance_tab:
                importance_col1, importance_col2 = st.columns([2, 1])

                with importance_col1:
                    st.pyplot(
                        themed_figure(
                            plot_feature_importance(
                                feature_importance,
                                language=current_language()
                            )
                        ),
                        width="stretch"
                    )

                with importance_col2:
                    st.dataframe(
                        localize_generated_table(feature_importance),
                        width="stretch",
                        hide_index=True
                    )

                st.caption(
                    tr("La importancia por permutación muestra utilidad predictiva: no demuestra que una variable cause el resultado.")
                )

            with review_tab:
                st.markdown(f"##### {tr('Casos con mayor error')}")

                largest_errors = get_largest_errors(
                    prediction_table,
                    n=10
                )

                st.dataframe(
                    localize_generated_table(largest_errors),
                    width="stretch",
                    hide_index=True
                )

                st.markdown(f"##### {tr('Rendimiento por grupos')}")

                if subgroup_errors.empty:
                    st.info(
                        tr("No hay grupos categóricos con suficientes casos para comparar su rendimiento.")
                    )
                else:
                    st.dataframe(
                        localize_generated_table(subgroup_errors),
                        width="stretch",
                        hide_index=True
                    )

            st.divider()

            # -------------------------------------------------
            # INFORME FINAL
            # -------------------------------------------------

            st.subheader(tr("Informe final"))

            final_report = build_full_report(
                profile,
                quality_report,
                model_results,
                evaluation_summary,
                target_column=target_column,
                diagnostics_summary=diagnostics_summary,
                user_context=user_context,
                language=current_language()
            )

            st.caption(
                tr("Resumen de resultados, diagnósticos y recomendaciones para interpretar el modelo de forma responsable.")
            )

            st.markdown(
                """
                <style>
                .biodata-summary-grid {
                    display: grid;
                    grid-template-columns: repeat(3, minmax(0, 1fr));
                    gap: 1rem;
                    margin: 1rem 0 2rem;
                }
                .biodata-summary-card,
                .biodata-reading-card {
                    border: 1px solid rgba(250, 250, 250, 0.16);
                    border-radius: 14px;
                    background: linear-gradient(
                        145deg,
                        rgba(255, 255, 255, 0.045),
                        rgba(255, 255, 255, 0.015)
                    );
                    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
                }
                .biodata-summary-card {
                    min-height: 142px;
                    padding: 1rem 1.1rem;
                }
                .biodata-card-label {
                    color: rgba(250, 250, 250, 0.68);
                    font-size: 0.78rem;
                    font-weight: 700;
                    letter-spacing: 0.055em;
                    line-height: 1.35;
                    text-transform: uppercase;
                }
                .biodata-card-value {
                    color: #ffffff;
                    font-size: clamp(1.45rem, 2.5vw, 2.15rem);
                    font-weight: 700;
                    line-height: 1.15;
                    margin: 0.55rem 0 0.45rem;
                    overflow-wrap: anywhere;
                }
                .biodata-card-helper {
                    color: rgba(250, 250, 250, 0.68);
                    font-size: 0.86rem;
                    line-height: 1.45;
                }
                .biodata-reading-grid {
                    display: grid;
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                    gap: 1rem;
                    margin: 0.8rem 0 1rem;
                }
                .biodata-reading-card {
                    padding: 1.2rem 1.25rem;
                }
                .biodata-reading-card h5 {
                    color: #ffffff;
                    font-size: 1.12rem;
                    line-height: 1.3;
                    margin: 0 0 1rem;
                }
                .biodata-reading-card p {
                    color: rgba(250, 250, 250, 0.86);
                    font-size: 0.96rem;
                    line-height: 1.65;
                    margin: 0 0 0.9rem;
                }
                .biodata-reading-card p:last-child {
                    margin-bottom: 0;
                }
                .biodata-status {
                    border-radius: 10px;
                    margin-bottom: 1rem;
                    padding: 0.8rem 0.9rem;
                }
                .biodata-status strong,
                .biodata-status span {
                    display: block;
                }
                .biodata-status span {
                    font-size: 0.86rem;
                    line-height: 1.45;
                    margin-top: 0.2rem;
                }
                .biodata-status-good {
                    background: rgba(61, 220, 132, 0.12);
                    border: 1px solid rgba(61, 220, 132, 0.35);
                }
                .biodata-status-warning {
                    background: rgba(255, 193, 7, 0.10);
                    border: 1px solid rgba(255, 193, 7, 0.32);
                }
                @media (max-width: 760px) {
                    .biodata-summary-grid,
                    .biodata-reading-grid {
                        grid-template-columns: 1fr;
                    }
                    .biodata-summary-card {
                        min-height: auto;
                    }
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            target_label = format_variable_label(target_column)
            selected_model_label = model_label(
                best_model_name,
                current_language()
            )
            mae_text = format_spanish_number(
                evaluation_summary["mae"],
                decimals=2
            )
            r2_value = evaluation_summary["r2"]

            if r2_value >= 0:
                r2_text = (
                    f"{format_spanish_number(r2_value * 100, decimals=1)} %"
                )
                r2_helper = tr("de la variabilidad observada en la prueba")
            else:
                r2_text = format_spanish_number(r2_value, decimals=2)
                r2_helper = tr("rinde peor que predecir usando el promedio")

            st.markdown(
                f"""
                <div class="biodata-summary-grid">
                    <div class="biodata-summary-card">
                        <div class="biodata-card-label">{tr("Modelo seleccionado")}</div>
                        <div class="biodata-card-value">{escape(selected_model_label)}</div>
                        <div class="biodata-card-helper">
                            {tr("Menor error promedio en la validación cruzada")}
                        </div>
                    </div>
                    <div class="biodata-summary-card">
                        <div class="biodata-card-label">{tr("Error promedio (MAE)")}</div>
                        <div class="biodata-card-value">{mae_text} {tr("unidades")}</div>
                        <div class="biodata-card-helper">
                            {tr("por predicción de {target}", target=escape(target_label.lower()))}
                        </div>
                    </div>
                    <div class="biodata-summary-card">
                        <div class="biodata-card-label">{tr("R² en datos de prueba")}</div>
                        <div class="biodata-card-value">{r2_text}</div>
                        <div class="biodata-card-helper">{r2_helper}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(f"#### {tr('Lectura rápida')}")

            top_features = diagnostics_summary["top_features"]

            if top_features:
                feature_names_html = ", ".join(
                    (
                        "<strong>"
                        + escape(format_variable_label(item["variable"]))
                        + "</strong>"
                    )
                    for item in top_features[:3]
                )
                if current_language() == "es":
                    feature_paragraph = (
                        "<p><strong>Qué información resultó más útil:</strong> "
                        f"{feature_names_html} fueron las variables que más ayudaron "
                        "al modelo a realizar sus estimaciones. Esto no significa "
                        "que provoquen cambios en el resultado.</p>"
                    )
                else:
                    feature_paragraph = (
                        "<p><strong>Which information was most useful:</strong> "
                        f"{feature_names_html} contributed the most to the model's "
                        "estimates. This does not mean they cause changes in the "
                        "outcome.</p>"
                    )
            else:
                if current_language() == "es":
                    feature_paragraph = (
                        "<p><strong>Qué información resultó más útil:</strong> En "
                        "esta evaluación no se identificaron variables con un "
                        "aporte predictivo positivo y estable.</p>"
                    )
                else:
                    feature_paragraph = (
                        "<p><strong>Which information was most useful:</strong> "
                        "This evaluation did not identify variables with a stable, "
                        "positive predictive contribution.</p>"
                    )

            if r2_value >= 0:
                unexplained_text = format_spanish_number(
                    max(0, (1 - r2_value) * 100),
                    decimals=1
                )
                if current_language() == "es":
                    performance_paragraph = (
                        "<p><strong>Cuánto logra explicar:</strong> De las diferencias "
                        f"observadas en {escape(target_label.lower())}, el modelo "
                        f"logra captar aproximadamente el <strong>{r2_text}</strong>. "
                        f"El {unexplained_text} % restante queda sin explicar con "
                        "la información disponible.</p>"
                    )
                else:
                    performance_paragraph = (
                        "<p><strong>How much it explains:</strong> The model captures "
                        f"approximately <strong>{r2_text}</strong> of the observed "
                        f"variation in {escape(target_label.lower())}. The remaining "
                        f"{unexplained_text}% is not explained by the available "
                        "information.</p>"
                    )
            else:
                performance_paragraph = (
                    "<p><strong>Cuánto logra explicar:</strong> El R² fue "
                    "negativo. Con estos datos de prueba, el modelo no mejora "
                    "una estimación basada solamente en el valor promedio.</p>"
                    if current_language() == "es"
                    else
                    "<p><strong>How much it explains:</strong> R² is negative. "
                    "On this test set, the model does not improve on an estimate "
                    "based only on the mean value.</p>"
                )

            if acceptable_error > 0:
                acceptable_error_text = format_spanish_number(
                    acceptable_error,
                    decimals=2
                )

                if evaluation_summary["mae"] <= acceptable_error:
                    status_class = "biodata-status-good"
                    if current_language() == "es":
                        status_title = "Dentro de la tolerancia declarada"
                        status_detail = (
                            f"El MAE de {mae_text} es menor o igual al límite de "
                            f"{acceptable_error_text} unidades."
                        )
                    else:
                        status_title = "Within the declared tolerance"
                        status_detail = (
                            f"The MAE of {mae_text} is at or below the limit of "
                            f"{acceptable_error_text} units."
                        )
                else:
                    status_class = "biodata-status-warning"
                    if current_language() == "es":
                        status_title = "Supera la tolerancia declarada"
                        status_detail = (
                            f"El MAE de {mae_text} supera el límite de "
                            f"{acceptable_error_text} unidades."
                        )
                    else:
                        status_title = "Above the declared tolerance"
                        status_detail = (
                            f"The MAE of {mae_text} exceeds the limit of "
                            f"{acceptable_error_text} units."
                        )

                decision_status_html = f"""
                    <div class="biodata-status {status_class}">
                        <strong>{status_title}</strong>
                        <span>{status_detail}</span>
                    </div>
                """
            else:
                if current_language() == "es":
                    decision_status_html = (
                        "<p>Antes de usar el resultado, definí si un error promedio "
                        f"de <strong>{mae_text} unidades</strong> es aceptable para "
                        "el objetivo del análisis.</p>"
                    )
                else:
                    decision_status_html = (
                        "<p>Before using the result, decide whether an average "
                        f"error of <strong>{mae_text} units</strong> is acceptable "
                        "for the purpose of the analysis.</p>"
                    )

            impact_paragraph = ""

            if context_impact in ("Alto", "Crítico"):
                impact_paragraph = (
                    "<p>Como el impacto declarado es alto, necesitás validación "
                    "externa y revisión especializada antes de usar el modelo.</p>"
                    if current_language() == "es"
                    else
                    "<p>Because the declared impact is high, external validation "
                    "and specialist review are required before using the model.</p>"
                )

            if current_language() == "es":
                practical_heading = "¿Qué significa en la práctica?"
                practical_intro = (
                    "<p><strong>Qué tan cerca suele estar:</strong> Al predecir "
                    f"{escape(target_label.lower())}, las estimaciones se "
                    f"diferencian del valor real en <strong>{mae_text} "
                    "unidades en promedio</strong>. No es un error máximo: "
                    "algunos casos quedan más cerca y otros más lejos.</p>"
                )
                decision_heading = "¿Cómo usar esta información?"
                decision_paragraph = (
                    "<p>Puede ayudar a <strong>ordenar, priorizar o revisar "
                    "casos</strong>. Las decisiones de mayor impacto requieren "
                    "confirmación humana.</p>"
                )
            else:
                practical_heading = "What does this mean in practice?"
                practical_intro = (
                    "<p><strong>How close predictions usually are:</strong> When "
                    f"predicting {escape(target_label.lower())}, estimates differ "
                    f"from the actual value by <strong>{mae_text} units on "
                    "average</strong>. This is not a maximum error: some cases "
                    "are closer and others are farther away.</p>"
                )
                decision_heading = "How should this information be used?"
                decision_paragraph = (
                    "<p>It can help <strong>rank, prioritize or review cases</strong>. "
                    "Higher-impact decisions require human confirmation.</p>"
                )

            reading_html = (
                '<div class="biodata-reading-grid">'
                '<div class="biodata-reading-card">'
                f"<h5>{practical_heading}</h5>"
                f"{practical_intro}{performance_paragraph}{feature_paragraph}"
                "</div>"
                '<div class="biodata-reading-card">'
                f"<h5>{decision_heading}</h5>"
                f"{decision_status_html}{decision_paragraph}{impact_paragraph}"
                "</div></div>"
            )
            st.markdown(reading_html, unsafe_allow_html=True)

            with st.expander(tr("Limitaciones y controles recomendados")):
                if current_language() == "es":
                    st.markdown(
                        """
- **Métricas promedio:** pueden ocultar casos extremos o diferencias importantes entre grupos.
- **Validación interna:** el desempeño puede cambiar con otra población, laboratorio, región o período.
- **Predicción, no causalidad:** la utilidad de una variable no demuestra que sea la causa del resultado.
- **Sin intervalos individuales:** todavía no se cuantifica la incertidumbre de cada predicción.
                        """
                    )
                else:
                    st.markdown(
                        """
- **Average metrics:** can hide extreme cases or important differences between groups.
- **Internal validation:** performance may change in another population, laboratory, region or period.
- **Prediction, not causality:** a variable's usefulness does not prove that it causes the outcome.
- **No individual intervals:** uncertainty is not yet quantified for each prediction.
                        """
                    )

                st.info(
                    tr("Antes de tomar decisiones importantes: validá el modelo con datos nuevos, revisá los grupos relevantes y mantené supervisión humana.")
                )

            st.divider()
            st.markdown(f"#### {tr('Informe detallado')}")

            st.caption(
                tr("Descargá el perfil del dataset, la calidad de los datos, la comparación de modelos, las métricas, los diagnósticos y las recomendaciones en un único archivo.")
            )

            st.download_button(
                tr("Descargar informe completo (.txt)"),
                data=final_report.encode("utf-8"),
                file_name=(
                    f"biodata_report_{target_column}.txt"
                    if current_language() == "en"
                    else f"reporte_biodata_{target_column}.txt"
                ),
                mime="text/plain",
                type="primary"
            )
