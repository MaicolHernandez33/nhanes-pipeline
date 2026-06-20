import pandas as pd

def preparar_datos_ml(df: pd.DataFrame) -> pd.DataFrame:
    """
    Toma el dataset limpio intermedio, aplica clipping a outliers basándose en 
    desviaciones estándar, remueve variables con fuga de datos (Data Leakage) 
    e identificadores, dejando el dataset listo para el entrenamiento de Machine Learning.
    """
    df_ml = df.copy()
    
    # 1. Definir las variables numéricas a las que les controlaremos los extremos
    todas_las_numericas = [
        'Edad', 'Ratio_Ingresos', 'Peso_kg', 'Estatura_cm', 'IMC', 
        'Cintura_cm', 'Colesterol_Total', 'Presion_Sistolica', 'Presion_Diastolica'
    ]
    
    # Asegurar que solo procese las columnas si existen en el dataframe de entrada
    columnas_numericas_presentes = [col for col in todas_las_numericas if col in df_ml.columns]
    
    # 2. Aplicar el Escudo de Clipping (Media +/- 4 desviaciones estándar)
    # Esto controla outliers reales sin destruir la escala original de tus datos
    for col in columnas_numericas_presentes:
        media = df_ml[col].mean()
        desviacion = df_ml[col].std()
        
        limite_inferior = media - (4 * desviacion)
        limite_superior = media + (4 * desviacion)
        
        df_ml[col] = df_ml[col].clip(lower=limite_inferior, upper=limite_superior)
    
    # 3. Eliminar variables que causan Fuga de Datos (Data Leakage)
    # Quitamos la presión porque de ahí se calculó la variable objetivo (Riesgo_Hipertension)
    columnas_fuga = ['Presion_Sistolica', 'Presion_Diastolica']
    
    # 4. Eliminar variables administrativas sin valor predictivo médico
    columnas_administrativas = ['ID_Paciente']
    
    # Juntar todas las columnas a remover de forma segura
    columnas_a_borrar = [col for col in (columnas_fuga + columnas_administrativas) if col in df_ml.columns]
    df_ml = df_ml.drop(columns=columnas_a_borrar)
    
    return df_ml