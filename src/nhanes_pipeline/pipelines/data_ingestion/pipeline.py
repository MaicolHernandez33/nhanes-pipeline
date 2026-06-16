from kedro.pipeline import Pipeline, node, pipeline
from .nodes import ingest_and_merge_nhanes

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=ingest_and_merge_nhanes,
                inputs=[
                    "demographics_raw",   # Fuente 1: CSV
                    "body_measures_sql",  # Fuente 2: SQL
                    "laboratory_api"      # Fuente 3: JSON / API
                ],
                outputs="nhanes_merged_data", # El dataset resultante unificado
                name="node_ingestion_and_merge",
            ),
        ]
    )