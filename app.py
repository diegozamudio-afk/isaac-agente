import streamlit as st
import time
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
if "loc" not in st.session_state:
    st.session_state.loc = streamlit_geolocation()
loc = st.session_state.loc

foto = st.camera_input("📸 Capturar Acta o Patente")

if foto:
    if st.button("🤖 Procesar y Enviar"):
        with st.spinner("Conectando..."):
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            lat = loc.get("latitude") if loc.get("latitude") else -26.8241
            lon = loc.get("longitude") if loc.get("longitude") else -65.2072
            
            try:
                hoja = conectar_sheets()
                # ENVIAMOS CADA DATO EN UNA CELDA DISTINTA
                hoja.append_row([fecha, "AB 123 CD", "34.567.890", "Mal estacionamiento", lat, lon])
                st.success("🚀 ¡Infracción enviada!")
            except Exception as e:
                st.error(f"Error: {e}")
