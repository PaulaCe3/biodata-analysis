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


st.set_page_config(
    page_title="BioIA",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 BioIA")

st.write(
    "Asistente para análisis de datos biológicos."
)

st.subheader("Subir un archivo de datos")

uploaded_file = st.file_uploader(
    "Seleccioná un archivo",
    type=["csv", "data", "txt"]
)

has_header = st.checkbox(
    "El archivo tiene nombres de columnas",
    value=True
)

header = "infer" if has_header else None


if uploaded_file is not None:

    df = load_dataset(
        uploaded_file,
        header=header
    )
    profile = get_dataset_profile(df)
quality_report = get_quality_report(df)
numeric_summary = get_numeric_summary(df)
categorical_summary = get_categorical_summary(df)
st.success("Dataset cargado correctamente.")
st.subheader("Resumen del dataset")
st.subheader("Calidad de datos")
st.subheader("Resumen estadístico")

st.dataframe(
    numeric_summary
)
st.subheader("Distribución de variable numérica")

numeric_columns = numeric_summary.columns.tolist()

selected_numeric_column = st.selectbox(
    "Elegí una variable numérica",
    numeric_columns
)

fig = plot_numeric_distribution(
    df,
    selected_numeric_column
)

st.pyplot(fig)
st.subheader("Mapa de correlaciones")

correlation_fig = plot_correlation_heatmap(df)

st.pyplot(correlation_fig)

st.subheader("Resumen categórico")

for column, counts in categorical_summary.items():

    st.write(f"Variable: {column}")

    st.dataframe(
        {
            "Categoría": list(counts.keys()),
            "Frecuencia": list(counts.values())
        }
    )
    if categorical_summary:

     st.subheader("Distribución de variable categórica")

categorical_columns = list(
        categorical_summary.keys()
    )

selected_categorical_column = st.selectbox(
        "Elegí una variable categórica",
        categorical_columns
    )

fig = plot_categorical_distribution(
        df,
        selected_categorical_column
    )

st.pyplot(fig)


total_missing = sum(
    quality_report["missing_values"].values()
)

col3, col4 = st.columns(2)

col3.metric(
    "Valores faltantes",
    total_missing
)

col4.metric(
    "Filas duplicadas",
    quality_report["duplicate_rows"]
)

col1, col2 = st.columns(2)

col1.metric(
    "Filas",
    profile["n_rows"]
)

col2.metric(
    "Columnas",
    profile["n_columns"]
)

st.write("Vista previa de los datos:")

st.dataframe(
        df.head()
    )

