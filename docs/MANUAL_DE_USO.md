# Manual de uso de Biodata

Biodata es una aplicación web para explorar datos tabulares, revisar su calidad y comparar modelos predictivos de regresión. Está pensada para acompañar el análisis: organiza el proceso, explica los resultados y muestra sus limitaciones, pero no reemplaza el criterio de quien conoce el problema.

## Recorrido rápido

Para completar un primer análisis:

1. Elegí el idioma y la apariencia desde **Preferencias**.
2. Cargá un archivo CSV, DATA o TXT desde la barra lateral.
3. Confirmá si la primera fila contiene los nombres de las columnas.
4. Revisá **Resumen** y **Exploración** antes de modelar.
5. En **Modelos**, elegí una variable objetivo numérica.
6. Conservá solo los predictores que estarían disponibles al realizar una predicción real.
7. Presioná **Analizar y comparar modelos**.
8. Leé las métricas, los diagnósticos y las limitaciones.
9. Si necesitás estudiar un caso nuevo, completá **Predecir una observación nueva**.
10. Descargá el informe para conservar el resultado.

## 1. Qué tipo de datos admite

Biodata trabaja con datos tabulares: cada fila representa una observación y cada columna representa una variable.

| especie | longitud_pico | masa_corporal | sexo | año |
|---|---:|---:|---|---:|
| Adelie | 39.1 | 3750 | macho | 2007 |
| Gentoo | 46.1 | 4500 | hembra | 2008 |

El archivo puede tener variables numéricas, variables categóricas y valores faltantes. La demostración pública admite archivos de hasta 25 MB.

La versión actual necesita una **variable objetivo numérica** porque resuelve problemas de regresión. Por ejemplo: predecir peso, longitud, concentración, rendimiento o tiempo.

## 2. Antes de cargar un archivo

Comprobá que:

- Cada columna tenga un significado único.
- Los nombres de columnas no estén repetidos.
- Los números estén almacenados como números y no mezclados con unidades como `25 kg`.
- Las categorías estén escritas de forma consistente; por ejemplo, no mezclar `hembra`, `Hembra` y `F` si significan lo mismo.
- La variable que querés predecir tenga suficientes valores conocidos y más de un valor diferente.
- El archivo no contenga datos personales, clínicos, confidenciales o regulados.

Si el archivo no tiene encabezados, desactivá **El archivo tiene nombres de columnas**. Biodata te permitirá asignarlos antes de continuar.

## 3. Preferencias de idioma y apariencia

En la barra lateral, abrí **Preferencias**.

- **Idioma / Language:** cambia la interfaz, los gráficos y el informe entre español e inglés.
- **Automático:** sigue el modo claro u oscuro del dispositivo.
- **Oscuro:** mantiene la interfaz oscura.
- **Claro:** mantiene la interfaz clara.

Cambiar estas preferencias no debería eliminar el archivo cargado ni los resultados conservados en la sesión.

## 4. Pestaña Resumen

Esta pestaña permite saber con qué datos se está trabajando antes de tomar decisiones.

- **Observaciones:** cantidad de filas.
- **Variables:** cantidad de columnas.
- **Valores faltantes:** celdas sin información.
- **Filas duplicadas:** filas completamente repetidas.

La vista previa muestra las primeras observaciones para verificar nombres, tipos de valores y estructura general. No representa necesariamente toda la distribución del dataset.

Biodata informa faltantes, valores infinitos y filas duplicadas. No elimina duplicados ni reemplaza el archivo original de manera automática. El objetivo es que esos problemas sean visibles y que la persona responsable decida si deben corregirse en la fuente.

## 5. Pestaña Exploración

Usá esta pestaña para comprender patrones, escalas y posibles problemas antes de entrenar modelos.

### Resumen numérico

Incluye promedio, desvío, mínimo, máximo y cuartiles. Ayuda a detectar escalas inesperadas y valores extremos.

### Resumen categórico

Muestra la frecuencia de las categorías más comunes. Permite encontrar categorías poco frecuentes, etiquetas inconsistentes o grupos muy desbalanceados.

### Distribución numérica

El histograma muestra cómo se reparten los valores de una variable. Puede revelar asimetría, concentraciones, huecos y posibles valores extremos.

### Distribución categórica

El gráfico de barras compara cuántas observaciones contiene cada categoría. Los faltantes se muestran como **Sin dato**.

### Correlaciones

La matriz de correlación resume relaciones lineales entre variables numéricas.

- Un valor cercano a `1` indica que suelen aumentar juntas.
- Un valor cercano a `-1` indica que una suele disminuir cuando la otra aumenta.
- Un valor cercano a `0` indica poca relación lineal.

Correlación no significa causalidad. Dos variables pueden moverse juntas sin que una produzca cambios en la otra.

## 6. Pestaña Modelos

### Paso 1: Variable objetivo

