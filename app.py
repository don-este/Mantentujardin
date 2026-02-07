import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="MantenTuJardin Pro", layout="wide", page_icon="🌱")

# --- 1. ESTILO Y LOGO ---
def mostrar_logo():
    try:
        st.sidebar.image("logo.jpg", use_container_width=True)
    except:
        st.sidebar.title("🌱 MantenTuJardin")

# --- 2. SISTEMA DE AUTENTICACIÓN ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
    st.session_state.rol = None
    st.session_state.usuario = None

def login():
    st.title("Bienvenido a MantenTuJardin")
    st.subheader("Sistema de Gestión Operativa")
    
    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            with st.form("login_form"):
                user = st.text_input("Usuario (Correo)")
                password = st.text_input("Contraseña", type="password")
                submit = st.form_submit_button("Iniciar Sesión")
                
                if submit:
                    # Lógica de acceso (Temporal hasta conectar Base de Datos)
                    if user == "esteban" and password == "admin123":
                        st.session_state.autenticado = True
                        st.session_state.rol = "admin"
                        st.session_state.usuario = "Esteban"
                        st.rerun()
                    elif user == "trabajador" and password == "jardin2026":
                        st.session_state.autenticado = True
                        st.session_state.rol = "trabajador"
                        st.session_state.usuario = "Operario"
                        st.rerun()
                    else:
                        st.error("Credenciales incorrectas. Verifica tu usuario y clave.")

# --- 3. INTERFAZ PRINCIPAL ---
if not st.session_state.autenticado:
    login()
else:
    mostrar_logo()
    st.sidebar.write(f"👤 **Usuario:** {st.session_state.usuario}")
    st.sidebar.write(f"🛡️ **Rol:** {st.session_state.rol.capitalize()}")
    st.sidebar.divider()

    # NAVEGACIÓN SEGÚN ROL
    if st.session_state.rol == "admin":
        menu = st.sidebar.radio("NAVEGACIÓN", [
            "🏠 Dashboard", 
            "👥 Trabajadores", 
            "📍 Clientes", 
            "🛠️ Servicios", 
            "📊 Cierre de Mes"
        ])
    else:
        menu = st.sidebar.radio("NAVEGACIÓN", ["📝 Registrar Servicio", "📅 Mis Servicios"])

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.autenticado = False
        st.rerun()

    # --- LÓGICA DE SECCIONES ---

    if menu == "🏠 Dashboard":
        st.title("📊 Resumen del Negocio")
        st.write(f"Hoy es: {datetime.now().strftime('%A, %d de %B de %Y')}")
        
        # Simulación de métricas
        col1, col2, col3 = st.columns(3)
        col1.metric("Servicios Hoy", "4")
        col2.metric("Clientes Activos", "12")
        col3.metric("Pagos Pendientes", "$120.000")

    elif menu == "👥 Trabajadores":
        st.title("Gestionar Equipo")
        tab1, tab2 = st.tabs(["Lista de Trabajadores", "Registrar Nuevo"])
        
        with tab1:
            st.write("Aquí podrás ver el rendimiento de tu equipo.")
            # Simulación de tabla
            df_t = pd.DataFrame({'Nombre': ['Juan Perez', 'Luis Soto'], 'Correo': ['juan@mail.com', 'luis@mail.com'], 'Estado': ['Activo', 'Activo']})
            st.table(df_t)
            
        with tab2:
            with st.form("nuevo_t"):
                st.text_input("Nombre Completo")
                st.text_input("Correo Electrónico")
                st.text_input("Contraseña Provisoria")
                if st.form_submit_button("Crear Trabajador"):
                    st.success("Trabajador registrado exitosamente.")

    elif menu == "📍 Clientes":
        st.title("Cartera de Clientes")
        acc = st.selectbox("¿Qué deseas hacer?", ["Ver Clientes", "Nuevo Cliente", "Modificar Cliente", "Eliminar Cliente"])
        
        if acc == "Nuevo Cliente":
            with st.form("form_cliente"):
                st.text_input("Nombre del Cliente (Ej: Yasna)")
                st.text_input("Dirección del Servicio")
                st.text_input("Teléfono de Contacto")
                if st.form_submit_button("Guardar"):
                    st.success("Cliente añadido a la base de datos.")

    elif menu == "🛠️ Servicios" or menu == "📝 Registrar Servicio":
        st.title("Registro Diario de Servicios")
        st.info("Registra aquí los trabajos realizados hoy.")
        
        with st.form("form_servicio"):
            fecha = st.date_input("Fecha", datetime.now())
            cliente = st.selectbox("Seleccionar Cliente", ["Yasna", "Francisca", "Jose Manuel"])
            tareas = st.multiselect("Trabajos realizados", ["Corte de Césped", "Limpieza de Piscina", "Poda", "Fumigación", "Riego"])
            comentario = st.text_area("Notas adicionales (opcional)")
            
            if st.form_submit_button("Guardar Registro"):
                st.success(f"Servicio para {cliente} registrado correctamente el día {fecha}.")
                # Aquí guardaremos el log para el Excel final

    elif menu == "📊 Cierre de Mes":
        st.title("Exportación y Pagos")
        st.write("Genera el reporte para pagar a tus trabajadores y enviar boletas.")
        
        mes = st.selectbox("Seleccionar Mes", ["Enero", "Febrero", "Marzo", "Abril"])
        
        if st.button("📥 Generar y Descargar Excel"):
            # Lógica para crear el Excel (Simulada)
            st.balloons()
            st.success(f"Reporte de {mes} generado con éxito.")
            st.download_button(label="Descargar Archivo", data="Contenido del excel", file_name=f"Reporte_{mes}.csv")

    elif menu == "📅 Mis Servicios":
        st.title("Mi Historial")
        st.write("Servicios realizados por ti este mes:")
        # Aquí se mostraría una tabla filtrada por el usuario logueado
