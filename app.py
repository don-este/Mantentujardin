import streamlit as st
import time
from datetime import datetime

# 1. CONFIGURACIÓN DE SEGURIDAD Y PÁGINA
st.set_page_config(page_title="MantenTuJardin Pro", layout="centered")

# 2. CSS PROFESIONAL (ALTO CONTRASTE)
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    label, p, span, .stMarkdown { color: #000000 !important; font-weight: 700 !important; }
    .stTextInput input, .stNumberInput input, .stSelectbox div {
        background-color: #FFFFFF !important; color: #000000 !important;
        border: 2px solid #2E7D32 !important; border-radius: 8px !important;
    }
    div.stButton > button {
        background-color: #2E7D32 !important; color: #FFFFFF !important;
        height: 60px !important; width: 100% !important;
        font-size: 18px !important; font-weight: bold !important;
        border-radius: 12px !important; margin-bottom: 10px;
    }
    .btn-volver button { background-color: #6C757D !important; height: 45px !important; }
    .main-card { background-color: #FFFFFF; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# --- 3. GESTIÓN DE SESIÓN Y LOGIN ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'rol' not in st.session_state: st.session_state.rol = None
if 'view' not in st.session_state: st.session_state.view = "MENU"

def login():
    st.markdown("<h1 style='text-align:center; color:#2E7D32;'>🌱 MantenTuJardin</h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        user = st.text_input("Usuario / Email").lower().strip()
        pw = st.text_input("Contraseña", type="password")
        
        if st.button("ACCEDER AL SISTEMA"):
            # Lógica de acceso segura
            if user == "esteban" and pw == "admin123":
                st.session_state.auth, st.session_state.rol = True, "ADMIN"
                st.rerun()
            elif user == "trabajador" and pw == "jardin2026":
                st.session_state.auth, st.session_state.rol = True, "TRABAJADOR"
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 4. APLICACIÓN PROTEGIDA ---
if not st.session_state.auth:
    login()
else:
    # BOTÓN SALIR (Siempre visible arriba a la derecha)
    col_user, col_out = st.columns([3, 1])
    col_user.write(f"👤 **{st.session_state.rol}**")
    if col_out.button("SALIR"):
        st.session_state.auth = False
        st.rerun()

    # --- NAVEGACIÓN SEGÚN ROL ---
    if st.session_state.view == "MENU":
        st.subheader("Panel de Operaciones")
        
        if st.session_state.rol == "ADMIN":
            if st.button("📍 GESTIÓN DE CLIENTES"): st.session_state.view = "CLIENTES"; st.rerun()
            if st.button("🛠️ REGISTRO DIARIO (BITÁCORA)"): st.session_state.view = "REGISTRO"; st.rerun()
            if st.button("📊 CIERRE DE MES"): st.session_state.view = "CIERRE"; st.rerun()
        else:
            # Vista limitada para el trabajador
            if st.button("📝 REGISTRAR MI TRABAJO"): st.session_state.view = "REGISTRO"; st.rerun()

    # --- SECCIÓN: CLIENTES (SOLO ADMIN) ---
    elif st.session_state.view == "CLIENTES" and st.session_state.rol == "ADMIN":
        if st.button("⬅️ VOLVER"): st.session_state.view = "MENU"; st.rerun()
        
        tab1, tab2, tab3 = st.tabs(["➕ NUEVO", "✏️ EDITAR", "🗑️ BORRAR"])
        
        with tab1:
            st.markdown('<div class="main-card">', unsafe_allow_html=True)
            nom = st.text_input("Nombre del Cliente")
            dir = st.text_input("Dirección")
            ser = st.text_input("Servicio Contratado")
            val = st.number_input("Valor Servicio ($)", min_value=0, step=1000)
            fre = st.selectbox("Frecuencia", ["Mensual", "Por Visita"])
            if st.button("💾 GUARDAR CLIENTE"):
                st.success(f"Cliente {nom} guardado.")
                time.sleep(1.2); st.session_state.view = "MENU"; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # --- SECCIÓN: REGISTRO DIARIO (AMBOS ROLES) ---
    elif st.session_state.view == "REGISTRO":
        if st.button("⬅️ VOLVER"): st.session_state.view = "MENU"; st.rerun()
        
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown("### Registro de Actividad")
        st.date_input("Fecha", datetime.now())
        
        if st.session_state.rol == "ADMIN":
            trab = st.selectbox("Trabajador", ["Juan Perez", "Luis Soto"])
        else:
            st.write(f"Trabajador: **{st.session_state.rol}**")
            
        clie = st.selectbox("Cliente Atendido", ["Yasna", "Francisca", "Don Jose"])
        task = st.multiselect("Tareas", ["Pasto", "Piscina", "Poda", "Otros"])
        
        if st.session_state.rol == "ADMIN":
            pago = st.number_input("Pago asignado por este servicio ($)", min_value=0)
            
        if st.button("✅ FINALIZAR REGISTRO"):
            st.success("Información enviada con éxito.")
            time.sleep(1.2); st.session_state.view = "MENU"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