Es la variable numérica que se quiere estimar. Elegila según una pregunta concreta, por ejemplo: “¿Podemos estimar la masa corporal usando las medidas disponibles?”.

No elijas como objetivo un identificador, código o número de registro aunque sea numérico.

### Paso 2: Variables predictoras

Son los datos que el modelo utiliza para realizar la estimación.

Incluí únicamente variables que:

- Estarían disponibles al momento de predecir.
- Tengan una relación razonable con el problema.
- No revelen directamente el resultado que se quiere estimar.

Excluí identificadores únicos, información conocida solo después del resultado y variables creadas a partir del propio objetivo.

Incluir información futura o derivada del objetivo produce **fuga de información**: el modelo parece muy preciso durante la prueba, pero falla cuando se usa en situaciones reales.

### Paso 3: Contexto de uso

Esta sección opcional permite explicar para qué se utilizaría el resultado, qué error sería aceptable y qué grupos merecen atención. El informe usa ese contexto para ofrecer una interpretación más útil.

### Paso 4: Ejecutar análisis

Biodata:

1. Reserva el 20 % de las observaciones para la evaluación final.
2. Usa el 80 % restante para entrenar y comparar modelos.
3. Completa faltantes numéricos con la mediana calculada en el entrenamiento.
4. Completa faltantes categóricos con la categoría más frecuente del entrenamiento.
5. Convierte categorías a una representación que los modelos puedan utilizar.
6. Compara cuatro alternativas mediante validación cruzada.
7. Elige la de menor MAE promedio.
8. Evalúa una sola vez el modelo ganador con los datos reservados.

Las filas cuyo objetivo está vacío o es infinito se excluyen del modelado porque no existe un valor real con el cual aprender o evaluar.

## 7. Modelos comparados

- **Dummy:** usa una regla muy simple, como predecir el promedio. Sirve como referencia mínima.
- **Regresión lineal:** representa relaciones lineales entre predictores y objetivo.
- **Random Forest:** combina muchos árboles y puede aprender relaciones no lineales.
- **Gradient Boosting:** construye árboles sucesivos que intentan corregir los errores anteriores.

Que un modelo sea más complejo no garantiza que sea mejor. Biodata selecciona según el rendimiento medido, no por el nombre del algoritmo.

## 8. Cómo interpretar las métricas

### MAE

Es el error absoluto promedio y se expresa en las mismas unidades que el objetivo.

Si el MAE es `1.58` y el objetivo es peso en kilogramos, las predicciones se alejan en promedio unos `1.58 kg` del valor real.

Un valor menor es mejor, pero debe compararse con el error tolerable para el uso real.

### RMSE

También mide error, pero penaliza con más fuerza los errores grandes. Si es bastante mayor que el MAE, algunos casos pueden estar fallando mucho más que el promedio.

### R²

Indica qué proporción de la variabilidad observada logra representar el modelo.

- Cerca de `1`: explica gran parte de las diferencias observadas.
- Cerca de `0`: aporta poco frente a predecir un promedio.
- Menor que `0`: rinde peor que esa referencia simple en la prueba.

Un R² alto no demuestra causalidad ni garantiza que cada predicción individual sea precisa.

### Error P90

Es el valor por debajo del cual se encuentra el error del 90 % de los casos. Ayuda a mirar más allá del promedio.

### Residuo

Es la diferencia entre el valor real y la predicción. Revisar residuos ayuda a detectar sesgos, patrones no aprendidos y casos difíciles.

## 9. Diagnóstico e importancia de variables

### Valores reales frente a predicciones

Cuanto más cerca estén los puntos de la diagonal, más próximas son las predicciones a los valores reales.

### Gráficos de residuos

Un patrón claro puede indicar que el modelo no capturó parte de la estructura de los datos. Residuos concentrados de un solo lado pueden sugerir sobreestimación o subestimación sistemática.

### Importancia predictiva

Biodata altera cada variable y observa cuánto empeora el modelo. Una caída mayor indica mayor utilidad predictiva global.

Importancia no significa causa. Tampoco explica por sí sola una predicción individual.

### Errores por grupos

Si existen variables categóricas adecuadas, Biodata compara el error entre grupos con suficientes observaciones. Diferencias importantes deben revisarse antes de usar el modelo para decidir.

## 10. Cómo usar el resultado para decidir

Antes de usar el modelo:

1. Definí cuánto error es aceptable para el problema.
2. Compará ese límite con MAE, RMSE y P90.
3. Revisá los casos con errores más altos.
4. Comprobá si algún grupo recibe predicciones sistemáticamente peores.
5. Validá con datos nuevos de otro momento, lugar o población.
6. Mantené revisión humana en decisiones de impacto.

El modelo puede ayudar a ordenar, priorizar o revisar casos. No debería tomar decisiones importantes por sí solo.

### Predecir una observación nueva

