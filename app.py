import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN TÉCNICA
st.set_page_config(page_title="MantenTuJardin Pro", layout="centered", page_icon="🌱")

# 2. DISEÑO PROFESIONAL (CSS PERSONALIZADO)
st.markdown("""
    <style>
    /* Fondo y tipografía */
    .stApp { background-color: #f8f9fa; }
    
    /* Botones Principales */
    div.stButton > button {
        background-color: #ffffff;
        color: #2e7d32; /* Verde bosque */
        border: 2px solid #2e7d32;
        border-radius: 12px;
        height: 70px;
        font-weight: bold;
        font-size: 18px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.05);
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        background-color: #2e7d32;
        color: white;
        transform: translateY(-2px);
    }
    
    /* Botón de Salir */
    .logout-btn button {
        background-color: #fce4ec !important;
        color: #c2185b !important;
        border: none !important;
        height: 40px !important;
    }
    
    /* Tarjetas de información */
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DE ESTADO ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'seccion' not in st.session_state:
    st.session_state.seccion = "Inicio"

# --- PANTALLA DE LOGIN PROFESIONAL ---
if not st.session_state.autenticado:
    st.markdown("<h1 style='text-align: center; color: #1b5e20;'>MantenTuJardin</h1>", unsafe_allow_html=True)
    try:
        st.image("logo.jpg", width=200)
    except: pass
    
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        user = st.text_input("Usuario / Email").lower()
        password = st.text_input("Contraseña", type="password")
        if st.button("ACCEDER AL SISTEMA"):
            if user == "esteban" and password == "admin123":
                st.session_state.autenticado, st.session_state.rol, st.session_state.usuario = True, "admin", "Esteban"
                st.rerun()
            elif user == "trabajador" and password == "jardin2026":
                st.session_state.autenticado, st.session_state.rol, st.session_state.usuario = True, "trabajador", "Operario"
                st.rerun()
            else:
                st.error("Credenciales no autorizadas.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- PANEL DE CONTROL ---
else:
    # Encabezado con Logo
    col_logo, col_text = st.columns([1, 2])
    with col_logo:
        try: st.image("logo.jpg", width=80)
        except: st.write("🌱")
    with col_text:
        st.markdown(f"**{st.session_state.usuario}**<br><small>{st.session_state.rol.upper()}</small>", unsafe_allow_html=True)

    st.divider()

    if st.session_state.seccion == "Inicio":
        st.subheader("Menú de Gestión")
        
        # Botonera Estilo App Móvil Profesional
        if st.session_state.rol == "admin":
            if st.button("📍 Gestión de Clientes"): 
                st.session_state.seccion = "Clientes"; st.rerun()
            if st.button("🛠️ Registro de Servicio"): 
                st.session_state.seccion = "Servicio"; st.rerun()
            if st.button("📊 Reportes y Cierre"): 
                st.session_state.seccion = "Cierre"; st.rerun()
            if st.button("👥 Gestión de Equipo"): 
                st.session_state.seccion = "Equipo"; st.rerun()
        else:
            if st.button("🛠️ Registrar Trabajo Diario"): 
                st.session_state.seccion = "Servicio"; st.rerun()
            if st.button("📅 Mi Historial"): 
                st.session_state.seccion = "Historial"; st.rerun()

        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("SALIR DEL SISTEMA"):
            st.session_state.autenticado = False
            st.rerun()

    # --- SECCIONES DETALLADAS ---
    else:
        if st.button("⬅️ VOLVER"):
            st.session_state.seccion = "Inicio"
            st.rerun()

        st.markdown(f"### {st.session_state.seccion}")
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        if st.session_state.seccion == "Clientes":
            modo = st.radio("Acción", ["Ver Todos", "Nuevo", "Modificar"], horizontal=True)
            if modo == "Nuevo":
                st.text_input("Nombre Completo")
                st.text_input("Dirección Google Maps")
                st.button("CONFIRMAR REGISTRO")

        elif st.session_state.seccion == "Servicio":
            st.date_input("Fecha de Servicio", datetime.now())
            st.selectbox("Cliente", ["Yasna", "Francisca", "Don Jose"])
            st.multiselect("Actividades", ["Corte de Pasto", "Aspirado Piscina", "Químicos", "Poda", "Abono"])
            st.text_area("Notas del Terreno")
            if st.button("FINALIZAR Y GUARDAR"):
                st.success("Registro almacenado correctamente.")

        elif st.session_state.seccion == "Cierre":
            st.write("Generación de documentos mensuales.")
            st.selectbox("Seleccione Mes", ["Febrero 2026", "Enero 2026"])
            st.button("📥 EXPORTAR PLANILLA EXCEL")

        st.markdown("</div>", unsafe_allow_html=True)
