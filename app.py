import streamlit as st
import pandas as pd
import os
from datetime import date

# =========================
# ARCHIVOS DE DATOS
# =========================

ARCH_CLIENTES = "clientes.xlsx"
ARCH_SERVICIOS = "servicios.xlsx"
ARCH_TRABAJADORES = "trabajadores.xlsx"
ARCH_REGISTROS = "registros_diarios.xlsx"

def crear_archivos_si_no_existen():
    if not os.path.exists(ARCH_CLIENTES):
        pd.DataFrame(columns=["nombre","direccion","telefono"]).to_excel(ARCH_CLIENTES, index=False)

    if not os.path.exists(ARCH_SERVICIOS):
        pd.DataFrame(columns=["servicio","descripcion"]).to_excel(ARCH_SERVICIOS, index=False)

    if not os.path.exists(ARCH_TRABAJADORES):
        # usuario, password, nombre, rol
        df = pd.DataFrame([{
            "usuario":"admin",
            "password":"admin",
            "nombre":"Administrador",
            "rol":"admin"
        }])
        df.to_excel(ARCH_TRABAJADORES, index=False)

    if not os.path.exists(ARCH_REGISTROS):
        pd.DataFrame(columns=[
            "fecha","cliente","servicio","trabajador",
            "valor_servicio","registrado_por"
        ]).to_excel(ARCH_REGISTROS, index=False)

crear_archivos_si_no_existen()

# =========================
# FUNCIONES DE CARGA/GUARDADO
# =========================

def cargar_excel(ruta):
    return pd.read_excel(ruta)

def guardar_excel(df, ruta):
    df.to_excel(ruta, index=False)

# =========================
# LOGIN
# =========================

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
    st.session_state["rol"] = None
    st.session_state["usuario"] = None
    st.session_state["nombre"] = None

def login():
    st.title("🔐 Acceso al Sistema")

    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        trabajadores = cargar_excel(ARCH_TRABAJADORES)

        # LIMPIEZA PARA EVITAR ERRORES DE LOGIN
        trabajadores["usuario"] = trabajadores["usuario"].astype(str).str.strip()
        trabajadores["password"] = trabajadores["password"].astype(str).str.strip()
        trabajadores["rol"] = trabajadores["rol"].astype(str).str.strip()
        trabajadores["nombre"] = trabajadores["nombre"].astype(str).str.strip()

        usuario = usuario.strip()
        password = password.strip()

        fila = trabajadores[
            (trabajadores["usuario"] == usuario) &
            (trabajadores["password"] == password)
        ]

        if len(fila) == 1:
            st.session_state["autenticado"] = True
            st.session_state["rol"] = fila.iloc[0]["rol"]
            st.session_state["usuario"] = usuario
            st.session_state["nombre"] = fila.iloc[0]["nombre"]
            st.experimental_rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

# =========================
# MENÚ PRINCIPAL CON BOTONES
# =========================

def menu_principal():
    st.title("📋 Menú Principal")

    st.write(f"👤 Sesión iniciada como: **{st.session_state['nombre']}** ({st.session_state['rol']})")

    st.markdown("---")

    if st.session_state["rol"] == "admin":
        col1, col2 = st.columns(2)

        with col1:
            if st.button("📅 Registro Diario"):
                st.session_state["pantalla"] = "registro"
        with col2:
            if st.button("👥 Clientes"):
                st.session_state["pantalla"] = "clientes"

        col3, col4 = st.columns(2)

        with col3:
            if st.button("🛠️ Servicios"):
                st.session_state["pantalla"] = "servicios"
        with col4:
            if st.button("🧑‍🔧 Trabajadores"):
                st.session_state["pantalla"] = "trabajadores"

    else:  # TRABAJADOR
        if st.button("📅 Registro Diario"):
            st.session_state["pantalla"] = "registro"

    st.markdown("---")
    if st.button("Cerrar sesión"):
        st.session_state.clear()
        st.experimental_rerun()

# =========================
# REGISTRO DIARIO
# =========================

