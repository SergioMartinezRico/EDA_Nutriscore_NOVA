# Análisis Exploratorio de Datos (EDA): Coherencia NutriScore vs. Clasificación NOVA

## Descripción del Proyecto

Este proyecto consiste en un Análisis Exploratorio de Datos (EDA) cuyo objetivo principal es evaluar la coherencia y correlación entre dos sistemas clave de etiquetado de alimentos:

NutriScore (A a E): Evalúa la calidad nutricional del producto (contenido en calorías, azúcares, grasas saturadas, sodio, fibra, proteínas, frutas y verduras).

Clasificación NOVA (1 a 4): Evalúa el grado de procesamiento industrial del alimento.

El estudio busca determinar si un buen perfil nutricional (A/B en NutriScore) se alinea consistentemente con un bajo nivel de procesamiento (NOVA 1/2), o si existen productos ultraprocesados (NOVA 4) que logran una calificación NutriScore favorable.

## Dataset

Los datos utilizados provienen de la plataforma colaborativa Open Food Facts. Tras un proceso de limpieza y depuración, el dataset final comprende 3.534 productos que fueron analizados en profundidad.

## Hipótesis de Trabajo

El análisis se estructura en torno a las siguientes hipótesis clave:

H1: Un peor NutriScore implica mayor contenido en azúcar, grasa y sal.

H2: A mayor nivel de procesamiento (peor NOVA), peor NutriScore.

H3: Los productos bajos en calorías no siempre obtienen un buen NutriScore.

H4: Dentro de los productos ultraprocesados (NOVA 4), el NutriScore no diferencia bien la calidad nutricional.

H5: Los alimentos más consumidos en España tienden a tener bajo NutriScore y alto nivel NOVA.

## Hallazgos Principales (Resumen)

El EDA reveló una compleja relación entre los dos sistemas, destacando los siguientes puntos:

Correlación entre Nutrientes y NutriScore (H1): Se confirmó una fuerte correlación negativa: los peores NutriScores (D y E) presentan sistemáticamente los niveles más altos de azúcares, grasas y sodio.

Discrepancia NutriScore vs. NOVA (H2): Aunque existe una tendencia, se encontró una brecha significativa. Un porcentaje notable de productos ultraprocesados (NOVA 4) lograron obtener una calificación NutriScore 'A' o 'B', indicando que el sistema nutricional no penaliza suficientemente el grado de procesamiento industrial.

Polarización del Consumo (H5): El análisis de una "cesta de la compra" promedio reveló que el consumo está fuertemente polarizado: una alta proporción de alimentos son básicos sin procesar (NOVA 1), pero el grupo más grande de productos manufacturados son ultraprocesados (NOVA 4).

## Estructura del Repositorio

Archivo/Directorio

Contenido

EDA_Nutricore.ipynb 

El informe completo del análisis, incluyendo código, visualizaciones y conclusiones detalladas.

data/

Directorio que contiene el dataset original y/o el dataset limpio utilizado para el análisis.

utils/

Directorio que contiene los scripts necesarios para sacar datos de la API de OpenFoodFacts asi como las funciones, variables y main necesarios para sacar los gráficos del EDA

README.md

Este archivo.

Tecnología y Librerías

El análisis fue realizado utilizando el ecosistema de Python, con las siguientes librerías:

Pandas: Manipulación y limpieza de datos.

NumPy: Operaciones numéricas y matemáticas.

Matplotlib / Seaborn / Plotly: Visualización de datos y gráficos interactivos.

Autor

Sergio Martinez Rico
