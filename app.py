import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="MantenTuJardín", layout="centered")

# ---------------------------------------------------
# INICIALIZAR ARCHIVOS
# ---------------------------------------------------

def inicializar_archivos():

    if not os.path.exists("clientes.csv"):
        pd.DataFrame(columns=[
            "nombre", "direccion", "telefono",
            "tipo_contrato", "valor", "servicio"
        ]).to_csv("clientes.csv", index=False)

    if not os.path.exists("servicios.csv"):
        pd.DataFrame(columns=[
            "nombre", "descripcion"
        ]).to_csv("servicios.csv", index=False)

    if not os.path.exists("trabajadores.csv"):
        df = pd.DataFrame(columns=[
            "usuario", "password", "nombre", "rol"
        ])
        df.loc[0] = ["admin", "1234", "Administrador", "admin"]
        df.to_csv("trabajadores.csv", index=False)

    if not os.path.exists("registros.csv"):
        pd.DataFrame(columns=[
            "fecha", "cliente", "servicio",
            "trabajador", "valor", "pagado"
        ]).to_csv("registros.csv", index=False)

inicializar_archivos()

# ---------------------------------------------------
# FUNCION CARGAR CSV SEGURA
# ---------------------------------------------------

def cargar_csv(nombre, columnas):
    df = pd.read_csv(nombre)
    for col in columnas:
        if col not in df.columns:
            df[col] = ""
    return df

# ---------------------------------------------------
# LOGIN
# ---------------------------------------------------

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
            st.session_state.usuario = usuario
            st.session_state.rol = user.iloc[0]["rol"]
            st.session_state.menu = "principal"
            st.rerun()
        else:
            st.error("Credenciales inválidas")

# ---------------------------------------------------
# MENU PRINCIPAL
# ---------------------------------------------------

