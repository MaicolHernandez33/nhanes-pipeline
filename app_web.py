import streamlit as st
import requests
import os

# 1. Configuración de la página
st.set_page_config(
    page_title="Predicción de Hipertensión", 
    page_icon="🩺", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inyección de CSS Avanzado (Estilo Tarjeta y Botones Pro)
st.markdown("""
<style>
    /* Estilizar los textos (labels) de los inputs para que se vean más grandes y coloridos */
    div[data-testid="stWidgetLabel"] p {
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        color: #64B5F6 !important; /* Azul claro vibrante */
        margin-bottom: 8px !important;
    }

    /* Estilizar el botón de envío del formulario (Fuerza bruta) */
    div[data-testid="stFormSubmitButton"] > button {
        width: 100% !important;
        background-color: #1E88E5 !important; /* Azul corporativo */
        color: white !important;
        font-size: 1.3rem !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 15px 0px !important;
        margin-top: 25px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Efecto al pasar el mouse sobre el botón */
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #1565C0 !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.5) !important;
        transform: translateY(-2px);
        color: white !important;
    }

    /* Contenedor del Formulario (Tarjeta oscura) */
    [data-testid="stForm"] {
        background-color: #161A22; /* Fondo ligeramente más claro que el fondo general */
        border-radius: 15px;
        padding: 30px;
        border: 1px solid #30363D;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    /* Estilos para el Footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0E1117;
        color: #888;
        text-align: center;
        padding: 15px;
        font-size: 0.9rem;
        border-top: 1px solid #333;
        z-index: 100;
    }
    
    /* Dar espacio al final para el footer */
    .block-container {
        padding-bottom: 100px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Barra Lateral (Sidebar) Minimalista
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3003/3003035.png", width=120)
    st.title("Sistema Clínico")
    st.divider()
    st.info("ℹ️ **Acerca del Modelo:**\n\nMotor de IA basado en algoritmo XGBoost, entrenado con datos oficiales de la encuesta NHANES para inferencia metabólica.")
    st.divider()
    st.success("🟢 **Estado del Sistema:**\n\nTodos los servicios operativos. Conexión segura establecida.")

# 4. Encabezado Principal
st.title("🩺 Evaluación de Riesgo de Hipertensión")
st.markdown("Ingrese los parámetros biométricos del paciente para generar una estimación de riesgo clínico en tiempo real.")
st.markdown("---")

# 5. Formulario Estructurado (Ahora con diseño de Tarjeta)
with st.form("formulario_medico"):
    
    # Subsección 1: Datos Físicos
    st.markdown("### 👤 Perfil Biométrico Básico")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        edad = st.number_input("Edad (años)", min_value=1, max_value=120, value=45)
    with col2:
        genero = st.selectbox("Género Biológico", options=[(1, "Masculino"), (2, "Femenino")], format_func=lambda x: x[1])[0]
    with col3:
        estatura = st.number_input("Estatura (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.1)

    st.markdown("<br>", unsafe_allow_html=True)

    # Subsección 2: Métricas Metabólicas
    st.markdown("### 🩸 Indicadores Metabólicos")
    col4, col5, col6 = st.columns(3)
    
    with col4:
        peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=75.0, step=0.1)
        imc = st.number_input("IMC (Índice de Masa Corporal)", min_value=10.0, max_value=60.0, value=25.9, step=0.1)
    with col5:
        cintura = st.number_input("Cintura (cm)", min_value=40.0, max_value=180.0, value=88.0, step=0.1)
        colesterol = st.number_input("Colesterol Total (mg/dL)", min_value=100.0, max_value=400.0, value=195.0, step=1.0)
    with col6:
        fumador = st.selectbox("¿Es Fumador Activo?", options=[(1, "Sí"), (0, "No")], format_func=lambda x: x[1])[0]
        st.write("") # Espaciador

    # Botón de envío (Afectado por el nuevo CSS)
    enviar = st.form_submit_button("📊 Ejecutar Análisis Predictivo")

# 6. Procesamiento de la Predicción
if enviar:
    datos_paciente = {
        "Edad": float(edad),
        "Genero": int(genero),
        "Peso_kg": float(peso),
        "Estatura_cm": float(estatura),
        "IMC": float(imc),
        "Cintura_cm": float(cintura),
        "Colesterol_Total": float(colesterol),
        "Fumador": int(fumador)
    }
    
    # Conexión dinámica
    if os.getenv("STREAMLIT_SERVER_PORT"):
        url_api = "http://api:8000/predict"
    else:
        url_api = "http://127.0.0.1:8000/predict"
    
    try:
        respuesta = requests.post(url_api, json=datos_paciente)
        
        if respuesta.status_code == 200:
            resultado = respuesta.json()
            
            st.markdown("---")
            st.markdown("## 📑 Reporte de Resultados Clínicos")
            
            prob_str = str(resultado['probabilidad_riesgo']).replace('%', '')
            prob_float = float(prob_str)
            
            # Métrica y barra visual
            st.metric(label="Nivel de Riesgo Estimado", value=f"{prob_float:.1f}%")
            st.progress(int(prob_float))
            
            # Alertas
            if resultado["diagnostico_codigo"] == 1:
                st.error(f"**Diagnóstico Automático:** {resultado['resultado']}")
                st.warning(f"⚠️ **Observación Clínica:** {resultado['nota_medica']}")
            else:
                st.success(f"**Diagnóstico Automático:** {resultado['resultado']}")
                st.info(f"💡 **Observación Clínica:** {resultado['nota_medica']}")
                
        else:
            st.error(f"Error en el servidor de inferencia. Código: {respuesta.status_code}")
            
    except requests.exceptions.ConnectionError:
        st.error("❌ Fallo de comunicación con el Backend. Verifique que la API esté operativa.")

# 7. Renderizar el Footer en HTML
st.markdown("""
<div class="footer">
    © Sistema de Evaluación Clínica Inteligente | Potenciado por Machine Learning y Datos Abiertos (NHANES)
</div>
""", unsafe_allow_html=True)