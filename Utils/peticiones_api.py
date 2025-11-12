import pandas as pd
from functions import buscar_producto
from variables import productos
from time import sleep



# Busqueda en la API 
resultados = []
for i, prod in enumerate(productos, 1):
    print(f"Buscando ({i}/{len(productos)}): {prod}")
    data = buscar_producto(prod)
    resultados.append(data)
    sleep(0.5)  # Pequeña pausa para no saturar la API
# Convertir en DataFrame
df_api = pd.DataFrame(resultados)
df_api.to_csv("../Data/resultados_api.csv", index=False)