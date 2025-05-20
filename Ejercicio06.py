import pandas as pd
import random

print("==========================================")
print("EJERCICIO 06 - USANDO EL DATASET EXAM QUESTIONS")
print("==========================================")
# --- Cargar datos ---
file_path = r'C:\Users\yolog\OneDrive\Escritorio\ACTIVIDADES\ALGORITMOS EVOLUTIVOS\LAB 05\Datasets.xlsx'
exam_questions_df = pd.read_excel(file_path, sheet_name='ExamQuestions')

# Parámetros
num_preguntas = 30
dificultad_min = 180
dificultad_max = 200
tiempo_max = 90

# Variables del dataset
costos = [0] * len(exam_questions_df)  # Costos no están especificados en el dataset proporcionado
tiempos = exam_questions_df['Time_min'].values
dificultades = exam_questions_df['Difficulty'].values

# --- Función objetivo para evaluar una solución ---
def evaluar_seleccion(seleccion):
    "Evalúa la selección de preguntas en base a las restricciones de dificultad y tiempo."
    dificultad_total = sum(dificultades[i] for i in seleccion)
    tiempo_total = sum(tiempos[i] for i in seleccion)
    
    # Penalizar si no cumple las restricciones
    if dificultad_total < dificultad_min or dificultad_total > dificultad_max or tiempo_total > tiempo_max:
        return float('inf')  # Penalización muy alta si no cumple restricciones
    
    return 0  # Costo = 0 ya que no se especifica un costo real

# --- Generar una solución inicial aleatoria ---
def generar_seleccion_inicial():
    "Genera una selección inicial de 30 preguntas aleatorias."
    seleccion = random.sample(range(len(exam_questions_df)), num_preguntas)
    return seleccion

# --- Búsqueda de vecino: cambiar una pregunta seleccionada por una no seleccionada ---
def vecino(seleccion_actual):
    "Genera una nueva selección cambiando una pregunta seleccionada por una no seleccionada."
    seleccion_vecino = seleccion_actual[:]
    
    # Intentamos seleccionar una pregunta que no esté ya en la selección actual
    no_seleccionadas = [i for i in range(len(exam_questions_df)) if i not in seleccion_vecino]
    
    if no_seleccionadas:  # Si hay preguntas no seleccionadas, elegimos una
        nueva_pregunta = random.choice(no_seleccionadas)
        idx = random.randint(0, num_preguntas - 1)
        seleccion_vecino[idx] = nueva_pregunta
    else:  # Si no hay preguntas no seleccionadas, movemos una pregunta dentro de la selección
        idx = random.randint(0, num_preguntas - 1)
        nueva_pregunta = random.choice([i for i in range(len(exam_questions_df)) if i != seleccion_vecino[idx]])
        seleccion_vecino[idx] = nueva_pregunta
        
    # Verificar que la nueva selección cumple con las restricciones de dificultad y tiempo
    if evaluar_seleccion(seleccion_vecino) == float('inf'):
        return seleccion_actual  # Si no cumple, devolver la selección original
    
    return seleccion_vecino

# --- Algoritmo de búsqueda local ---
def hill_climbing(iteraciones=10000):
    "Algoritmo de búsqueda local para encontrar la mejor selección de preguntas."
    seleccion = generar_seleccion_inicial()
    mejor_seleccion = seleccion
    mejor_costo = evaluar_seleccion(seleccion)

    for _ in range(iteraciones):
        nueva_seleccion = vecino(mejor_seleccion)
        nuevo_costo = evaluar_seleccion(nueva_seleccion)

        if nuevo_costo < mejor_costo:
            mejor_seleccion = nueva_seleccion
            mejor_costo = nuevo_costo

    return mejor_seleccion, mejor_costo

# --- Ejecución ---
if __name__ == "__main__":
    seleccion_final, costo_total = hill_climbing()

    # Mostrar las preguntas seleccionadas
    print("\nPreguntas seleccionadas:")
    for idx in seleccion_final:
        print(f"Pregunta ID: {exam_questions_df.loc[idx, 'QuestionID']} - Dificultad: {exam_questions_df.loc[idx, 'Difficulty']} - Tiempo: {exam_questions_df.loc[idx, 'Time_min']}")