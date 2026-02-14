import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="MantenTuJardín", layout="centered")

# =========================
# ESTILOS PERSONALIZADOS
# =========================

st.markdown("""
<style>
.big-button {
    width: 100%;
    height: 70px;
    font-size: 20px;
    font-weight: bold;
    border-radius: 12px;
    margin-bottom: 15px;
}
.center-logo {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# INICIALIZAR ARCHIVOS
# =========================

def inicializar_archivos():

    if not os.path.exists("clientes.csv"):
        pd.DataFrame(columns=["nombre", "direccion", "telefono"]).to_csv("clientes.csv", index=False)

    if not os.path.exists("servicios.csv"):
        pd.DataFrame(columns=["servicio", "descripcion"]).to_csv("servicios.csv", index=False)

    if not os.path.exists("trabajadores.csv"):
        pd.DataFrame([{
            "usuario": "admin",
            "password": "1234",
            "rol": "admin"
        }]).to_csv("trabajadores.csv", index=False)

    if not os.path.exists("registros.csv"):
        pd.DataFrame(columns=[
            "fecha", "cliente", "servicio",
            "trabajador", "valor_servicio",
            "pago_trabajador"
        ]).to_csv("registros.csv", index=False)

    # asegurar admin
    trabajadores = pd.read_csv("trabajadores.csv")
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

    st.markdown('<div class="center-logo">', unsafe_allow_html=True)
    st.image("logo.png", width=220)
    st.markdown('</div>', unsafe_allow_html=True)

    st.title("Iniciar Sesión")

    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar", use_container_width=True):

        trabajadores = pd.read_csv("trabajadores.csv").astype(str)

        usuario_encontrado = trabajadores[
            (trabajadores["usuario"] == usuario.strip()) &
            (trabajadores["password"] == password.strip())
        ]

        if not usuario_encontrado.empty:
            st.session_state["autenticado"] = True
            st.session_state["usuario"] = usuario
            st.session_state["rol"] = usuario_encontrado.iloc[0]["rol"]
            st.rerun()
        else:
            st.error("Credenciales inválidas")

# =========================
# MENU PRINCIPAL PROFESIONAL
# =========================

def menu():

    st.markdown('<div class="center-logo">', unsafe_allow_html=True)
    st.image("logo.png", width=200)
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader(f"Bienvenido {st.session_state['usuario']}")

    if st.button("📝 REGISTRO DIARIO", use_container_width=True):
        st.session_state["menu"] = "registro"
        st.rerun()

    if st.session_state["rol"] == "admin":

        if st.button("👥 CLIENTES", use_container_width=True):
            st.session_state["menu"] = "clientes"
            st.rerun()

        if st.button("🛠 SERVICIOS", use_container_width=True):
            st.session_state["menu"] = "servicios"
            st.rerun()

        if st.button("👷 TRABAJADORES", use_container_width=True):
            st.session_state["menu"] = "trabajadores"
            st.rerun()

        if st.button("💰 GESTIONAR PAGOS", use_container_width=True):
            st.session_state["menu"] = "pagos"
            st.rerun()

    st.markdown("---")

    if st.button("🚪 Cerrar sesión", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# =========================
# REGISTRO DIARIO
# =========================

def registro_diario():

    st.title("Registro Diario")

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

    if st.button("Guardar Registro", use_container_width=True):

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

        st.success("Registro guardado correctamente")

    if st.button("⬅ Volver al menú", use_container_width=True):
        st.session_state["menu"] = "principal"
        st.rerun()

# =========================
# CLIENTES
# =========================

def clientes():
    st.title("Clientes")

    nombre = st.text_input("Nombre")
    direccion = st.text_input("Dirección")
    telefono = st.text_input("Teléfono")

    if st.button("Agregar Cliente", use_container_width=True):
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

    if st.button("⬅ Volver", use_container_width=True):
        st.session_state["menu"] = "principal"
        st.rerun()

# =========================
# SERVICIOS
# =========================

def servicios():
    st.title("Servicios")

    nombre = st.text_input("Nombre del servicio")
    descripcion = st.text_area("Descripción")

    if st.button("Agregar Servicio", use_container_width=True):
        nuevo = pd.DataFrame([{
            "servicio": nombre,
            "descripcion": descripcion
        }])
        df = pd.read_csv("servicios.csv")
        df = pd.concat([df, nuevo], ignore_index=True)
        df.to_csv("servicios.csv", index=False)
        st.success("Servicio agregado")

    st.dataframe(pd.read_csv("servicios.csv"))

    if st.button("⬅ Volver", use_container_width=True):
        st.session_state["menu"] = "principal"
        st.rerun()

# =========================
# TRABAJADORES
# =========================

def trabajadores():
    st.title("Trabajadores")

    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña")

    if st.button("Agregar Trabajador", use_container_width=True):
        nuevo = pd.DataFrame([{
            "usuario": usuario,
            "password": password,
            "rol": "trabajador"
        }])
        df = pd.read_csv("trabajadores.csv")
        df = pd.concat([df, nuevo], ignore_index=True)
        df.to_csv("trabajadores.csv", index=False)
        st.success("Trabajador agregado")

    st.dataframe(pd.read_csv("trabajadores.csv"))

    if st.button("⬅ Volver", use_container_width=True):
        st.session_state["menu"] = "principal"
        st.rerun()

# =========================
# PAGOS
# =========================

def pagos():
    st.title("Gestionar Pagos")

    registros = pd.read_csv("registros.csv")

    if registros.empty:
        st.info("No hay registros aún")
        return

    st.dataframe(registros)

    index = st.number_input("Número de fila", min_value=0, max_value=len(registros)-1, step=1)
    pago = st.number_input("Pago trabajador", min_value=0)

    if st.button("Guardar Pago", use_container_width=True):
        registros.loc[index, "pago_trabajador"] = pago
        registros.to_csv("registros.csv", index=False)
        st.success("Pago actualizado")

    if st.button("⬅ Volver", use_container_width=True):
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
