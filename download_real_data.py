import os
import pandas as pd

data_dir = "data/01_raw"
ciclos = ["G", "H", "I", "J"]

print("🔄 Consolidando de forma SEGURA los archivos SAS para FastAPI y respaldos...")

list_demo = []
list_measures = []
list_lab = []

for c in ciclos:
    print(f"📦 Procesando Bloque Clínico del Ciclo {c}...")
    
    # Rutas por ciclo
    f_demo = os.path.join(data_dir, f"DEMO_{c}.xpt")
    f_bmx  = os.path.join(data_dir, f"BMX_{c}.xpt")
    f_bpx  = os.path.join(data_dir, f"BPX_{c}.xpt")
    f_smq  = os.path.join(data_dir, f"SMQ_{c}.xpt")
    f_tchol = os.path.join(data_dir, f"TCHOL_{c}.xpt")

    # Leer archivos si existen
    df_demo = pd.read_sas(f_demo, format="xport") if os.path.exists(f_demo) else pd.DataFrame()
    df_bmx  = pd.read_sas(f_bmx, format="xport")  if os.path.exists(f_bmx) else pd.DataFrame()
    df_bpx  = pd.read_sas(f_bpx, format="xport")  if os.path.exists(f_bpx) else pd.DataFrame()
    df_smq  = pd.read_sas(f_smq, format="xport")  if os.path.exists(f_smq) else pd.DataFrame()
    df_tchol = pd.read_sas(f_tchol, format="xport") if os.path.exists(f_tchol) else pd.DataFrame()

    # Estandarizar el ID del paciente para evitar errores de fusión
    for df in [df_demo, df_bmx, df_bpx, df_smq, df_tchol]:
        if not df.empty and "SEQN" in df.columns:
            df["SEQN"] = df["SEQN"].astype(float)

    # 1. Acumular Demografía
    if not df_demo.empty:
        list_demo.append(df_demo)
    
    # 2. Fusionar Medidas + Presión de forma segura (Mismo Ciclo)
    if not df_bmx.empty or not df_bpx.empty:
        if df_bmx.empty: m_df = df_bpx
        elif df_bpx.empty: m_df = df_bmx
        else: m_df = pd.merge(df_bmx, df_bpx, on="SEQN", how="outer")
        list_measures.append(m_df)
        
    # 3. Fusionar Colesterol + Tabaquismo de forma segura (Mismo Ciclo)
    if not df_tchol.empty or not df_smq.empty:
        if df_tchol.empty: l_df = df_smq
        elif df_smq.empty: l_df = df_tchol
        else: l_df = pd.merge(df_tchol, df_smq, on="SEQN", how="outer")
        list_lab.append(l_df)

print("\n🔀 Generando archivos maestros consolidados de 4 ciclos...")

# Guardar Demografía (Respaldo CSV)
if list_demo:
    df_demo_all = pd.concat(list_demo, ignore_index=True)
    df_demo_all.to_csv(os.path.join(data_dir, "demographics.csv"), index=False)
    print(f"✅ demographics.csv actualizado ({df_demo_all.shape[0]} filas).")

# Guardar Medidas Reales (Respaldo CSV)
if list_measures:
    df_meas_all = pd.concat(list_measures, ignore_index=True)
    df_meas_all.to_csv(os.path.join(data_dir, "body_measures_real.csv"), index=False)
    print(f"✅ body_measures_real.csv actualizado ({df_meas_all.shape[0]} filas).")

# Guardar Laboratorio EN JSON (¡Esto alimenta a tu FastAPI!)
if list_lab:
    df_lab_all = pd.concat(list_lab, ignore_index=True)
    
    # Limpieza rápida: Convertir columnas de bytes a strings si las hay (común en read_sas)
    for col in df_lab_all.columns:
        if df_lab_all[col].dtype == object:
            df_lab_all[col] = df_lab_all[col].str.decode('utf-8', errors='ignore')
            
    df_lab_all.to_json(os.path.join(data_dir, "laboratory.json"), orient="records", indent=4)
    print(f"✅ laboratory.json generado con éxito ({df_lab_all.shape[0]} filas).")

print("\n🎉 ¡Éxito total! Tu API de FastAPI ahora tiene el combustible completo listo.")