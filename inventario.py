import streamlit as st
import json
import os
import pandas as pd
from io import BytesIO

INVENTARIO_FILE = "inventario_categorias.json"

productos_por_categoria = {
    "Impulsivo": {
        "Galletas": 0,
        "Chicles": 0,
        "Snack Salado": 0
    },
    "Por Kilos": {
        "Helado Vainilla": 0,
        "Helado Chocolate": 0,
        "Helado Fresa": 0
    },
    "Extras": {
        "Vasos": 0,
        "Cucharas": 0,
        "Servilletas": 0
    }
}

usuarios = {
    'empleado1': 'empleado',
    'admin1': 'administrador'
}

def cargar_inventario():
    if os.path.exists(INVENTARIO_FILE):
        with open(INVENTARIO_FILE, "r") as f:
            return json.load(f)
    else:
        return productos_por_categoria.copy()

def guardar_inventario(inventario):
    with open(INVENTARIO_FILE, "w") as f:
        json.dump(inventario, f)

def login():
    st.sidebar.title("Inicio de sesión")
    usuario = st.sidebar.text_input("Usuario")
    if usuario in usuarios:
        st.sidebar.success(f"Hola {usuario}, rol: {usuarios[usuario]}")
        return usuario, usuarios[usuario]
    elif usuario:
        st.sidebar.error("Usuario no reconocido")
    return None, None

def to_excel_bytes(df):
    """Convierte un DataFrame a bytes de archivo Excel en memoria"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

def empleado_interfaz(inventario):
    st.title("Panel Empleado: Cargar productos")

    tabs = st.tabs(list(inventario.keys()))
    for i, categoria in enumerate(inventario.keys()):
        with tabs[i]:
            productos = inventario[categoria]
            producto_seleccionado = st.selectbox(f"Selecciona un producto de {categoria}", list(productos.keys()))
            cantidad = st.number_input("Cantidad a agregar", min_value=1, step=1, key=f"{categoria}_cant")
            if st.button(f"Actualizar stock en {categoria}", key=f"{categoria}_btn"):
                productos[producto_seleccionado] += cantidad
                guardar_inventario(inventario)
                st.success(f"Se agregaron {cantidad} unidades a {producto_seleccionado} en {categoria}. Nuevo stock: {productos[producto_seleccionado]}")

            st.write(f"Inventario en categoría {categoria}:")
            for p, c in productos.items():
                st.write(f"- {p}: {c}")

def administrador_interfaz(inventario):
    st.title("Panel Administrador: Inventario total por categoría")

    total_general = 0
    for categoria, productos in inventario.items():
        st.subheader(f"Categoría: {categoria}")
        total_categoria = sum(productos.values())
        total_general += total_categoria
        for p, c in productos.items():
            st.write(f"- {p}: {c}")
        st.markdown(f"**Total en {categoria}: {total_categoria}**")

    st.markdown(f"## Total general en la heladería: {total_general}")

    st.markdown("---")
    st.subheader("Descargar inventarios por categoría")

    for categoria, productos in inventario.items():
        df = pd.DataFrame({
            "Producto": list(productos.keys()),
            "Cantidad": list(productos.values())
        })
        excel_bytes = to_excel_bytes(df)
        st.download_button(
            label=f"Descargar Excel de {categoria}",
            data=excel_bytes,
            file_name=f"inventario_{categoria.lower().replace(' ', '_')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

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
