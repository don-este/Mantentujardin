import streamlit as st
import pandas as pd
from datetime import date
import os

# =========================
# CONFIGURACIÓN INICIAL
# =========================

ARCHIVO = "registros_mantencion.xlsx"

if not os.path.exists(ARCHIVO):
    df_init = pd.DataFrame(columns=[
        "fecha",
        "cliente",
        "tipo_servicio",
        "trabajador",
        "monto_cliente",
        "observaciones"
    ])
    df_init.to_excel(ARCHIVO, index=False, engine="openpyxl")

def cargar_datos():
    return pd.read_excel(ARCHIVO, engine="openpyxl")

def guardar_datos(df):
    df.to_excel(ARCHIVO, index=False, engine="openpyxl")

# =========================
# SISTEMA DE LOGIN SIMPLE
# =========================

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

st.title("🔐 Acceso al Registro de Mantenciones")

if not st.session_state["autenticado"]:
    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if usuario == "admin" and password == "1234":
            st.session_state["autenticado"] = True
            st.experimental_rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

    st.stop()  # Detiene la app hasta que inicies sesión

# =========================
# APP PRINCIPAL
# =========================

st.title("🌿 Mantenciones - Jardín & Piscina")

menu = st.sidebar.selectbox(
    "Menú",
    ["Nueva Mantención", "Historial", "Resumen Mensual"]
)

df = cargar_datos()

# -----------------------------
# NUEVA MANTENCIÓN (MÓVIL FRIENDLY)
# -----------------------------
if menu == "Nueva Mantención":

    st.header("📌 Nueva Mantención")

    with st.form("form_mantencion"):

        # Columnas para que se vea mejor en celular
        col1, col2 = st.columns(2)

        with col1:
            fecha = st.date_input("Fecha", date.today())
            cliente = st.selectbox(
                "Cliente",
                [
                    "Francisca Las Rastras",
                    "Condominio",
                    "Yasna P San Valentín",
                    "Felipe",
                    "José Manuel",
                    "Jorge el llano",
                    "Alex el Galpón",
                    "Sebastián"
                ]
            )

        with col2:
            tipo_servicio = st.selectbox(
                "Tipo de servicio",
                ["Jardín", "Piscina", "Ambos", "Especial"]
            )

            trabajador = st.selectbox(
                "Trabajador",
                ["Diego", "Solo", "Otro"]
            )

        monto = st.number_input("Monto cliente ($)", min_value=0, step=1000)

        observaciones = st.text_area("Observaciones")

        enviado = st.form_submit_button("💾 Guardar Mantención")

        if enviado:
            nuevo_registro = pd.DataFrame([{
                "fecha": fecha,
                "cliente": cliente,
                "tipo_servicio": tipo_servicio,
                "trabajador": trabajador,
                "monto_cliente": monto,
                "observaciones": observaciones
            }])

            df_actualizado = pd.concat([df, nuevo_registro], ignore_index=True)
            guardar_datos(df_actualizado)

            st.success("✅ Registro guardado correctamente!")

# -----------------------------
# HISTORIAL
# -----------------------------
elif menu == "Historial":
    st.header("📋 Historial de Mantenciones")

    cliente_filtro = st.selectbox(
        "Filtrar por cliente",
        ["Todos"] + list(df["cliente"].unique())
    )

    if cliente_filtro != "Todos":
        df = df[df["cliente"] == cliente_filtro]

    st.dataframe(df)

# -----------------------------
# RESUMEN MENSUAL
# -----------------------------
elif menu == "Resumen Mensual":
    st.header("📊 Resumen Mensual")

    if not df.empty:
        df["mes"] = pd.to_datetime(df["fecha"]).dt.to_period("M")

        mes_seleccionado = st.selectbox(
            "Selecciona mes",
            df["mes"].astype(str).unique()
        )

        df_mes = df[df["mes"].astype(str) == mes_seleccionado]

        total_mes = df_mes["monto_cliente"].sum()

        st.metric("💰 Total facturado en el mes", f"${total_mes:,.0f}")

        st.subheader("Ingresos por cliente")
        st.dataframe(
            df_mes.groupby("cliente")["monto_cliente"].sum().reset_index()
        )