def registro_diario():
    st.header("📅 Registro Diario de Servicios")

    clientes = cargar_excel(ARCH_CLIENTES)
    servicios = cargar_excel(ARCH_SERVICIOS)
    trabajadores = cargar_excel(ARCH_TRABAJADORES)

    if clientes.empty:
        st.warning("No hay clientes registrados aún")
        return

    if servicios.empty:
        st.warning("No hay servicios registrados aún")
        return

    fecha = st.date_input("Fecha", date.today())
    cliente = st.selectbox("Cliente", clientes["nombre"])
    servicio = st.selectbox("Servicio", servicios["servicio"])
    trabajador = st.selectbox("Trabajador", trabajadores["nombre"])

    valor = None
    if st.session_state["rol"] == "admin":
        valor = st.number_input("Valor del servicio ($)", min_value=0, step=1000)

    if st.button("Guardar registro"):
        registros = cargar_excel(ARCH_REGISTROS)

        nuevo = pd.DataFrame([{
            "fecha": fecha,
            "cliente": cliente,
            "servicio": servicio,
            "trabajador": trabajador,
            "valor_servicio": valor if st.session_state["rol"]=="admin" else "",
            "registrado_por": st.session_state["nombre"]
        }])

        registros = pd.concat([registros, nuevo], ignore_index=True)
        guardar_excel(registros, ARCH_REGISTROS)

        st.success("Registro guardado correctamente ✅")

# =========================
# CLIENTES (SOLO ADMIN)
# =========================

def gestion_clientes():
    st.header("👥 Gestión de Clientes")

    clientes = cargar_excel(ARCH_CLIENTES)

    opcion = st.radio("Selecciona acción", ["Agregar","Modificar","Eliminar"])

    if opcion == "Agregar":
        nombre = st.text_input("Nombre")
        direccion = st.text_input("Dirección")
        telefono = st.text_input("Teléfono")

        if st.button("Agregar cliente"):
            nuevo = pd.DataFrame([{
                "nombre": nombre.strip(),
                "direccion": direccion.strip(),
                "telefono": telefono.strip()
            }])

            clientes = pd.concat([clientes, nuevo], ignore_index=True)
            guardar_excel(clientes, ARCH_CLIENTES)
            st.success("Cliente agregado ✅")

    elif opcion == "Modificar":
        sel = st.selectbox("Cliente", clientes["nombre"])
        fila = clientes[clientes["nombre"] == sel].iloc[0]

        nuevo_nombre = st.text_input("Nombre", fila["nombre"])
        nueva_dir = st.text_input("Dirección", fila["direccion"])
        nuevo_tel = st.text_input("Teléfono", fila["telefono"])

        if st.button("Guardar cambios"):
            clientes.loc[clientes["nombre"]==sel, ["nombre","direccion","telefono"]] = [
                nuevo_nombre, nueva_dir, nuevo_tel
            ]
            guardar_excel(clientes, ARCH_CLIENTES)
            st.success("Cliente modificado ✅")

    else: # Eliminar
        sel = st.selectbox("Cliente", clientes["nombre"])
        if st.button("Eliminar cliente"):
            clientes = clientes[clientes["nombre"] != sel]
            guardar_excel(clientes, ARCH_CLIENTES)
            st.success("Cliente eliminado ❌")

# =========================
# SERVICIOS (SOLO ADMIN)
# =========================

