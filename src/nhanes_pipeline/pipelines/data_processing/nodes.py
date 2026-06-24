import pandas as pd
import numpy as np

def preparar_datos_ml(df: pd.DataFrame) -> pd.DataFrame:
    """
    Toma el dataset masivo de NHANES, selecciona variables clave para riesgo cardiovascular,
    renombra las columnas, calcula la variable objetivo (Hipertensión) y previene la fuga de datos.
    """
    print("🧹 [Procesamiento] Iniciando limpieza profunda y selección de variables...")
    df_ml = df.copy()
    
    # 1. Diccionario de traducción: De nombres técnicos de NHANES a Español legible
    # Solo seleccionamos las columnas que realmente aportan al modelo predictivo
    columnas_clave = {
        'RIDAGEYR': 'Edad',
        'RIAGENDR': 'Genero',           # 1: Hombre, 2: Mujer
        'BMXWT': 'Peso_kg',
        'BMXHT': 'Estatura_cm',
        'BMXBMI': 'IMC',
        'BMXWAIST': 'Cintura_cm',
        'BPXSY1': 'Presion_Sistolica',  # Presión sistólica (1ra lectura)
        'BPXDI1': 'Presion_Diastolica', # Presión diastólica (1ra lectura)
        'LBXTC': 'Colesterol_Total',    # Colesterol en sangre
        'SMQ020': 'Fumador'             # 1: Sí, 2: No
    }
    
    # Filtrar solo las columnas que existen en nuestro dataset y renombrarlas
    cols_presentes = {k: v for k, v in columnas_clave.items() if k in df_ml.columns}
    df_ml = df_ml[list(cols_presentes.keys())].rename(columns=cols_presentes)
    
    # 2. Limpieza básica de Nulos
    # Eliminamos pacientes que no se tomaron la presión (nuestra variable vital)
    if 'Presion_Sistolica' in df_ml.columns and 'Presion_Diastolica' in df_ml.columns:
        df_ml = df_ml.dropna(subset=['Presion_Sistolica', 'Presion_Diastolica'])
    
    # Imputar (rellenar) nulos restantes con la mediana para no perder al paciente
    for col in df_ml.columns:
        if df_ml[col].isnull().any():
            df_ml[col] = df_ml[col].fillna(df_ml[col].median())
            
    # 3. Creación de la Variable Objetivo (Etiqueta para Machine Learning)
    # Criterio AHA: Sistólica >= 130 o Diastólica >= 80 se considera Hipertensión (1), si no (0)
    print("🎯 [Procesamiento] Calculando variable objetivo: Riesgo_Hipertension...")
    df_ml['Riesgo_Hipertension'] = np.where(
        (df_ml['Presion_Sistolica'] >= 130) | (df_ml['Presion_Diastolica'] >= 80), 
        1, 0
    )
    
    # 4. Eliminar Fuga de Datos (Data Leakage)
    # Si le dejamos la presión al modelo, hará trampa. ¡El objetivo es predecir el riesgo 
    # ANTES de tomarle la presión al paciente, usando solo su edad, IMC, colesterol, etc.!
    df_ml = df_ml.drop(columns=['Presion_Sistolica', 'Presion_Diastolica'])
    
    print(f"✅ [Procesamiento] Dataset listo. Filas: {df_ml.shape[0]}, Variables predictivas: {df_ml.shape[1]}")
    return df_ml