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

# Inicializar el estado de la sesión
if "generar_excel" not in st.session_state:
    st.session_state.generar_excel = False

# Configuración de la página
st.set_page_config(page_title="Apps Tienda Pauli", layout="centered")

# Centramos el título y los botones
st.markdown("""
    <style>
    .centered {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        text-align: center;
    }
    .button-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 20px;
        margin-top: 20px;
    }
    .stButton button {
        font-size: 16px;
        padding: 8px 20px;
        white-space: nowrap;  /* Evita que el texto se divida en múltiples filas */
    }
    </style>
    """, unsafe_allow_html=True)

# Título principal
st.markdown("<div class='centered'><h1 style='color: #333;'>Apps Tienda Pauli</h1></div>", unsafe_allow_html=True)

# Mostrar los botones "Generar Excel" y "Generar PDF" en un contenedor centrado
st.markdown('<div class="centered"><div class="button-container">', unsafe_allow_html=True)

# Usamos `st.columns()` con un espacio vacío en los extremos para centrar los botones
col1, col2, col3 = st.columns([2, 1, 2])

with col2:
    if st.button("📊 Generar Excel", key="excel"):
        st.session_state.generar_excel = True
    st.button("📄 Generar PDF", key="pdf")  # Este botón no hace nada por ahora

st.markdown('</div></div>', unsafe_allow_html=True)

# Si se hizo clic en "Generar Excel"
if st.session_state.generar_excel:
    # Subir el archivo CSV
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
