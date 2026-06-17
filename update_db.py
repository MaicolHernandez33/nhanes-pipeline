import pandas as pd
import sqlite3

print("🗄️ Conectando a la base de datos SQLite...")
conexion = sqlite3.connect("data/01_raw/nhanes.db")

print("📥 Cargando body_measures_real.csv a la base de datos...")
df_exam = pd.read_csv("data/01_raw/body_measures_real.csv")

# Guardar en la tabla 'body_measures' (reemplaza los datos de prueba anteriores)
df_exam.to_sql("body_measures", conexion, if_exists="replace", index=False)

conexion.close()
print("✅ Base de datos nhanes.db actualizada exitosamente con miles de registros reales.")