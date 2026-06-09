import streamlit as st
import time
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="ISAAC Agente", page_icon="📱", layout="centered")

# --- MOTOR DE CONEXIÓN A GOOGLE SHEETS ---
def conectar_sheets():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    # Traemos el secreto de la caja fuerte de Streamlit
    credenciales_dict = json.loads(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(credenciales_dict, scopes=scopes)
    cliente = gspread.authorize(creds)
    
    # Abrimos la planilla por su nombre exacto
    return cliente.open("ISAAC - Monitoreo").sheet1

# --- INTERFAZ DEL AGENTE ---
st.title("🚓 ISAAC - Terminal Móvil")
st.markdown("**Agente en calle:** Operativo Activo")
st.divider()

# Widget nativo para activar la cámara
foto = st.camera_input("📸 Capturar Acta o Patente")

if foto:
    st.success("✅ Imagen capturada con alta calidad.")
    
    if st.button("🤖 Procesar y Extraer Datos (OCR)"):
        with st.spinner("Analizando imagen y conectando con el Tribunal..."):
            time.sleep(3) # Simulación de los 3 segundos de lectura IA
            
            # 1. Generamos los datos extraídos
            fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            patente = "AB 123 CD"
            dni = "34.567.890"
            infraccion = "Mal estacionamiento"
            ubicacion = "-26.8300, -65.2050"
            
            # 2. Los mostramos en pantalla
            st.info("📋 **Datos extraídos automáticamente:**")
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Dominio (Patente):", patente)
                st.text_input("DNI Infractor:", dni)
            with col2:
                st.text_input("Tipo de Infracción:", infraccion)
                st.text_input("Ubicación GPS:", ubicacion)
            
            # 3. ¡EL IMPACTO REAL EN GOOGLE SHEETS!
            try:
                hoja = conectar_sheets()
                hoja.append_row([fecha_actual, patente, dni, infraccion, ubicacion])
                st.success("🚀 ¡Infracción enviada exitosamente a la base de datos central!")
            except Exception as e:
                st.error(f"Ocurrió un error al intentar guardar: {e}")
                from streamlit_geolocation import streamlit_geolocation

# ... dentro de la app ...
loc = streamlit_geolocation()

if loc:
    lat = loc["latitude"]
    lon = loc["longitude"]
else:
    lat, lon = -26.8241, -65.2072 # Ubicación por defecto en caso de error
    # Importación necesaria
from streamlit_geolocation import streamlit_geolocation

# ... dentro de tu app, cuando capturás la infracción ...
loc = streamlit_geolocation()

if loc:
    lat = loc["latitude"]
    lon = loc["longitude"]
else:
    # Fallback por si el GPS tarda o no tiene señal
    lat, lon = -26.8241, -65.2072 

# Ahora usás estas variables 'lat' y 'lon' para enviarlas a tu Google Sheets
hoja.append_row([fecha_actual, patente, dni, infraccion, lat, lon])
