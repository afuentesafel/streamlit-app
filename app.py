import streamlit as st
import pandas as pd
import openpyxl
from openpyxl import Workbook
from io import BytesIO

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
        rm = 'Delivery Región Metropolitana' in envio
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

# Interfaz de Streamlit
st.title('Procesador de Pedidos')

uploaded_file = st.file_uploader("Sube tu archivo CSV", type="csv")

if uploaded_file is not None:
    # Pedir la fecha de retiro al usuario
    fecha_retiro = st.text_input("Ingresa la fecha de retiro (dd-mm-aaaa):")
    
    if fecha_retiro:
        st.write("Procesando el archivo...")
        excel_file = procesar_archivo(uploaded_file)
        
        # Configurar el nombre del archivo usando la fecha de retiro
        nombre_archivo = f"envio_{fecha_retiro}.xlsx"
        
        st.download_button(
            label="Descargar archivo procesado",
            data=excel_file,
            file_name=nombre_archivo,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
