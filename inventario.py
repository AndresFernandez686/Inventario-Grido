import streamlit as st
import json
import os

# Archivo donde se guardará el inventario
INVENTARIO_FILE = "inventario.json"

# Productos base (sin stock)
productos_base = {
    'Helado de Chocolate': 0,
    'Helado de Vainilla': 0,
    'Capuchino': 0,
    'Sundae': 0
}

def cargar_inventario():
    if os.path.exists(INVENTARIO_FILE):
        with open(INVENTARIO_FILE, "r") as f:
            return json.load(f)
    else:
        return productos_base.copy()

def guardar_inventario(inventario):
    with open(INVENTARIO_FILE, "w") as f:
        json.dump(inventario, f)

# Usuarios y roles (solo para demo)
usuarios = {
    'empleado1': 'empleado',
    'admin1': 'administrador'
}

def login():
    st.sidebar.title("Inicio de sesión")
    usuario = st.sidebar.text_input("Usuario")
    if usuario in usuarios:
        st.sidebar.success(f"Hola {usuario}, rol: {usuarios[usuario]}")
        return usuario, usuarios[usuario]
    elif usuario:
        st.sidebar.error("Usuario no reconocido")
    return None, None

def empleado_interfaz(inventario):
    st.title("Panel Empleado: Cargar productos")

    producto_seleccionado = st.selectbox("Selecciona un producto", list(inventario.keys()))
    cantidad = st.number_input("Cantidad a agregar", min_value=1, step=1)

    if st.button("Actualizar stock"):
        inventario[producto_seleccionado] += cantidad
        guardar_inventario(inventario)
        st.success(f"Se agregaron {cantidad} unidades a {producto_seleccionado}. Nuevo stock: {inventario[producto_seleccionado]}")

    st.subheader("Inventario actual:")
    for p, c in inventario.items():
        st.write(f"- {p}: {c}")

def administrador_interfaz(inventario):
    st.title("Panel Administrador: Inventario total")

    st.subheader("Inventario actual:")
    for p, c in inventario.items():
        st.write(f"- {p}: {c}")

    total = sum(inventario.values())
    st.markdown(f"**Total de productos en la heladería:** {total}")

def main():
    usuario, rol = login()

    if usuario and rol:
        inventario = cargar_inventario()

        if rol == 'empleado':
            empleado_interfaz(inventario)
        elif rol == 'administrador':
            administrador_interfaz(inventario)
    else:
        st.title("Por favor, ingresa un usuario válido en el panel lateral para continuar.")

if __name__ == "__main__":
    main()
