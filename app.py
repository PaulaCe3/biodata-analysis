import streamlit as st

from src.data_loader import load_dataset
from src.data_profiler import get_dataset_profile
from src.data_quality import get_quality_report

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
    split_features_target,
    split_train_test
)


# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

st.set_page_config(
    page_title="BioIA",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# ENCABEZADO
# =========================================================

st.title("🧬 BioIA")

st.write(
    "Herramienta para exploración, control de calidad "
    "y modelado de datos biológicos."
)


# =========================================================
# BARRA LATERAL
# =========================================================

with st.sidebar:

    st.header("Dataset")

    uploaded_file = st.file_uploader(
        "Seleccioná un archivo",
        type=["csv", "data", "txt"]
    )

    has_header = st.checkbox(
        "El archivo tiene nombres de columnas",
        value=True
    )

    st.divider()

    st.caption(
        "Los análisis se realizan localmente con Python."
    )


# =========================================================
# ESPERAR ARCHIVO
# =========================================================

if uploaded_file is None:

    st.info(
        "Subí un archivo desde la barra lateral para comenzar."
    )

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


# Dataset piloto conocido: UCI Abalone
if uploaded_file.name.lower() == "abalone.data":

    df = load_dataset(
        uploaded_file,
        header=None,
        column_names=abalone_columns
    )


# Cualquier otro dataset
else:

    header = "infer" if has_header else None

    df = load_dataset(
        uploaded_file,
        header=header
    )

    # Si el archivo no trae encabezados,
    # generamos nombres temporales comprensibles.
    if not has_header:

        df.columns = [
            f"Variable_{i + 1}"
            for i in range(df.shape[1])
        ]

# =========================================================
# NOMBRES DE COLUMNAS
# =========================================================

# Si el archivo no tiene encabezado, evitamos mostrar
# columnas como 0, 1, 2, 3...
# y generamos nombres neutros y comprensibles.

# =========================================================
# NOMBRES DE VARIABLES
# =========================================================

if not has_header:

    # Dataset piloto conocido: UCI Abalone
    if (
        uploaded_file.name.lower() == "abalone.data"
        and df.shape[1] == 9
    ):

        df.columns = [
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

    # Para cualquier otro archivo sin encabezados
    else:

        st.subheader("Nombres de las variables")

        st.info(
            "Este archivo no contiene encabezados. "
            "Asigná un nombre a cada columna antes de continuar."
        )

        new_column_names = []

        for i in range(df.shape[1]):

            column_name = st.text_input(
                f"Columna {i + 1}",
                value=f"Variable_{i + 1}",
                key=f"column_name_{i}"
            )

            new_column_names.append(column_name)

        df.columns = new_column_names


# =========================================================
# ANÁLISIS GENERAL
# =========================================================

profile = get_dataset_profile(df)

quality_report = get_quality_report(df)

numeric_summary = get_numeric_summary(df)

categorical_summary = get_categorical_summary(df)


# =========================================================
# DATASET ACTUAL
# =========================================================

st.success(
    f"Dataset cargado correctamente: {uploaded_file.name}"
)

st.caption(
    f"{profile['n_rows']} observaciones · "
    f"{profile['n_columns']} variables"
)


# =========================================================
# PESTAÑAS
# =========================================================

tab_summary, tab_eda, tab_model = st.tabs(
    [
        "Resumen",
        "Exploración",
        "Modelado"
    ]
)


# =========================================================
# TAB 1 — RESUMEN
# =========================================================

with tab_summary:

    # -----------------------------------------------------
    # MÉTRICAS GENERALES
    # -----------------------------------------------------

    st.header("Resumen del dataset")

    total_missing = sum(
        quality_report["missing_values"].values()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Observaciones",
        profile["n_rows"]
    )

    col2.metric(
        "Variables",
        profile["n_columns"]
    )

    col3.metric(
        "Valores faltantes",
        total_missing
    )

    col4.metric(
        "Filas duplicadas",
        quality_report["duplicate_rows"]
    )

    st.divider()


    # -----------------------------------------------------
    # VISTA PREVIA
    # -----------------------------------------------------

    st.subheader("Vista previa de datos")

    st.caption(
        "Primeras 10 observaciones del dataset."
    )

    st.dataframe(
        df.head(10),
        use_container_width=True,
        hide_index=True
    )

    st.divider()


    # -----------------------------------------------------
    # CALIDAD
    # -----------------------------------------------------

    st.subheader("Calidad de los datos")

    quality_col1, quality_col2 = st.columns(2)

    missing_with_values = {
        column: count
        for column, count
        in quality_report["missing_values"].items()
        if count > 0
    }

    with quality_col1:

        st.markdown("**Valores faltantes**")

        if missing_with_values:

            missing_table = {
                "Variable": list(
                    missing_with_values.keys()
                ),
                "Cantidad de faltantes": list(
                    missing_with_values.values()
                )
            }

            st.dataframe(
                missing_table,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.write(
                "No se detectaron valores faltantes."
            )

    with quality_col2:

        st.markdown("**Filas duplicadas**")

        if quality_report["duplicate_rows"] > 0:

            st.write(
                f"Se detectaron "
                f"{quality_report['duplicate_rows']} "
                f"filas duplicadas."
            )

        else:

            st.write(
                "No se detectaron filas duplicadas."
            )

    st.divider()


    # -----------------------------------------------------
    # ESTADÍSTICAS DESCRIPTIVAS
    # -----------------------------------------------------

    st.subheader("Estadísticas descriptivas")

    st.caption(
        "Resumen de las variables numéricas del dataset."
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
            "Variable",
            "N",
            "Media",
            "Desv. estándar",
            "Mínimo",
            "25 %",
            "Mediana",
            "75 %",
            "Máximo"
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
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No se detectaron variables numéricas."
        )

    st.divider()


    # -----------------------------------------------------
    # VARIABLES CATEGÓRICAS
    # -----------------------------------------------------

    st.subheader("Variables categóricas")

    if categorical_summary:

        for column, counts in categorical_summary.items():

            with st.expander(
                f"{column}"
            ):

                categorical_table = {
                    "Categoría": list(
                        counts.keys()
                    ),
                    "Frecuencia": list(
                        counts.values()
                    )
                }

                st.dataframe(
                    categorical_table,
                    use_container_width=True,
                    hide_index=True
                )

    else:

        st.info(
            "No se detectaron variables categóricas."
        )


# =========================================================
# TAB 2 — EXPLORACIÓN
# =========================================================

with tab_eda:

    st.header("Exploración de datos")

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

    st.subheader("Distribución de variable numérica")

    if numeric_columns:

        selected_numeric_column = st.selectbox(
            "Elegí una variable numérica",
            numeric_columns,
            key="numeric_distribution"
        )

        numeric_fig = plot_numeric_distribution(
            df,
            selected_numeric_column
        )

        st.pyplot(
            numeric_fig,
            use_container_width=True
        )

    else:

        st.info(
            "No hay variables numéricas para visualizar."
        )

    st.divider()


    # -----------------------------------------------------
    # DISTRIBUCIÓN CATEGÓRICA
    # -----------------------------------------------------

    st.subheader("Distribución de variable categórica")

    if categorical_columns:

        selected_categorical_column = st.selectbox(
            "Elegí una variable categórica",
            categorical_columns,
            key="categorical_distribution"
        )

        categorical_fig = plot_categorical_distribution(
            df,
            selected_categorical_column
        )

        st.pyplot(
            categorical_fig,
            use_container_width=True
        )

    else:

        st.info(
            "No hay variables categóricas para visualizar."
        )

    st.divider()


    # -----------------------------------------------------
    # CORRELACIONES
    # -----------------------------------------------------

    st.subheader("Mapa de correlaciones")

    if len(numeric_columns) >= 2:

        correlation_fig = plot_correlation_heatmap(
            df
        )

        st.pyplot(
            correlation_fig,
            use_container_width=True
        )

    else:

        st.info(
            "Se necesitan al menos dos variables numéricas "
            "para calcular correlaciones."
        )


# =========================================================
# TAB 3 — MODELADO
# =========================================================

with tab_model:

    st.header("Modelado")

    st.caption(
        "La versión actual de BioIA trabaja "
        "con problemas de regresión."
    )


    # -----------------------------------------------------
    # VARIABLES OBJETIVO VÁLIDAS
    # -----------------------------------------------------

    # Como todavía trabajamos solamente con regresión,
    # permitimos seleccionar únicamente targets numéricos.

    target_options = df.select_dtypes(
        include="number"
    ).columns.tolist()


    if not target_options:

        st.warning(
            "No hay variables numéricas disponibles "
            "para utilizar como variable objetivo."
        )


    else:

        # -------------------------------------------------
        # VARIABLE OBJETIVO
        # -------------------------------------------------

        st.subheader("Variable objetivo")

        target_column = st.selectbox(
            "Elegí la variable que querés predecir",
            target_options,
            index=len(target_options) - 1
        )

        X, y = split_features_target(
            df,
            target_column
        )

        feature_types = detect_feature_types(
            df,
            target_column=target_column
        )

        numeric_features = feature_types[
            "numeric_features"
        ]

        categorical_features = feature_types[
            "categorical_features"
        ]

        st.divider()


        # -------------------------------------------------
        # VARIABLES PREDICTORAS
        # -------------------------------------------------

        st.subheader("Variables predictoras")

        pred_col1, pred_col2 = st.columns(2)

        pred_col1.metric(
            "Variables numéricas",
            len(numeric_features)
        )

        pred_col2.metric(
            "Variables categóricas",
            len(categorical_features)
        )


        if numeric_features:

            numeric_text = ", ".join(
                str(column)
                for column in numeric_features
            )

            st.markdown(
                f"**Numéricas:** {numeric_text}"
            )

        else:

            st.markdown(
                "**Numéricas:** ninguna"
            )


        if categorical_features:

            categorical_text = ", ".join(
                str(column)
                for column in categorical_features
            )

            st.markdown(
                f"**Categóricas:** {categorical_text}"
            )

        else:

            st.markdown(
                "**Categóricas:** ninguna"
            )

        st.divider()


        # -------------------------------------------------
        # PREPARACIÓN
        # -------------------------------------------------

        st.subheader("Preparación de datos")

        st.caption(
            "Los datos se dividirán en 80 % entrenamiento "
            "y 20 % prueba. El preprocesamiento se ajustará "
            "únicamente con los datos de entrenamiento."
        )


        if st.button(
            "Preparar datos para modelado",
            type="primary"
        ):

            X_train, X_test, y_train, y_test = split_train_test(
                X,
                y
            )

            preprocessor = build_preprocessor(
                numeric_features,
                categorical_features
            )

            X_train_processed = preprocessor.fit_transform(
                X_train
            )

            X_test_processed = preprocessor.transform(
                X_test
            )

            st.success(
                "Datos preparados correctamente."
            )

            prep_col1, prep_col2, prep_col3 = st.columns(3)

            prep_col1.metric(
                "Entrenamiento",
                X_train.shape[0]
            )

            prep_col2.metric(
                "Prueba",
                X_test.shape[0]
            )

            prep_col3.metric(
                "Variables procesadas",
                X_train_processed.shape[1]
            )

            st.caption(
                "El preprocesador se ajustó únicamente con "
                "el conjunto de entrenamiento para evitar "
                "data leakage."
            )