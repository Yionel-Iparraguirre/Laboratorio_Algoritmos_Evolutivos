import pandas as pd
import numpy as np
import random
from collections import defaultdict
file_path = r'C:\Users\yolog\OneDrive\Escritorio\ACTIVIDADES\ALGORITMOS EVOLUTIVOS\LAB 05\Datasets.xlsx'
tesistas_df = pd.read_excel(file_path, sheet_name='Tesistas')
print("==========================================")
print("EJERCICIO 05 - USANDO EL DATASET GRADES")
print("==========================================")
# Parámetros
tesistas = tesistas_df['TesistaID'].tolist()
num_tesistas = len(tesistas)
num_franjas = 6 
num_salas = 6    
max_horas_continuas = 4

# --- Inicializar horarios y asignaciones ---
def generar_asignacion_inicial():
    """Genera una asignación inicial aleatoria de tesistas a franjas y salas"""
    asignacion = []
    for _ in range(num_tesistas):
        disponibles = tesistas_df.iloc[_, 1:].values  # Obtener las franjas disponibles para el tesista
        franjas_disponibles = [i for i, val in enumerate(disponibles) if val == 1]
        if franjas_disponibles:
            franja = random.choice(franjas_disponibles)
            sala = random.randint(0, num_salas - 1)  # Asignar sala aleatoriamente
            asignacion.append((franja, sala))
        else:
            asignacion.append((-1, -1))  # No asignar si no hay franjas disponibles
    return asignacion

# --- Función para evaluar solapamientos y huecos ---
def evaluar_asignacion(asignacion):
    """Evaluar los solapamientos y huecos en la asignación actual."""
    # Contar solapamientos por sala y franja
    solapamientos = defaultdict(int)
    horarios = defaultdict(list)  # Almacena la lista de tesistas por franja y sala

    for i, (franja, sala) in enumerate(asignacion):
        if franja != -1:
            horarios[(franja, sala)].append(i)

    # Contamos los solapamientos (más de un tesista en la misma sala y franja)
    for key, tesistas_en_sala in horarios.items():
        if len(tesistas_en_sala) > 1:
            solapamientos[key] = len(tesistas_en_sala) - 1  # Solapamiento es la cantidad de tesistas extra

    # Verificar que ninguna sala tenga más de 4 horas continuas
    horas_continuas_excedidas = 0
    for sala in range(num_salas):
        tesistas_en_sala = [i for i, (franja, sala_asignada) in enumerate(asignacion) if sala_asignada == sala]
        franjas_asignadas = [asignacion[i][0] for i in tesistas_en_sala]
        franjas_asignadas.sort()

        # Verificar bloques de 4 horas continuas
        for i in range(len(franjas_asignadas) - max_horas_continuas + 1):
            if franjas_asignadas[i + max_horas_continuas - 1] - franjas_asignadas[i] == max_horas_continuas - 1:
                horas_continuas_excedidas += 1

    # Los huecos son el número de franjas no ocupadas por ningún tesista
    franjas_ocupadas = set([franja for franja, _ in asignacion if franja != -1])
    huecos = num_franjas - len(franjas_ocupadas)

    return sum(solapamientos.values()), huecos, horas_continuas_excedidas

# --- Generar un vecino moviendo un tesista ---
def vecino(asignacion_actual):
    """Genera un vecino cambiando la asignación de un tesista a una nueva franja o sala."""
    asignacion_vecino = asignacion_actual[:]
    idx = random.randint(0, len(asignacion_actual) - 1)
    disponibles = tesistas_df.iloc[idx, 1:].values  # Obtener las franjas disponibles para el tesista
    franjas_disponibles = [i for i, val in enumerate(disponibles) if val == 1]
    if franjas_disponibles:
        nueva_franja = random.choice(franjas_disponibles)
        nueva_sala = random.randint(0, num_salas - 1)
        asignacion_vecino[idx] = (nueva_franja, nueva_sala)
    return asignacion_vecino

# --- Algoritmo de búsqueda local ---
def hill_climbing(iteraciones=10000):
    """Algoritmo de búsqueda local para encontrar la mejor asignación."""
    asignacion = generar_asignacion_inicial()
    mejor_asignacion = asignacion
    mejor_solapamientos, mejor_huecos, mejor_horas_continuas = evaluar_asignacion(asignacion)

    for _ in range(iteraciones):
        nueva_asignacion = vecino(mejor_asignacion)
        solapamientos, huecos, horas_continuas = evaluar_asignacion(nueva_asignacion)

        if solapamientos < mejor_solapamientos or (solapamientos == mejor_solapamientos and huecos < mejor_huecos):
            mejor_asignacion = nueva_asignacion
            mejor_solapamientos = solapamientos
            mejor_huecos = huecos
            mejor_horas_continuas = horas_continuas

    return mejor_asignacion, mejor_solapamientos, mejor_huecos, mejor_horas_continuas

# --- Ejecución ---
if __name__ == "__main__":
    asignacion_final, solapamientos, huecos, horas_continuas_excedidas = hill_climbing()

    # Mostrar calendario
    calendario = defaultdict(list)
    for idx, (franja, sala) in enumerate(asignacion_final):
        if franja != -1:
            calendario[f"F{franja+1}_S{sala+1}"].append(tesistas[idx])

    print("Calendario de defensas de tesis:")
    for key, tesistas_lista in calendario.items():
        # Imprimir los tesistas directamente, sin intentar indexar
        print(f"{key}: {', '.join(tesistas_lista)}")

    print(f"\nMétricas de la asignación:")
    print(f"Solapamientos totales: {solapamientos}")
    print(f"Cantidad de huecos (franjas sin tesistas): {huecos}")
    print(f"Cantidad de horas continuas excedidas: {horas_continuas_excedidas}")