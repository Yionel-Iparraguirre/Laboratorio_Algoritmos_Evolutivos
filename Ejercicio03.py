
import random
import pandas as pd
import numpy as np
file_path = r'C:\Users\yolog\OneDrive\Escritorio\ACTIVIDADES\ALGORITMOS EVOLUTIVOS\LAB 05\Datasets.xlsx'
dist_df = pd.read_excel(file_path, sheet_name='LabDistances', index_col=0)
# Convertir a matriz numpy para velocidad
dist_matrix = dist_df.values
labs = dist_df.index.tolist()  # nombres de laboratorios

print("==========================================")
print("EJERCICIO 03 - USANDO EL DATASET LABDISTANCES")
print("==========================================")
# --- Funciones ---
def calcular_distancia_total(ruta, dist_matrix):
    distancia = 0
    n = len(ruta)
    for i in range(n):
        distancia += dist_matrix[ruta[i], ruta[(i+1)%n]]
    return distancia

def vecino_intercambio(ruta_actual):
    vecino = ruta_actual[:]
    i, j = random.sample(range(len(ruta_actual)), 2)
    vecino[i], vecino[j] = vecino[j], vecino[i]
    return vecino

def busqueda_local(dist_matrix, iteraciones=10000):
    n = dist_matrix.shape[0]
    # Solución inicial aleatoria
    ruta = list(range(n))
    random.shuffle(ruta)
    mejor_ruta = ruta
    mejor_dist = calcular_distancia_total(ruta, dist_matrix)

    for _ in range(iteraciones):
        vecino = vecino_intercambio(mejor_ruta)
        dist_vecino = calcular_distancia_total(vecino, dist_matrix)
        if dist_vecino < mejor_dist:
            mejor_ruta = vecino
            mejor_dist = dist_vecino

    return mejor_ruta, mejor_dist

# --- Ejecución ---
if __name__ == "__main__":
    mejor_ruta, mejor_dist = busqueda_local(dist_matrix)
    ruta_nombres = [labs[i] for i in mejor_ruta]
    print("Ruta óptima de visita:")
    print(" -> ".join(ruta_nombres))
    print(f"Distancia total mínima: {mejor_dist:.2f} metros")