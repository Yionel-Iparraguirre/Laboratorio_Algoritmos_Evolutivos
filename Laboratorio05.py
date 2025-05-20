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


