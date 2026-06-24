import streamlit as st
import requests

# Configuración de la página
st.set_page_config(page_title="Predicción de Hipertensión", page_icon="🩺", layout="centered")

st.title("🩺 Sistema de Evaluación de Riesgo de Hipertensión")
st.write("Introduzca los datos clínicos del paciente para obtener un diagnóstico en tiempo real basado en el modelo oficial XGBoost.")

st.markdown("---")

# Crear el formulario en la interfaz
with st.form("formulario_medico"):
    col1, col2 = st.columns(2)
    
    with col1:
        edad = st.number_input("Edad (años)", min_value=1, max_value=120, value=45)
        genero = st.selectbox("Género Biológico", options=[(1, "Masculino"), (2, "Femenino")], format_func=lambda x: x[1])[0]
        peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=75.0, step=0.1)
        estatura = st.number_input("Estatura (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.1)
        
    with col2:
        imc = st.number_input("IMC (Índice de Masa Corporal)", min_value=10.0, max_value=60.0, value=25.9, step=0.1)
        cintura = st.number_input("Circunferencia de Cintura (cm)", min_value=40.0, max_value=180.0, value=88.0, step=0.1)
        colesterol = st.number_input("Colesterol Total (mg/dL)", min_value=100.0, max_value=400.0, value=195.0, step=1.0)
        fumador = st.selectbox("¿Es Fumador?", options=[(1, "Sí"), (0, "No")], format_func=lambda x: x[1])[0]

    # Botón de envío
    enviar = st.form_submit_button("📊 Calcular Riesgo Clínico")

# Cuando el usuario presiona el botón
if enviar:
    # 1. Preparar los datos tal como los espera tu API (FastAPI)
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
    
    # 2. Dirección local de tu FastAPI
    url_api = "http://127.0.0.1:8000/predict"
    
    try:
        # Enviar los datos a la API por el método POST
        respuesta = requests.post(url_api, json=datos_paciente)
        
        if respuesta.status_code == 200:
            resultado = respuesta.json()
            
            # 3. Mostrar los resultados de forma bonita según el diagnóstico
            st.markdown("### 📋 Resultado de la Evaluación")
            
            if resultado["diagnostico_codigo"] == 1:
                st.error(f"**Resultado:** {resultado['resultado']} (Probabilidad: {resultado['probabilidad_riesgo']})")
                st.warning(f"⚠️ **Nota Médica:** {resultado['nota_medica']}")
            else:
                st.success(f"**Resultado:** {resultado['resultado']} (Probabilidad: {resultado['probabilidad_riesgo']})")
                st.info(f"💡 **Nota Médica:** {resultado['nota_medica']}")
                
        else:
            st.error("Error en el servidor de predicción. Código de respuesta no exitoso.")
            
    except requests.exceptions.ConnectionError:
        st.error("❌ No se pudo conectar con el motor de IA. Asegúrate de que FastAPI esté corriendo en el puerto 8000.")