"""Textos de interfaz de Biodata en español e inglés."""


ENGLISH = {
    "Preferencias": "Preferences",
    "Personalizá Biodata sin perder el archivo ni los resultados de la sesión.": (
        "Customize Biodata without losing the file or results stored in the session."
    ),
    "Idioma": "Language",
    "Apariencia": "Appearance",
    "Automático": "Automatic",
    "Oscuro": "Dark",
    "Claro": "Light",
    "Sigue la configuración visual de tu dispositivo.": (
        "Follows your device appearance settings."
    ),
    "Manual de uso": "User guide",
    "Abrir manual de uso": "Open user guide",
    "Guía para cargar, explorar, modelar e interpretar datos con criterio.": (
        "A guide to uploading, exploring, modeling and interpreting data responsibly."
    ),
    "El contenido se adapta al idioma seleccionado.": (
        "The content follows the selected language."
    ),
    "Descargar manual (.md)": "Download user guide (.md)",
    "No se pudo cargar el manual. Volvé a intentarlo en unos minutos.": (
        "The user guide could not be loaded. Please try again in a few minutes."
    ),
    "Espacio de trabajo": "Workspace",
    "Nuevo análisis": "New analysis",
    "Cargá un dataset biológico tabular para iniciar el análisis.": (
        "Upload a tabular biological dataset to begin the analysis."
    ),
    "Archivo de datos": "Data file",
    "Formatos admitidos: CSV, DATA y TXT. Tamaño máximo: 25 MB.": (
        "Supported formats: CSV, DATA and TXT. Maximum size: 25 MB."
    ),
    "Usá datos públicos o de prueba. No subas información personal, clínica, confidencial o regulada.": (
        "Use public or test data. Do not upload personal, clinical, confidential or regulated information."
    ),
    "El archivo tiene nombres de columnas": "The file has column names",
    "Desactivá esta opción si la primera fila contiene datos y no los nombres de las variables.": (
        "Turn this option off when the first row contains data rather than variable names."
    ),
    "Procesamiento y privacidad": "Processing and privacy",
    "El archivo se transfiere a los servidores de Streamlit Community Cloud en Estados Unidos y se procesa temporalmente en memoria. Biodata no guarda una copia permanente ni lo envía a otros servicios. Al cerrar la pestaña, reemplazar o quitar el archivo, deja de estar disponible.": (
        "The file is transferred to Streamlit Community Cloud servers in the United States and processed temporarily in memory. Biodata does not keep a permanent copy or send it to other services. It is removed when you close the tab, replace it or delete it."
    ),
    "Versión 1 · Análisis y modelos predictivos": (
        "Version 1 · Data analysis and predictive models"
    ),
    "Análisis de datos y modelos predictivos": (
        "Data analysis and predictive models"
    ),
    "Modelos predictivos integrados": "Integrated predictive models",
    "Análisis de datos y predicción": "Data analysis and prediction",
    "Entendé tus datos antes de tomar decisiones.": (
        "Understand your data before making decisions."
    ),
    "Biodata combina el análisis exploratorio con modelos predictivos. Estos modelos usan aprendizaje automático (machine learning) para detectar patrones y estimar resultados con datos nuevos.": (
        "Biodata combines exploratory analysis with predictive models. These models use machine learning to detect patterns and estimate outcomes for new data."
    ),
    "Calidad de datos": "Data quality",
    "Etapas disponibles": "Available stages",
    "Exploración visual": "Visual exploration",
    "Modelos predictivos": "Predictive models",
    "Diseñado para trabajar con criterio": "Designed for responsible use",
    "Prueba separada": "Separate test set",
    "El resultado final se evalúa con datos reservados.": (
        "The final result is evaluated with held-out data."
    ),
    "Errores visibles": "Visible errors",
    "Las métricas se traducen a una lectura práctica.": (
        "Metrics are translated into practical meaning."
    ),
    "Límites explícitos": "Explicit limitations",
    "El informe aclara qué no puede concluir el modelo.": (
        "The report explains what the model cannot conclude."
    ),
    "Un proceso claro, desde los datos hasta la decisión.": (
        "A clear process, from data to decision."
    ),
    "Primero se comprenden los datos, después se comparan modelos y al final se traducen sus resultados, errores y limitaciones.": (
        "First understand the data, then compare models, and finally translate their results, errors and limitations."
    ),
    "Análisis de datos": "Data analysis",
    "Prepará y comprendé": "Prepare and understand",
    "Revisá faltantes, duplicados, tipos de variables y distribuciones antes de entrenar un modelo.": (
        "Review missing values, duplicates, variable types and distributions before training a model."
    ),
    "Entrená y compará": "Train and compare",
    "Biodata prueba varias alternativas para aprender patrones. Las compara de forma justa y evalúa la mejor con datos que no vio.": (
        "Biodata tests several alternatives for learning patterns, compares them fairly and evaluates the best one on unseen data."
    ),
    "Evaluación e informe": "Evaluation and report",
    "Interpretá y decidí": "Interpret and decide",
    "Entendé el error, revisá los casos difíciles y descargá un informe que explique resultados, controles y limitaciones.": (
        "Understand the error, review difficult cases and download a report explaining results, safeguards and limitations."
    ),
    "Para comenzar:": "To begin:",
    "si es tu primera vez, abrí el manual de uso. Después seleccioná un archivo desde la barra lateral para iniciar el análisis.": (
        "if this is your first visit, open the user guide. Then select a file from the sidebar to begin the analysis."
    ),
    "Nombres de las variables": "Variable names",
    "Este archivo no contiene encabezados. Asigná un nombre a cada columna antes de continuar.": (
        "This file has no headers. Assign a name to every column before continuing."
    ),
    "Columna {number}": "Column {number}",
    "Variable_{number}": "Variable_{number}",
    "Dataset cargado correctamente: {filename}": (
        "Dataset uploaded successfully: {filename}"
    ),
    "{rows} observaciones · {columns} variables": (
        "{rows} observations · {columns} variables"
    ),
    "Resumen": "Overview",
    "Exploración": "Explore",
    "Modelos": "Models",
    "Resumen del dataset": "Dataset overview",
    "Observaciones": "Observations",
    "Variables": "Variables",
    "Variable": "Variable",
    "Valores faltantes": "Missing values",
    "Filas duplicadas": "Duplicate rows",
    "Vista previa de datos": "Data preview",
    "Primeras 10 observaciones del dataset.": "First 10 observations in the dataset.",
    "Calidad de los datos": "Data quality",
    "Valores infinitos": "Infinite values",
    "Cantidad de faltantes": "Missing count",
    "Cantidad": "Count",
    "No se detectaron valores faltantes.": "No missing values were detected.",
    "En el modelado se tratarán como valores faltantes.": (
        "They will be treated as missing values during modeling."
    ),
    "No se detectaron valores infinitos.": "No infinite values were detected.",
    "Se detectaron {count} filas duplicadas.": "{count} duplicate rows were detected.",
    "No se detectaron filas duplicadas.": "No duplicate rows were detected.",
    "Estadísticas descriptivas": "Descriptive statistics",
    "Resumen de las variables numéricas del dataset.": (
        "Summary of the dataset's numeric variables."
    ),
    "Media": "Mean",
    "Desv. estándar": "Std. deviation",
    "Mínimo": "Minimum",
    "Mediana": "Median",
    "Máximo": "Maximum",
    "No se detectaron variables numéricas.": "No numeric variables were detected.",
    "Variables categóricas": "Categorical variables",
    "Categoría": "Category",
    "Frecuencia": "Frequency",
    "Se muestran las {shown} categorías más frecuentes de {total}.": (
        "Showing the {shown} most frequent categories out of {total}."
    ),
    "No se detectaron variables categóricas.": "No categorical variables were detected.",
    "Exploración de datos": "Data exploration",
    "Distribución de variable numérica": "Numeric variable distribution",
    "Distribución de {column}": "Distribution of {column}",
    "Elegí una variable numérica": "Choose a numeric variable",
    "No hay variables numéricas para visualizar.": "There are no numeric variables to display.",
    "Distribución de variable categórica": "Categorical variable distribution",
    "Elegí una variable categórica": "Choose a categorical variable",
    "No hay variables categóricas para visualizar.": (
        "There are no categorical variables to display."
    ),
    "Mapa de correlaciones": "Correlation map",
    "Mapa de calor de correlaciones": "Correlation heatmap",
    "Correlación": "Correlation",
    "Variables incluidas en el mapa": "Variables included in the map",
    "Elegí entre 2 y 20 variables. Limitar el mapa ayuda a mantenerlo legible en datasets grandes.": (
        "Choose between 2 and 20 variables. Limiting the map keeps large datasets readable."
    ),
    "Seleccioná al menos dos variables para construir el mapa.": (
        "Select at least two variables to build the map."
    ),
    "Se necesitan al menos dos variables numéricas para calcular correlaciones.": (
        "At least two numeric variables are required to calculate correlations."
    ),
    "Estos modelos usan aprendizaje automático (machine learning) para aprender patrones y estimar un resultado numérico. Configurá el problema, compará alternativas y revisá su desempeño antes de utilizarlo.": (
        "These models use machine learning to learn patterns and estimate a numeric outcome. Define the problem, compare alternatives and review performance before using the result."
    ),
    "Objetivo": "Target",
    "Predictores": "Predictors",
    "Contexto": "Context",
    "Comparación": "Comparison",
    "Aplicación": "Application",
    "No hay una variable objetivo numérica con al menos 10 valores válidos y dos valores diferentes.": (
        "There is no numeric target with at least 10 valid values and two distinct values."
    ),
    "Configuración": "Setup",
    "1. Variable objetivo": "1. Target variable",
    "Es la medida numérica que querés que el modelo estime.": (
        "This is the numeric measure you want the model to estimate."
    ),
    "Variable a predecir": "Variable to predict",
    "Datos disponibles": "Available data",
    "Filas con objetivo válido": "Rows with a valid target",
    "Objetivo seleccionado: {target}": "Selected target: {target}",
    "Se excluyeron {count} filas porque la variable objetivo no tenía un valor numérico válido.": (
        "{count} rows were excluded because the target did not contain a valid numeric value."
    ),
    "2. Variables predictoras": "2. Predictor variables",
    "Las variables predictoras son las pistas que usará el modelo para estimar {target}. Podés mantener todas o quitar las que no correspondan al uso real.": (
        "Predictor variables are the information the model will use to estimate {target}. Keep all relevant variables or remove those that would not be available in real use."
    ),
    "¿Por qué importa? Si el modelo recibe información que no existiría en una situación real, puede mostrar resultados demasiado buenos que después no se repiten.": (
        "Why does this matter? If the model receives information that would not exist in a real situation, its results may look unrealistically good and fail later."
    ),
    "Variables incluidas": "Included variables",
    "Usá la X de cada etiqueta para quitar una variable. Esto no borra la columna del archivo: solo evita que el modelo la utilice.": (
        "Use the X on each label to remove a variable. This does not delete the column from the file; it only prevents the model from using it."
    ),
    "Biodata excluyó variables vacías o no compatibles: {variables}": (
        "Biodata excluded empty or unsupported variables: {variables}"
    ),
    "Seleccioná al menos una variable predictora.": "Select at least one predictor variable.",
    "Revisá estas variables: tienen muchas categorías y podrían ser identificadores: {variables}.": (
        "Review these variables: they contain many categories and may be identifiers: {variables}."
    ),
    "{selected} variables seleccionadas · {numeric} numéricas · {categorical} categóricas": (
        "{selected} selected variables · {numeric} numeric · {categorical} categorical"
    ),
    "Ver detalle de las variables seleccionadas": "View selected variable details",
    "Ninguna": "None",
    "Numéricas": "Numeric",
    "Categóricas": "Categorical",
    "3. Contexto de uso (recomendado)": "3. Use context (recommended)",
    "Ayuda a convertir las métricas en recomendaciones útiles. No modifica el entrenamiento.": (
        "This helps turn metrics into useful recommendations. It does not change training."
    ),
    "¿Cuál es el objetivo del análisis?": "What is the purpose of the analysis?",
    "Ejemplo: estimar la edad para priorizar muestras que necesitan una revisión especializada.": (
        "Example: estimate age to prioritize samples that need specialist review."
    ),
    "¿Qué decisión querés apoyar con el resultado?": (
        "What decision do you want the result to support?"
    ),
    "Ejemplo: decidir qué casos revisar primero, sin reemplazar la evaluación de una persona especialista.": (
        "Example: decide which cases to review first without replacing specialist assessment."
    ),
    "Audiencia del informe": "Report audience",
    "Público general": "General audience",
    "Equipo técnico": "Technical team",
    "Equipo científico": "Scientific team",
    "Responsables de decisión": "Decision makers",
    "Impacto de la decisión": "Decision impact",
    "Bajo": "Low",
    "Medio": "Medium",
    "Alto": "High",
    "Crítico": "Critical",
    "Error máximo tolerable": "Maximum tolerable error",
    "Usá 0 si todavía no fue definido.": "Use 0 if it has not been defined yet.",
    "4. Ejecutar análisis": "4. Run analysis",
    "Biodata reservará 20 % de los datos para la prueba final y comparará los modelos solo con el conjunto de entrenamiento.": (
        "Biodata will reserve 20% of the data for final testing and compare models using only the training set."
    ),
    "Analizar y comparar modelos": "Analyze and compare models",
    "Preparando datos, comparando modelos y generando diagnósticos...": (
        "Preparing data, comparing models and generating diagnostics..."
    ),
    "Ejecutá el análisis para ver la comparación, los diagnósticos y el informe final.": (
        "Run the analysis to view the comparison, diagnostics and final report."
    ),
    "Resultados": "Results",
    "Modelo seleccionado": "Selected model",
    "Menor MAE en la validación cruzada": "Lowest MAE in cross-validation",
    "División de los datos": "Data split",
    "Entrenamiento / prueba": "Training / test",
    "Variables procesadas": "Processed variables",
    "Después del preprocesamiento": "After preprocessing",
    "Modelo": "Model",
    "MAE promedio (CV)": "Mean MAE (CV)",
    "Ver comparación de los cuatro modelos": "Compare all four models",
    "La comparación usa únicamente el entrenamiento. Un MAE menor representa un error promedio menor.": (
        "The comparison uses training data only. A lower MAE represents a lower average error."
    ),
    "Rendimiento en datos de prueba": "Performance on test data",
    "Error promedio": "Average error",
    "Penaliza errores grandes": "Penalizes large errors",
    "Ajuste global": "Overall fit",
    "El 90 % queda por debajo": "90% falls below this value",
    "Las métricas y los gráficos siguientes se calcularon sobre el conjunto de prueba reservado. El preprocesador se ajustó solo con entrenamiento para evitar filtraciones.": (
        "The following metrics and charts were calculated on the held-out test set. Preprocessing was fitted on training data only to prevent leakage."
    ),
    "No se activaron advertencias con las reglas diagnósticas actuales.": (
        "No warnings were triggered by the current diagnostic rules."
    ),
    "Predecir una observación nueva": "Predict a new observation",
    "Ingresá las mediciones o características de un caso nuevo. Biodata aplicará la misma preparación utilizada durante el entrenamiento y estimará {target}.": (
        "Enter the measurements or characteristics of a new case. Biodata will apply the same preparation used during training and estimate {target}."
    ),
    "Para esta etapa, el modelo seleccionado se ajustó nuevamente con todos los casos válidos. Las métricas mostradas siguen proviniendo del conjunto de prueba reservado.": (
        "For this stage, the selected model was fitted again using all valid cases. The displayed metrics still come from the held-out test set."
    ),
    "Volvé a ejecutar el análisis para habilitar predicciones con casos nuevos.": (
        "Run the analysis again to enable predictions for new cases."
    ),
    "En la prueba, este modelo rindió peor que una estimación basada en el promedio. Podés explorar un caso, pero no conviene utilizar la predicción para decidir.": (
        "On the test set, this model performed worse than a mean-based estimate. You can explore a case, but the prediction should not be used for decision-making."
    ),
    "Usá las mismas unidades y definiciones del dataset original. Los campos vacíos se completarán con la referencia aprendida durante el entrenamiento.": (
        "Use the same units and definitions as the original dataset. Empty fields will be filled using the reference learned during training."
    ),
    "Datos del nuevo caso": "New case data",
    "Completá solamente la información que realmente conocés antes de obtener el resultado.": (
        "Enter only the information that is genuinely available before the outcome is known."
    ),
    "Ingresá un valor o dejalo vacío": "Enter a value or leave it empty",
    "Rango observado durante el entrenamiento: {minimum} a {maximum}.": (
        "Range observed during training: {minimum} to {maximum}."
    ),
    "Seleccioná o escribí un valor": "Select or enter a value",
    "Podés elegir una categoría conocida, escribir una nueva o dejar el campo vacío.": (
        "You can select a known category, enter a new one or leave the field empty."
    ),
    "Estimar nuevo caso": "Estimate new case",
    "Ingresá al menos un dato del caso nuevo antes de solicitar la estimación.": (
        "Enter at least one value for the new case before requesting an estimate."
    ),
    "No se pudo calcular la estimación con los valores ingresados. Revisá los datos y volvé a intentarlo.": (
        "The estimate could not be calculated from the entered values. Review the data and try again."
    ),
    "La estimación estará disponible mientras esta sesión de Biodata permanezca abierta.": (
        "The estimate will remain available while this Biodata session stays open."
    ),
    "Estimación de {target}": "Estimated {target}",
    "En las mismas unidades utilizadas en el dataset": (
        "In the same units used in the dataset"
    ),
    "Referencia en datos de prueba": "Test-set reference",
    "El 90 % de los errores fue igual o menor a {p90}. No es un intervalo individual.": (
        "Ninety percent of errors were at or below {p90}. This is not an individual interval."
    ),
    "No se ingresaron valores para: {variables}. Biodata los completó con la mediana o la categoría más frecuente del entrenamiento; la estimación puede ser menos representativa.": (
        "No values were entered for: {variables}. Biodata filled them using the training median or most frequent category, so the estimate may be less representative."
    ),
    "Estas variables están fuera del rango observado durante el entrenamiento: {variables}. El modelo está extrapolando y el error puede ser mayor.": (
        "These variables fall outside the range observed during training: {variables}. The model is extrapolating and the error may be larger."
    ),
    "Estas categorías no aparecían en el entrenamiento: {variables}. El modelo puede aprovechar menos información para este caso.": (
        "These categories were not present during training: {variables}. The model may have less useful information for this case."
    ),
    "Los valores ingresados están dentro de las referencias observadas durante el entrenamiento.": (
        "The entered values are within the references observed during training."
    ),
    "La estimación queda fuera del rango conocido de la variable objetivo. Interpretala con especial cautela.": (
        "The estimate falls outside the known target range. Interpret it with particular caution."
    ),
    "Ver los datos utilizados en esta estimación": (
        "View the data used for this estimate"
    ),
    "Esta es una estimación estadística, no una medición confirmada ni una explicación causal. Para decisiones importantes, contrastala con observaciones reales y criterio especializado.": (
        "This is a statistical estimate, not a confirmed measurement or a causal explanation. For important decisions, compare it with real observations and specialist judgment."
    ),
    "Posible sesgo sistemático": "Possible systematic bias",
    "subestimar": "underestimate",
    "sobreestimar": "overestimate",
    "El residuo promedio es {residual:.3f}. El modelo muestra una tendencia general a {direction} los valores.": (
        "The mean residual is {residual:.3f}. The model shows an overall tendency to {direction} values."
    ),
    "Errores extremos relevantes": "Relevant extreme errors",
    "El 10 % de los casos con mayor error supera aproximadamente {error:.3f} unidades. Conviene revisarlos antes de tomar decisiones de alto impacto.": (
        "The 10% of cases with the largest errors exceed approximately {error:.3f} units. Review them before making high-impact decisions."
    ),
    "Diferencia de rendimiento en {feature}": "Performance difference in {feature}",
    "El grupo {group} presenta el mayor MAE ({mae:.3f}). Revisá si esta diferencia es aceptable para el uso previsto.": (
        "Group {group} has the highest MAE ({mae:.3f}). Review whether this difference is acceptable for the intended use."
    ),
    "Diagnóstico del modelo": "Model diagnostics",
    "Explorá cómo se distribuyen los errores, qué variables aportan información y qué casos conviene revisar.": (
        "Explore how errors are distributed, which variables add information and which cases deserve review."
    ),
    "Predicciones": "Predictions",
    "Residuos": "Residuals",
    "Variables importantes": "Important variables",
    "Casos a revisar": "Cases to review",
    "Cuanto más cerca esté un punto de la línea diagonal, más cercana fue la predicción al valor real.": (
        "The closer a point is to the diagonal line, the closer the prediction was to the actual value."
    ),
    "Valor real de {target}": "Actual {target}",
    "Predicción de {target}": "Predicted {target}",
    "Valores reales frente a predicciones": "Actual values versus predictions",
    "Valor predicho": "Predicted value",
    "Residuo (real − predicción)": "Residual (actual − predicted)",
    "Errores a lo largo de las predicciones": "Errors across predictions",
    "Cantidad de casos": "Number of cases",
    "Distribución de errores": "Error distribution",
    "Aumento del MAE al alterar la variable": "MAE increase after changing the variable",
    "Importancia predictiva por permutación": "Permutation predictive importance",
    "Un patrón aleatorio alrededor de cero es deseable. Patrones o desplazamientos persistentes pueden indicar sesgo o relaciones que el modelo no aprendió.": (
        "A random pattern around zero is desirable. Persistent patterns or shifts may indicate bias or relationships the model did not learn."
    ),
    "La importancia por permutación muestra utilidad predictiva: no demuestra que una variable cause el resultado.": (
        "Permutation importance shows predictive usefulness; it does not prove that a variable causes the outcome."
    ),
    "Casos con mayor error": "Cases with the largest errors",
    "Rendimiento por grupos": "Performance by group",
    "No hay grupos categóricos con suficientes casos para comparar su rendimiento.": (
        "No categorical groups have enough cases for a performance comparison."
    ),
    "Informe final": "Final report",
    "Resumen de resultados, diagnósticos y recomendaciones para interpretar el modelo de forma responsable.": (
        "Summary of results, diagnostics and recommendations for responsible model interpretation."
    ),
    "Menor error promedio en la validación cruzada": "Lowest average error in cross-validation",
    "Error promedio (MAE)": "Average error (MAE)",
    "unidades": "units",
    "por predicción de {target}": "per {target} prediction",
    "R² en datos de prueba": "R² on test data",
    "de la variabilidad observada en la prueba": "of the variation observed in the test set",
    "rinde peor que predecir usando el promedio": "performs worse than predicting the mean",
    "Lectura rápida": "Quick interpretation",
    "¿Qué significa en la práctica?": "What does this mean in practice?",
    "¿Cómo usar esta información?": "How should this information be used?",
    "Limitaciones y controles recomendados": "Recommended limitations and safeguards",
    "Antes de tomar decisiones importantes: validá el modelo con datos nuevos, revisá los grupos relevantes y mantené supervisión humana.": (
        "Before making important decisions, validate the model with new data, review relevant groups and maintain human oversight."
    ),
    "Informe detallado": "Detailed report",
    "Descargá el perfil del dataset, la calidad de los datos, la comparación de modelos, las métricas, los diagnósticos y las recomendaciones en un único archivo.": (
        "Download the dataset profile, data quality, model comparison, metrics, diagnostics and recommendations in a single file."
    ),
    "Descargar informe completo (.txt)": "Download full report (.txt)",
    "Regresión lineal": "Linear regression",
    "Sin dato": "Missing"
}


def translate(text, language="es", **values):
    """Devuelve una cadena localizada y aplica valores con nombre."""

    template = ENGLISH.get(text, text) if language == "en" else text
    return template.format(**values) if values else template


def model_label(model_name, language="es"):
    """Localiza nombres de modelos sin cambiar sus claves internas."""

    return translate(str(model_name), language)
