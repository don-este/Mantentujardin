import streamlit as st
import time # Importamos time para dar un segundo de feedback antes de volver

# 1. CONFIGURACIÓN
st.set_page_config(page_title="MantenTuJardin Admin", layout="centered")

# 2. CSS DE ALTO CONTRASTE (Mantenemos tu diseño profesional)
st.markdown("""
    <style>
    .stApp { background-color: #F0F2F5; }
    label, p, span, .stMarkdown { color: #1C1E21 !important; font-weight: 600 !important; }
    .stTextInput input, .stNumberInput input, .stSelectbox div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #2E7D32 !important;
        border-radius: 8px !important;
    }
    div.stButton > button {
        background-color: #2E7D32 !important;
        color: #FFFFFF !important;
        border: none !important;
        height: 55px !important;
        width: 100% !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }
    .main-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DE NAVEGACIÓN ---
if 'view' not in st.session_state: st.session_state.view = "MENU"

# --- VISTA PRINCIPAL ---
if st.session_state.view == "MENU":
    st.markdown("<h1 style='text-align:center; color:#2E7D32;'>MantenTuJardin</h1>", unsafe_allow_html=True)
    
    # Botonera Principal
    if st.button("📍 GESTIÓN DE CLIENTES"):
        st.session_state.view = "CLIENTES"; st.rerun()
    
    # Aquí puedes ir sumando los otros botones que pediste antes (Servicios, Equipo, etc.)
    if st.button("🛠️ SERVICIOS"):
        st.info("Sección en desarrollo...")

# --- VISTA CLIENTES ---
elif st.session_state.view == "CLIENTES":
    if st.button("⬅️ VOLVER AL MENÚ"):
        st.session_state.view = "MENU"; st.rerun()
    
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#2E7D32;'>📍 Registro de Cliente</h2>", unsafe_allow_html=True)
    
    nom = st.text_input("Nombre Completo del Cliente")
    dir = st.text_input("Dirección (Calle, Número, Comuna)")
    ser = st.text_input("Servicio (Ej: Jardín Completo + Piscina)")
    
    c1, c2 = st.columns(2)
    with c1:
        val = st.number_input("Valor del Servicio ($)", min_value=0, step=1000)
    with c2:
        frq = st.selectbox("Modalidad de Pago", ["Mensual", "Por Visita"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # LÓGICA DE GUARDADO Y RETORNO AUTOMÁTICO
    if st.button("💾 GUARDAR CLIENTE"):
        if nom and dir: # Validación simple
            st.success(f"¡Cliente {nom} guardado! Volviendo al menú...")
            time.sleep(1.5) # Pausa de 1.5 segundos para que alcances a leer el mensaje verde
            st.session_state.view = "MENU"
            st.rerun()
        else:
            st.warning("Por favor, completa al menos el nombre y la dirección.")
    
    st.markdown("</div>", unsafe_allow_html=True)
