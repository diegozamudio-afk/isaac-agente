import streamlit as st
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from streamlit_geolocation import streamlit_geolocation

st.set_page_config(page_title="ISAAC Agente", page_icon="🚓")

def conectar_sheets():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    credenciales_dict = json.loads(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(credenciales_dict, scopes=scopes)
    cliente = gspread.authorize(creds)
    return cliente.open("ISAAC - Monitoreo").sheet1

st.title("🚓 ISAAC - Terminal Móvil")

# Captura de ubicación
loc = streamlit_geolocation()

if loc and loc.get("latitude") is not None:
    st.session_state.lat = loc["latitude"]
    st.session_state.lon = loc["longitude"]

lat = st.session_state.get("lat", -26.8241)
lon = st.session_state.get("lon", -65.2072)

# --- NUEVO: SELECTOR DE INFRACCIONES ---
opciones = ["Mal estacionamiento", "Rampa discapacitados", "Senda peatonal", "Sin casco", "Sentido contrario"]
tipo_infraccion = st.selectbox("Seleccionar tipo de infracción:", opciones)

foto = st.camera_input("📸 Capturar Acta o Patente")

if foto:
    if st.button("🤖 Procesar y Enviar"):
        with st.spinner("Enviando..."):
            try:
                hoja = conectar_sheets()
                fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                
                # Se envían los datos: 
                # [Fecha, Patente_dummy, DNI_dummy, Tipo_Elegido, Lat, Lon]
                hoja.append_row([fecha, "AB 123 CD", "34.567.890", tipo_infraccion, lat, lon])
                
                st.success("🚀 ¡Infracción enviada correctamente!")
            except Exception as e:
                st.error(f"Error: {e}")
