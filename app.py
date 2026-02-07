import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración básica
st.set_page_config(page_title="MantenTuJardin", layout="centered")

# Estilo para botones gigantes y estética móvil
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        height: 80px;
        font-size: 20px;
        border-radius: 15px;
        margin-bottom: 10px;
    }
    .volver-btn button {
        height: 40px;
        background-color: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. LOGO Y SESIÓN ---
try:
    st.image("logo.jpg", width=200)
except:
    st.title("🌱 MantenTuJardin")

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'menu_actual' not in st.session_state:
    st.session_state.menu_actual = "Inicio"

# --- 2. LOGIN ---
if not st.session_state.autenticado:
    user = st.text_input("Usuario").lower()
    password = st.text_input("Clave", type="password")
    if st.button("INICIAR SESIÓN"):
        if user == "esteban" and password == "admin123":
            st.session_state.autenticado, st.session_state.rol = True, "admin"
            st.rerun()
        elif user == "trabajador" and password == "jardin2026":
            st.session_state.autenticado, st.session_state.rol = True, "trabajador"
            st.rerun()
        else:
            st.error("Datos incorrectos")

# --- 3. MENÚ PRINCIPAL (BOTONERA) ---
else:
    if st.session_state.menu_actual == "Inicio":
        st.subheader(f"Hola, {st.session_state.usuario if 'usuario' in st.session_state else 'Bienvenido'}")
        
        # Botones según Rol
        if st.session_state.rol == "admin":
            if st.button("📍 CLIENTES"): st.session_state.menu_actual = "Clientes"; st.rerun()
            if st.button("🛠️ NUEVO SERVICIO"): st.session_state.menu_actual = "Servicio"; st.rerun()
            if st.button("📊 CIERRE DE MES"): st.session_state.menu_actual = "Cierre"; st.rerun()
            if st.button("👥 EQUIPO"): st.session_state.menu_actual = "Equipo"; st.rerun()
        else:
            if st.button("🛠️ REGISTRAR TRABAJO"): st.session_state.menu_actual = "Servicio"; st.rerun()
            if st.button("📅 MIS TRABAJOS"): st.session_state.menu_actual = "MisTrabajos"; st.rerun()
        
        st.divider()
        if st.button("SALIR"):
            st.session_state.autenticado = False
            st.rerun()

    # --- 4. SECCIONES (CRUD) ---
    else:
        # Botón para volver siempre arriba
        if st.button("⬅️ VOLVER AL MENÚ"):
            st.session_state.menu_actual = "Inicio"
            st.rerun()

        if st.session_state.menu_actual == "Clientes":
            st.header("📍 Clientes")
            opc = st.radio("Acción", ["Ver Lista", "Nuevo", "Modificar", "Eliminar"], horizontal=True)
            if opc == "Nuevo":
                st.text_input("Nombre Cliente")
                st.text_input("Dirección")
                st.button("GUARDAR CLIENTE")
            else:
                st.write("Lista de clientes aparecerá aquí.")

        elif st.session_state.menu_actual == "Servicio":
            st.header("🛠️ Registro Diario")
            with st.form("registro"):
                st.date_input("Fecha", datetime.now())
                st.selectbox("Cliente", ["Yasna", "Francisca", "Don Jose"])
                st.multiselect("Trabajo", ["Césped", "Piscina", "Poda", "Riego"])
                st.text_area("Notas")
                if st.form_submit_button("REGISTRAR"):
                    st.success("¡Registrado!")

        elif st.session_state.menu_actual == "Cierre":
            st.header("📊 Cierre Mensual")
            st.selectbox("Mes", ["Enero", "Febrero", "Marzo"])
            st.button("📥 EXPORTAR EXCEL")

        elif st.session_state.menu_actual == "Equipo":
            st.header("👥 Trabajadores")
            st.write("Configuración de operarios.")
            st.button("AÑADIR TRABAJADOR")
