import streamlit as st
import pandas as pd
import os
from datetime import date

# =========================
# ARCHIVOS DE DATOS
# =========================

ARCH_TRABAJADORES = "trabajadores.xlsx"
ARCH_CLIENTES = "clientes.xlsx"
ARCH_SERVICIOS = "servicios.xlsx"
ARCH_REGISTROS = "registros_diarios.xlsx"

# Crear archivos si no existen
if not os.path.exists(ARCH_TRABAJADORES):
    pd.DataFrame(columns=["usuario", "password", "nombre"]).to_excel(
        ARCH_TRABAJADORES, index=False, engine="openpyxl"
    )

if not os.path.exists(ARCH_CLIENTES):
    pd.DataFrame(columns=["nombre", "direccion", "telefono"]).to_excel(
        ARCH_CLIENTES, index=False, engine="openpyxl"
    )

if not os.path.exists(ARCH_SERVICIOS):
    pd.DataFrame(columns=["servicio", "descripcion"]).to_excel(
        ARCH_SERVICIOS, index=False, engine="openpyxl"
    )

if not os.path.exists(ARCH_REGISTROS):
    pd.DataFrame(columns=[
        "fecha",
        "trabajador",
        "cliente",
        "servicio",
        "observaciones",
        "monto_pago"
    ]).to_excel(ARCH_REGISTROS, index=False, engine="openpyxl")

# =========================
# FUNCIONES AUXILIARES
# =========================

def cargar_excel(ruta):
    return pd.read_excel(ruta, engine="openpyxl")

def guardar_excel(df, ruta):
    df.to_excel(ruta, index=False, engine="openpyxl")

# =========================
# LOGIN
# =========================

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
    st.session_state["rol"] = None
    st.session_state["usuario"] = None

st.title("🔐 Acceso - Mantenciones Jardín & Piscina")

if not st.session_state["autenticado"]:

    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):

        # 1) Ver si es ADMIN
        if usuario == "admin" and password == "admin123":
            st.session_state["autenticado"] = True
            st.session_state["rol"] = "admin"
            st.session_state["usuario"] = "admin"
            st.rerun()

        else:
            # 2) Ver si es TRABAJADOR
            trabajadores = cargar_excel(ARCH_TRABAJADORES)

            fila = trabajadores[
                (trabajadores["usuario"] == usuario) &
                (trabajadores["password"] == password)
            ]

            if not fila.empty:
                st.session_state["autenticado"] = True
                st.session_state["rol"] = "trabajador"
                st.session_state["usuario"] = usuario
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

    st.stop()

# =========================
# MENÚ PRINCIPAL
# =========================

st.sidebar.title(f"👤 Sesión: {st.session_state['usuario']}")

if st.session_state["rol"] == "admin":
    opcion = st.sidebar.radio(
        "Menú",
        ["Registro Diario", "Clientes", "Servicios", "Trabajadores"]
    )
else:
    opcion = st.sidebar.radio(
        "Menú",
        ["Registro Diario"]
    )

# =========================
# 1) REGISTRO DIARIO
# =========================

if opcion == "Registro Diario":

    st.header("📅 Registro Diario de Mantenciones")

    registros = cargar_excel(ARCH_REGISTROS)

    if st.session_state["rol"] == "trabajador":

        st.subheader("➡️ Ingresar tu trabajo del día")

        clientes = cargar_excel(ARCH_CLIENTES)["nombre"].tolist()
        servicios = cargar_excel(ARCH_SERVICIOS)["servicio"].tolist()

        fecha = st.date_input("Fecha", date.today())
        cliente = st.selectbox("Cliente", clientes)
        servicio = st.selectbox("Servicio", servicios)
        obs = st.text_area("Observaciones (opcional)")

        if st.button("Guardar Registro"):
            nuevo = pd.DataFrame([{
                "fecha": fecha,
                "trabajador": st.session_state["usuario"],
                "cliente": cliente,
                "servicio": servicio,
                "observaciones": obs,
                "monto_pago": ""
            }])

            registros = pd.concat([registros, nuevo], ignore_index=True)
            guardar_excel(registros, ARCH_REGISTROS)

            st.success("Registro guardado correctamente ✅")

    else:  # ADMIN

        st.subheader("📝 Registros enviados por los trabajadores")

        if registros.empty:
            st.info("Aún no hay registros.")
        else:
            st.dataframe(registros)

            st.markdown("---")
            st.subheader("💰 Asignar monto de pago al trabajador")

            seleccion = st.selectbox(
                "Selecciona un registro",
                registros.index
            )

            monto = st.number_input(
                "Monto a pagar ($)",
                min_value=0,
                step=1000
            )

            if st.button("Guardar Monto"):
                registros.loc[seleccion, "monto_pago"] = monto
                guardar_excel(registros, ARCH_REGISTROS)
                st.success("Monto guardado correctamente ✅")
                st.rerun()

# =========================
# 2) CLIENTES (SOLO ADMIN)
# =========================

