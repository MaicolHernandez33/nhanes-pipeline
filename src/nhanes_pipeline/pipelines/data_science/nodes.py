import os
import pickle
import logging
import pandas as pd
import xgboost as xgb
import sqlalchemy
from datetime import datetime, timezone
from typing import Any, Dict
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report

# ==============================================================================
# NODO 1: ENTRENAMIENTO Y AFINAMIENTO DEL MODELO (TUNING)
# ==============================================================================
def entrenar_modelo_hipertension(df: pd.DataFrame, umbral: float) -> xgb.XGBClassifier:
    """
    Entrena un modelo XGBoost aplicando Ajuste de Hiperparámetros (GridSearchCV)
    para optimizar la detección del riesgo de hipertensión.
    
    Args:
        df: DataFrame primario limpio listo para Machine Learning.
        umbral: Valor de corte para determinar el riesgo (ej. 0.60).
        
    Returns:
        xgb.XGBClassifier: El mejor modelo entrenado y optimizado.
    """
    log = logging.getLogger(__name__)
    log.info("Iniciando preparación de datos y Tuning para XGBoost...")

    # Separar variables predictoras (X) y objetivo (y)
    X = df.drop(columns=['Riesgo_Hipertension'])
    y = df['Riesgo_Hipertension']

    # División Train/Test (80% entrenamiento, 20% prueba)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Calcular ratio para balancear clases (XGBoost scale_pos_weight)
    ratio_desbalance = (len(y_train) - sum(y_train)) / sum(y_train)
    
    # 1. Definir el modelo base (sin parámetros fijos de profundidad ni árboles)
    xgb_base = xgb.XGBClassifier(
        scale_pos_weight=ratio_desbalance, 
        random_state=42,
        eval_metric="logloss"
    )

    # 2. Definir la grilla de búsqueda (Tuning de Hiperparámetros)
    param_grid = {
        'max_depth': [3, 5],               # Profundidad de los árboles
        'learning_rate': [0.01, 0.1],      # Tasa de aprendizaje
        'n_estimators': [50, 100]          # Cantidad de árboles
    }

    log.info("Iniciando Búsqueda de Hiperparámetros (GridSearchCV)... esto tomará unos segundos.")

    # 3. Configurar GridSearchCV (optimizando 'recall' para evitar falsos negativos médicos)
    grid_search = GridSearchCV(
        estimator=xgb_base,
        param_grid=param_grid,
        scoring='recall', 
        cv=3,
        n_jobs=-1, 
        verbose=1
    )

    # 4. Ejecutar el entrenamiento masivo para encontrar la mejor combinación
    grid_search.fit(X_train, y_train)

    # 5. Extraer el modelo ganador
    mejor_modelo = grid_search.best_estimator_
    log.info(f"✅ ¡Tuning Completado! Los mejores hiperparámetros son: {grid_search.best_params_}")

    # 6. Evaluar usando el MEJOR modelo y el umbral personalizado
    probabilidades_test = mejor_modelo.predict_proba(X_test)[:, 1]
    preds_personalizadas = (probabilidades_test >= umbral).astype(int)
    
    reporte = classification_report(y_test, preds_personalizadas)
    log.info(f"\n🏆 Reporte de Clasificación Final (Modelo Optimizado | Umbral: {umbral}):\n{reporte}")

    # Retornamos el modelo ganador para que el pipeline lo envíe a los siguientes nodos
    return mejor_modelo


# ==============================================================================
# NODO 2: GENERACIÓN MASIVA DE PREDICCIONES (PARA BASE DE DATOS)
# ==============================================================================
def build_predictions(df: pd.DataFrame, modelo: Any) -> pd.DataFrame:
    """
    Genera predicciones usando el modelo pre-entrenado y arma un DataFrame 
    para ser persistido en la base de datos SQL.
    
    Args:
        df: DataFrame de validación o test.
        modelo: Modelo de Machine Learning entrenado (XGBoost).
        
    Returns:
        pd.DataFrame: DataFrame con la llave primaria y las predicciones.
    """
    log = logging.getLogger(__name__)
    
    # Rescatar la llave primaria SEQN si está en el índice
    if 'SEQN' not in df.columns:
        df = df.reset_index(names='SEQN') if df.index.name == 'SEQN' else df.reset_index()
    
    # Seleccionar exclusivamente las variables con las que se entrenó el modelo
    # Ignora automáticamente la llave SEQN y la variable objetivo si vienen incluidas
    features = getattr(modelo, "feature_names_in_", df.columns.drop(['SEQN', 'Riesgo_Hipertension'], errors='ignore'))
    df_features = df[features]
    
    log.info(f"Generando predicciones masivas para {len(df)} registros...")
    
    # Generar probabilidades y clases
    probabilidades = modelo.predict_proba(df_features)[:, 1] if hasattr(modelo, "predict_proba") else None
    clase = modelo.predict(df_features)
    
    # Armar DataFrame final
    df_pred = pd.DataFrame({
        'SEQN': df['SEQN'] if 'SEQN' in df.columns else range(len(df)),
        'prediction_class': clase,
        'risk_probability': probabilidades
    })
    
    log.info("Predicciones generadas correctamente. Listas para enviar a SQL.")
    return df_pred


# ==============================================================================
# NODO 3: PERSISTENCIA DEL MODELO (SERIALIZACIÓN BLOB EN SQL)
# ==============================================================================
def store_models_in_db(modelo: Any) -> Dict[str, Any]:
    """
    Serializa el modelo a formato binario (Pickle) y lo persiste 
    en una tabla de metadatos dentro de la base de datos SQL.
    
    Args:
        modelo: Modelo entrenado.
        
    Returns:
        Dict: Diccionario con el resumen de la operación.
    """
    log = logging.getLogger(__name__)
    
    # Lógica de conexión: Prioriza variable de entorno (Docker), sino usa SQLite local
    db_url = os.getenv("DB_URL", "sqlite:///data/01_raw/nhanes.db")
    
    try:
        log.info(f"Intentando guardar el modelo en la BD: {db_url.split('@')[-1]}")
        engine = sqlalchemy.create_engine(db_url)
        
        # 1. Serializar el modelo de forma segura
        model_blob = pickle.dumps(modelo)
        
        # 2. Rescatar cantidad de variables usadas (si existe)
        n_features = getattr(modelo, "n_features_in_", None)
        
        # 3. Armar DataFrame de una sola fila con los metadatos del modelo
        df_modelo = pd.DataFrame([{
            "name": "modelo_hipertension_xgboost",
            "model_type": type(modelo).__name__,
            "trained_at": datetime.now(timezone.utc).isoformat(),
            "n_features": n_features,
            "model_blob": model_blob
        }])
        
        # 4. Enviar a SQL (Sobrescribe si ya existe)
        df_modelo.to_sql("ml_models", engine, if_exists="replace", index=False)
        log.info(f"¡Modelo serializado ({len(model_blob)} bytes) guardado exitosamente en tabla 'ml_models'!")
        
        return {"status": "success", "db": db_url, "model_size_bytes": len(model_blob)}
        
    except Exception as e:
        log.warning(f"No se pudo guardar el modelo en la base de datos SQL. Razón: {e}")
        return {"status": "failed", "error": str(e)}