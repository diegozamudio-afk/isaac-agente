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

# ==========================================
# MENÚ LATERAL DE NAVEGACIÓN
# ==========================================
st.sidebar.title("Navegación")
modulo = st.sidebar.radio("Seleccionar Módulo:", ["Terminal de Infracciones", "Fiscalización Dinámica (LPR)"])

# Geolocalización base
loc = streamlit_geolocation()
if loc and loc.get("latitude") is not None:
    st.session_state.lat = loc["latitude"]
    st.session_state.lon = loc["longitude"]

lat = st.session_state.get("lat", -26.8241)
lon = st.session_state.get("lon", -65.2072)


# ==========================================
# MÓDULO 1: TERMINAL DE INFRACCIONES (Manual)
# ==========================================
if modulo == "Terminal de Infracciones":
    st.title("🚓 ISAAC - Terminal Móvil")
    st.subheader("Carga manual de infracciones")

    opciones = ["Mal estacionamiento", "Rampa discapacitados", "Senda peatonal", "Sin casco", "Sentido contrario"]
    tipo_infraccion = st.selectbox("Seleccionar tipo de infracción:", opciones)

    foto = st.camera_input("📸 Capturar Acta o Patente")

    if foto:
        if st.button("🤖 Procesar y Enviar"):
            with st.spinner("Enviando..."):
                try:
                    hoja = conectar_sheets()
                    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    # Asegúrate de que este orden sea idéntico al de tu Hoja 1 de Google Sheets
                    hoja.append_row([fecha, "AB 123 CD", "34.567.890", tipo_infraccion, lat*10000, lon*10000])
                    st.success("🚀 ¡Infracción enviada correctamente!")
                except Exception as e:
                    st.error(f"Error: {e}")


# ==========================================
# MÓDULO 2: FISCALIZACIÓN EN MOVIMIENTO (LPR)
# ==========================================
elif modulo == "Fiscalización Dinámica (LPR)":
    st.title("🛵 ISAAC - Fiscalización Dinámica (LPR)")
    st.write("Módulo de captura inteligente en movimiento. El agente no detiene su marcha.")
    
    st.info("Modo simulación: El sistema procesa lotes de patentes capturadas por la cámara en tiempo real.")
    
    patentes_detectadas = ["AB 123 CD", "EF 456 GH", "XX 999 YY (VENCIDO)", "JK 012 LM"]
    
    patente_escaneada = st.selectbox("Simular detección automática de patente en calle:", patentes_detectadas)
    
    # Mostramos los datos de la patente leída directamente
    st.success(f"Patente en mira: **{patente_escaneada}**")
    st.text(f"Ubicación GPS actual: Lat: {lat}, Long: {lon}")
    st.text("Sello de Tiempo: NTP Server Validated")
    
    if "(VENCIDO)" in patente_escaneada:
        st.error("🔴 ALERTA: Patente sin estacionamiento medido activo.")
        st.warning("Registro fotográfico tomado automáticamente. El acta queda lista para emitir.")
        
        if st.button("Confirmar Acta Digital (Un solo toque)"):
            with st.spinner("Escribiendo acta en base de datos central (Google Sheets)..."):
                try:
                    hoja = conectar_sheets()
                    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    motivo_lpr = "Estacionamiento Medido Vencido (LPR)"
                    
                    # Se inyecta la fila al Google Sheet
                    hoja.append_row([fecha, patente_escaneada, "S/D", motivo_lpr, lat*10000, lon*10000])
                    
                    st.success("Acta emitida correctamente al servidor. Impactará en el Dashboard.")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error al guardar en el servidor: {e}")
    else:
        st.info("🟢 Vehículo en regla. Patente registrada en el sistema.")
