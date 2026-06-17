import subprocess
import time
import sys
import os

def run_project():
    print("🚀 [Orquestador] Iniciando el ecosistema de datos NHANES...")

    # 1. Levantar la API en segundo plano
    print("🌐 [Orquestador] Encendiendo el servidor de la API (FastAPI) de fondo...")
    api_process = subprocess.Popen(
        ["uvicorn", "api_server:app", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Darle 2 segundos a la API para asegurarse de que el puerto 8000 responda
    time.sleep(2)

    try:
        # 2. Ejecutar el Pipeline de Kedro
        print("⚡ [Orquestador] Ejecutando el Pipeline Modular de Kedro...")
        # Usamos sys.executable para asegurarnos de que corra dentro de tu (.venv)
        kedro_result = subprocess.run([sys.executable, "-m", "kedro", "run"], check=True)
        
        if kedro_result.returncode == 0:
            print("\n🎉 [Orquestador] ¡Proceso completado con éxito absoluto!")
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ [Orquestador] Hubo un error al ejecutar Kedro: {e}")
        
    finally:
        # 3. Apagar la API para liberar el puerto de tu computadora
        print("🔌 [Orquestador] Apagando el servidor de la API de forma limpia...")
        api_process.terminate()
        api_process.wait()
        print("✅ [Orquestador] Todo cerrado correctamente.")

if __name__ == "__main__":
    run_project()