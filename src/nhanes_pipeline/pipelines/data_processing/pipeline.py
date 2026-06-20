from kedro.pipeline import Pipeline, node, pipeline
from .nodes import preparar_datos_ml

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            
            node(
                func=preparar_datos_ml,           # Tu función de limpieza
                inputs="nhanes_merged_data",      
                outputs="df_nhanes_limpio",       # El output sí está bien que sea el limpio
                name="nodo_preparar_datos_ml",
            )
        ]
    )

