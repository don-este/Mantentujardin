import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="MantenTuJardín", layout="centered")

# =========================
# CREAR ARCHIVOS SI NO EXISTEN
# =========================

def inicializar_archivos():

    # CLIENTES
    if not os.path.exists("clientes.csv"):
        pd.DataFrame(columns=["nombre", "direccion", "telefono"]).to_csv("clientes.csv", index=False)

    # SERVICIOS
    if not os.path.exists("servicios.csv"):
        pd.DataFrame(columns=["servicio", "descripcion"]).to_csv("servicios.csv", index=False)

    # TRABAJADORES
    if not os.path.exists("trabajadores.csv"):
        admin = pd.DataFrame([{
            "usuario": "admin",
            "password": "1234",
            "rol": "admin"
        }])
        admin.to_csv("trabajadores.csv", index=False)

    # REGISTROS
    if not os.path.exists("registros.csv"):
        pd.DataFrame(columns=[
            "fecha", "cliente", "servicio",
            "trabajador", "valor_servicio",
            "pago_trabajador"
        ]).to_csv("registros.csv", index=False)

    # 🔥 Asegurar que admin exista SIEMPRE
    trabajadores = pd.read_csv("trabajadores.csv")

    if "usuario" not in trabajadores.columns:
        trabajadores = pd.DataFrame(columns=["usuario", "password", "rol"])

    if not (trabajadores["usuario"] == "admin").any():
        nuevo_admin = pd.DataFrame([{
            "usuario": "admin",
            "password": "1234",
            "rol": "admin"
        }])
        trabajadores = pd.concat([trabajadores, nuevo_admin], ignore_index=True)
        trabajadores.to_csv("trabajadores.csv", index=False)


inicializar_archivos()

# =========================
# LOGIN
# =========================

def login():

    st.title("🔐 Login")

    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):

        trabajadores = pd.read_csv("trabajadores.csv")

        trabajadores = trabajadores.astype(str)
        trabajadores["usuario"] = trabajadores["usuario"].str.strip()
        trabajadores["password"] = trabajadores["password"].str.strip()
        trabajadores["rol"] = trabajadores["rol"].str.strip()

        usuario = usuario.strip()
        password = password.strip()

        usuario_encontrado = trabajadores[
            (trabajadores["usuario"] == usuario) &
            (trabajadores["password"] == password)
        ]

        if not usuario_encontrado.empty:
            st.session_state["autenticado"] = True
            st.session_state["usuario"] = usuario
            st.session_state["rol"] = usuario_encontrado.iloc[0]["rol"]
            st.rerun()
        else:
            st.error("Credenciales inválidas")

# =========================
# MENU PRINCIPAL (BOTONES)
# =========================

def menu():

    st.title("🏡 MantenTuJardín")

    if st.button("📝 Registro Diario"):
        st.session_state["menu"] = "registro"
        st.rerun()

    if st.session_state["rol"] == "admin":

        if st.button("👥 Clientes"):
            st.session_state["menu"] = "clientes"
            st.rerun()

        if st.button("🛠 Servicios"):
            st.session_state["menu"] = "servicios"
            st.rerun()

        if st.button("👷 Trabajadores"):
            st.session_state["menu"] = "trabajadores"
            st.rerun()

        if st.button("💰 Gestionar Pagos"):
            st.session_state["menu"] = "pagos"
            st.rerun()

    if st.button("🚪 Cerrar sesión"):
        st.session_state.clear()
        st.rerun()

# =========================
# REGISTRO DIARIO
# =========================

def registro_diario():

    st.title("📝 Registro Diario")

    clientes = pd.read_csv("clientes.csv")
    servicios = pd.read_csv("servicios.csv")
    trabajadores = pd.read_csv("trabajadores.csv")

    if clientes.empty or servicios.empty:
        st.warning("Debes crear clientes y servicios primero")
        return

    fecha = st.date_input("Fecha", value=date.today())

    cliente = st.selectbox("Cliente", clientes["nombre"])
    servicio = st.selectbox("Servicio", servicios["servicio"])

    if st.session_state["rol"] == "admin":
        trabajador = st.selectbox("Trabajador", trabajadores["usuario"])
    else:
        trabajador = st.session_state["usuario"]

    valor = st.number_input("Valor del servicio", min_value=0)

    if st.button("Guardar Registro"):

        nuevo = pd.DataFrame([{
            "fecha": fecha,
            "cliente": cliente,
            "servicio": servicio,
            "trabajador": trabajador,
            "valor_servicio": valor,
            "pago_trabajador": 0
        }])

        registros = pd.read_csv("registros.csv")
        registros = pd.concat([registros, nuevo], ignore_index=True)
        registros.to_csv("registros.csv", index=False)

        st.success("Registro guardado")

    if st.button("⬅ Volver"):
        st.session_state["menu"] = "principal"
        st.rerun()

