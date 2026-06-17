from fastapi import FastAPI
import json
import os

app = FastAPI()

# La ruta donde está tu archivo JSON
DATA_PATH = "data/01_raw/laboratory.json"

@app.get("/laboratorio")
def get_laboratorio():
    """Endpoint que sirve los datos de laboratorio como una API real"""
    if not os.path.exists(DATA_PATH):
        return {"error": "Archivo de datos no encontrado"}
    
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    return data