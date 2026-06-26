import os
import requests
import streamlit as st


st.set_page_config(
    page_title="Predicción de Hipertensión",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


if "datos_paciente" not in st.session_state:
    st.session_state.datos_paciente = None
if "resultado" not in st.session_state:
    st.session_state.resultado = None


st.markdown(
    """
    <style>
        div[data-testid="stWidgetLabel"] p {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            color: #64B5F6 !important;
            margin-bottom: 8px !important;
        }
        div[data-testid="stFormSubmitButton"] > button {
            width: 100% !important;
            background-color: #1E88E5 !important;
            color: white !important;
            font-size: 1.2rem !important;
            font-weight: bold !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 12px 0px !important;
            margin-top: 20px !important;
        }
        [data-testid="stForm"] {
            background-color: #161A22;
            border-radius: 15px;
            padding: 24px;
            border: 1px solid #30363D;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #0E1117;
            color: #888;
            text-align: center;
            padding: 12px;
            font-size: 0.9rem;
            border-top: 1px solid #333;
            z-index: 100;
        }
        .block-container {
            padding-bottom: 100px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3003/3003035.png", width=120)
    st.title("Sistema Clínico")
    st.divider()
    st.info(
        "ℹ️ El sistema utiliza un modelo XGBoost para estimar el riesgo de hipertensión a partir de datos clínicos básicos."
    )
    st.divider()
    st.success("🟢 El flujo está preparado para trabajar con el backend y la API de predicción.")


st.title("🩺 Evaluación de Riesgo de Hipertensión")
st.markdown("Una interfaz guiada para que el médico registre datos clínicos y obtenga una evaluación rápida del riesgo.")
st.markdown("---")


inicio_tab, datos_tab, resultado_tab = st.tabs(["Inicio", "Registrar datos", "Resultado"])


with inicio_tab:
    st.markdown("### Bienvenido al módulo clínico")
    st.write(
        "Este panel está dividido en tres ventanas para facilitar el flujo de trabajo del profesional de salud:"
    )
    st.markdown(
        "1. Inicio: comprende el propósito del sistema y los datos que se evaluarán.\n"
        "2. Registrar datos: permite capturar los parámetros clínicos del paciente.\n"
        "3. Resultado: muestra la predicción del modelo y la recomendación clínica."
    )
    st.info("El modelo utiliza variables como edad, peso, IMC, cintura, colesterol y hábito de fumar para estimar el riesgo.")

    with st.container():
        st.markdown("#### Flujo recomendado")
        st.markdown("- Revisar la información del paciente")
        st.markdown("- Completar el formulario clínico")
        st.markdown("- Consultar el resultado del análisis")


with datos_tab:
    st.markdown("### 🧾 Datos del paciente")
    st.write("Complete la información clínica para generar la evaluación predictiva.")

    with st.form("formulario_medico"):
        st.markdown("#### 👤 Perfil biométrico")
        col1, col2, col3 = st.columns(3)
        with col1:
            edad = st.number_input("Edad (años)", min_value=1, max_value=120, value=45)
        with col2:
            genero = st.selectbox(
                "Género biológico",
                options=[(1, "Masculino"), (2, "Femenino")],
                format_func=lambda x: x[1],
            )[0]
        with col3:
            estatura = st.number_input("Estatura (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.1)

        st.markdown("#### 🩸 Indicadores metabólicos")
        col4, col5, col6 = st.columns(3)
        with col4:
            peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=75.0, step=0.1)
            imc = st.number_input("IMC", min_value=10.0, max_value=60.0, value=25.9, step=0.1)
        with col5:
            cintura = st.number_input("Cintura (cm)", min_value=40.0, max_value=180.0, value=88.0, step=0.1)
            colesterol = st.number_input("Colesterol total (mg/dL)", min_value=100.0, max_value=400.0, value=195.0, step=1.0)
        with col6:
            fumador = st.selectbox(
                "¿Es fumador activo?",
                options=[(1, "Sí"), (0, "No")],
                format_func=lambda x: x[1],
            )[0]

        enviar = st.form_submit_button("📊 Ejecutar análisis predictivo")

    if enviar:
        datos_paciente = {
            "Edad": float(edad),
            "Genero": int(genero),
            "Peso_kg": float(peso),
            "Estatura_cm": float(estatura),
            "IMC": float(imc),
            "Cintura_cm": float(cintura),
            "Colesterol_Total": float(colesterol),
            "Fumador": int(fumador),
        }

        if os.getenv("STREAMLIT_SERVER_PORT"):
            url_api = "http://api:8000/predict"
        else:
            url_api = "http://127.0.0.1:8000/predict"

        try:
            respuesta = requests.post(url_api, json=datos_paciente, timeout=10)
            if respuesta.status_code == 200:
                st.session_state.datos_paciente = datos_paciente
                st.session_state.resultado = respuesta.json()
                st.success("Análisis completado. Puede revisar el resultado en la ventana de resultados.")
            else:
                st.error(f"Error en el servidor de inferencia. Código: {respuesta.status_code}")
        except requests.exceptions.RequestException as exc:
            st.error(f"No fue posible contactar con la API: {exc}")


with resultado_tab:
    st.markdown("### 📑 Resultado del análisis")
    if st.session_state.resultado is None:
        st.info("Aún no hay un resultado disponible. Complete el formulario en la ventana de registro para generar la evaluación.")
    else:
        resultado = st.session_state.resultado
        prob_str = str(resultado["probabilidad_riesgo"]).replace("%", "")
        prob_float = float(prob_str)

        st.metric("Nivel de riesgo estimado", f"{prob_float:.1f}%")
        st.progress(int(prob_float))

        if resultado["diagnostico_codigo"] == 1:
            st.error(f"**Diagnóstico automático:** {resultado['resultado']}")
            st.warning(f"⚠️ **Observación clínica:** {resultado['nota_medica']}")
        else:
            st.success(f"**Diagnóstico automático:** {resultado['resultado']}")
            st.info(f"💡 **Observación clínica:** {resultado['nota_medica']}")

        st.markdown("#### Datos utilizados")
        st.json(st.session_state.datos_paciente)


st.markdown(
    """
    <div class="footer">
        © Sistema de Evaluación Clínica Inteligente | Potenciado por Machine Learning y Datos Abiertos (NHANES)
    </div>
    """,
    unsafe_allow_html=True,
)