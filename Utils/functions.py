import pandas as pd
import requests
import numpy as np
from variables import *


# Función de búsqueda en la API de OpenFoodFacts
def buscar_producto(nombre_producto):
    
    """
    funcion que busca en la api de openfoodfacts por un nombre de producto
    devuelve un json con marca,categoria,nutriscore,nova y valores de nutrientes
    """
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": nombre_producto,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1  # Solo el primer resultado
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["products"]:
            prod = data["products"][0]
            return {
                "product_input": nombre_producto,
                "product_found": prod.get("product_name"),
                "brand": prod.get("brands"),
                "category": prod.get("main_category"),
                "nutriscore_grade": prod.get("nutriscore_grade"),
                "nova_group": prod.get("nova_group"),
                "energy_100g": prod.get("nutriments", {}).get("energy_100g"),
                "sugars_100g": prod.get("nutriments", {}).get("sugars_100g"),
                "salt_100g": prod.get("nutriments", {}).get("salt_100g"),
                "fat_100g": prod.get("nutriments", {}).get("fat_100g"),
                "saturated_fat_100g": prod.get("nutriments", {}).get("saturated-fat_100g"),
            }
    return {
        "product_input": nombre_producto,
        "product_found": None,
        "brand": None,
        "category": None,
        "nutriscore_grade": None,
        "nova_group": None,
        "energy_100g": None,
        "sugars_100g": None,
        "salt_100g": None,
        "fat_100g": None,
        "saturated_fat_100g": None,
    }

def map_category(category_text):
       
    """
    Aplica el mapeo para asignar una Categoría de Nivel 1.
    """
    sorted_keywords = sorted(category_mapping.keys(), key=len, reverse=True)
    if pd.isna(category_text):
        return np.nan # Dejar el NaN original para su posterior imputación
    
    text = str(category_text).lower()
    
    for keyword in sorted_keywords:
        if keyword in text:
            # Devuelve la primera coincidencia (la más larga/específica)
            return category_mapping[keyword]
            
    # Si no se encuentra ninguna palabra clave
    return "Otros / Sin Coincidencia"

def cargar_csv(archivo):

    """
    funcion para cargar un csv en un df
    requiere meter la ruta del archivo en string
    """
    try:
        df = pd.read_csv(archivo) 
        print("Dataset cargado correctamente\n")
        return df
    except FileNotFoundError:
        print(f"Error: Asegúrate de que el archivo {archivo} está en el directorio correcto.")