if opcion == "Clientes" and st.session_state["rol"] == "admin":

    st.header("👥 Gestión de Clientes")

    clientes = cargar_excel(ARCH_CLIENTES)

    tab1, tab2, tab3 = st.tabs(["Agregar", "Modificar", "Eliminar"])

    with tab1:
        nombre = st.text_input("Nombre cliente")
        direccion = st.text_input("Dirección")
        telefono = st.text_input("Teléfono")

        if st.button("Agregar cliente"):
            nuevo = pd.DataFrame([{
                "nombre": nombre,
                "direccion": direccion,
                "telefono": telefono
            }])

            clientes = pd.concat([clientes, nuevo], ignore_index=True)
            guardar_excel(clientes, ARCH_CLIENTES)
            st.success("Cliente agregado ✅")
            st.rerun()

    with tab2:
        cliente_sel = st.selectbox("Selecciona cliente", clientes["nombre"])

        nueva_dir = st.text_input("Nueva dirección")
        nuevo_tel = st.text_input("Nuevo teléfono")

        if st.button("Modificar cliente"):
            clientes.loc[clientes["nombre"] == cliente_sel, "direccion"] = nueva_dir
            clientes.loc[clientes["nombre"] == cliente_sel, "telefono"] = nuevo_tel
            guardar_excel(clientes, ARCH_CLIENTES)
            st.success("Cliente modificado ✅")
            st.rerun()

    with tab3:
        cliente_del = st.selectbox("Cliente a eliminar", clientes["nombre"])

        if st.button("Eliminar cliente"):
            clientes = clientes[clientes["nombre"] != cliente_del]
            guardar_excel(clientes, ARCH_CLIENTES)
            st.success("Cliente eliminado ❌")
            st.rerun()

# =========================
# 3) SERVICIOS (SOLO ADMIN)
# =========================

if opcion == "Servicios" and st.session_state["rol"] == "admin":

    st.header("🛠 Gestión de Servicios")

    servicios = cargar_excel(ARCH_SERVICIOS)

    tab1, tab2, tab3 = st.tabs(["Agregar", "Modificar", "Eliminar"])

    with tab1:
        servicio = st.text_input("Nombre del servicio")
        descripcion = st.text_area("Descripción")

        if st.button("Agregar servicio"):
            nuevo = pd.DataFrame([{
                "servicio": servicio,
                "descripcion": descripcion
            }])

            servicios = pd.concat([servicios, nuevo], ignore_index=True)
            guardar_excel(servicios, ARCH_SERVICIOS)
            st.success("Servicio agregado ✅")
            st.rerun()

    with tab2:
        serv_sel = st.selectbox("Selecciona servicio", servicios["servicio"])
        nueva_desc = st.text_area("Nueva descripción")

        if st.button("Modificar servicio"):
            servicios.loc[servicios["servicio"] == serv_sel, "descripcion"] = nueva_desc
            guardar_excel(servicios, ARCH_SERVICIOS)
            st.success("Servicio modificado ✅")
            st.rerun()

    with tab3:
        serv_del = st.selectbox("Servicio a eliminar", servicios["servicio"])

        if st.button("Eliminar servicio"):
            servicios = servicios[servicios["servicio"] != serv_del]
            guardar_excel(servicios, ARCH_SERVICIOS)
            st.success("Servicio eliminado ❌")
            st.rerun()

# =========================
# 4) TRABAJADORES (SOLO ADMIN)
# =========================

if opcion == "Trabajadores" and st.session_state["rol"] == "admin":

    st.header("👷 Gestión de Trabajadores")

    trabajadores = cargar_excel(ARCH_TRABAJADORES)

    tab1, tab2, tab3 = st.tabs(["Agregar", "Modificar", "Eliminar"])

    with tab1:
        nombre = st.text_input("Nombre trabajador")
        usuario = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")

        if st.button("Agregar trabajador"):
            nuevo = pd.DataFrame([{
                "usuario": usuario,
                "password": password,
                "nombre": nombre
            }])

            trabajadores = pd.concat([trabajadores, nuevo], ignore_index=True)
            guardar_excel(trabajadores, ARCH_TRABAJADORES)
            st.success("Trabajador agregado ✅")
            st.rerun()

    with tab2:
        trab_sel = st.selectbox("Selecciona trabajador", trabajadores["usuario"])
        nueva_pass = st.text_input("Nueva contraseña", type="password")

        if st.button("Modificar contraseña"):
            trabajadores.loc[trabajadores["usuario"] == trab_sel, "password"] = nueva_pass
            guardar_excel(trabajadores, ARCH_TRABAJADORES)
            st.success("Contraseña actualizada ✅")
            st.rerun()

    with tab3:
        trab_del = st.selectbox("Trabajador a eliminar", trabajadores["usuario"])

        if st.button("Eliminar trabajador"):
            trabajadores = trabajadores[trabajadores["usuario"] != trab_del]
            guardar_excel(trabajadores, ARCH_TRABAJADORES)
            st.success("Trabajador eliminado ❌")
            st.rerun()
