import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="MantenTuJardín", layout="centered")

# ---------- INICIALIZAR ARCHIVOS ----------

def inicializar_archivos():

    if not os.path.exists("clientes.csv"):
        df = pd.DataFrame(columns=["nombre", "direccion", "telefono",
                                   "tipo_contrato", "valor", "servicio"])
        df.to_csv("clientes.csv", index=False)

    if not os.path.exists("servicios.csv"):
        df = pd.DataFrame(columns=["nombre", "descripcion"])
        df.to_csv("servicios.csv", index=False)

    if not os.path.exists("trabajadores.csv"):
        df = pd.DataFrame(columns=["usuario", "password", "nombre", "rol"])
        df.loc[0] = ["admin", "1234", "Administrador", "admin"]
        df.to_csv("trabajadores.csv", index=False)

    if not os.path.exists("registros.csv"):
        df = pd.DataFrame(columns=["fecha", "cliente", "servicio",
                                   "trabajador", "valor", "pagado"])
        df.to_csv("registros.csv", index=False)

inicializar_archivos()

# ---------- FUNCION SEGURA CSV ----------

def cargar_csv(nombre, columnas):
    df = pd.read_csv(nombre)
    for col in columnas:
        if col not in df.columns:
            df[col] = ""
    return df

# ---------- LOGIN ----------

def login():

    st.markdown("<h2 style='text-align:center;'>🌿 MantenTuJardín</h2>", unsafe_allow_html=True)

    if os.path.exists("logo.jpg"):
        st.image("logo.jpg", width=220)

    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar", use_container_width=True):

        trabajadores = cargar_csv("trabajadores.csv",
                                  ["usuario", "password", "nombre", "rol"])

        user = trabajadores[
            (trabajadores["usuario"].astype(str).str.strip() == usuario.strip()) &
            (trabajadores["password"].astype(str).str.strip() == password.strip())
        ]

        if not user.empty:
            st.session_state["usuario"] = usuario
            st.session_state["rol"] = user.iloc[0]["rol"]
            st.session_state["menu"] = "principal"
            st.rerun()
        else:
            st.error("Credenciales inválidas")

# ---------- MENU PRINCIPAL ----------

def menu_principal():

    st.markdown("## 📋 Menú Principal")

    if st.button("📝 Registro Diario", use_container_width=True):
        st.session_state["menu"] = "registro"

    if st.session_state["rol"] == "admin":

        if st.button("👥 Clientes", use_container_width=True):
            st.session_state["menu"] = "clientes_menu"

        if st.button("🛠 Servicios", use_container_width=True):
            st.session_state["menu"] = "servicios_menu"

        if st.button("👷 Trabajadores", use_container_width=True):
            st.session_state["menu"] = "trabajadores_menu"

        if st.button("💰 Revisar Registros", use_container_width=True):
            st.session_state["menu"] = "revisar"

    if st.button("🚪 Cerrar sesión", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ---------- SUBMENU SERVICIOS ----------

def servicios_menu():

    st.markdown("## 🛠 Gestión de Servicios")

    if st.button("➕ Nuevo Servicio", use_container_width=True):
        st.session_state["menu"] = "servicio_nuevo"

    if st.button("✏ Modificar Servicio", use_container_width=True):
        st.session_state["menu"] = "servicio_modificar"

    if st.button("🗑 Eliminar Servicio", use_container_width=True):
        st.session_state["menu"] = "servicio_eliminar"

    if st.button("⬅ Volver", use_container_width=True):
        st.session_state["menu"] = "principal"
        st.rerun()

# ---------- NUEVO SERVICIO ----------

def servicio_nuevo():

    st.markdown("## ➕ Nuevo Servicio")

    servicios = cargar_csv("servicios.csv", ["nombre", "descripcion"])

    nombre = st.text_input("Nombre del servicio")
    descripcion = st.text_area("Descripción")

    if st.button("Guardar Servicio", use_container_width=True):

        if nombre.strip() == "":
            st.error("El nombre es obligatorio")
        else:
            nuevo = pd.DataFrame([{
                "nombre": nombre,
                "descripcion": descripcion
            }])

            servicios = pd.concat([servicios, nuevo], ignore_index=True)
            servicios.to_csv("servicios.csv", index=False)
            st.success("Servicio guardado")

    if st.button("⬅ Volver", use_container_width=True):
        st.session_state["menu"] = "servicios_menu"
        st.rerun()

# ---------- REGISTRO DIARIO ----------

def registro_diario():

    st.markdown("## 📝 Registro Diario")

    clientes = cargar_csv("clientes.csv",
                          ["nombre", "direccion", "telefono",
                           "tipo_contrato", "valor", "servicio"])

    trabajadores = cargar_csv("trabajadores.csv",
                               ["usuario", "password", "nombre", "rol"])

    if clientes.empty:
        st.warning("No hay clientes registrados.")
        return

    cliente = st.selectbox("Cliente", clientes["nombre"])
    cliente_info = clientes[clientes["nombre"] == cliente].iloc[0]

    trabajador = st.selectbox(
        "Trabajador",
        trabajadores[trabajadores["rol"] == "trabajador"]["nombre"]
    )

    fecha = st.date_input("Fecha", datetime.today())

    if st.button("Guardar Registro", use_container_width=True):

        nuevo = pd.DataFrame([{
            "fecha": fecha,
            "cliente": cliente,
            "servicio": cliente_info["servicio"],
            "trabajador": trabajador,
            "valor": cliente_info["valor"],
            "pagado": "No"
        }])

        registros = cargar_csv("registros.csv",
                               ["fecha", "cliente", "servicio",
                                "trabajador", "valor", "pagado"])

        registros = pd.concat([registros, nuevo], ignore_index=True)
        registros.to_csv("registros.csv", index=False)

        st.success("Registro guardado")

    if st.button("⬅ Volver", use_container_width=True):
        st.session_state["menu"] = "principal"
        st.rerun()

# ---------- CONTROL PRINCIPAL ----------

if "usuario" not in st.session_state:
    login()
else:

    menu = st.session_state.get("menu", "principal")

    if menu == "principal":
        menu_principal()
    elif menu == "servicios_menu":
        servicios_menu()
    elif menu == "servicio_nuevo":
        servicio_nuevo()
    elif menu == "registro":
        registro_diario()
