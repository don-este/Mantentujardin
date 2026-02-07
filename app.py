import streamlit as st
import time
from datetime import datetime

# 1. CONFIGURACIÓN
st.set_page_config(page_title="MantenTuJardin Admin", layout="centered")

# 2. CSS DE ALTO CONTRASTE (Profesional y legible)
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
        height: 60px !important;
        width: 100% !important;
        font-size: 18px !important;
        font-weight: bold !important;
        margin-bottom: 10px;
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

# --- VISTA PRINCIPAL (MENÚ DE BOTONES GRANDES) ---
if st.session_state.view == "MENU":
    st.markdown("<h1 style='text-align:center; color:#2E7D32;'>MantenTuJardin</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Panel de Control</p>", unsafe_allow_html=True)
    
    if st.button("📍 GESTIÓN DE CLIENTES"):
        st.session_state.view = "CLIENTES"; st.rerun()
    
    if st.button("🛠️ SERVICIOS"):
        st.session_state.view = "SERVICIOS"; st.rerun()

# --- VISTA CLIENTES ---
elif st.session_state.view == "CLIENTES":
    if st.button("⬅️ VOLVER AL MENÚ"):
        st.session_state.view = "MENU"; st.rerun()
    
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#2E7D32;'>📍 Nuevo Cliente</h2>", unsafe_allow_html=True)
    
    nom = st.text_input("Nombre Completo")
    dir = st.text_input("Dirección")
    ser_clie = st.text_input("Servicio Contratado")
    
    c1, c2 = st.columns(2)
    with c1: val_clie = st.number_input("Valor Cobrado ($)", min_value=0, step=1000)
    with c2: frq = st.selectbox("Tipo", ["Mensual", "Visita"])
    
    if st.button("💾 GUARDAR CLIENTE"):
        st.success("¡Cliente guardado! Volviendo...")
        time.sleep(1.2)
        st.session_state.view = "MENU"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- VISTA SERVICIOS (AÑADIR TRABAJOS REALIZADOS) ---
elif st.session_state.view == "SERVICIOS":
    if st.button("⬅️ VOLVER AL MENÚ"):
        st.session_state.view = "MENU"; st.rerun()
    
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#2E7D32;'>🛠️ Registro de Servicio Diario</h2>", unsafe_allow_html=True)
    
    fecha = st.date_input("Fecha del Servicio", datetime.now())
    # Aquí en el futuro cargaremos los nombres de tu lista de clientes
    cliente_serv = st.selectbox("Seleccionar Cliente", ["Yasna", "Francisca", "Don Jose", "Otro"])
    
    detalle = st.text_area("Descripción del trabajo (Ej: Corte de pasto y limpieza de orillas)")
    
    # Campo para que tú asignes el pago al trabajador por ese servicio
    pago_trabajador = st.number_input("Monto Pago para Trabajador ($)", min_value=0, step=500, help="Valor que le pagarás al empleado por este servicio")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✅ REGISTRAR SERVICIO"):
        st.success(f"Servicio registrado para {cliente_serv}. Volviendo...")
        time.sleep(1.2)
        st.session_state.view = "MENU"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
