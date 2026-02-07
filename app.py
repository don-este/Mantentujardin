import streamlit as st
import pandas as pd
from datetime import date
import os

# ======================================================
# ARCHIVOS DE DATOS
# ======================================================

ARCHIVO_CLIENTES = "clientes.xlsx"
ARCHIVO_REGISTROS = "registros_diarios.xlsx"
ARCHIVO_SERVICIOS = "servicios.xlsx"

# Crear archivos si no existen
if not os.path.exists(ARCHIVO_CLIENTES):
    pd.DataFrame(columns=["nombre", "direccion", "telefono"]).to_excel(
        ARCHIVO_CLIENTES, index=False, engine="openpyxl"
    )

if not os.path.exists(ARCHIVO_REGISTROS):
    pd.DataFrame(columns=[
        "fecha",
        "cliente",
        "servicio",
        "trabajador",
        "valor_visita"
    ]).to_excel(ARCHIVO_REGISTROS, index=False, engine="openpyxl")

if not os.path.exists(ARCHIVO_SERVICIOS):
    pd.DataFrame(columns=["nombre_servicio", "descripcion"]).to_excel(
        ARCHIVO_SERVICIOS, index=False, engine="openpyxl"
    )

def cargar_clientes():
    return pd.read_excel(ARCHIVO_CLIENTES, engine="openpyxl")

def guardar_clientes(df):
    df.to_excel(ARCHIVO_CLIENTES, index=False, engine="openpyxl")

def cargar_registros():
    return pd.read_excel(ARCHIVO_REGISTROS, engine="openpyxl")

def guardar_registros(df):
    df.to_excel(ARCHIVO_REGISTROS, index=False, engine="openpyxl")

def cargar_servicios():
    return pd.read_excel(ARCHIVO_SERVICIOS, engine="openpyxl")

def guardar_servicios(df):
    df.to_excel(ARCHIVO_SERVICIOS, index=False, engine="openpyxl")

# ======================================================
# LOGIN (SE MANTIENE)
# ======================================================

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

st.title("🔐 Acceso al Sistema")

if not st.session_state["autenticado"]:
    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if usuario == "admin" and password == "1234":
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

    st.stop()

# ======================================================
# MENÚ PRINCIPAL CON BOTONES (ACTUALIZADO)
# ======================================================

st.title("🌿 Sistema de Mantenciones")

if "pantalla" not in st.session_state:
    st.session_state["pantalla"] = "menu"

if st.session_state["pantalla"] == "menu":

    st.subheader("Selecciona una opción")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📅 Registro Diario", use_container_width=True):
            st.session_state["pantalla"] = "registro"
            st.rerun()

    with col2:
        if st.button("👥 Clientes", use_container_width=True):
            st.session_state["pantalla"] = "clientes"
            st.rerun()

    with col3:
        if st.button("🛠️ Servicios", use_container_width=True):
            st.session_state["pantalla"] = "servicios"
            st.rerun()

    st.stop()

# Cargar datos (solo después del menú)
clientes_df = cargar_clientes()
registros_df = cargar_registros()
servicios_df = cargar_servicios()

# ======================================================
# 1️⃣ REGISTRO DIARIO (AHORA USA TUS SERVICIOS)
# ======================================================
if st.session_state["pantalla"] == "registro":

    if st.button("⬅️ Volver al menú"):
        st.session_state["pantalla"] = "menu"
        st.rerun()

    st.header("📅 Registro Diario")

    with st.form("form_registro"):

        fecha = st.date_input("Fecha", date.today())

        lista_clientes = list(clientes_df["nombre"]) if not clientes_df.empty else ["(Sin clientes)"]

        cliente = st.selectbox("Cliente", lista_clientes)

        # NUEVO: servicios dinámicos
        lista_servicios = list(servicios_df["nombre_servicio"]) if not servicios_df.empty else ["(Sin servicios)"]

        servicio = st.selectbox("Servicio", lista_servicios)

        trabajador = st.selectbox(
            "Trabajador",
            ["Diego", "Solo", "Otro"]
        )

        valor = st.number_input("Valor de la visita ($)", min_value=0, step=1000)

        enviado = st.form_submit_button("💾 Guardar Registro")

        if enviado:
            nuevo = pd.DataFrame([{
                "fecha": fecha,
                "cliente": cliente,
                "servicio": servicio,
                "trabajador": trabajador,
                "valor_visita": valor
            }])

            registros_actualizados = pd.concat([registros_df, nuevo], ignore_index=True)
            guardar_registros(registros_actualizados)

            st.success("✅ Registro diario guardado correctamente")
            st.rerun()

    st.subheader("Últimos registros")
    st.dataframe(registros_df.tail(10))

