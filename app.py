import streamlit as st
import pandas as pd
from datetime import date
import os

# ======================================================
# ARCHIVOS DE DATOS
# ======================================================

ARCHIVO_CLIENTES = "clientes.xlsx"
ARCHIVO_REGISTROS = "registros_diarios.xlsx"

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

def cargar_clientes():
    return pd.read_excel(ARCHIVO_CLIENTES, engine="openpyxl")

def guardar_clientes(df):
    df.to_excel(ARCHIVO_CLIENTES, index=False, engine="openpyxl")

def cargar_registros():
    return pd.read_excel(ARCHIVO_REGISTROS, engine="openpyxl")

def guardar_registros(df):
    df.to_excel(ARCHIVO_REGISTROS, index=False, engine="openpyxl")

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
# MENÚ PRINCIPAL CON BOTONES (NUEVO)
# ======================================================

st.title("🌿 Sistema de Mantenciones")

# Guardamos la opción de menú en session_state
if "pantalla" not in st.session_state:
    st.session_state["pantalla"] = "menu"

# --- BOTONES DEL MENÚ ---
if st.session_state["pantalla"] == "menu":

    st.subheader("Selecciona una opción")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📅 Registro Diario", use_container_width=True):
            st.session_state["pantalla"] = "registro"
            st.rerun()

    with col2:
        if st.button("👥 Clientes", use_container_width=True):
            st.session_state["pantalla"] = "clientes"
            st.rerun()

    st.stop()  # Detiene aquí hasta elegir opción

# Cargar datos (solo después del menú)
clientes_df = cargar_clientes()
registros_df = cargar_registros()

# ======================================================
# 1️⃣ REGISTRO DIARIO
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

        servicio = st.selectbox(
            "Servicio",
            ["Mantención Jardín", "Mantención Piscina", "Ambos", "Especial"]
        )

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
# 2️⃣ CLIENTES (CRUD)
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

    # -------------------------
    # NUEVO CLIENTE
    # -------------------------
    if opcion == "➕ Nuevo cliente":

        st.subheader("Agregar nuevo cliente")

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

    # -------------------------
    # MODIFICAR CLIENTE
    # -------------------------
    elif opcion == "✏️ Modificar cliente":

        st.subheader("Modificar cliente")

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

    # -------------------------
    # ELIMINAR CLIENTE
    # -------------------------
    elif opcion == "🗑️ Eliminar cliente":

        st.subheader("Eliminar cliente")

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
