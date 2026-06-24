from kedro.pipeline import Pipeline, node, pipeline
from .nodes import entrenar_modelo_hipertension

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=entrenar_modelo_hipertension,
                inputs=["df_nhanes_limpio","params:umbral_decision"],
                outputs="modelo_hipertension",
                name="entrenar_modelo_hipertension_node",
            )
        ]
    )