# ======================================================
# 2️⃣ CLIENTES (SIN CAMBIOS)
# ======================================================
elif st.session_state["pantalla"] == "clientes":

    if st.button("⬅️ Volver al menú"):
        st.session_state["pantalla"] = "menu"
        st.rerun()

    st.header("👥 Gestión de Clientes")

    opcion = st.radio(
        "¿Qué quieres hacer?",
        ["➕ Nuevo cliente", "✏️ Modificar cliente", "🗑️ Eliminar cliente"]
    )

    if opcion == "➕ Nuevo cliente":
        with st.form("form_cliente"):
            nombre = st.text_input("Nombre del cliente")
            direccion = st.text_input("Dirección")
            telefono = st.text_input("Teléfono")

            guardar = st.form_submit_button("Guardar cliente")

            if guardar:
                nuevo_cliente = pd.DataFrame([{
                    "nombre": nombre,
                    "direccion": direccion,
                    "telefono": telefono
                }])

                clientes_actualizados = pd.concat([clientes_df, nuevo_cliente], ignore_index=True)
                guardar_clientes(clientes_actualizados)
                st.success("Cliente agregado correctamente")
                st.rerun()

    elif opcion == "✏️ Modificar cliente":
        if clientes_df.empty:
            st.warning("No hay clientes registrados")
        else:
            cliente_seleccionado = st.selectbox(
                "Selecciona cliente",
                clientes_df["nombre"]
            )

            fila = clientes_df[clientes_df["nombre"] == cliente_seleccionado].iloc[0]

            with st.form("form_modificar"):
                nuevo_nombre = st.text_input("Nombre", fila["nombre"])
                nueva_direccion = st.text_input("Dirección", fila["direccion"])
                nuevo_telefono = st.text_input("Teléfono", str(fila["telefono"]))

                actualizar = st.form_submit_button("Actualizar cliente")

                if actualizar:
                    clientes_df.loc[
                        clientes_df["nombre"] == cliente_seleccionado,
                        ["nombre", "direccion", "telefono"]
                    ] = [nuevo_nombre, nueva_direccion, nuevo_telefono]

                    guardar_clientes(clientes_df)
                    st.success("Cliente actualizado")
                    st.rerun()

    elif opcion == "🗑️ Eliminar cliente":
        if clientes_df.empty:
            st.warning("No hay clientes registrados")
        else:
            cliente_borrar = st.selectbox(
                "Selecciona cliente a eliminar",
                clientes_df["nombre"]
            )

            if st.button("Eliminar definitivamente"):
                clientes_df = clientes_df[clientes_df["nombre"] != cliente_borrar]
                guardar_clientes(clientes_df)
                st.success("Cliente eliminado")
                st.rerun()

    st.subheader("Lista actual de clientes")
    st.dataframe(clientes_df)

# ======================================================
# 3️⃣ SERVICIOS (NUEVO MÓDULO)
# ======================================================
elif st.session_state["pantalla"] == "servicios":

    if st.button("⬅️ Volver al menú"):
        st.session_state["pantalla"] = "menu"
        st.rerun()

    st.header("🛠️ Gestión de Servicios")

    opcion = st.radio(
        "¿Qué quieres hacer?",
        ["➕ Nuevo servicio", "✏️ Modificar servicio", "🗑️ Eliminar servicio"]
    )

    # NUEVO SERVICIO
    if opcion == "➕ Nuevo servicio":

        with st.form("form_servicio"):
            nombre_servicio = st.text_input("Nombre del servicio")
            descripcion = st.text_area("Descripción del servicio")

            guardar = st.form_submit_button("Guardar servicio")

            if guardar:
                nuevo_servicio = pd.DataFrame([{
                    "nombre_servicio": nombre_servicio,
                    "descripcion": descripcion
                }])

                servicios_actualizados = pd.concat([servicios_df, nuevo_servicio], ignore_index=True)
                guardar_servicios(servicios_actualizados)

                st.success("Servicio agregado correctamente")
                st.rerun()

    # MODIFICAR SERVICIO
    elif opcion == "✏️ Modificar servicio":

        if servicios_df.empty:
            st.warning("No hay servicios registrados")
        else:
            servicio_sel = st.selectbox(
                "Selecciona servicio",
                servicios_df["nombre_servicio"]
            )

            fila = servicios_df[servicios_df["nombre_servicio"] == servicio_sel].iloc[0]

            with st.form("form_modificar_servicio"):
                nuevo_nombre = st.text_input("Nombre", fila["nombre_servicio"])
                nueva_descripcion = st.text_area("Descripción", fila["descripcion"])

                actualizar = st.form_submit_button("Actualizar servicio")

                if actualizar:
                    servicios_df.loc[
                        servicios_df["nombre_servicio"] == servicio_sel,
                        ["nombre_servicio", "descripcion"]
                    ] = [nuevo_nombre, nueva_descripcion]

                    guardar_servicios(servicios_df)
                    st.success("Servicio actualizado")
                    st.rerun()

    # ELIMINAR SERVICIO
    elif opcion == "🗑️ Eliminar servicio":

        if servicios_df.empty:
            st.warning("No hay servicios registrados")
        else:
            servicio_borrar = st.selectbox(
                "Selecciona servicio a eliminar",
                servicios_df["nombre_servicio"]
            )

            if st.button("Eliminar definitivamente"):
                servicios_df = servicios_df[servicios_df["nombre_servicio"] != servicio_borrar]
                guardar_servicios(servicios_df)
                st.success("Servicio eliminado")
                st.rerun()

    st.subheader("Lista actual de servicios")
    st.dataframe(servicios_df)
