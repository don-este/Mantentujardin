import streamlit as st
import time
from datetime import datetime

# 1. CONFIGURACIÓN
st.set_page_config(page_title="MantenTuJardin Operaciones", layout="centered")

# 2. CSS PROFESIONAL (Basado en tu logo y feedback de colores)
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    /* Etiquetas en negro puro para lectura clara */
    label, p, .stMarkdown { color: #000000 !important; font-weight: 700 !important; }
    
    /* Inputs con bordes verdes definidos */
    .stTextInput input, .stNumberInput input, .stSelectbox div, .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #2E7D32 !important;
    }
    
    /* Botones de acción principal */
    div.stButton > button {
        background-color: #2E7D32 !important;
        color: #FFFFFF !important;
        height: 60px !important;
        font-size: 18px !important;
        border-radius: 10px;
    }
    /* Botón Volver */
    .btn-volver button {
        background-color: #6c757d !important;
        height: 40px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DE NAVEGACIÓN ---
if 'view' not in st.session_state: st.session_state.view = "MENU"

# --- MENÚ PRINCIPAL ---
if st.session_state.view == "MENU":
    st.markdown("<h1 style='text-align:center; color:#2E7D32;'>🌱 MantenTuJardin</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📍 CLIENTES"): st.session_state.view = "CLIENTES"; st.rerun()
    with col2:
        if st.button("🛠️ REGISTRO DIARIO"): st.session_state.view = "REGISTRO"; st.rerun()

# --- VISTA: REGISTRO DIARIO (UN CLIENTE A LA VEZ) ---
elif st.session_state.view == "REGISTRO":
    st.markdown("<div class='btn-volver'>", unsafe_allow_html=True)
    if st.button("⬅️ VOLVER"): st.session_state.view = "MENU"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.header("📝 Registro de Servicio Diario")
    st.info("Ingresa los datos del servicio realizado para que quede en la bitácora mensual.")

    with st.container():
        # 1. Datos de Identificación
        fecha = st.date_input("Fecha del Servicio", datetime.now())
        
        col_t, col_c = st.columns(2)
        with col_t:
            # Esto vendrá de tu lista de trabajadores
            trabajador = st.selectbox("Trabajador asignado", ["Juan Perez", "Luis Soto", "Esteban (Admin)"])
        with col_c:
            # Esto vendrá de tu lista de clientes
            cliente = st.selectbox("Cliente atendido", ["Yasna", "Francisca", "Don Jose", "Empresa X"])

        # 2. Detalle del Trabajo
        servicio_tipo = st.multiselect("Servicios realizados", 
                                       ["Corte de Pasto", "Limpieza Piscina", "Poda", "Fumigación", "Riego"])
        
        descripcion = st.text_area("Notas específicas del día", placeholder="Ej: Se aplicó cloro adicional a la piscina...")

        # 3. Valorización
        monto_pago = st.number_input("Monto a pagar al trabajador por este servicio ($)", min_value=0, step=1000)

        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("✅ GUARDAR Y REGISTRAR SIGUIENTE"):
            if cliente and trabajador:
                # Aquí simulamos el guardado
                st.success(f"¡Registrado! El servicio de {trabajador} para {cliente} se guardó correctamente.")
                time.sleep(1.5)
                # Volvemos al menú para decidir si registrar otro o ir a clientes
                st.session_state.view = "MENU"
                st.rerun()
            else:
                st.error("Por favor completa los campos obligatorios.")

# --- VISTA: CLIENTES (Mantenemos tu diseño funcional) ---
elif st.session_state.view == "CLIENTES":
    if st.button("⬅️ VOLVER AL MENÚ"): st.session_state.view = "MENU"; st.rerun()
    st.subheader("📍 Gestión de Clientes")
    # (Aquí va el código de Nuevo/Editar/Eliminar que ya aprobaste)
