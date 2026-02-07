import streamlit as st
from datetime import datetime

# 1. CONFIGURACIÓN E IDENTIDAD
st.set_page_config(page_title="MantenTuJardin Admin", layout="centered")

# 2. CSS DE ALTO NIVEL (Diseño App Nativa)
st.markdown("""
    <style>
    /* Fondo general */
    .stApp { background-color: #F0F2F5; }
    
    /* Input Fields Profesionales */
    .stTextInput input, .stNumberInput input, .stSelectbox div {
        background-color: white !important;
        color: #1C1E21 !important;
        border-radius: 8px !important;
        border: 1px solid #CCD0D5 !important;
    }
    
    /* Botones de Navegación */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        height: 50px;
        transition: 0.3s;
    }
    
    /* Botón Principal (Verde Corporativo) */
    .btn-main button {
        background-color: #2E7D32 !important;
        color: white !important;
        border: none !important;
        width: 100%;
    }
    
    /* Contenedor de Formulario */
    .main-card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DE ESTADO ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'view' not in st.session_state: st.session_state.view = "LOGIN"

# --- LOGIN ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; color:#2E7D32;'>MantenTuJardin</h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        user = st.text_input("Usuario")
        pw = st.text_input("Clave", type="password")
        if st.button("ACCEDER"):
            if user == "esteban" and pw == "admin123":
                st.session_state.auth = True; st.session_state.view = "MENU"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- MENÚ PRINCIPAL ---
    if st.session_state.view == "MENU":
        st.markdown("### Panel de Administración")
        st.markdown('<div class="btn-main">', unsafe_allow_html=True)
        if st.button("📍 GESTIÓN DE CLIENTES"):
            st.session_state.view = "CLIENTES"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🚪 CERRAR SESIÓN"):
            st.session_state.auth = False; st.rerun()

    # --- VISTA CLIENTES ---
    elif st.session_state.view == "CLIENTES":
        col_back, col_title = st.columns([1, 4])
        with col_back:
            if st.button("⬅️"): st.session_state.view = "MENU"; st.rerun()
        with col_title:
            st.subheader("📍 Clientes")

        tab1, tab2, tab3 = st.tabs(["➕ NUEVO", "✏️ EDITAR", "🗑️ BORRAR"])

        with tab1:
            st.markdown('<div class="main-card">', unsafe_allow_html=True)
            st.markdown("#### Registro de Cliente")
            nom = st.text_input("Nombre Completo")
            dir = st.text_input("Dirección Google Maps")
            ser = st.text_input("Servicio Contratado (Ej: Jardín + Piscina)")
            
            c1, c2 = st.columns(2)
            with c1: val = st.number_input("Valor del Servicio", min_value=0, step=5000)
            with c2: frq = st.selectbox("Modalidad", ["Mensual", "Por Visita"])
            
            st.markdown('<div class="btn-main">', unsafe_allow_html=True)
            if st.button("💾 GUARDAR CLIENTE"):
                st.success(f"Cliente {nom} registrado con éxito.")
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.write("Seleccione cliente para modificar...")
            st.selectbox("Buscar Cliente", ["Yasna", "Francisca"])
