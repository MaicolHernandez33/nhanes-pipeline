import os
import requests
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# 1. CONFIGURACIÓN INICIAL DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Clínica Vida & Salud",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================
# 2. GESTIÓN DEL ESTADO DE LA SESIÓN (ROUTING)
# ==========================================
if "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = "Inicio"
if "resultado" not in st.session_state:
    st.session_state.resultado = None
if "datos_paciente" not in st.session_state:
    st.session_state.datos_paciente = None

# ==========================================
# 3. CSS GLOBAL Y DISEÑO CORPORATIVO Premium
# ==========================================
st.markdown(
    """
    <style>
        /* Ocultar elementos nativos de Streamlit */
        [data-testid="collapsedControl"] { display: none; }
        header { visibility: hidden; }
        footer { visibility: hidden; }
        
        /* Imagen de fondo con filtro blanco fusionado directamente */
        .stApp {
            background-image: linear-gradient(rgba(244, 247, 246, 0.94), rgba(244, 247, 246, 0.94)), url("https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?q=80&w=2053&auto=format&fit=crop");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        
        /* Contenedores tipo tarjeta blanca general */
        .white-card {
            background-color: white;
            padding: 2.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            margin-bottom: 1.5rem;
            border: 1px solid #e2e8f0;
        }
        
        /* Tipografía de la Landing Page */
        .hero-tag { color: #007bc0; font-weight: 700; letter-spacing: 1.5px; font-size: 0.95rem; text-transform: uppercase; }
        .hero-title { color: #007bc0; font-size: 3.5rem !important; font-weight: 800 !important; line-height: 1.1 !important; margin-bottom: 1.5rem; margin-top: 0;}
        .hero-subtitle { color: #334155; font-size: 1.25rem; line-height: 1.6; margin-bottom: 2.5rem; }
        
        /* Estilos EXCLUSIVOS para botones primarios (Azul Clínico) */
        button[kind="primary"] {
            background-color: #007bc0 !important;
            color: white !important;
            padding: 0.75rem 2rem !important;
            border-radius: 8px !important;
            font-size: 1.15rem !important;
            font-weight: 600 !important;
            border: none !important;
            box-shadow: 0 4px 14px rgba(0, 123, 192, 0.3) !important;
            transition: all 0.3s ease !important;
        }
        button[kind="primary"]:hover {
            background-color: #005f9e !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(0, 123, 192, 0.4) !important;
        }

        /* Botones de navegación superior (Navbar) */
        div[data-testid="stButton"] button[kind="secondary"] {
            border: none;
            box-shadow: none;
            background-color: transparent;
            color: #475569;
            font-weight: 700;
            font-size: 1.05rem !important;
            transition: all 0.2s;
        }
        div[data-testid="stButton"] button[kind="secondary"]:hover { color: #007bc0; background-color: #f1f5f9; }
        
        /* Ocultar barra lateral por completo */
        section[data-testid="stSidebar"] { display: none; }

        /* ======== MEJORAS DEL FORMULARIO (LETRAS MÁS GRANDES) ======== */
        
        /* Tarjeta del formulario */
        [data-testid="stForm"] {
            background-color: rgba(255, 255, 255, 0.98);
            padding: 3.5rem;
            border-radius: 12px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.08);
            border: 1px solid #cbd5e1;
            margin-top: 1rem;
        }
        
        /* Agrandar el texto de los labels de inputs (Edad, Peso, etc) */
        div[data-testid="stWidgetLabel"] p {
            font-size: 1.15rem !important;
            font-weight: 600 !important;
            color: #1e293b !important;
        }
        
        /* Subtítulos del formulario limpios */
        .form-subheader {
            color: #007bc0;
            font-size: 1.25rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 0.5rem;
            margin-top: 2rem;
            margin-bottom: 1.5rem;
        }

        /* Tarjetas con Imágenes para la Landing Page */
        .feature-card {
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.06);
            margin-bottom: 1.8rem;
            border: 1px solid #e2e8f0;
            overflow: hidden;
            transition: transform 0.3s ease;
        }
        .feature-card:hover { transform: translateY(-5px); }
        .feature-img-1 { background-image: url('https://images.unsplash.com/photo-1581056771107-24ca5f033842?q=80&w=800&auto=format&fit=crop'); height: 140px; background-size: cover; background-position: center; }
        .feature-img-2 { background-image: url('https://images.unsplash.com/photo-1551076805-e1869033e561?q=80&w=800&auto=format&fit=crop'); height: 140px; background-size: cover; background-position: center 20%; }
        .feature-content { padding: 1.5rem; }
        .feature-content h4 { color: #007bc0; margin-top: 0; margin-bottom: 0.5rem; font-weight: 800; font-size: 1.2rem; }
        .feature-content p { color: #475569; font-size: 0.95rem; margin: 0; line-height: 1.6; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# 4. BARRA DE NAVEGACIÓN SUPERIOR (NAVBAR)
# ==========================================
nav_c1, nav_c2, nav_c3, nav_c4, nav_c5 = st.columns([3, 1, 1, 1, 1.5])

with nav_c1:
    st.markdown("<h3 style='color: #007bc0; margin-top: 5px; font-weight: 800;'>✚ Vida&Salud</h3>", unsafe_allow_html=True)
with nav_c2:
    if st.button("Inicio", use_container_width=True): 
        st.session_state.pagina_actual = "Inicio"
        st.rerun()
with nav_c3:
    if st.button("Evaluación", use_container_width=True): 
        st.session_state.pagina_actual = "Evaluación"
        st.rerun()
with nav_c4:
    if st.button("Resultados", use_container_width=True): 
        st.session_state.pagina_actual = "Resultados"
        st.rerun()
with nav_c5:
    # Vinculamos el botón para que lleve a la nueva página de Agendar
    if st.button("Agendar Hora", type="primary", use_container_width=True):
        st.session_state.pagina_actual = "Agendar"
        st.rerun()

st.markdown("<hr style='margin-top: 0; margin-bottom: 3rem; border-color: #cbd5e1;'>", unsafe_allow_html=True)


# ==========================================
# PÁGINA 1: INICIO (Landing Page)
# ==========================================
if st.session_state.pagina_actual == "Inicio":
    col_hero, col_space, col_cards = st.columns([1.2, 0.1, 1])
    
    with col_hero:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<p class='hero-tag'>Bienestar Integral</p>", unsafe_allow_html=True)
        st.markdown("<h1 class='hero-title'>Evaluación de Riesgo de Hipertensión</h1>", unsafe_allow_html=True)
        st.markdown("<p class='hero-subtitle'>Atención preventiva basada en inteligencia artificial clínica. Diagnósticos inmediatos con tecnología de vanguardia desde la comodidad de su hogar.</p>", unsafe_allow_html=True)
        
        if st.button("Iniciar Evaluación Clínica ➔", type="primary"):
            st.session_state.pagina_actual = "Evaluación"
            st.rerun()
        
    with col_cards:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-img-1'></div>
            <div class='feature-content'>
                <h4>Diagnóstico Avanzado</h4>
                <p>Nuestros modelos predictivos, entrenados con miles de historiales clínicos (NHANES), evalúan sus factores metabólicos con alta precisión.</p>
            </div>
        </div>
        <div class='feature-card'>
            <div class='feature-img-2'></div>
            <div class='feature-content'>
                <h4>Privacidad y Seguridad</h4>
                <p>Sus datos biométricos son procesados bajo estrictos estándares de seguridad y no se almacenan permanentemente en nuestros servidores.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# PÁGINA 2: EVALUACIÓN (Formulario Centrado)
# ==========================================
elif st.session_state.pagina_actual == "Evaluación":
    
    # Creamos un layout de 3 columnas para que el formulario quede en el centro y no se estire
    col_espacio_izq, col_form, col_espacio_der = st.columns([1, 6, 1])
    
    with col_form:
        st.markdown("<h2 class='hero-title' style='font-size: 2.5rem !important; margin-top: 0; text-align: center;'>Registro de Paciente</h2>", unsafe_allow_html=True)
        st.markdown("<p class='hero-subtitle' style='margin-bottom: 1rem; text-align: center;'>Complete los parámetros clínicos para iniciar el análisis predictivo.</p>", unsafe_allow_html=True)
        
        with st.form("formulario_clinico", border=False):
            st.markdown("<div class='form-subheader'>Perfil Biométrico</div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1: edad = st.number_input("Edad (años)", min_value=18, max_value=120, value=45)
            with c2: genero = st.selectbox("Género biológico", options=[(1, "Masculino"), (2, "Femenino")], format_func=lambda x: x[1])[0]
            with c3: estatura = st.number_input("Estatura (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.1)

            st.markdown("<div class='form-subheader'>Indicadores Metabólicos</div>", unsafe_allow_html=True)
            c4, c5, c6 = st.columns(3)
            with c4:
                peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=75.0, step=0.1)
                imc = st.number_input("IMC Calculado", min_value=10.0, max_value=60.0, value=25.9, step=0.1)
            with c5:
                cintura = st.number_input("Cintura (cm)", min_value=40.0, max_value=180.0, value=88.0, step=0.1)
                colesterol = st.number_input("Colesterol total (mg/dL)", min_value=100.0, max_value=400.0, value=195.0, step=1.0)
            with c6:
                fumador = st.selectbox("¿Es fumador activo?", options=[(1, "Sí"), (0, "No")], format_func=lambda x: x[1])[0]

            st.markdown("<br>", unsafe_allow_html=True)
            enviar = st.form_submit_button("Realizar Análisis Predictivo", type="primary", use_container_width=True)

        if enviar:
            datos_paciente = {
                "Edad": float(edad), "Genero": int(genero), "Peso_kg": float(peso),
                "Estatura_cm": float(estatura), "IMC": float(imc), "Cintura_cm": float(cintura),
                "Colesterol_Total": float(colesterol), "Fumador": int(fumador),
            }
            
            url_api = "http://api:8000/predict" if os.getenv("STREAMLIT_SERVER_PORT") else "http://127.0.0.1:8000/predict"
            
            try:
                respuesta = requests.post(url_api, json=datos_paciente, timeout=10)
                if respuesta.status_code == 200:
                    st.session_state.resultado = respuesta.json()
                    st.session_state.datos_paciente = datos_paciente
                    st.session_state.pagina_actual = "Resultados"
                    st.rerun()
                else:
                    st.error(f"Error de red. Código HTTP: {respuesta.status_code}")
            except requests.exceptions.RequestException as exc:
                st.error(f"Error de conexión con el motor de inferencia: {exc}")


# ==========================================
# PÁGINA 3: RESULTADOS (Dashboard)
# ==========================================
elif st.session_state.pagina_actual == "Resultados":
    
    if st.session_state.resultado is None:
        st.warning("⚠️ No hay datos clínicos procesados. Por favor, complete la evaluación en la pestaña correspondiente.")
        if st.button("Ir a Evaluación", type="primary"):
            st.session_state.pagina_actual = "Evaluación"
            st.rerun()
    else:
        res = st.session_state.resultado
        datos = st.session_state.datos_paciente
        prob_str = str(res["probabilidad_riesgo"]).replace("%", "")
        prob_float = float(prob_str)
        
        st.markdown("<h2 style='color: #007bc0; margin-bottom: 0.5rem;'>Resultados de Evaluación Médica</h2>", unsafe_allow_html=True)
        
        st.markdown("<p style='color: #475569; font-weight: 600; font-size: 1.1rem; margin-bottom: 1rem;'>Resumen del Paciente Registrado:</p>", unsafe_allow_html=True)
        
        c_res1, c_res2, c_res3, c_res4 = st.columns(4)
        c_res1.metric("Edad", f"{int(datos['Edad'])} años")
        c_res2.metric("Género", "Masculino" if datos['Genero'] == 1 else "Femenino")
        c_res3.metric("IMC Calculado", f"{datos['IMC']}")
        c_res4.metric("Colesterol", f"{int(datos['Colesterol_Total'])} mg/dL")
        
        st.markdown("<hr style='border-color: #cbd5e1; margin-top: 1rem; margin-bottom: 2rem;'>", unsafe_allow_html=True)
        
        col_grafico, col_texto = st.columns([1, 1.2])
        
        with col_grafico:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = prob_float,
                number = {'suffix': "%", 'font': {'size': 40, 'color': '#334155'}},
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "#334155", 'thickness': 0.25},
                    'bgcolor': "white",
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0, 40], 'color': '#10b981'},     
                        {'range': [40, 70], 'color': '#f59e0b'},    
                        {'range': [70, 100], 'color': '#ef4444'}]   
                }
            ))
            fig.update_layout(height=320, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
            
        with col_texto:
            if res["diagnostico_codigo"] == 1:
                html_resultado = f"""
                <div class='white-card' style='height: 100%; margin-bottom: 0;'>
                    <h3 style='color: #ef4444; margin-top: 0;'>⚠️ Atención Requerida</h3>
                    <p style='font-size: 1.1rem; color: #1e293b;'><strong>Diagnóstico Automático:</strong> {res['resultado']}</p>
                    <p style='color: #475569;'>{res['nota_medica']}</p>
                    <hr style='border-color: #e2e8f0;'>
                    <h4 style='color: #334155;'>Siguientes Pasos Recomendados:</h4>
                    <ol style='color: #475569; line-height: 1.6;'>
                        <li><strong>Agendar hora médica</strong> para revisión presencial y holter de presión.</li>
                        <li>Iniciar monitoreo frecuente de presión arterial en casa.</li>
                        <li>Evaluar panel de lípidos completo en laboratorio.</li>
                    </ol>
                </div>
                """
            else:
                html_resultado = f"""
                <div class='white-card' style='height: 100%; margin-bottom: 0;'>
                    <h3 style='color: #10b981; margin-top: 0;'>✅ Parámetros Saludables</h3>
                    <p style='font-size: 1.1rem; color: #1e293b;'><strong>Diagnóstico Automático:</strong> {res['resultado']}</p>
                    <p style='color: #475569;'>{res['nota_medica']}</p>
                    <hr style='border-color: #e2e8f0;'>
                    <h4 style='color: #334155;'>Consejos Preventivos:</h4>
                    <ol style='color: #475569; line-height: 1.6;'>
                        <li>Mantener su chequeo preventivo anual.</li>
                        <li>Continuar con una dieta balanceada baja en sodio.</li>
                        <li>Realizar al menos 150 minutos de actividad física a la semana.</li>
                    </ol>
                </div>
                """
            st.markdown(html_resultado, unsafe_allow_html=True)


# ==========================================
# PÁGINA 4: AGENDAR HORA (Contacto Elegante)
# ==========================================
elif st.session_state.pagina_actual == "Agendar":
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Columnas para centrar la tarjeta de contacto
    c_izq, c_centro, c_der = st.columns([1, 3, 1])
    
    with c_centro:
        st.markdown("""
        <div class='white-card' style='text-align: center; padding: 4rem 2rem;'>
            <h2 style='color: #007bc0; font-weight: 800; font-size: 2.5rem; margin-bottom: 1rem;'>🗓️ Agendar Consulta Médica</h2>
            <p style='color: #475569; font-size: 1.15rem; margin-bottom: 2rem;'>
                Atención presencial en nuestras sucursales de <strong>Puerto Montt</strong> y consultas por Telemedicina a todo Chile. Nuestro equipo de especialistas está listo para atenderte.
            </p>
            <hr style='border-color: #e2e8f0; margin-bottom: 2rem;'>
            <div style='display: flex; justify-content: space-around; margin-bottom: 2.5rem;'>
                <div>
                    <h4 style='color: #007bc0; margin-bottom: 0.5rem;'>📞 Llámanos</h4>
                    <p style='color: #334155; font-size: 1.2rem; font-weight: 600;'>+56 9 7624 7370</p>
                </div>
                <div>
                    <h4 style='color: #007bc0; margin-bottom: 0.5rem;'>✉️ Escríbenos</h4>
                    <p style='color: #334155; font-size: 1.2rem; font-weight: 600;'>contacto@vidasalud.cl</p>
                </div>
            </div>
            <button style='background-color: #10b981; color: white; border: none; padding: 1rem 3rem; font-size: 1.2rem; font-weight: 600; border-radius: 8px; cursor: pointer; box-shadow: 0 4px 10px rgba(16,185,129,0.3); transition: transform 0.2s;'>
                Chatear por WhatsApp
            </button>
        </div>
        """, unsafe_allow_html=True)