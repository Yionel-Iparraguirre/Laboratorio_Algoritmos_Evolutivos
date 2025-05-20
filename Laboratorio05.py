import pandas as pd
import numpy as np
file_path = r'C:\Users\yolog\OneDrive\Escritorio\ACTIVIDADES\ALGORITMOS EVOLUTIVOS\LAB 05\Datasets.xlsx'

print("==========================================")
print("EJERCICIO 01 - USANDO EL DATASET GRADES")
print("==========================================")
grades_df = pd.read_excel(file_path, sheet_name='Grades')
# Calcular promedio por estudiante
grades_df['Promedio'] = grades_df[['Parcial1', 'Parcial2', 'Parcial3']].mean(axis=1)

# Definir rango de offsets
offsets = np.arange(-5, 5.5, 0.5)

# Variables para guardar resultados óptimos
best_offset = None
best_pass_percentage = -1
best_adjusted_grades = None

for offset in offsets:
    # Aplicar offset
    adjusted = grades_df['Promedio'] + offset
    
    # Limitar notas mínimas a 0 y máximas a 20 si quieres (opcional)
    adjusted = adjusted.clip(lower=0, upper=20)
    
    # Calcular porcentaje de aprobados (≥ 11)
    pass_percentage = (adjusted >= 11).mean() * 100
    
    # Calcular promedio total
    avg_grade = adjusted.mean()
    
    # Verificar condiciones para actualización del mejor offset
    if avg_grade <= 14:
        if pass_percentage > best_pass_percentage:
            best_pass_percentage = pass_percentage
            best_offset = offset
            best_adjusted_grades = adjusted

print(f'Offset óptimo: {best_offset}')
print(f'Porcentaje de aprobados con offset óptimo: {best_pass_percentage:.2f}%')
print(f'Promedio total con offset óptimo: {best_adjusted_grades.mean():.2f}')

print("==========================================")
print("EJERCICIO 02 - USANDO EL DATASET MENTOR AVAILABILITY")
print("==========================================")
import random

# --- Cargar datos ---
file_path = r'C:\Users\yolog\OneDrive\Escritorio\ACTIVIDADES\ALGORITMOS EVOLUTIVOS\LAB 05\Datasets.xlsx'
df = pd.read_excel(file_path, sheet_name='MentorAvailability')  # Ajusta nombre si difiere

# --- Preparación ---
slot_cols = [col for col in df.columns if col.startswith('Slot')]
bloques_disponibles = [(i, i+1) for i in range(len(slot_cols)-1)]

# --- Funciones ---
def contar_choques(df, asignacion):
    choques = 0
    for idx, mentor in enumerate(df.itertuples(index=False)):
        slot_a = slot_cols[asignacion[idx][0]]
        slot_b = slot_cols[asignacion[idx][1]]
        if getattr(mentor, slot_a) == 0:
            choques += 1
        if getattr(mentor, slot_b) == 0:
            choques += 1
    return choques

def asignacion_inicial():
    return [random.choice(bloques_disponibles) for _ in range(len(df))]

def vecino(asignacion_actual):
    nueva_asignacion = asignacion_actual[:]
    idx = random.randint(0, len(df) - 1)
    nueva_opcion = random.choice(bloques_disponibles)
    nueva_asignacion[idx] = nueva_opcion
    return nueva_asignacion

def hill_climbing(df, iteraciones=1000):
    asignacion = asignacion_inicial()
    mejor_choque = contar_choques(df, asignacion)

    for _ in range(iteraciones):
        nueva_asignacion = vecino(asignacion)
        nuevo_choque = contar_choques(df, nueva_asignacion)

        if nuevo_choque < mejor_choque:
            asignacion = nueva_asignacion
            mejor_choque = nuevo_choque

    return asignacion, mejor_choque

# --- Ejecución ---
if __name__ == "__main__":
    asignacion_final, total_choques = hill_climbing(df)
    print(f"Total de choques: {total_choques}")
    for i, (slot_a, slot_b) in enumerate(asignacion_final):
        print(f"{df.loc[i, 'MentorID']}: Slot{slot_a+1} y Slot{slot_b+1}")
    print("==========================================")
