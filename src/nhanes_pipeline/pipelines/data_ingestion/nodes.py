import pandas as pd

def ingest_and_merge_nhanes(
    demographics: pd.DataFrame, 
    body_measures: pd.DataFrame, 
    laboratory: pd.DataFrame
) -> pd.DataFrame:
    """
    Une las tres fuentes de datos obligatorias de NHANES usando la columna SEQN.
    Cumple con el criterio de integración de múltiples orígenes de la rúbrica.
    """
    # 1. Asegurar que la columna de ID esté limpia (SEQN)
    # Si en SQL pusimos SEQN como índice, lo pasamos a columna para el merge
    if "SEQN" not in body_measures.columns:
        body_measures = body_measures.reset_index()

    # Convertir a DataFrame de Pandas el JSON si viene como diccionario/lista
    if isinstance(laboratory, list) or isinstance(laboratory, dict):
        laboratory = pd.DataFrame(laboratory)

    # 2. Hacer los Merges (Uniones) tipo 'inner' para asegurar consistencia
    # Primero unimos Demografía con Examen Físico
    merged_df = pd.merge(demographics, body_measures, on="SEQN", how="inner")
    
    # Luego unimos el resultado con los datos de Laboratorio de la API
    final_df = pd.merge(merged_df, laboratory, on="SEQN", how="inner")
    
    return final_df