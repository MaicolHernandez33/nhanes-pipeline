import pandas as pd
import os

print("🚀 Iniciando procesamiento local de los 5 archivos reales de NHANES...")

folder = "data/01_raw"

try:
    # Leer los 5 archivos locales .xpt respetando los nombres de tu carpeta
    print("📖 Leyendo archivos SAS (.xpt)... esto puede tomar unos segundos.")
    df_demo = pd.read_sas(os.path.join(folder, "DEMO_J.xpt"), format='xport')
    df_bmx = pd.read_sas(os.path.join(folder, "BMX_J.xpt"), format='xport')
    df_bpx = pd.read_sas(os.path.join(folder, "BPX_J.xpt"), format='xport')
    df_tchol = pd.read_sas(os.path.join(folder, "TCHOL_J.xpt"), format='xport')
    df_smq = pd.read_sas(os.path.join(folder, "SMQ_J.xpt"), format='xport')

    # Convertir el ID (SEQN) a entero en todas las tablas para evitar problemas al unir
    print("🧹 Ajustando los IDs (SEQN)...")
    for df in [df_demo, df_bmx, df_bpx, df_tchol, df_smq]:
        if 'SEQN' in df.columns:
            df['SEQN'] = df['SEQN'].astype(int)

    # 1. FUENTE 1: Demografía -> Reemplaza el CSV viejo
    df_demo.to_csv(os.path.join(folder, "demographics.csv"), index=False)
    print("✅ demographics.csv actualizado con data real.")

    # 2. FUENTE 2: Exámenes -> Unimos Medidas Corporales + Presión Arterial
    df_exam = pd.merge(df_bmx, df_bpx, on="SEQN", how="outer")
    df_exam.to_csv(os.path.join(folder, "body_measures_real.csv"), index=False)
    print("✅ body_measures_real.csv (Medidas + Presión) generado con data real.")

    # 3. FUENTE 3: Laboratorio y Cuestionario -> Unimos Colesterol + Tabaquismo
    df_api_data = pd.merge(df_tchol, df_smq, on="SEQN", how="outer")
    df_api_data.to_json(os.path.join(folder, "laboratory.json"), orient="records")
    print("✅ laboratory.json (Colesterol + Tabaquismo) actualizado con data real.")

    print("\n🎉 ¡Éxito! Los datos reales están listos para alimentar tu base de datos y tu pipeline de Kedro.")

except Exception as e:
    print(f"\n💥 Ocurrió un error al procesar: {e}")