import streamlit as st
import time
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from streamlit_geolocation import streamlit_geolocation

# Configuración de la página
st.set_page_config(page_title="ISAAC Agente", page_icon="🚓", layout="centered")

# --- MOTOR DE CONEXIÓN A GOOGLE SHEETS ---
def conectar_sheets():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    # Traemos el secreto desde la caja fuerte de Streamlit
    credenciales_dict = json.loads(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(credenciales_dict, scopes=scopes)
    cliente = gspread.authorize(creds)
    # Abrimos la planilla por su nombre exacto
    return cliente.open("ISAAC - Monitoreo").sheet1

# --- INTERFAZ DEL AGENTE ---
st.title("🚓 ISAAC - Terminal Móvil")
st.markdown("**Agente en calle:** Operativo Activo")
st.divider()

# Captura de ubicación única
loc = streamlit_geolocation(key="mi_ubicacion_unica")

# Widget nativo para activar la cámara
foto = st.camera_input("📸 Capturar Acta o Patente")

if foto:
    st.success("✅ Imagen capturada con alta calidad.")
    
    if st.button("🤖 Procesar y Extraer Datos (OCR)"):
        with st.spinner("Analizando imagen y conectando con el Tribunal..."):
            time.sleep(3) # Simulamos el tiempo de procesamiento de IA
            
            # Obtener datos de ubicación o valores por defecto
            fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            lat = loc.get("latitude", -26.8241)
            lon = loc.get("longitude", -65.2072)
            
            patente = "AB 123 CD"
            dni = "34.567.890"
            infraccion = "Mal estacionamiento"
            ubicacion_texto = f"{lat}, {lon}"
            
            # Mostrar datos
            st.info("📋 **Datos extraídos automáticamente:**")
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Dominio (Patente):", patente)
                st.text_input("DNI Infractor:", dni)
            with col2:
                st.text_input("Tipo de Infracción:", infraccion)
                st.text_input("Ubicación GPS:", ubicacion_texto)
            
            # Impacto real en Google Sheets
            try:
                hoja = conectar_sheets()
                hoja.append_row([fecha_actual, patente, dni, infraccion, ubicacion_texto])
                st.success("🚀 ¡Infracción enviada exitosamente a la base de datos central!")
            except Exception as e:
                st.error(f"Error al guardar: {e}")
