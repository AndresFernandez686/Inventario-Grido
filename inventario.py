import streamlit as st

productos = {
    'Helado de Chocolate': 0,
    'Helado de Vainilla': 0,
    'Capuchino': 0,
    'Sundae': 0
}

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

def empleado_interfaz():
    st.title("Panel Empleado: Cargar productos")

    producto_seleccionado = st.selectbox("Selecciona un producto", list(productos.keys()))
    cantidad = st.number_input("Cantidad a agregar", min_value=1, step=1)

    if st.button("Actualizar stock"):
        productos[producto_seleccionado] += cantidad
        st.success(f"Se agregaron {cantidad} unidades a {producto_seleccionado}. Nuevo stock: {productos[producto_seleccionado]}")

    st.subheader("Inventario actual:")
    for p, c in productos.items():
        st.write(f"- {p}: {c}")

def administrador_interfaz():
    st.title("Panel Administrador: Inventario total")

    st.subheader("Inventario actual:")
    for p, c in productos.items():
        st.write(f"- {p}: {c}")

    total = sum(productos.values())
    st.markdown(f"**Total de productos en la heladería:** {total}")

def main():
    usuario, rol = login()

    if usuario and rol:
        if rol == 'empleado':
            empleado_interfaz()
        elif rol == 'administrador':
            administrador_interfaz()
    else:
        st.title("Por favor, ingresa un usuario válido en el panel lateral para continuar.")

if __name__ == "__main__":
    main()
