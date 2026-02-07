import streamlit as st
import pandas as pd
import os
from datetime import date

# =========================
# ARCHIVOS
# =========================

ARCH_TRABAJADORES = "trabajadores.xlsx"
ARCH_CLIENTES = "clientes.xlsx"
ARCH_SERVICIOS = "servicios.xlsx"
ARCH_REGISTROS = "registros_diarios.xlsx"

# Crear archivos si no existen (estructura correcta)
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
        "cliente",
        "servicio",
        "trabajador",
        "valor_servicio",
        "observaciones",
        "quien_registro"
    ]).to_excel(ARCH_REGISTROS, index=False, engine="openpyxl")

# =========================
# FUNCIONES SEGURAS DE CARGA
# =========================

def cargar_excel_seguro(ruta, columnas_esperadas):
    df = pd.read_excel(ruta, engine="openpyxl")

    # Si faltan columnas, las crea vacías (EVITA ERRORES)
    for col in columnas_esperadas:
        if col not in df.columns:
            df[col] = ""

    return df[columnas_esperadas]

def guardar_excel(df, ruta):
    df.to_excel(ruta, index=False, engine="openpyxl")

# =========================
# LOGIN
# =========================

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
    st.session_state["rol"] = None
    st.session_state["usuario"] = None
    st.session_state["menu"] = "Registro Diario"

st.title("🔐 Acceso - Mantenciones Jardín & Piscina")

if not st.session_state["autenticado"]:

    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):

        # ADMIN
        if usuario == "admin" and password == "admin123":
            st.session_state["autenticado"] = True
            st.session_state["rol"] = "admin"
            st.session_state["usuario"] = "admin"
            st.rerun()

        else:
            # TRABAJADOR
            trabajadores = cargar_excel_seguro(
                ARCH_TRABAJADORES, ["usuario", "password", "nombre"]
            )

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
# MENÚ CON BOTONES
# =========================

st.sidebar.title(f"👤 Sesión: {st.session_state['usuario']}")

st.sidebar.markdown("## 📋 Menú")

if st.session_state["rol"] == "admin":
    if st.sidebar.button("🗓 Registro Diario"):
        st.session_state["menu"] = "Registro Diario"
    if st.sidebar.button("👥 Clientes"):
        st.session_state["menu"] = "Clientes"
    if st.sidebar.button("🛠 Servicios"):
        st.session_state["menu"] = "Servicios"
    if st.sidebar.button("👷 Trabajadores"):
        st.session_state["menu"] = "Trabajadores"
else:
    if st.sidebar.button("🗓 Registro Diario"):
        st.session_state["menu"] = "Registro Diario"

# =========================
# CARGA DE DATOS (SEGURA)
# =========================

clientes = cargar_excel_seguro(
    ARCH_CLIENTES, ["nombre", "direccion", "telefono"]
)

servicios = cargar_excel_seguro(
    ARCH_SERVICIOS, ["servicio", "descripcion"]
)

trabajadores = cargar_excel_seguro(
    ARCH_TRABAJADORES, ["usuario", "password", "nombre"]
)

registros = cargar_excel_seguro(
    ARCH_REGISTROS,
    ["fecha", "cliente", "servicio", "trabajador",
     "valor_servicio", "observaciones", "quien_registro"]
)

# =========================
# 1) REGISTRO DIARIO
# =========================

if st.session_state["menu"] == "Registro Diario":

    st.header("📅 Registro Diario de Mantenciones")

    if st.session_state["rol"] == "admin":

        st.subheader("➡️ Registrar servicio (cliente por cliente)")

        fecha = st.date_input("Fecha", date.today())

        cliente = st.selectbox(
            "Cliente",
            clientes["nombre"].dropna().tolist()
        )

        servicio = st.selectbox(
            "Servicio",
            servicios["servicio"].dropna().tolist()
        )

        trabajador = st.selectbox(
            "Trabajador",
            trabajadores["usuario"].dropna().tolist()
        )

        valor = st.number_input(
            "Valor del servicio ($)",
            min_value=0,
            step=1000
        )

        obs = st.text_area("Observaciones (opcional)")

        if st.button("Guardar registro"):
            nuevo = pd.DataFrame([{
                "fecha": fecha,
                "cliente": cliente,
                "servicio": servicio,
                "trabajador": trabajador,
                "valor_servicio": valor,
                "observaciones": obs,
                "quien_registro": "admin"
            }])

            registros = pd.concat([registros, nuevo], ignore_index=True)
            guardar_excel(registros, ARCH_REGISTROS)
            st.success("Registro guardado correctamente ✅")
            st.rerun()

        st.markdown("---")
        st.subheader("📋 Historial de registros")
        st.dataframe(
            registros.sort_values("fecha", ascending=False)
        )

    else:
        # Vista del trabajador
        st.subheader("➡️ Registrar tu trabajo del día")

        fecha = st.date_input("Fecha", date.today())

        cliente = st.selectbox(
            "Cliente",
            clientes["nombre"].dropna().tolist()
        )

        servicio = st.selectbox(
            "Servicio",
            servicios["servicio"].dropna().tolist()
        )

        obs = st.text_area("Observaciones (opcional)")

        if st.button("Enviar registro"):
            nuevo = pd.DataFrame([{
                "fecha": fecha,
                "cliente": cliente,
                "servicio": servicio,
                "trabajador": st.session_state["usuario"],
                "valor_servicio": "",
                "observaciones": obs,
                "quien_registro": st.session_state["usuario"]
            }])

            registros = pd.concat([registros, nuevo], ignore_index=True)
            guardar_excel(registros, ARCH_REGISTROS)

            st.success("Registro enviado al administrador ✅")

# =========================
# 2) CLIENTES (SOLO ADMIN)
# =========================

if st.session_state["menu"] == "Clientes" and st.session_state["rol"] == "admin":

    st.header("👥 Gestión de Clientes")

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
            clientes.loc[
                clientes["nombre"] == cliente_sel, "direccion"
            ] = nueva_dir

            clientes.loc[
                clientes["nombre"] == cliente_sel, "telefono"
            ] = nuevo_tel

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

if st.session_state["menu"] == "Servicios" and st.session_state["rol"] == "admin":

    st.header("🛠 Gestión de Servicios")

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
            servicios.loc[
                servicios["servicio"] == serv_sel, "descripcion"
            ] = nueva_desc

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

if st.session_state["menu"] == "Trabajadores" and st.session_state["rol"] == "admin":

    st.header("👷 Gestión de Trabajadores")

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
            trabajadores.loc[
                trabajadores["usuario"] == trab_sel, "password"
            ] = nueva_pass

            guardar_excel(trabajadores, ARCH_TRABAJADORES)
            st.success("Contraseña actualizada ✅")
            st.rerun()

    with tab3:
        trab_del = st.selectbox("Trabajador a eliminar", trabajadores["usuario"])

        if st.button("Eliminar trabajador"):
            trabajadores = trabajadores[
                trabajadores["usuario"] != trab_del
            ]
            guardar_excel(trabajadores, ARCH_TRABAJADORES)
            st.success("Trabajador eliminado ❌")
            st.rerun()
