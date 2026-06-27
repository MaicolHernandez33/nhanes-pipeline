from kedro.pipeline import Pipeline, node, pipeline
from .nodes import entrenar_modelo_hipertension, build_predictions, store_models_in_db

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            # 1. Entrenar el modelo (Tu nodo original)
            node(
                func=entrenar_modelo_hipertension,
                inputs=["df_nhanes_limpio", "params:umbral_decision"],
                outputs="modelo_hipertension",
                name="entrenar_modelo_hipertension_node",
            ),
            # 2. Generar predicciones masivas y mandarlas a SQL
            node(
                func=build_predictions,
                inputs=["df_nhanes_limpio", "modelo_hipertension"],
                outputs="model_predictions",
                name="build_predictions_node"
            ),
            # 3. Guardar el modelo en SQL
            node(
                func=store_models_in_db,
                inputs="modelo_hipertension",
                outputs="model_save_summary",
                name="store_model_in_db_node"
            )
        ]
    )