import streamlit as st
import pandas as pd
import time
from datetime import datetime
from io import BytesIO

# --- 1. CONFIGURACIÓN Y ESTILO (UX MÓVIL) ---
st.set_page_config(page_title="MantenTuJardin Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    /* Texto Negro Puro para máxima legibilidad */
    label, p, span, h1, h2, h3 { color: #000000 !important; font-weight: 800 !important; }
    
    /* Inputs Estilo Premium */
    .stTextInput input, .stNumberInput input, .stSelectbox div, .stTextArea textarea {
        background-color: #F1F3F4 !important;
        color: #000000 !important;
        border: 2px solid #2E7D32 !important;
        border-radius: 12px !important;
        height: 45px;
    }

    /* Botones Gigantes para Pulgar */
    div.stButton > button {
        background-color: #2E7D32 !important;
        color: white !important;
        height: 70px !important;
        width: 100% !important;
        border-radius: 15px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: none !important;
    }
    
    /* Tarjeta de Formulario */
    .form-container {
        background-color: #FFFFFF;
        padding: 20px;
        border: 1px solid #E0E0E0;
        border-radius: 20px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. PERSISTENCIA DE DATOS (ESTADO DE SESIÓN) ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'view' not in st.session_state: st.session_state.view = "MENU"
if 'clientes' not in st.session_state: st.session_state.clientes = []
if 'servicios' not in st.session_state: st.session_state.servicios = []

# --- 3. FUNCIONES CORE ---
def logo():
    try: st.image("logo.jpg", width=160)
    except: st.markdown("<h1 style='color:#2E7D32;'>🌱 MANTEN TU JARDÍN</h1>", unsafe_allow_html=True)

def generar_excel():
    if not st.session_state.servicios: return None
    df = pd.DataFrame(st.session_state.servicios)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

# --- 4. LÓGICA DE PANTALLAS ---

# A. LOGIN
if not st.session_state.auth:
    logo()
    st.markdown("### Acceso al Sistema")
    with st.container():
        user = st.text_input("Usuario")
        pw = st.text_input("Contraseña", type="password")
        if st.button("ENTRAR"):
            if user.lower() == "esteban" and pw == "admin123":
                st.session_state.auth, st.session_state.rol = True, "ADMIN"
                st.rerun()
            elif user.lower() == "trabajador" and pw == "jardin2026":
                st.session_state.auth, st.session_state.rol = True, "TRABAJADOR"
                st.rerun()
            else: st.error("Acceso Denegado")

# B. MENÚ PRINCIPAL
elif st.session_state.view == "MENU":
    logo()
    st.write(f"Conectado como: **{st.session_state.rol}**")
    
    if st.session_state.rol == "ADMIN":
        # Métricas rápidas (Dashboard)
        c1, c2 = st.columns(2)
        c1.metric("Clientes", len(st.session_state.clientes))
        c2.metric("Servicios hoy", len([s for s in st.session_state.servicios if s['Fecha'] == datetime.now().date()]))
        
        st.divider()
        if st.button("📍 GESTIÓN DE CLIENTES"): st.session_state.view = "CLIENTES"; st.rerun()
        if st.button("🛠️ REGISTRO DIARIO"): st.session_state.view = "REGISTRO"; st.rerun()
        if st.button("📊 CIERRE Y REPORTES"): st.session_state.view = "REPORTES"; st.rerun()
    else:
        if st.button("📝 REGISTRAR TRABAJO"): st.session_state.view = "REGISTRO"; st.rerun()

    if st.button("🚪 CERRAR SESIÓN"):
        st.session_state.auth = False
        st.rerun()

# C. GESTIÓN DE CLIENTES
elif st.session_state.view == "CLIENTES":
    if st.button("⬅️ VOLVER"): st.session_state.view = "MENU"; st.rerun()
    
    opcion = st.radio("Acción", ["Nuevo Cliente", "Modificar/Eliminar"], horizontal=True)
    
    if opcion == "Nuevo Cliente":
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        nom = st.text_input("Nombre Completo")
        dir = st.text_input("Dirección")
        ser = st.text_input("Servicio Contratado")
        val = st.number_input("Valor Cobrado ($)", min_value=0)
        fre = st.selectbox("Frecuencia", ["Mensual", "Por Visita"])
        
        if st.button("💾 GUARDAR"):
            if nom and dir:
                st.session_state.clientes.append({"Nombre": nom, "Direccion": dir, "Servicio": ser, "Valor": val, "Plan": fre})
                st.success("Cliente Registrado")
                time.sleep(1); st.session_state.view = "MENU"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# D. REGISTRO DIARIO (BITÁCORA)
elif st.session_state.view == "REGISTRO":
    if st.button("⬅️ VOLVER"): st.session_state.view = "MENU"; st.rerun()
    st.header("Registro Diario")
    
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
    fec = st.date_input("Fecha", datetime.now())
    
    # Lista de clientes dinámica
    clie_list = [c['Nombre'] for c in st.session_state.clientes] if st.session_state.clientes else ["Yasna", "Francisca", "Jose"]
    clie = st.selectbox("Seleccionar Cliente", clie_list)
    
    det = st.multiselect("Trabajos realizados", ["Corte Pasto", "Orillado", "Piscina (Aspirado)", "Piscina (Químicos)", "Poda", "Riego"])
    obs = st.text_area("Notas del terreno")
    
    if st.session_state.rol == "ADMIN":
        pago = st.number_input("Monto Pago para Trabajador ($)", min_value=0)
    else: pago = 0 # El trabajador no ve esto
    
    if st.button("✅ FINALIZAR Y VOLVER"):
        st.session_state.servicios.append({"Fecha": fec, "Cliente": clie, "Tareas": det, "Pago": pago, "Obs": obs})
        st.success("¡Registro Exitoso!")
        time.sleep(1); st.session_state.view = "MENU"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# E. REPORTES Y CIERRE
elif st.session_state.view == "REPORTES":
    if st.button("⬅️ VOLVER"): st.session_state.view = "MENU"; st.rerun()
    st.header("Cierre de Mes")
    
    if st.session_state.servicios:
        df = pd.DataFrame(st.session_state.servicios)
        st.write("Resumen de servicios registrados:")
        st.dataframe(df)
        
        data = generar_excel()
        st.download_button("📥 DESCARGAR EXCEL DE PAGOS", data, "Cierre_Mes.xlsx")
    else:
        st.warning("No hay datos registrados aún.")