Después de evaluar el modelo ganador con el conjunto de prueba reservado, Biodata vuelve a ajustarlo utilizando todos los casos válidos. Ese modelo final queda disponible durante la sesión para estimar el objetivo de una observación que no formaba parte del dataset.

1. Buscá la sección **Predecir una observación nueva** dentro de **Modelos**.
2. Ingresá las mediciones y categorías disponibles para el caso nuevo.
3. Conservá las mismas unidades y definiciones utilizadas en el dataset original.
4. Dejá vacío un campo solamente cuando ese dato sea realmente desconocido. Biodata aplicará la misma imputación utilizada durante el entrenamiento.
5. Presioná **Estimar nuevo caso**.
6. Leé la estimación junto con el MAE, el error P90 y las advertencias mostradas.

Biodata avisa si una medición está fuera del rango observado, si una categoría no apareció durante el entrenamiento, si faltan predictores o si la estimación queda fuera del rango conocido del objetivo. En esas situaciones, el modelo está trabajando con menos referencia y el error puede aumentar.

El MAE y el error P90 describen el rendimiento general del conjunto de prueba; no son un intervalo de certeza para ese caso particular. La estimación permanece en la memoria de la sesión y desaparece al cerrar o reiniciar la aplicación.

## 11. Informe descargable

El informe reúne el perfil y la calidad del dataset, el contexto, la comparación de modelos, la evaluación final, los diagnósticos, la importancia predictiva, la interpretación y las limitaciones.

El informe describe la sesión actual. Guardalo junto con la versión del dataset y la fecha del análisis para mantener trazabilidad.

## 12. Privacidad y límites

En la demostración pública, el archivo se transfiere a Streamlit Community Cloud y se procesa temporalmente en memoria. Biodata no guarda una copia permanente ni envía el contenido a otros servicios.

Usá únicamente datos públicos, sintéticos o de prueba. No cargues datos personales, clínicos, confidenciales o regulados.

Limitaciones actuales:

- Solo admite objetivos numéricos de regresión.
- La validación es interna y no reemplaza una prueba externa.
- No calcula intervalos individuales de incertidumbre.
- El modelo para casos nuevos permanece disponible solo durante la sesión actual.
- No demuestra relaciones causales.
- No reemplaza la revisión de una persona especialista en el área.

## 13. Problemas frecuentes

### No aparece una variable como objetivo

Debe ser numérica, tener al menos diez valores válidos y contener más de un valor diferente.

### Una columna numérica aparece como categórica

Revisá que no incluya unidades, símbolos o textos mezclados con los números.

### El modelo parece demasiado bueno

Buscá identificadores, información futura o variables derivadas del objetivo. Podría existir fuga de información.

### El resultado cambia con otro dataset

Es esperable si cambia la población, el período, el método de medición o la calidad de los datos. Volvé a validar y, si corresponde, actualizá el modelo.

### Aparece un error en la aplicación

Actualizá la página, quitá y volvé a cargar el archivo. Si continúa, anotá el paso realizado, el tipo de archivo y el mensaje mostrado, evitando compartir datos sensibles.

## Glosario esencial

- **Dataset:** conjunto organizado de datos.
- **Observación:** una fila del dataset.
- **Variable:** una característica almacenada en una columna.
- **Variable objetivo:** valor que se quiere predecir.
- **Predictor:** variable usada para estimar el objetivo.
- **Valor faltante:** dato ausente o desconocido.
- **Imputación:** reemplazo controlado de faltantes para poder modelar.
- **Entrenamiento:** etapa en la que el modelo aprende patrones.
- **Prueba:** datos reservados para evaluar el resultado final.
- **Validación cruzada:** comparación repetida de modelos usando distintas partes del entrenamiento.
- **Sobreajuste:** buen rendimiento en los datos conocidos y pobre rendimiento en datos nuevos.
- **Fuga de información:** uso accidental de información que no estaría disponible al predecir.
- **Regresión:** modelado de un objetivo numérico continuo.
- **Inferencia:** uso de un modelo ya entrenado para estimar el objetivo de una observación nueva.
- **Causalidad:** relación en la que un cambio produce otro; una predicción no la demuestra.

## Lista final antes de decidir

- [ ] Comprendí qué representa cada fila y cada variable.
- [ ] Revisé faltantes, infinitos, duplicados y valores extremos.
- [ ] Elegí un objetivo coherente con la pregunta.
- [ ] Excluí identificadores e información futura.
- [ ] Definí un error aceptable antes de mirar el resultado.
- [ ] Revisé MAE, RMSE, R² y P90.
- [ ] Revisé errores grandes y grupos relevantes.
- [ ] Los casos nuevos usan las mismas variables, definiciones y unidades del entrenamiento.
- [ ] Entiendo que importancia predictiva no significa causalidad.
- [ ] Voy a validar el modelo con datos nuevos.
- [ ] Mantendré supervisión humana para decisiones importantes.
