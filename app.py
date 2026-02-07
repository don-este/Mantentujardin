import streamlit as st
import pandas as pd
from datetime import date
import os

# -----------------------------
# CONFIGURACIÓN DEL ARCHIVO
# -----------------------------
ARCHIVO = "registros_mantencion.xlsx"

# Si el archivo no existe, crearlo con columnas base
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

# Función para cargar datos
def cargar_datos():
    return pd.read_excel(ARCHIVO, engine="openpyxl")

# Función para guardar datos
def guardar_datos(df):
    df.to_excel(ARCHIVO, index=False, engine="openpyxl")

# -----------------------------
# APP STREAMLIT
# -----------------------------
st.title("🌿 Registro de Mantenciones - Jardines y Piscinas")

menu = st.sidebar.selectbox(
    "Selecciona una opción:",
    ["Nueva Mantención", "Historial", "Resumen Mensual"]
)

df = cargar_datos()

# -----------------------------
# PESTAÑA 1: NUEVA MANTENCIÓN
# -----------------------------
if menu == "Nueva Mantención":
    st.header("📌 Nueva Mantención")

    with st.form("form_mantencion"):
        fecha = st.date_input("Fecha", date.today())

        cliente = st.selectbox(
            "Cliente",
            options=[
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

        tipo_servicio = st.selectbox(
            "Tipo de servicio",
            ["Jardín", "Piscina", "Ambos", "Trabajo especial"]
        )

        trabajador = st.selectbox(
            "Trabajador",
            ["Diego", "Solo", "Otro"]
        )

        monto = st.number_input("Monto cliente ($)", min_value=0, step=1000)

        observaciones = st.text_area("Observaciones")

        enviado = st.form_submit_button("Guardar registro")

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

            st.success("✅ Mantención registrada correctamente!")

# -----------------------------
# PESTAÑA 2: HISTORIAL
# -----------------------------
elif menu == "Historial":
    st.header("📋 Historial de Mantenciones")

    # Filtros
    cliente_filtro = st.selectbox(
        "Filtrar por cliente",
        ["Todos"] + list(df["cliente"].unique())
    )

    if cliente_filtro != "Todos":
        df = df[df["cliente"] == cliente_filtro]

    st.dataframe(df)

# -----------------------------
# PESTAÑA 3: RESUMEN MENSUAL
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

        st.subheader("Trabajos por cliente")
        st.dataframe(
            df_mes.groupby("cliente")["monto_cliente"].sum().reset_index()
        )

