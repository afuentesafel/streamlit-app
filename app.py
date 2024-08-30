import streamlit as st
import pandas as pd
import openpyxl
from openpyxl import Workbook
from io import BytesIO

# Configuración de la página
st.set_page_config(page_title="Apps Tienda Pauli", layout="centered")

# Título principal
st.markdown("<h1 style='text-align: center; color: #333;'>Apps Tienda Pauli</h1>", unsafe_allow_html=True)

# Función para procesar el archivo CSV y generar el archivo Excel
def procesar_archivo(file):
    # Leer el archivo CSV
    df = pd.read_csv(file)

    # Crear un nuevo archivo de Excel
    wb = Workbook()
    ws = wb.active

    # Agregar encabezados
    ws.append(["Nombre", "Dirección", "Teléfono"])

    # Iterar sobre las filas del DataFrame y aplicar filtros
    for index, row in df.iterrows():
        envio = row['Título del método de envío']

        # Filtros
        rm = 'Delivery RM' in envio
        r5a = 'Delivery 5ta Región: Viña del Mar, Valparaíso, Concón, Quilpué y Villa Alemana' in envio
        r5b = 'Delivery 5ta Región: Hijuelas, La Calera, La Cruz, Nogales, Quillota, Limache, Olmué' in envio
        r6 = 'Delivery 6ta Región: San Francisco de Mostazal, Machalí, Rancagua, Codegua y Graneros' in envio

        if rm or r5a or r5b or r6:
            ws.append([
                f"{row['Nombre (envío)']} {row['Apellidos (envío)']}",
                f"{row['Dirección línea 1 (envío)']} {row['Dirección línea 2 (envío)']} {row['Comuna1']}",
                row['Teléfono (facturación)']
            ])

    # Guardar el archivo Excel en un objeto de bytes
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    return output

# Inicializar el estado de la sesión
if "generar_excel" not in st.session_state:
    st.session_state.generar_excel = False

# Centramos los botones en una sola fila con HTML y CSS
st.markdown("""
    <style>
    .button-container {
        display: flex;
        justify-content: center;
        gap: 20px;
    }
    .button-container button {
        flex: 1;
        font-size: 18px;
        padding: 10px 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Mostrar los botones "Generar Excel", "Generar PDF", y "Reiniciar proceso"
st.markdown('<div class="button-container">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Generar Excel", key="excel"):
        st.session_state.generar_excel = True

with col2:
    st.button("📄 Generar PDF", key="pdf")  # Este botón no hace nada por ahora

with col3:
    if st.button("🔄 Reiniciar proceso"):
        # Restablecer el estado y recargar la página
        st.session_state.generar_excel = False
        st.session_state.clear()  # Borrar todo el estado
        st.experimental_rerun()  # Intentar recargar la aplicación

st.markdown('</div>', unsafe_allow_html=True)

# Si se hizo clic en "Generar Excel"
if st.session_state.generar_excel:
    # Subir el archivo CSV
    uploaded_file = st.file_uploader("Sube tu archivo CSV", type="csv")

    # Pedir la fecha de retiro al usuario
    fecha_retiro = st.text_input("Ingresa la fecha de retiro (dd-mm-aaaa):")

    # Si se sube un archivo y se ingresa la fecha de retiro
    if uploaded_file and fecha_retiro:
        st.write("Procesando el archivo...")
        excel_file = procesar_archivo(uploaded_file)
        nombre_archivo = f"envio_{fecha_retiro}.xlsx"
        st.download_button(
            label="Descargar Excel",
            data=excel_file,
            file_name=nombre_archivo,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
