import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import logging

def entrenar_modelo_hipertension(df: pd.DataFrame, umbral: float) -> xgb.XGBClassifier:
    """
    Entrena un modelo XGBoost para predecir el riesgo de hipertensión
    y evalúa el reporte usando un umbral personalizado.
    """
    log = logging.getLogger(__name__)
    log.info("Iniciando entrenamiento del modelo XGBoost...")

    # Separar variables
    X = df.drop(columns=['Riesgo_Hipertension'])
    y = df['Riesgo_Hipertension']

    # División Train/Test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entrenar modelo con balanceo de clases
    ratio_desbalance = (len(y_train) - sum(y_train)) / sum(y_train)
    modelo = xgb.XGBClassifier(
        n_estimators=100, 
        max_depth=5, 
        scale_pos_weight=ratio_desbalance, 
        random_state=42
    )
    modelo.fit(X_train, y_train)

    # --- CAMBIO CLAVE AQUÍ ---
    # En vez de usar modelo.predict(), obtenemos las probabilidades de la clase 1 (Riesgo)
    probabilidades_test = modelo.predict_proba(X_test)[:, 1]
    
    # Aplicamos el umbral configurado (ej: 0.60) para generar las nuevas predicciones
    preds_personalizadas = (probabilidades_test >= umbral).astype(int)
    
    # El reporte reflejará la realidad de tu nuevo umbral
    reporte = classification_report(y_test, preds_personalizadas)
    log.info(f"\n🏆 Reporte de Clasificación Final (Umbral: {umbral}):\n{reporte}")

    # Retornar el modelo para que Kedro lo guarde
    return modelo