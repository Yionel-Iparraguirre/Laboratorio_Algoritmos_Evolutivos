import pandas as pd
import numpy as np
import random

print("==========================================")
print("EJERCICIO 07 - USANDO EL DATASET GRADES")
print("==========================================")
# --- Cargar datos ---
file_path = r'C:\Users\yolog\OneDrive\Escritorio\ACTIVIDADES\ALGORITMOS EVOLUTIVOS\LAB 05\Datasets.xlsx'
students_df = pd.read_excel(file_path, sheet_name='Students')
# Parámetros
num_teams = 5
team_size = 4

# --- Funciones de evaluación ---
def calcular_varianza_gpa(equipo):
    gpas = [students_df.loc[i, 'GPA'] for i in equipo]
    return np.var(gpas)

def penalizacion_skill(equipo):
    skills = [students_df.loc[i, 'Skill'] for i in equipo]
    unique_skills = set(skills)
    return len(unique_skills)  # Penaliza más si hay demasiados skills distintos en el equipo

def aptitud(equipos):
    aptitud_total = 0
    for equipo in equipos:
        aptitud_total += calcular_varianza_gpa(equipo)
        aptitud_total += penalizacion_skill(equipo)
    return aptitud_total

# --- Generar una solución inicial aleatoria ---
def generar_equipos_inicial():
    estudiantes = list(range(len(students_df)))
    random.shuffle(estudiantes)
    equipos = [estudiantes[i:i + team_size] for i in range(0, len(estudiantes), team_size)]
    return equipos

# --- Búsqueda de vecino: swap entre dos estudiantes ---
def vecino(equipos_actuales):
    equipos_vecino = [equipo[:] for equipo in equipos_actuales]  # Copiar equipos actuales
    equipo1_idx, equipo2_idx = random.sample(range(num_teams), 2)
    estudiante1_idx = random.randint(0, team_size - 1)
    estudiante2_idx = random.randint(0, team_size - 1)

    # Swap de estudiantes entre los equipos
    estudiante1 = equipos_vecino[equipo1_idx][estudiante1_idx]
    estudiante2 = equipos_vecino[equipo2_idx][estudiante2_idx]
    equipos_vecino[equipo1_idx][estudiante1_idx] = estudiante2
    equipos_vecino[equipo2_idx][estudiante2_idx] = estudiante1

    return equipos_vecino

# --- Algoritmo de búsqueda local (Hill Climbing) ---
def hill_climbing(iteraciones=10000):
    equipos = generar_equipos_inicial()
    mejor_equipos = equipos
    mejor_aptitud = aptitud(equipos)

    for _ in range(iteraciones):
        nueva_asignacion = vecino(mejor_equipos)
        nueva_aptitud = aptitud(nueva_asignacion)

        # Si la nueva asignación tiene mejor aptitud (menor aptitud total)
        if nueva_aptitud < mejor_aptitud:
            mejor_equipos = nueva_asignacion
            mejor_aptitud = nueva_aptitud

    return mejor_equipos, mejor_aptitud

# --- Ejecución ---
if __name__ == "__main__":
    equipos_finales, aptitud_total = hill_climbing()

    # Mostrar los equipos finales
    print("\nEquipos finales:")
    for idx, equipo in enumerate(equipos_finales):
        print(f"Equipo {idx+1}:")
        for estudiante in equipo:
            print(f"  - {students_df.loc[estudiante, 'StudentID']} - GPA: {students_df.loc[estudiante, 'GPA']} - Skill: {students_df.loc[estudiante, 'Skill']}")
        print()

    print(f"\nAptitud total de la asignación: {aptitud_total}")