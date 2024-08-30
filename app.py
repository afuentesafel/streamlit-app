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

# Mostrar botones de "Generar Excel" y "Generar PDF"
col1, col2 = st.columns(2)

with col1:
    generar_excel = st.button("📊 Generar Excel", key="excel")

with col2:
    generar_pdf = st.button("📄 Generar PDF", key="pdf")

# Si se hace clic en "Generar Excel"
if generar_excel:
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

# Botón para reiniciar el proceso
if st.button("🔄 Reiniciar proceso"):
    st.experimental_rerun()
