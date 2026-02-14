import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="MantenTuJardín", layout="centered")

# ---------- CREAR ARCHIVOS SI NO EXISTEN ----------

def inicializar_archivos():
    if not os.path.exists("clientes.csv"):
        df = pd.DataFrame(columns=["nombre", "direccion", "telefono",
                                   "tipo_contrato", "valor", "servicio"])
        df.to_csv("clientes.csv", index=False)

    if not os.path.exists("trabajadores.csv"):
        df = pd.DataFrame(columns=["usuario", "password", "nombre", "rol"])
        df.loc[0] = ["admin", "1234", "Administrador", "admin"]
        df.to_csv("trabajadores.csv", index=False)

    if not os.path.exists("registros.csv"):
        df = pd.DataFrame(columns=["fecha", "cliente", "servicio",
                                   "trabajador", "valor", "pagado"])
        df.to_csv("registros.csv", index=False)

inicializar_archivos()

# ---------- FUNCION CARGAR CSV SEGURA ----------

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

        trabajadores["usuario"] = trabajadores["usuario"].astype(str).str.strip()
        trabajadores["password"] = trabajadores["password"].astype(str).str.strip()
        trabajadores["rol"] = trabajadores["rol"].astype(str).str.strip()

        user = trabajadores[
            (trabajadores["usuario"] == usuario.strip()) &
            (trabajadores["password"] == password.strip())
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
            st.session_state["menu"] = "clientes"

        if st.button("👷 Trabajadores", use_container_width=True):
            st.session_state["menu"] = "trabajadores"

        if st.button("💰 Revisar Registros", use_container_width=True):
            st.session_state["menu"] = "revisar"

    if st.button("🚪 Cerrar sesión", use_container_width=True):
        st.session_state.clear()
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

    servicio = cliente_info.get("servicio", "")
    valor = cliente_info.get("valor", 0)

    trabajador = st.selectbox(
        "Trabajador",
        trabajadores[trabajadores["rol"] == "trabajador"]["nombre"]
    )

    fecha = st.date_input("Fecha", datetime.today())

    if st.button("Guardar Registro", use_container_width=True):

        nuevo = pd.DataFrame([{
            "fecha": fecha,
            "cliente": cliente,
            "servicio": servicio,
            "trabajador": trabajador,
            "valor": valor,
            "pagado": "No"
        }])

        registros = cargar_csv("registros.csv",
                               ["fecha", "cliente", "servicio",
                                "trabajador", "valor", "pagado"])

        registros = pd.concat([registros, nuevo], ignore_index=True)
        registros.to_csv("registros.csv", index=False)

        st.success("Registro guardado correctamente")

    if st.button("⬅ Volver", use_container_width=True):
        st.session_state["menu"] = "principal"
        st.rerun()

# ---------- CLIENTES ----------

def clientes_menu():

    st.markdown("## 👥 Gestión de Clientes")

    clientes = cargar_csv("clientes.csv",
                          ["nombre", "direccion", "telefono",
                           "tipo_contrato", "valor", "servicio"])

    opcion = st.selectbox("Seleccione opción",
                          ["Nuevo Cliente", "Modificar Cliente", "Eliminar Cliente"])

    # -------- NUEVO --------
    if opcion == "Nuevo Cliente":

        nombre = st.text_input("Nombre")
        direccion = st.text_input("Dirección")
        telefono = st.text_input("Teléfono")
        servicio = st.text_input("Servicio que realiza")
        tipo = st.selectbox("Tipo de contrato", ["Mensual", "Por Visita"])
        valor = st.number_input("Valor", min_value=0)

        if st.button("Guardar Cliente", use_container_width=True):

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

                st.success("Cliente guardado correctamente")

    # -------- MODIFICAR --------
    if opcion == "Modificar Cliente":

        if not clientes.empty:

            cliente_sel = st.selectbox("Seleccione cliente", clientes["nombre"])
            datos = clientes[clientes["nombre"] == cliente_sel].iloc[0]

            direccion = st.text_input("Dirección", value=datos["direccion"])
            telefono = st.text_input("Teléfono", value=datos["telefono"])
            servicio = st.text_input("Servicio", value=datos["servicio"])
            tipo = st.selectbox("Tipo de contrato",
                                ["Mensual", "Por Visita"],
                                index=0 if datos["tipo_contrato"] == "Mensual" else 1)
            valor = st.number_input("Valor", value=float(datos["valor"]))

            if st.button("Actualizar Cliente", use_container_width=True):

                clientes.loc[clientes["nombre"] == cliente_sel,
                             ["direccion", "telefono", "servicio",
                              "tipo_contrato", "valor"]] = [
                                 direccion, telefono, servicio, tipo, valor
                             ]

                clientes.to_csv("clientes.csv", index=False)
                st.success("Cliente actualizado correctamente")

    # -------- ELIMINAR --------
    if opcion == "Eliminar Cliente":

        if not clientes.empty:

            eliminar = st.selectbox("Seleccione cliente a eliminar",
                                    clientes["nombre"])

            if st.button("Eliminar", use_container_width=True):
                clientes = clientes[clientes["nombre"] != eliminar]
                clientes.to_csv("clientes.csv", index=False)
                st.success("Cliente eliminado")

    if st.button("⬅ Volver", use_container_width=True):
        st.session_state["menu"] = "principal"
        st.rerun()

# ---------- TRABAJADORES ----------

def trabajadores_menu():

    st.markdown("## 👷 Gestión de Trabajadores")

    trabajadores = cargar_csv("trabajadores.csv",
                               ["usuario", "password", "nombre", "rol"])

    opcion = st.selectbox("Seleccione opción",
                          ["Agregar Trabajador", "Eliminar Trabajador"])

    if opcion == "Agregar Trabajador":

        nombre = st.text_input("Nombre")
        usuario = st.text_input("Usuario")
        password = st.text_input("Contraseña")

        if st.button("Guardar Trabajador", use_container_width=True):

            nuevo = pd.DataFrame([{
                "usuario": usuario,
                "password": password,
                "nombre": nombre,
                "rol": "trabajador"
            }])

            trabajadores = pd.concat([trabajadores, nuevo], ignore_index=True)
            trabajadores.to_csv("trabajadores.csv", index=False)

            st.success("Trabajador creado")

    if opcion == "Eliminar Trabajador":

        lista = trabajadores[trabajadores["rol"] == "trabajador"]

        if not lista.empty:
            eliminar = st.selectbox("Seleccione trabajador",
                                    lista["nombre"])

            if st.button("Eliminar", use_container_width=True):
                trabajadores = trabajadores[trabajadores["nombre"] != eliminar]
                trabajadores.to_csv("trabajadores.csv", index=False)
                st.success("Trabajador eliminado")

    if st.button("⬅ Volver", use_container_width=True):
        st.session_state["menu"] = "principal"
        st.rerun()

# ---------- REVISAR REGISTROS ----------

def revisar_registros():

    st.markdown("## 💰 Revisar Registros")

    registros = cargar_csv("registros.csv",
                           ["fecha", "cliente", "servicio",
                            "trabajador", "valor", "pagado"])

    if registros.empty:
        st.info("No hay registros aún.")
    else:
        st.dataframe(registros)

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
    elif menu == "registro":
        registro_diario()
    elif menu == "clientes":
        clientes_menu()
    elif menu == "trabajadores":
        trabajadores_menu()
    elif menu == "revisar":
        revisar_registros()
