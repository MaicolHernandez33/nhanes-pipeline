import pandas as pd
import sqlite3
import json
import os

print("⏳ Generando datos simulados de NHANES para el pipeline...")

# --- DATOS BASE DE PACIENTES (SEQN comunes para que el merge funcione)
seqn_list = [100001, 100002, 100003, 100004, 100005]

# ==========================================
# 1. Fuente Demográfica (CSV)
# ==========================================
demo_data = {
    "SEQN": seqn_list,
    "RIAGENDR": [1, 2, 1, 2, 1],       # 1=Hombre, 2=Mujer
    "RIDAGEYR": [34, 45, 22, 68, 51],   # Edad en años
    "DMDBORN4": [1, 1, 2, 1, 1]        # País de nacimiento
}
df_demo = pd.DataFrame(demo_data)
df_demo.to_csv("data/01_raw/demographics.csv", index=False)
print("✅ Fuente 1 (demographics.csv) creada con éxito.")

# ==========================================
# 2. Fuente de Examen Físico / Medidas (SQL - SQLite)
# ==========================================
measures_data = {
    "SEQN": seqn_list,
    "BMXWT": [78.5, 62.0, 91.2, 70.4, 83.1],   # Peso en kg
    "BMXHT": [175.2, 160.5, 182.0, 155.1, 170.0], # Estatura en cm
    "BMXBMI": [25.6, 24.1, 27.5, 29.3, 28.7]   # Índice de Masa Corporal
}
df_measures = pd.DataFrame(measures_data)

# Conectar e inyectar en la base de datos local
conn = sqlite3.connect("data/01_raw/nhanes.db")
df_measures.to_sql("body_measures", conn, if_exists="replace", index=False)
conn.close()
print("✅ Fuente 2 (nhanes.db - Tabla 'body_measures') creada con éxito.")

# ==========================================
# 3. Fuente de Laboratorio (JSON / API REST)
# ==========================================
# Simula el formato JSON de lista de diccionarios que entregará la API
lab_data = [
    {"SEQN": 100001, "LBXGLU": 95, "LBXCHO": 180},  # Glucosa y Colesterol
    {"SEQN": 100002, "LBXGLU": 112, "LBXCHO": 210},
    {"SEQN": 100003, "LBXGLU": 88, "LBXCHO": 195},
    {"SEQN": 100004, "LBXGLU": 140, "LBXCHO": 240},
    {"SEQN": 100005, "LBXGLU": 101, "LBXCHO": 189}
]

with open("data/01_raw/laboratory.json", "w") as f:
    json.dump(lab_data, f, indent=4)
print("✅ Fuente 3 (laboratory.json) creada con éxito.")

print("\n🎉 ¡Todo listo! Ya puedes correr 'kedro run' en tu terminal.")