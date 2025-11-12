#importar bibliotecas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from time import sleep
import warnings
warnings.filterwarnings("ignore")
from variables import *
from functions import *


df = cargar_csv(ruta_csv_inicial)
"""
Primeros pasos: distribucion de variables Nutri
"""
# Mapeo de Variables Numéricas (Necesario para el conteo)
nutri_map = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
# Creamos la columna 'nutriscore_num' para el resto del análisis
df['nutriscore_num'] = df['off:nutriscore_grade'].map(nutri_map)
len(df['nutriscore_num'])
#  Distribución del Grado NutriScore (Calidad) 
nutri_distribucion = (df['off:nutriscore_grade'].value_counts(normalize=True).sort_index() * 100)

# Preparación de datos para el gráfico

nutri_df_inicial = nutri_distribucion.reindex(nutri_orden, fill_value=0).rename('Porcentaje').reset_index()
nutri_df_inicial.columns = ['Grado', 'Porcentaje']
nutri_df_inicial['Grado'] = nutri_df_inicial['Grado'].str.upper()

# Generación del Gráfico
plt.figure(figsize=(8, 6))
ax = sns.barplot(
    x='Grado', 
    y='Porcentaje', 
    data=nutri_df_inicial, 
    order=['A', 'B', 'C', 'D', 'E'],
    palette=colores
)