def menu_principal():

    st.markdown("## 📋 Menú Principal")

    if st.button("📝 Registro Diario", use_container_width=True):
        st.session_state.menu = "registro"

    if st.session_state.rol == "admin":

        if st.button("👥 Clientes", use_container_width=True):
            st.session_state.menu = "clientes_menu"

        if st.button("🛠 Servicios", use_container_width=True):
            st.session_state.menu = "servicios_menu"

        if st.button("👷 Trabajadores", use_container_width=True):
            st.session_state.menu = "trabajadores_menu"

        if st.button("💰 Revisar Registros", use_container_width=True):
            st.session_state.menu = "revisar"

    if st.button("🚪 Cerrar sesión", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ---------------------------------------------------
# SUBMENU CLIENTES
# ---------------------------------------------------

def clientes_menu():

    st.markdown("## 👥 Gestión de Clientes")

    if st.button("➕ Nuevo Cliente", use_container_width=True):
        st.session_state.menu = "cliente_nuevo"

    if st.button("✏ Modificar Cliente", use_container_width=True):
        st.session_state.menu = "cliente_modificar"

    if st.button("🗑 Eliminar Cliente", use_container_width=True):
        st.session_state.menu = "cliente_eliminar"

    if st.button("⬅ Volver", use_container_width=True):
        st.session_state.menu = "principal"
        st.rerun()

# ---------------------------------------------------
# NUEVO CLIENTE
# ---------------------------------------------------

def cliente_nuevo():

    st.markdown("## ➕ Nuevo Cliente")

    clientes = cargar_csv("clientes.csv",
                          ["nombre", "direccion", "telefono",
                           "tipo_contrato", "valor", "servicio"])

    nombre = st.text_input("Nombre")
    direccion = st.text_input("Dirección")
    telefono = st.text_input("Teléfono")
    servicio = st.text_input("Servicio")
    tipo = st.selectbox("Tipo de contrato", ["Mensual", "Por Visita"])
    valor = st.number_input("Valor", min_value=0)

    if st.button("Guardar", use_container_width=True):

        if nombre.strip() == "" or servicio.strip() == "" or valor == 0:
            st.error("Complete los campos obligatorios")
        else:
            nuevo = pd.DataFrame([{
                "nombre": nombre,
                "direccion": direccion,
                "telefono": telefono,
                "tipo_contrato": tipo,
                "valor": valor,
                "servicio": servicio
            }])

            clientes = pd.concat([clientes, nuevo], ignore_index=True)
            clientes.to_csv("clientes.csv", index=False)
            st.success("Cliente guardado")

    if st.button("⬅ Volver", use_container_width=True):
        st.session_state.menu = "clientes_menu"
        st.rerun()

# ---------------------------------------------------
# REGISTRO DIARIO
# ---------------------------------------------------

def registro_diario():

    st.title("📅 Registro Diario")

    opcion = st.radio(
        "Seleccione una opción",
        ["➕ Nuevo registro", "✏ Modificar registro", "🗑 Eliminar registro"]
    )

    clientes = cargar_clientes()
    trabajadores = cargar_trabajadores()
    registros = cargar_registros()

    # ==============================
    # NUEVO REGISTRO
    # ==============================
    if opcion == "➕ Nuevo registro":

        if clientes.empty:
            st.warning("No hay clientes registrados.")
            return

        cliente_nombre = st.selectbox(
            "Seleccione Cliente",
            clientes["nombre"].unique()
        )

        cliente_info = clientes[clientes["nombre"] == cliente_nombre].iloc[0]

        servicio = cliente_info.get("servicio", "No definido")
        tipo_contrato = cliente_info.get("tipo_contrato", "No definido")
        valor = cliente_info.get("valor", 0)

        st.write(f"**Servicio:** {servicio}")
        st.write(f"**Tipo de contrato:** {tipo_contrato}")
        st.write(f"**Valor:** ${valor}")

        trabajador = st.selectbox(
            "Seleccione Trabajador",
            trabajadores["nombre"].unique()
        )

        fecha = st.date_input("Fecha")
        estado = st.selectbox("Estado", ["Realizado", "Pendiente"])
        observaciones = st.text_area("Observaciones")

        if st.button("Guardar Registro"):

            nuevo = pd.DataFrame([{
                "fecha": fecha,
                "cliente": cliente_nombre,
                "servicio": servicio,
                "trabajador": trabajador,
                "tipo_contrato": tipo_contrato,
                "valor": valor,
                "estado": estado,
                "observaciones": observaciones
            }])

            registros = pd.concat([registros, nuevo], ignore_index=True)
            registros.to_csv("registros.csv", index=False)

            st.success("Registro guardado correctamente")

    # ==============================
    # MODIFICAR REGISTRO
    # ==============================
    elif opcion == "✏ Modificar registro":

        if registros.empty:
            st.warning("No hay registros disponibles.")
            return

        registro_id = st.selectbox(
            "Seleccione registro",
            registros.index
        )

        registro = registros.loc[registro_id]

        nuevo_estado = st.selectbox(
            "Estado",
            ["Realizado", "Pendiente"],
            index=0 if registro["estado"] == "Realizado" else 1
        )

        nuevas_obs = st.text_area(
            "Observaciones",
            value=registro["observaciones"]
        )

        if st.button("Actualizar Registro"):

            registros.at[registro_id, "estado"] = nuevo_estado
            registros.at[registro_id, "observaciones"] = nuevas_obs

            registros.to_csv("registros.csv", index=False)
            st.success("Registro actualizado")

    # ==============================
    # ELIMINAR REGISTRO
    # ==============================
    elif opcion == "🗑 Eliminar registro":

        if registros.empty:
            st.warning("No hay registros para eliminar.")
            return

        registro_id = st.selectbox(
            "Seleccione registro a eliminar",
            registros.index
        )

        if st.button("Eliminar"):

            registros = registros.drop(registro_id)
            registros.to_csv("registros.csv", index=False)

            st.success("Registro eliminado")


# ---------------------------------------------------
# REVISAR REGISTROS
# ---------------------------------------------------

def revisar():

    st.markdown("## 💰 Revisar Registros")

    registros = cargar_csv("registros.csv",
                           ["fecha", "cliente", "servicio",
                            "trabajador", "valor", "pagado"])

    if registros.empty:
        st.info("No hay registros.")
    else:
        st.dataframe(registros)

    if st.button("⬅ Volver", use_container_width=True):
        st.session_state.menu = "principal"
        st.rerun()

# ---------------------------------------------------
# CONTROL PRINCIPAL
# ---------------------------------------------------

if "usuario" not in st.session_state:
    login()
else:

    if "menu" not in st.session_state:
        st.session_state.menu = "principal"

    if st.session_state.menu == "principal":
        menu_principal()

    elif st.session_state.menu == "clientes_menu":
        clientes_menu()

    elif st.session_state.menu == "cliente_nuevo":
        cliente_nuevo()

    elif st.session_state.menu == "registro":
        registro_diario()

    elif st.session_state.menu == "revisar":
        revisar()

