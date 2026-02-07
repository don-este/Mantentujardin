import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="MantenTuJardin Pro", layout="centered")

# 2. ESTILO PROFESIONAL (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    div.stButton > button {
        width: 100%; height: 65px; border-radius: 12px;
        font-weight: bold; font-size: 18px; margin-bottom: 10px;
        background-color: #FFFFFF; color: #1A5D1A; border: 1px solid #1A5D1A;
    }
    .card {
        background-color: white; padding: 20px;
        border-radius: 10px; border-left: 5px solid #1A5D1A;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- ESTADOS DE NAVEGACIÓN ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'menu_principal' not in st.session_state: st.session_state.menu_principal = "INICIO"
if 'sub_menu' not in st.session_state: st.session_state.sub_menu = None

# --- LOGIN ---
if not st.session_state.auth:
    st.markdown("<h2 style='text-align: center;'>🌱 MantenTuJardin</h2>", unsafe_allow_html=True)
    user = st.text_input("Usuario")
    passw = st.text_input("Clave", type="password")
    if st.button("INGRESAR"):
        if user == "esteban" and passw == "admin123":
            st.session_state.auth = True
            st.rerun()
else:
    # --- MENÚ PRINCIPAL ---
    if st.session_state.menu_principal == "INICIO":
        st.subheader("Menú Principal")
        
        # Tal como pediste: Solo la opción "CLIENTE" al inicio
        if st.button("📍 CLIENTE"):
            st.session_state.menu_principal = "CLIENTE_MENU"
            st.rerun()
            
        if st.button("🚪 CERRAR SESIÓN"):
            st.session_state.auth = False
            st.rerun()

    # --- SUB-MENÚ: CLIENTE ---
    elif st.session_state.menu_principal == "CLIENTE_MENU":
        if st.button("⬅️ VOLVER AL INICIO"):
            st.session_state.menu_principal = "INICIO"
            st.session_state.sub_menu = None
            st.rerun()
            
        st.subheader("Gestión de Clientes")
        
        # Opciones del menú de cliente
        col1, col2, col3 = st.columns(3)
        if col1.button("➕ NUEVO"): st.session_state.sub_menu = "NUEVO"
        if col2.button("✏️ EDITAR"): st.session_state.sub_menu = "EDITAR"
        if col3.button("🗑️ ELIMINAR"): st.session_state.sub_menu = "ELIMINAR"

        st.divider()

        # Formularios según la opción pinchada
        if st.session_state.sub_menu == "NUEVO":
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.write("**Registrar Nuevo Cliente**")
            nombre = st.text_input("Nombre completo")
            direccion = st.text_input("Dirección")
            servicio = st.text_input("Tipo de Servicio (Ej: Jardín y Piscina)")
            valor = st.number_input("Valor del Servicio ($)", min_value=0, step=1000)
            tipo_plan = st.selectbox("Frecuencia", ["Visita única", "Mensual"])
            
            if st.button("💾 GUARDAR CLIENTE"):
                st.success(f"Cliente {nombre} registrado exitosamente.")
            st.markdown("</div>", unsafe_allow_html=True)

        elif st.session_state.sub_menu == "EDITAR":
            st.write("**Modificar datos de cliente existente**")
            cliente_sel = st.selectbox("Seleccione cliente", ["Yasna", "Francisca", "Don Jose"])
            st.text_input("Nueva Dirección", value="Calle Falsa 123")
            st.button("Actualizar Datos")

        elif st.session_state.sub_menu == "ELIMINAR":
            st.write("**Eliminar Cliente**")
            st.selectbox("Seleccione cliente a eliminar", ["Yasna", "Francisca", "Don Jose"])
            if st.button("❌ CONFIRMAR ELIMINACIÓN"):
                st.warning("Cliente eliminado.")