plt.title('Distribución Inicial del NutriScore en el Dataset', fontsize=14)
plt.xlabel('Grado NutriScore')
plt.ylabel('Porcentaje de Productos (%)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.ylim(0, nutri_df_inicial['Porcentaje'].max() * 1.1)

# Añadir etiquetas de porcentaje encima de las barras
for p in ax.patches:
    ax.annotate(
        f"{p.get_height():.1f}%", 
        (p.get_x() + p.get_width() / 2., p.get_height()), 
        ha='center', va='center', 
        xytext=(0, 9), 
        textcoords='offset points'
    )

plt.savefig("../Img/distribucion_nutri.jpg")

"""
Primeros pasos: distribucion de variables Nova
"""

#  Mapeo de Variables Numéricas (Necesario para el conteo)
df['nova_group'] = df['off:nova_groups_tags'].astype(str).str.extract(r'(\d)').astype(float) # Creamos la columna 'nova_group' (1 a 4)
#  Distribución del Grupo NOVA (Procesamiento)
nova_distribucion = (df['nova_group'].value_counts(normalize=True).sort_index() * 100)
# Convertir a DataFrame para graficos
nova_df_inicial = nova_distribucion.rename('Porcentaje').reset_index()
nova_df_inicial.columns = ['Grupo NOVA', 'Porcentaje']
nova_df_inicial['Grupo NOVA'] = nova_df_inicial['Grupo NOVA'].astype(int)
nova_df_inicial = nova_df_inicial.sort_values(by='Grupo NOVA') # Asegura el orden 1 a 4

# Generación del Gráfico
plt.figure(figsize=(8, 6))
ax = sns.barplot(
    x='Grupo NOVA', 
    y='Porcentaje', 
    data=nova_df_inicial, 
    order=[1,2,3,4],
    palette=colores
)

plt.title('Distribución Inicial del Grupo NOVA en el Dataset', fontsize=14)
plt.xlabel('Grupo NOVA (1: Mínimo Procesamiento | 4: Ultraprocesado)')
plt.ylabel('Porcentaje de Productos (%)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.ylim(0, nova_df_inicial['Porcentaje'].max() * 1.1)

# Añadir etiquetas de porcentaje encima de las barras
for p in ax.patches:
    ax.annotate(
        f"{p.get_height():.1f}%", 
        (p.get_x() + p.get_width() / 2., p.get_height()), 
        ha='center', va='center', 
        xytext=(0, 9), 
        textcoords='offset points'
    )

plt.savefig("../Img/distribucion_nova.jpg")


"""
Hipotesis 1
"""

# Columnas necesarias para la H1: NutriScore y los 3 nutrientes malos.
columnas_h1 = ['off:nutriscore_grade', 'sugars_value', 'fat_value', 'salt_value']

# Crear el DataFrame específico eliminando filas con NaN en las columnas clave
df_h1 = df.dropna(subset=columnas_h1).copy()

#graficos

df_h1 = df_h1[df_h1['off:nutriscore_grade'].isin(nutri_orden)]

# Definimos las variables a analizar y el orden del NutriScore
nutrientes = ['sugars_value', 'fat_value', 'salt_value']
titulos = ['Contenido de Azúcares (g/100g)', 'Contenido de Grasa (g/100g)', 'Contenido de Sal (g/100g)']


# Creamos la figura que contendrá los 3 gráficos
fig, axes = plt.subplots(1, 3, figsize=(20, 7), sharey=False)
plt.suptitle('H1: Distribución de Nutrientes Clave por Grado NutriScore (Tendencia Creciente)', fontsize=16)

for i, nutriente in enumerate(nutrientes):
    sns.boxplot(
        x='off:nutriscore_grade',
        y=nutriente,
        data=df_h1,
        order=nutri_orden,
        ax=axes[i],
        palette=colores,
        showfliers=False  # Ocultamos los outliers para mayor claridad en la tendencia central
    )
    
    
    # Añadimos etiquetas y título
    axes[i].set_title(titulos[i])
    axes[i].set_xlabel('Grado NutriScore')
    axes[i].set_ylabel(nutriente.replace('_value', '').capitalize() + ' (g/100g)')
    axes[i].grid(axis='y', linestyle='--', alpha=0.7)

plt.savefig("../Img/h1_boxplots.jpg")

# --- MEDIANAS POR NUTRISCORE ---
medianas = (
    df_h1.groupby('off:nutriscore_grade')[['sugars_value', 'fat_value', 'salt_value']]
    .median()
    .reindex(nutri_orden)
    .reset_index()
)

# --- GRÁFICO DE MEDIANAS ---
plt.figure(figsize=(8,5))
plt.plot(medianas['off:nutriscore_grade'], medianas['sugars_value'], marker='o', label='Azúcares')
plt.plot(medianas['off:nutriscore_grade'], medianas['fat_value'], marker='o', label='Grasas')
plt.plot(medianas['off:nutriscore_grade'], medianas['salt_value'], marker='o', label='Sal')
plt.title("Medianas de nutrientes por NutriScore")
plt.xlabel("NutriScore (A = mejor, E = peor)")
plt.ylabel("g/100g")
plt.legend()
plt.grid(True)
plt.savefig("../Img/h1_medianas.jpg")


"""
Hipotesis 2
"""

# Columnas necesarias para la H2: NutriScore numérico y el Grupo NOVA.
columnas_h2 = ['nutriscore_num', 'nova_group']

# Crear el DataFrame específico eliminando filas con NaN en las columnas clave 
df_h2 = df.dropna(subset=columnas_h2).copy()

# Calcular el NutriScore promedio para cada Grupo NOVA
promedio_nutriscore_por_nova = df_h2.groupby('nova_group')['nutriscore_num'].mean().reset_index()
promedio_nutriscore_por_nova.columns = ['Grupo_NOVA', 'NutriScore_Promedio']

#graficos

orden_nutri =[1,2,3,4,5]
valores_nutri=["A","B","C","D","E"]
plt.figure(figsize=(9, 6))
ax=sns.barplot(
    x='Grupo_NOVA',
    y='NutriScore_Promedio',
    data=promedio_nutriscore_por_nova,
    palette=colores,
    order=orden_nova 

)
ax.xaxis.set_ticks_position('top')
ax.xaxis.set_label_position('top')
ax.spines['bottom'].set_visible(False)
plt.title('H2: NutriScore Promedio por Nivel de Procesamiento NOVA,')
plt.xlabel('Grupo NOVA (1: Mínimo Procesamiento, 4: Ultraprocesado)')
plt.ylabel('NutriScore Promedio (Peor → E, Mejor → A)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.gca().invert_yaxis() 
plt.ylim(5, 1)
plt.yticks(orden_nutri,valores_nutri)

plt.savefig("../Img/h2_barplots.jpg")


"""
hipotesis 3
"""

umbral_calorias= 100

#Columnas necesarias: NutriScore y Calorías
columnas_h3 = ['off:nutriscore_grade', 'energy-kcal_value']

#Crear el DataFrame, primero eliminando NaN en las columnas clave y luego filtrando
df_h3_temp = df.dropna(subset=columnas_h3).copy()

#Aplicar el filtro de bajo valor calórico. Nos quedamos solo los que tienen menos de 100 calorias
df_h3 = df_h3_temp[df_h3_temp['energy-kcal_value'] < umbral_calorias].copy()

# Calcular la distribución porcentual en df_h3
distribucion_h3 = (df_h3['off:nutriscore_grade'].value_counts(normalize=True).reindex(nutri_orden) * 100)

distribucion_df = distribucion_h3.rename('Porcentaje').reset_index()
distribucion_df.columns = ['Grado', 'Porcentaje']
distribucion_df['Grado'] = distribucion_df['Grado'].str.upper()

#graficos

plt.figure(figsize=(8, 6))
sns.barplot(
    x='Grado', 
    y='Porcentaje', 
    data=distribucion_df, 
    order=['A', 'B', 'C', 'D', 'E'],
    palette=colores
)

plt.title('H3: Distribución del NutriScore en Productos Bajos en Calorías (< 100 kcal/100g)', fontsize=14)
plt.xlabel('Grado NutriScore')
plt.ylabel('Porcentaje de Productos (%)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.ylim(0, distribucion_df['Porcentaje'].max() * 1.1)

# Añadir etiquetas de porcentaje encima de las barras
for index, row in distribucion_df.iterrows():
    plt.text(
        index, 
        row['Porcentaje'] + 1, 
        f"{row['Porcentaje']:.1f}%", 
        color='black', 
        ha="center",
        fontsize=10
    )
plt.savefig("../Img/h3_barplots.jpg")

"""
Hipotesis 4
"""
grupo_nova = 4.0

#Columnas necesarias: NutriScore, NOVA, y los 3 nutrientes malos.
columnas_h4 = ['off:nutriscore_grade', 'nova_group', 'sugars_value', 'fat_value', 'salt_value']

#Crear el DataFrame, primero eliminando NaN en las columnas clave y luego filtrando
df_h4_temp = df.dropna(subset=columnas_h4).copy()

#Aplicar el filtro para quedarnos solo con los ultraprocesados
df_h4 = df_h4_temp[df_h4_temp['nova_group'] == grupo_nova].copy()

#graficos

#  Definimos la configuración para los gráficos
nutrientes = ['sugars_value', 'fat_value', 'salt_value']
titulos = [
    'Azúcares (g/100g) en Ultraprocesados', 
    'Grasa (g/100g) en Ultraprocesados', 
    'Sal (g/100g) en Ultraprocesados'
]

#  Creamos la figura que contendrá los 3 gráficos (1 fila, 3 columnas)
fig, axes = plt.subplots(1, 3, figsize=(20, 7), sharey=False)
plt.suptitle('H4: Variabilidad Nutricional dentro de Productos Ultraprocesados (NOVA 4)', fontsize=16)

for i, nutriente in enumerate(nutrientes):
    sns.boxplot(
        x='off:nutriscore_grade',
        y=nutriente,
        data=df_h4,
        order=nutri_orden,
        ax=axes[i],
        palette=colores,
        # Ocultamos los outliers para que la caja y los bigotes sean más claros
        showfliers=False 
    )
    
    # Añadimos etiquetas y título
    axes[i].set_title(titulos[i])
    axes[i].set_xlabel('Grado NutriScore (Solo Productos NOVA 4)')
    axes[i].set_ylabel(nutriente.replace('_value', '').capitalize())
    axes[i].grid(axis='y', linestyle='--', alpha=0.7)

# Ajustamos el layout
plt.tight_layout()
plt.savefig("../Img/h4_boxplots.jpg")

"""
Hipotesis 5
"""
df_api = cargar_csv(ruta_csv_cesta)

# Limpieza de NaN en las columnas clave (NutriScore y NOVA)
# Reemplazamos 'nan' y convertimos nova_group a numérico
df_api['nova_group'] = pd.to_numeric(df_api['nova_group'], errors='coerce')
df_h5 = df_api.dropna(subset=['nutriscore_grade', 'nova_group']).copy()

# Cálculo de las distribuciones porcentuales
# --- NutriScore ---
nutri_distribucion = (df_h5['nutriscore_grade'].str.upper().value_counts(normalize=True).reindex(['A', 'B', 'C', 'D', 'E']) * 100).fillna(0)
nutri_df = nutri_distribucion.rename('Porcentaje').reset_index()

# --- NOVA Group ---
nova_distribucion = (df_h5['nova_group'].value_counts(normalize=True).sort_index() * 100).fillna(0)
nova_df = nova_distribucion.rename('Porcentaje').reset_index()
nova_df['Grupo NOVA'] = nova_df['nova_group'].astype(int)

#graficos

fig, axes = plt.subplots(1, 2, figsize=(15, 6))
plt.suptitle('H5: Distribución de NutriScore y NOVA en la Lista de la Compra (Alimentos Consumidos)', fontsize=16)

# GRAFICO 1: DISTRIBUCIÓN NUTRISCORE
sns.barplot(
    x='nutriscore_grade', 
    y='Porcentaje', 
    data=nutri_df, 
    order=['A', 'B', 'C', 'D', 'E'],
    palette=colores,
    ax=axes[0]
    
)
axes[0].set_title('NutriScore en la Lista de la Compra')
axes[0].set_xlabel('Grado NutriScore')
axes[0].set_ylabel('Porcentaje de Productos (%)')
#axes[0].set
axes[0].grid(axis='y', linestyle='--', alpha=0.7)

# Etiquetas
for index, row in nutri_df.iterrows():
    axes[0].text(
        index, row['Porcentaje'] + 1, f"{row['Porcentaje']:.1f}%", color='black', ha="center", fontsize=9, 
    )

# GRAFICO 2: DISTRIBUCIÓN NOVA
sns.barplot(
    x='Grupo NOVA', 
    y='Porcentaje', 
    data=nova_df, 
    order=[1, 2, 3, 4],
    palette=colores_nova, # Colores NOVA
    ax=axes[1]
)
axes[1].set_title('Grupo NOVA en la Lista de la Compra')
axes[1].set_xlabel('Grupo NOVA (1: Mínimo Proc. | 4: Ultraproc.)')
axes[1].set_ylabel('Porcentaje de Productos (%)')
axes[1].grid(axis='y', linestyle='--', alpha=0.7)

# Etiquetas
for index, row in nova_df.iterrows():
    axes[1].text(
        index, row['Porcentaje'] + 1, f"{row['Porcentaje']:.1f}%", color='black', ha="center", fontsize=9
    )

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("../Img/h5_barplots.jpg")

