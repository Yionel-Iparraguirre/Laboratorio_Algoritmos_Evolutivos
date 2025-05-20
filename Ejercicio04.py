import pandas as pd
import numpy as np
import random

print("==========================================")
print("EJERCICIO 04 - USANDO EL DATASET PROJECTS")
print("==========================================")

# --- Cargar datos ---
file_path = r'C:\Users\yolog\OneDrive\Escritorio\ACTIVIDADES\ALGORITMOS EVOLUTIVOS\LAB 05\Datasets.xlsx'
projects_df = pd.read_excel(file_path, sheet_name='Projects')

# Usamos las columnas correctas
costs = projects_df['Cost_Soles'].values
benefits = projects_df['Benefit_Soles'].values
budget_limit = 10000

# --- Función objetivo ---
def beneficio_penalizado(bitstring):
    total_cost = sum(c * b for c, b in zip(costs, bitstring))
    total_benefit = sum(b * s for b, s in zip(benefits, bitstring))
    if total_cost > budget_limit:
        penalty = 10 * (total_cost - budget_limit)
        return total_benefit - penalty
    else:
        return total_benefit

# --- Generar solución inicial ---
def solucion_inicial():
    return [random.choice([0, 1]) for _ in range(len(costs))]

# --- Vecino cambiando un bit ---
def vecino(bitstring):
    vecino = bitstring[:]
    idx = random.randint(0, len(bitstring) -1)
    vecino[idx] = 1 - vecino[idx]  # Flips 0<->1
    return vecino

# --- Búsqueda local ---
def hill_climbing(iteraciones=10000):
    solucion = solucion_inicial()
    mejor_valor = beneficio_penalizado(solucion)
    mejor_solucion = solucion

    for _ in range(iteraciones):
        nueva_solucion = vecino(mejor_solucion)
        nuevo_valor = beneficio_penalizado(nueva_solucion)
        if nuevo_valor > mejor_valor:
            mejor_valor = nuevo_valor
            mejor_solucion = nueva_solucion

    return mejor_solucion, mejor_valor

# --- Ejecución ---
if __name__ == "__main__":
    seleccion, beneficio_total = hill_climbing()
    seleccion_proyectos = [projects_df.loc[i, 'ProjectID'] for i, val in enumerate(seleccion) if val == 1]

    print("Proyectos seleccionados:")
    for p in seleccion_proyectos:
        print(p)
    print(f"Beneficio total penalizado: {beneficio_total:.2f}")