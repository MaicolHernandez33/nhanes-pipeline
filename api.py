from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from pathlib import Path
from kedro.framework.startup import bootstrap_project
from kedro.framework.session import KedroSession

# 1. Inicializar FastAPI
app = FastAPI(
    title="API de Riesgo de Hipertensión - NHANES",
    description="Servicio web para predecir el riesgo de hipertensión usando XGBoost.",
    version="1.0"
)

# 2. Cargar el modelo usando el ecosistema de Kedro al arrancar el servidor
metadata = bootstrap_project(Path.cwd())
with KedroSession.create(project_path=Path.cwd()) as session:  # <-- Cambiado aquí
    context = session.load_context()
    modelo = context.catalog.load("modelo_hipertension")

# 3. Definir qué datos médicos debe recibir la API por cada paciente
class PacienteInput(BaseModel):
    Edad: float
    Genero: int
    Peso_kg: float
    Estatura_cm: float
    IMC: float
    Cintura_cm: float
    Colesterol_Total: float
    Fumador: int

# 4. Crear la ruta de predicción (Endpoint)
@app.post("/predict")
def predecir_hipertension(paciente: PacienteInput):
    # Convertir el JSON recibido a un DataFrame de Pandas
    df_paciente = pd.DataFrame([paciente.model_dump()])
    
    # Asegurar el orden exacto de las columnas que espera XGBoost
    columnas_esperadas = ['Edad', 'Genero', 'Peso_kg', 'Estatura_cm', 'IMC', 'Cintura_cm', 'Colesterol_Total', 'Fumador']
    df_paciente = df_paciente[columnas_esperadas]
    
    # Calcular la probabilidad con el modelo
    prob_riesgo = modelo.predict_proba(df_paciente)[0][1]
    
    # Aplicar nuestro umbral calibrado del 60%
    umbral = 0.60
    diagnostico = 1 if prob_riesgo >= umbral else 0
    
    return {
        "probabilidad_riesgo": f"{prob_riesgo * 100:.1f}%",
        "diagnostico_codigo": diagnostico,
        "resultado": "🚨 EN RIESGO" if diagnostico == 1 else "✅ SANO",
        "nota_medica": "Paciente requiere evaluación clínica prioritaria." if diagnostico == 1 else "Paciente en rangos de control."
    }