def gestion_servicios():
    st.header("🛠️ Gestión de Servicios")

    servicios = cargar_excel(ARCH_SERVICIOS)

    opcion = st.radio("Selecciona acción", ["Agregar","Modificar","Eliminar"])

    if opcion == "Agregar":
        nombre = st.text_input("Nombre del servicio")
        descripcion = st.text_area("Descripción")

        if st.button("Agregar servicio"):
            nuevo = pd.DataFrame([{
                "servicio": nombre.strip(),
                "descripcion": descripcion.strip()
            }])
            servicios = pd.concat([servicios, nuevo], ignore_index=True)
            guardar_excel(servicios, ARCH_SERVICIOS)
            st.success("Servicio agregado ✅")

    elif opcion == "Modificar":
        sel = st.selectbox("Servicio", servicios["servicio"])
        fila = servicios[servicios["servicio"]==sel].iloc[0]

        nuevo_nombre = st.text_input("Nombre", fila["servicio"])
        nueva_desc = st.text_area("Descripción", fila["descripcion"])

        if st.button("Guardar cambios"):
            servicios.loc[servicios["servicio"]==sel, ["servicio","descripcion"]] = [
                nuevo_nombre, nueva_desc
            ]
            guardar_excel(servicios, ARCH_SERVICIOS)
            st.success("Servicio modificado ✅")

    else:
        sel = st.selectbox("Servicio", servicios["servicio"])
        if st.button("Eliminar servicio"):
            servicios = servicios[servicios["servicio"] != sel]
            guardar_excel(servicios, ARCH_SERVICIOS)
            st.success("Servicio eliminado ❌")

# =========================
# TRABAJADORES (SOLO ADMIN)
# =========================

def gestion_trabajadores():
    st.header("🧑‍🔧 Gestión de Trabajadores")

    trabajadores = cargar_excel(ARCH_TRABAJADORES)

    opcion = st.radio("Selecciona acción", ["Agregar","Modificar","Eliminar"])

    if opcion == "Agregar":
        nombre = st.text_input("Nombre completo")
        usuario = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")

        if st.button("Agregar trabajador"):
            nuevo = pd.DataFrame([{
                "usuario": usuario.strip(),
                "password": password.strip(),
                "nombre": nombre.strip(),
                "rol": "trabajador"
            }])
            trabajadores = pd.concat([trabajadores, nuevo], ignore_index=True)
            guardar_excel(trabajadores, ARCH_TRABAJADORES)
            st.success(f"Trabajador creado ✅\nUsuario: {usuario}\nContraseña: {password}")

    elif opcion == "Modificar":
        sel = st.selectbox("Trabajador", trabajadores["nombre"])
        fila = trabajadores[trabajadores["nombre"]==sel].iloc[0]

        nuevo_nombre = st.text_input("Nombre", fila["nombre"])
        nuevo_usuario = st.text_input("Usuario", fila["usuario"])
        nueva_pass = st.text_input("Nueva contraseña", value=fila["password"])

        if st.button("Guardar cambios"):
            trabajadores.loc[trabajadores["nombre"]==sel, ["nombre","usuario","password"]] = [
                nuevo_nombre, nuevo_usuario, nueva_pass
            ]
            guardar_excel(trabajadores, ARCH_TRABAJADORES)
            st.success("Trabajador modificado ✅")

    else:
        sel = st.selectbox("Trabajador", trabajadores["nombre"])
        if st.button("Eliminar trabajador"):
            trabajadores = trabajadores[trabajadores["nombre"] != sel]
            guardar_excel(trabajadores, ARCH_TRABAJADORES)
            st.success("Trabajador eliminado ❌")

# =========================
# CONTROL DE PANTALLAS
# =========================

if not st.session_state["autenticado"]:
    login()
else:
    if "pantalla" not in st.session_state:
        st.session_state["pantalla"] = "menu"

    if st.session_state["pantalla"] == "menu":
        menu_principal()

    elif st.session_state["pantalla"] == "registro":
        registro_diario()
        if st.button("⬅️ Volver al menú"):
            st.session_state["pantalla"] = "menu"
            st.experimental_rerun()

    elif st.session_state["pantalla"] == "clientes":
        gestion_clientes()
        if st.button("⬅️ Volver al menú"):
            st.session_state["pantalla"] = "menu"
            st.experimental_rerun()

    elif st.session_state["pantalla"] == "servicios":
        gestion_servicios()
        if st.button("⬅️ Volver al menú"):
            st.session_state["pantalla"] = "menu"
            st.experimental_rerun()

    elif st.session_state["pantalla"] == "trabajadores":
        gestion_trabajadores()
        if st.button("⬅️ Volver al menú"):
            st.session_state["pantalla"] = "menu"
            st.experimental_rerun()
