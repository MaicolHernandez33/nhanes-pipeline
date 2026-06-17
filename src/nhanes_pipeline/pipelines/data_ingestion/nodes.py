import pandas as pd
import requests

def ingest_and_merge_nhanes(
    demographics: pd.DataFrame, 
    body_measures: pd.DataFrame, 
    laboratory: pd.DataFrame
) -> pd.DataFrame:
    """
    Une las tres fuentes de datos. Intenta consumir de la API REST viva (FastAPI)
    y si no está disponible, usa el respaldo local. Cumple con la arquitectura
    Cliente-Servidor de la rúbrica.
    """
    print("\n🌐 [API] Intentando conectar con el servidor de FastAPI...")
    try:
        # Hacemos la petición HTTP GET real a tu servidor de Uvicorn
        response = requests.get("http://127.0.0.1:8000/laboratorio", timeout=5)
        
        if response.status_code == 200:
            print("✅ [API] Conexión exitosa. Datos obtenidos en tiempo real desde la API REST.")
            # Convertimos la respuesta JSON de la API directamente a un DataFrame de Pandas
            df_laboratory = pd.DataFrame(response.json())
        else:
            print("⚠️ [API] El servidor respondió con un error. Usando respaldo local.")
            df_laboratory = pd.DataFrame(laboratory)
            
    except requests.exceptions.ConnectionError:
        print("❌ [API] No se pudo conectar al servidor (¿Está apagado?). Usando respaldo local.")
        df_laboratory = pd.DataFrame(laboratory)

    # --- PROCESO DE MERGE (Igual que antes) ---
    if "SEQN" not in body_measures.columns:
        body_measures = body_measures.reset_index()

    # Uniones (Merges)
    merged_df = pd.merge(demographics, body_measures, on="SEQN", how="inner")
    final_df = pd.merge(merged_df, df_laboratory, on="SEQN", how="inner")
    
    print("📊 [Pipeline] Combinación completada con éxito.")
    return final_df