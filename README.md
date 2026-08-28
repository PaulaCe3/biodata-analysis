# Biodata — análisis y modelado de datos biológicos

Biodata es una aplicación web de Ciencia de Datos para explorar, validar y
construir modelos predictivos con conjuntos de datos biológicos tabulares. La
versión actual trabaja con problemas de regresión y prioriza resultados
comprensibles, auditables y útiles como apoyo a decisiones.

## Aplicación en línea

[Abrir Biodata](https://biodata-analysis.streamlit.app/)

## Funcionalidades

- Carga de archivos CSV, DATA y TXT, con o sin encabezados.
- Perfil general y control de valores faltantes, infinitos y duplicados.
- Resúmenes y visualizaciones exploratorias.
- Separación reproducible entre entrenamiento y prueba.
- Preprocesamiento sin fuga de información.
- Selección de predictores para excluir identificadores o variables no disponibles.
- Comparación por validación cruzada de Dummy, regresión lineal, Random Forest
  y Gradient Boosting.
- Evaluación final con MAE, RMSE y R².
- Gráficos de valores reales, predicciones y residuos.
- Casos con mayor error y comparación de rendimiento por grupos categóricos.
- Importancia predictiva por permutación sobre las variables originales.
- Advertencias automáticas mediante reglas transparentes.
- Informe descargable con contexto, diagnóstico y recomendaciones.

## Inicio rápido

### 1. Crear y activar el entorno

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

```powershell
streamlit run app.py
```

Subí un dataset, abrí **Modelos**, elegí una variable objetivo numérica y
presioná **Analizar y comparar modelos**.

## Cómo interpretar los resultados

- **MAE:** distancia promedio entre la predicción y el valor real, expresada en
  unidades de la variable objetivo.
- **RMSE:** también mide error, pero penaliza más los errores grandes.
- **R²:** proporción de la variabilidad observada que el modelo logra explicar.
- **Error P90:** el 90 % de los casos tiene un error igual o menor a ese valor.
- **Importancia por permutación:** cuánto empeora el modelo al alterar una
  variable. Indica utilidad predictiva, no causalidad.

Antes de usar el modelo, definí un error tolerable, revisá los casos extremos y
los subgrupos relevantes, y validá el desempeño con datos nuevos. Para decisiones
de alto impacto, Biodata debe utilizarse como apoyo con supervisión humana.

## Pruebas

Las pruebas se ejecutan localmente y no llaman a servicios externos:

```powershell
python -m unittest discover -s tests -v
```

Cubren carga y validación de datos, flujo completo de regresión, diagnósticos,
gráficos e informe.

## Arquitectura

```text
app.py
  ├─ carga y perfilado            src/data_loader.py · src/data_profiler.py
  ├─ calidad y exploración        src/data_quality.py · src/eda.py
  ├─ preparación y entrenamiento  src/preprocessing.py · src/modeling.py
  ├─ evaluación                   src/evaluation.py
  ├─ diagnóstico y explicabilidad src/diagnostics.py
  └─ informe descargable          src/report.py
```

El conjunto de prueba se utiliza una sola vez después de seleccionar el modelo
mediante validación cruzada. Los resultados del modelado se conservan en la
sesión de Streamlit para evitar reentrenamientos al interactuar con el informe.

## Despliegue en Streamlit Community Cloud

La demostración pública se encuentra disponible en
[biodata-analysis.streamlit.app](https://biodata-analysis.streamlit.app/). El
despliegue utiliza la rama `main` y `app.py` como archivo principal.

Referencias oficiales:

- [Desplegar una app](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)

## Privacidad de la demostración pública

- Se admiten archivos CSV, DATA y TXT de hasta 25 MB.
- El dataset se transfiere al servidor de Streamlit Community Cloud en Estados
  Unidos y se procesa temporalmente en memoria durante la sesión.
- Biodata no guarda el archivo de forma permanente ni envía su contenido a
  otros servicios.
- Streamlit elimina el archivo de la memoria cuando la persona lo reemplaza,
  lo quita o cierra la pestaña.
- La demostración está destinada a datos públicos, sintéticos o de prueba.
- No deben cargarse datos personales, clínicos, confidenciales o regulados.

Referencias oficiales:

- [Almacenamiento temporal de archivos](https://docs.streamlit.io/knowledge-base/using-streamlit/where-file-uploader-store-when-deleted)
- [Seguridad de Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/trust-and-security)

## Limitaciones actuales

- Solo se admiten objetivos numéricos de regresión.
- No se calculan intervalos de predicción individuales.
- La importancia de variables es global y no explica cada predicción particular.
- Una validación interna no reemplaza una evaluación con datos externos.
- Los resultados predictivos no demuestran causalidad.

## Estado

Versión gratuita funcional para análisis, comparación, diagnóstico,
interpretación e informe de modelos de regresión, publicada en Streamlit
Community Cloud.
