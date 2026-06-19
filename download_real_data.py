import os
import pandas as pd

# Tus archivos ya están en 01_raw, así que trabajaremos todo aquí
data_dir = "data/01_raw"

# 🔥 ¡La magia ocurre aquí! Agregamos los ciclos G y H para cubrir los 4 períodos
ciclos = ["G", "H", "I", "J"]

data_por_tipo = {
    "demographics": [],
    "body_measures": [],
    "blood_pressure": [],
    "cholesterol": [],
    "smoking": []
}

print("🔄 Consolidando archivos SAS locales desde data/01_raw/ (4 Períodos)...")

for letra in ciclos:
    # Mapear los nombres de los archivos locales automáticamente por ciclo
    archivos = {
        "demographics": f"DEMO_{letra}.xpt",
        "body_measures": f"BMX_{letra}.xpt",
        "blood_pressure": f"BPX_{letra}.xpt",
        "cholesterol": f"TCHOL_{letra}.xpt",
        "smoking": f"SMQ_{letra}.xpt"
    }
    
    for tipo, nombre_archivo in archivos.items():
        # Validar si el archivo existe con .xpt o .XPT (por si acaso)
        ruta_completa = os.path.join(data_dir, nombre_archivo)
        ruta_alt = os.path.join(data_dir, nombre_archivo.replace('.xpt', '.XPT'))
        ruta_final = ruta_completa if os.path.exists(ruta_completa) else ruta_alt

        if os.path.exists(ruta_final):
            try:
                print(f"  📖 Leyendo archivo local {nombre_archivo}...")
                df_temp = pd.read_sas(ruta_final, format="xport")
                
                if "SEQN" in df_temp.columns:
                    df_temp["SEQN"] = df_temp["SEQN"].astype(int)
                    
                data_por_tipo[tipo].append(df_temp)
            except Exception as e:
                print(f"  ❌ Error al procesar {nombre_archivo}: {e}")
        else:
            print(f"  ⚠️ No se encontró el archivo: {ruta_final}")

print("\n🔀 Uniendo ciclos y generando archivos consolidados...")

if data_por_tipo["demographics"]:
    df_demo_all = pd.concat(data_por_tipo["demographics"], axis=0, ignore_index=True)
    df_demo_all.to_csv(os.path.join(data_dir, "demographics.csv"), index=False)
    print(f"✅ demographics.csv actualizado. (Total filas: {df_demo_all.shape[0]})")

    medidas_list = []
    for i in range(len(data_por_tipo["body_measures"])):
        bm = data_por_tipo["body_measures"][i]
        bp = data_por_tipo["blood_pressure"][i]
        medidas_list.append(pd.merge(bm, bp, on="SEQN", how="outer"))
    df_measures_all = pd.concat(medidas_list, axis=0, ignore_index=True)
    df_measures_all.to_csv(os.path.join(data_dir, "body_measures_real.csv"), index=False)
    print(f"✅ body_measures_real.csv actualizado. (Total filas: {df_measures_all.shape[0]})")

    lab_list = []
    for i in range(len(data_por_tipo["cholesterol"])):
        chol = data_por_tipo["cholesterol"][i]
        smk = data_por_tipo["smoking"][i]
        lab_list.append(pd.merge(chol, smk, on="SEQN", how="outer"))
    df_lab_all = pd.concat(lab_list, axis=0, ignore_index=True)
    df_lab_all.to_json(os.path.join(data_dir, "laboratory.json"), orient="records", indent=4)
    print(f"✅ laboratory.json actualizado. (Total filas: {df_lab_all.shape[0]})")
    
    print("\n🎉 ¡Éxito total! Los 4 períodos han sido consolidados perfectamente.")
else:
    print("❌ No se pudo consolidar: Revisa que los archivos estén en data/01_raw/")
    