# =========================
# CLIENTES
# =========================

def clientes():

    st.title("👥 Clientes")

    nombre = st.text_input("Nombre")
    direccion = st.text_input("Dirección")
    telefono = st.text_input("Teléfono")

    if st.button("Agregar Cliente"):
        nuevo = pd.DataFrame([{
            "nombre": nombre,
            "direccion": direccion,
            "telefono": telefono
        }])
        df = pd.read_csv("clientes.csv")
        df = pd.concat([df, nuevo], ignore_index=True)
        df.to_csv("clientes.csv", index=False)
        st.success("Cliente agregado")

    st.dataframe(pd.read_csv("clientes.csv"))

    if st.button("⬅ Volver"):
        st.session_state["menu"] = "principal"
        st.rerun()

# =========================
# SERVICIOS
# =========================

def servicios():

    st.title("🛠 Servicios")

    nombre = st.text_input("Nombre del servicio")
    descripcion = st.text_area("Descripción")

    if st.button("Agregar Servicio"):
        nuevo = pd.DataFrame([{
            "servicio": nombre,
            "descripcion": descripcion
        }])
        df = pd.read_csv("servicios.csv")
        df = pd.concat([df, nuevo], ignore_index=True)
        df.to_csv("servicios.csv", index=False)
        st.success("Servicio agregado")

    st.dataframe(pd.read_csv("servicios.csv"))

    if st.button("⬅ Volver"):
        st.session_state["menu"] = "principal"
        st.rerun()

# =========================
# TRABAJADORES
# =========================

def trabajadores():

    st.title("👷 Trabajadores")

    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña")
    rol = st.selectbox("Rol", ["trabajador"])

    if st.button("Agregar Trabajador"):
        nuevo = pd.DataFrame([{
            "usuario": usuario,
            "password": password,
            "rol": rol
        }])
        df = pd.read_csv("trabajadores.csv")
        df = pd.concat([df, nuevo], ignore_index=True)
        df.to_csv("trabajadores.csv", index=False)
        st.success("Trabajador agregado")

    st.dataframe(pd.read_csv("trabajadores.csv"))

    if st.button("⬅ Volver"):
        st.session_state["menu"] = "principal"
        st.rerun()

# =========================
# PAGOS
# =========================

def pagos():

    st.title("💰 Gestionar Pagos")

    registros = pd.read_csv("registros.csv")

    if registros.empty:
        st.info("No hay registros aún")
        return

    st.dataframe(registros)

    index = st.number_input("Número de fila a pagar", min_value=0, max_value=len(registros)-1, step=1)
    pago = st.number_input("Monto a pagar trabajador", min_value=0)

    if st.button("Guardar Pago"):
        registros.loc[index, "pago_trabajador"] = pago
        registros.to_csv("registros.csv", index=False)
        st.success("Pago actualizado")

    if st.button("⬅ Volver"):
        st.session_state["menu"] = "principal"
        st.rerun()

# =========================
# CONTROL PRINCIPAL
# =========================

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if "menu" not in st.session_state:
    st.session_state["menu"] = "principal"

if not st.session_state["autenticado"]:
    login()
else:

    if st.session_state["menu"] == "principal":
        menu()

    elif st.session_state["menu"] == "registro":
        registro_diario()

    elif st.session_state["menu"] == "clientes":
        clientes()

    elif st.session_state["menu"] == "servicios":
        servicios()

    elif st.session_state["menu"] == "trabajadores":
        trabajadores()

    elif st.session_state["menu"] == "pagos":
        pagos()
