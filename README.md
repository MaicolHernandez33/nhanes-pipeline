Markdown
# 🩺 Sistema Clínico de Predicción de Riesgo de Hipertensión (NHANES)

**Un Pipeline de Machine Learning *End-to-End* para la Toma de Decisiones Médicas**

---

## 👥 Equipo de Desarrollo
* **Maicol Hernández** - *Machine Learning & Data Engineering*
* **Francis Moya** - *Machine Learning & Data Engineering*

---

## 📝 Introducción y Contexto del Proyecto

Este proyecto implementa una solución tecnológica integral orientada al sector salud. Su objetivo principal es evaluar y predecir el riesgo de hipertensión arterial en pacientes, basándose en sus factores metabólicos y de estilo de vida. 

Utilizamos los datos oficiales de la encuesta estadounidense **NHANES** (National Health and Nutrition Examination Survey) para construir un sistema que no solo entrena un modelo predictivo, sino que lo despliega como un servicio web consumible. Este enfoque demuestra el ciclo de vida completo de un proyecto de datos: desde la ingesta bruta hasta una interfaz gráfica que un profesional médico podría utilizar en su consulta diaria.

---

## 🏆 Hitos y Logros Clave del Proyecto

Durante el desarrollo de esta solución, logramos implementar:

1. **Pipeline ETL Robusto:** Uso de **Kedro** para estructurar la limpieza de datos, validación de esquemas y transformaciones, garantizando la reproducibilidad y el manejo eficiente de los volúmenes de datos.
2. **Modelamiento Clínico (XGBoost):** Entrenamiento de un modelo de *Gradient Boosting* altamente preciso. Se puso especial énfasis en la **calibración de umbrales**, ajustando la sensibilidad para penalizar los falsos negativos (crucial en diagnósticos de salud).
3. **Desarrollo de API REST:** Integración del modelo en un servidor **FastAPI**, exponiendo un *endpoint* (`/predict`) documentado automáticamente con Swagger, preparado para procesar datos JSON en tiempo real.
4. **Dashboard Interactivo:** Creación de una interfaz gráfica de usuario (GUI) con **Streamlit**, diseñada con terminología clínica, validaciones de entrada y alertas visuales adaptadas para el personal médico.
5. **Orquestación y Despliegue:** Contenerización de toda la arquitectura utilizando **Docker** y **Docker Compose**, asegurando que el backend y el frontend se comuniquen de forma aislada e independiente del entorno local.

---

## 🛠️ Tecnologías y Herramientas Utilizadas

* **Gestión de Datos y Pipeline:** `Kedro`, `Pandas`, `NumPy`
* **Machine Learning:** `XGBoost`, `Scikit-Learn`
* **Desarrollo Backend (API):** `FastAPI`, `Uvicorn`, `Pydantic`
* **Desarrollo Frontend:** `Streamlit`, `Requests`
* **Infraestructura y DevOps:** `Docker`, `Docker Compose`, `Git`, `GitHub`

---

## 📂 Arquitectura y Estructura del Proyecto

```text
nhanes-pipeline/
├── conf/                   # Configuraciones de Kedro (Catálogo de datos, parámetros)
├── data/                   # Datos crudos, intermedios y modelo entrenado (.pkl)
├── src/                    # Código fuente del pipeline ETL de Kedro (Nodos y Pipelines)
├── api.py                  # Servidor Backend (FastAPI) para inferencias
├── app_web.py              # Frontend Dashboard interactivo (Streamlit)
├── Dockerfile.api          # Receta de construcción del contenedor Backend
├── Dockerfile.web          # Receta de construcción del contenedor Frontend
├── docker-compose.yml      # Orquestador de servicios
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Documentación de 
```

## 🔀 Flujo de Datos y Conectividad de Red

[ Usuario / Navegador ] 
       │
       ▼ (Puerto 8501)
┌─────────────────────────────────────────┐
│ Contenedor Frontend: Streamlit          │
│ - Captura parámetros clínicos           │
│ - Envía solicitudes POST HTTP           │
└──────────────────┬──────────────────────┘
                   │
                   ▼ (Puerto 8000: Red Interna Docker)
┌─────────────────────────────────────────┐
│ Contenedor Backend: FastAPI             │
│ - Endpoint REST: `/predict`             │
│ - Orquesta la carga del Modelo XGBoost  │
└─────────────────────────────────────────┘

### 🖥️ Puntos de Acceso Disponibles
Una vez iniciado el despliegue, la suite de herramientas estará disponible en las siguientes direcciones de red:

* **Interfaz de Usuario (Streamlit):** [http://localhost:8501](http://localhost:8501) (Diseño responsivo para personal clínico).
* **Documentación Interactiva de la API:** [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI integrado para pruebas de integración).
* **Consola Base de la API REST (FastAPI):** [http://localhost:8000/](http://localhost:8000/)

---

## 📈 Análisis Crítico y Futuras Mejoras

Si bien este proyecto cumple con un ciclo de vida completo de Machine Learning, identificamos las siguientes áreas de mejora para futuras iteraciones:

1. **Monitoreo de Modelos (MLOps):** Implementar herramientas como MLflow o Evidently AI para monitorear el *Data Drift* y degradación del modelo a lo largo del tiempo.
2. **Ampliación de Variables Clínicas:** Incorporar antecedentes médicos familiares e historial de presión arterial previa en el pipeline ETL para enriquecer las predicciones del XGBoost.
3. **Integración Continua (CI/CD):** Configurar GitHub Actions para que las pruebas unitarias y la construcción de las imágenes de Docker se realicen automáticamente con cada *commit*.
4. **Seguridad y Autenticación:** Añadir protocolos de autenticación (ej. OAuth2) a los *endpoints* de FastAPI para asegurar que solo personal médico autorizado pueda consultar el modelo.
5. **Mejoras UI/UX:** Refinar el diseño visual en Streamlit añadiendo gráficos dinámicos (SHAP values) que expliquen al médico por qué el algoritmo tomó dicha decisión predictiva (Interpretabilidad).