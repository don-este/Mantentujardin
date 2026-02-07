import streamlit as st
import pandas as pd
import time
from datetime import datetime
from io import BytesIO

# --- CONFIGURACIÓN E IDENTIDAD ---
st.set_page_config(page_title="MantenTuJardin Pro", layout="centered")

# CSS Profesional de Alto Contraste (Corregido para lectura clara)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    label, p, span, h1, h2, h3 { color: #000000 !important; font-weight: 700 !important; }
    .stTextInput input, .stNumberInput input, .stSelectbox div {
        background-color: #F8F9FA !important; color: #000000 !important;
        border: 2px solid #2E7D32 !important; border-radius: 8px !important;
    }
    div.stButton > button {
        background-color: #2E7D32 !important; color: white !important;
        height: 60px !important; font-weight: bold !important; border-radius: 12px !important;
    }
    .main-card { background-color: #F8F9FA; padding: 20px; border-radius: 15px; border: 1px solid #E0E0E0; }
    </style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS TEMPORAL (Para que funcione de inmediato) ---
if 'db_clientes' not in st.session_state:
    st.session_state.db_clientes = []
if 'db_servicios' not in st.session_state:
    st.session_state.db_servicios = []
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'view' not in st.session_state:
    st.session_state.view = "MENU"

# --- FUNCIONES DE LOGO Y EXPORTACIÓN ---
def mostrar_logo():
    try:
        st.image("logo.jpg", width=150)
    except:
        st.markdown("<h2 style='color:#2E7D32;'>🌱 MantenTuJardin</h2>", unsafe_allow_html=True)

def descargar_reporte():
    if not st.session_state.db_servicios:
        return None
    df = pd.DataFrame(st.session_state.db_servicios)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Servicios')
    return output.getvalue()

# --- PANTALLA DE ACCESO (LOGIN) ---
if not st.session_state.auth:
    mostrar_logo()
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    user = st.text_input("Usuario")
    pw = st.text_input("Contraseña", type="password")
    if st.button("INICIAR SESIÓN"):
        if user.lower() == "esteban" and pw == "admin123":
            st.session_state.auth, st.session_state.rol = True, "ADMIN"
            st.rerun()
        elif user.lower() == "trabajador" and pw == "jardin2026":
            st.session_state.auth, st.session_state.rol = True, "TRABAJADOR"
            st.rerun()
        else:
            st.error("Credenciales incorrectas")
    st.markdown("</div>", unsafe_allow_html=True)

# --- SISTEMA OPERATIVO ---
else:
    # Cabecera
    col_l, col_r = st.columns([2,1])
    with col_l: mostrar_logo()
    with col_r: 
        if st.button("SALIR"): 
            st.session_state.auth = False
            st.rerun()

    # MENU PRINCIPAL
    if st.session_state.view == "MENU":
        st.write(f"Bienvenido, **{st.session_state.rol}**")
        if st.session_state.rol == "ADMIN":
            if st.button("📍 GESTIÓN DE CLIENTES"): st.session_state.view = "CLIENTES"; st.rerun()
            if st.button("🛠️ REGISTRO DIARIO"): st.session_state.view = "REGISTRO"; st.rerun()
            if st.button("📊 CIERRE Y EXPORTACIÓN"): st.session_state.view = "CIERRE"; st.rerun()
        else:
            if st.button("📝 REGISTRAR MI TRABAJO"): st.session_state.view = "REGISTRO"; st.rerun()

    # SECCIÓN CLIENTES
    elif st.session_state.view == "CLIENTES":
        if st.button("⬅️ VOLVER"): st.session_state.view = "MENU"; st.rerun()
        st.subheader("Nuevo Cliente")
        with st.container():
            st.markdown("<div class='main-card'>", unsafe_allow_html=True)
            n = st.text_input("Nombre")
            d = st.text_input("Dirección")
            s = st.text_input("Servicio")
            v = st.number_input("Valor ($)", min_value=0)
            f = st.selectbox("Plan", ["Mensual", "Visita"])
            if st.button("GUARDAR CLIENTE"):
                st.session_state.db_clientes.append({"Nombre": n, "Direccion": d, "Servicio": s, "Valor": v, "Plan": f})
                st.success("Guardado"); time.sleep(1); st.session_state.view = "MENU"; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # SECCIÓN REGISTRO DIARIO
    elif st.session_state.view == "REGISTRO":
        if st.button("⬅️ VOLVER"): st.session_state.view = "MENU"; st.rerun()
        st.subheader("Bitácora Diaria")
        with st.container():
            st.markdown("<div class='main-card'>", unsafe_allow_html=True)
            fec = st.date_input("Fecha", datetime.now())
            # Si no hay clientes registrados, mostramos una lista manual
            lista_c = [c['Nombre'] for c in st.session_state.db_clientes] if st.session_state.db_clientes else ["Yasna", "Francisca"]
            cl = st.selectbox("Cliente", lista_c)
            det = st.multiselect("Trabajos", ["Pasto", "Piscina", "Poda", "Riego"])
            pag = st.number_input("Pago Trabajador ($)", min_value=0)
            if st.button("FINALIZAR REGISTRO"):
                st.session_state.db_servicios.append({"Fecha": fec, "Cliente": cl, "Trabajo": det, "Pago": pag})
                st.success("Registrado"); time.sleep(1); st.session_state.view = "MENU"; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # SECCIÓN CIERRE
    elif st.session_state.view == "CIERRE":
        if st.button("⬅️ VOLVER"): st.session_state.view = "MENU"; st.rerun()
        st.subheader("Exportar Datos")
        if st.session_state.db_servicios:
            st.write(f"Tienes {len(st.session_state.db_servicios)} registros este mes.")
            excel_data = descargar_reporte()
            st.download_button(label="📥 DESCARGAR EXCEL", data=excel_data, file_name="Reporte_Jardin.xlsx")
        else:
            st.warning("No hay datos para exportar aún.")
