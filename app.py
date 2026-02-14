import streamlit as st
import pandas as pd
import os
from datetime import date

# =========================
# ARCHIVOS
# =========================

ARCH_CLIENTES = "clientes.xlsx"
ARCH_SERVICIOS = "servicios.xlsx"
ARCH_TRABAJADORES = "trabajadores.xlsx"
ARCH_REGISTROS = "registros_diarios.xlsx"

# =========================
# CREAR ARCHIVOS SI NO EXISTEN
# =========================

def crear_archivos():
    if not os.path.exists(ARCH_CLIENTES):
        pd.DataFrame(columns=["nombre","direccion","telefono"]).to_excel(ARCH_CLIENTES, index=False)

    if not os.path.exists(ARCH_SERVICIOS):
        pd.DataFrame(columns=["servicio","descripcion"]).to_excel(ARCH_SERVICIOS, index=False)

    if not os.path.exists(ARCH_TRABAJADORES):
        df = pd.DataFrame([{
            "usuario": "admin",
            "password": "1234",
            "nombre": "Administrador",
            "rol": "admin"
        }])
        df.to_excel(ARCH_TRABAJADORES, index=False)

    if not os.path.exists(ARCH_REGISTROS):
        pd.DataFrame(columns=[
            "fecha","cliente","servicio",
            "trabajador","valor_servicio","registrado_por"
        ]).to_excel(ARCH_REGISTROS, index=False)

crear_archivos()

# =========================
# FUNCIONES
# =========================

def cargar(ruta):
    return pd.read_excel(ruta)

def guardar(df, ruta):
    df.to_excel(ruta, index=False)

# =========================
# SESSION STATE
# =========================

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
    st.session_state.rol = None
    st.session_state.nombre = None
    st.session_state.pantalla = "menu"

# =========================
# LOGIN
# =========================

def login():
    st.title("🔐 Sistema Mantenciones")

    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):

        trabajadores = cargar(ARCH_TRABAJADORES)

        # Asegurar columnas
        columnas = ["usuario","password","nombre","rol"]
        for col in columnas:
            if col not in trabajadores.columns:
                trabajadores[col] = ""

        # Limpiar datos
        trabajadores = trabajadores.fillna("")
        trabajadores["usuario"] = trabajadores["usuario"].astype(str).str.strip()
        trabajadores["password"] = trabajadores["password"].astype(str).str.strip()

        usuario = usuario.strip()
        password = password.strip()

        fila = trabajadores[
            (trabajadores["usuario"] == usuario) &
            (trabajadores["password"] == password)
        ]

        if len(fila) == 1:
            st.session_state.autenticado = True
            st.session_state.rol = fila.iloc[0]["rol"]
            st.session_state.nombre = fila.iloc[0]["nombre"]
            st.rerun()
        else:
            st.error("Credenciales inválidas")

# =========================
# MENÚ PRINCIPAL
# =========================

def menu():
    st.title("📋 Menú Principal")
    st.write(f"👤 {st.session_state.nombre} ({st.session_state.rol})")
    st.markdown("---")

    if st.session_state.rol == "admin":

        col1, col2 = st.columns(2)

        with col1:
            if st.button("📅 Registro Diario"):
                st.session_state.pantalla = "registro"

        with col2:
            if st.button("👥 Clientes"):
                st.session_state.pantalla = "clientes"

        col3, col4 = st.columns(2)

        with col3:
            if st.button("🛠 Servicios"):
                st.session_state.pantalla = "servicios"

        with col4:
            if st.button("🧑‍🔧 Trabajadores"):
                st.session_state.pantalla = "trabajadores"

    else:
        if st.button("📅 Registro Diario"):
            st.session_state.pantalla = "registro"

    st.markdown("---")

    if st.button("Cerrar sesión"):
        st.session_state.clear()
        st.rerun()

# =========================
# REGISTRO DIARIO
# =========================

def registro():
    st.header("📅 Registro Diario")

    clientes = cargar(ARCH_CLIENTES)
    servicios = cargar(ARCH_SERVICIOS)
    trabajadores = cargar(ARCH_TRABAJADORES)

    if clientes.empty or servicios.empty:
        st.warning("Debes crear al menos un cliente y un servicio.")
        return

    fecha = st.date_input("Fecha", date.today())
    cliente = st.selectbox("Cliente", clientes["nombre"])
    servicio = st.selectbox("Servicio", servicios["servicio"])
    trabajador = st.selectbox("Trabajador", trabajadores["nombre"])

    valor = 0
    if st.session_state.rol == "admin":
        valor = st.number_input("Valor del servicio", min_value=0, step=1000)

    if st.button("Guardar"):
        registros = cargar(ARCH_REGISTROS)

        nuevo = pd.DataFrame([{
            "fecha": fecha,
            "cliente": cliente,
            "servicio": servicio,
            "trabajador": trabajador,
            "valor_servicio": valor,
            "registrado_por": st.session_state.nombre
        }])

        registros = pd.concat([registros, nuevo], ignore_index=True)
        guardar(registros, ARCH_REGISTROS)

        st.success("Registro guardado ✅")

    if st.button("⬅ Volver"):
        st.session_state.pantalla = "menu"

# =========================
# CLIENTES
# =========================

def clientes():
    st.header("👥 Clientes")

    df = cargar(ARCH_CLIENTES)

    nombre = st.text_input("Nombre")
    direccion = st.text_input("Dirección")
    telefono = st.text_input("Teléfono")

    if st.button("Agregar Cliente"):
        nuevo = pd.DataFrame([{
            "nombre": nombre,
            "direccion": direccion,
            "telefono": telefono
        }])
        df = pd.concat([df, nuevo], ignore_index=True)
        guardar(df, ARCH_CLIENTES)
        st.success("Cliente agregado")

    if st.button("⬅ Volver"):
        st.session_state.pantalla = "menu"

# =========================
# SERVICIOS
# =========================

def servicios():
    st.header("🛠 Servicios")

    df = cargar(ARCH_SERVICIOS)

    nombre = st.text_input("Nombre Servicio")
    descripcion = st.text_area("Descripción")

    if st.button("Agregar Servicio"):
        nuevo = pd.DataFrame([{
            "servicio": nombre,
            "descripcion": descripcion
        }])
        df = pd.concat([df, nuevo], ignore_index=True)
        guardar(df, ARCH_SERVICIOS)
        st.success("Servicio agregado")

    if st.button("⬅ Volver"):
        st.session_state.pantalla = "menu"

# =========================
# TRABAJADORES
# =========================

def trabajadores():
    st.header("🧑‍🔧 Trabajadores")

    df = cargar(ARCH_TRABAJADORES)

    nombre = st.text_input("Nombre")
    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña")

    if st.button("Agregar Trabajador"):
        nuevo = pd.DataFrame([{
            "usuario": usuario,
            "password": password,
            "nombre": nombre,
            "rol": "trabajador"
        }])
        df = pd.concat([df, nuevo], ignore_index=True)
        guardar(df, ARCH_TRABAJADORES)
        st.success(f"Trabajador creado ✅ Usuario: {usuario}")

    if st.button("⬅ Volver"):
        st.session_state.pantalla = "menu"

# =========================
# CONTROL DE PANTALLAS
# =========================

if not st.session_state.autenticado:
    login()
else:
    if st.session_state.pantalla == "menu":
        menu()
    elif st.session_state.pantalla == "registro":
        registro()
    elif st.session_state.pantalla == "clientes":
        clientes()
    elif st.session_state.pantalla == "servicios":
        servicios()
    elif st.session_state.pantalla == "trabajadores":
        trabajadores()
