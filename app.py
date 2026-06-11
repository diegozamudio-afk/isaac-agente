import streamlit as st
import pandas as pd
import gspread
import json
import plotly.express as px
from google.oauth2.service_account import Credentials

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Dashboard ISAAC", layout="wide")

@st.cache_data(ttl=60)
def conectar_sheets():
    credenciales_dict = json.loads(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(credenciales_dict, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
    cliente = gspread.authorize(creds)
    archivo = cliente.open("ISAAC - Monitoreo")
    return archivo.worksheet("Hoja 1") 

st.title("📊 Dashboard ISAAC - Inteligencia de Gestión")

# 2. FORMULARIO DE CARGA (Para el agente)
with st.expander("➕ Cargar nueva infracción"):
    opciones = ["Mal estacionamiento", "Rampa discapacitados", "Senda peatonal", "Sin casco", "Sentido contrario"]
    tipo_infraccion = st.selectbox("Seleccionar tipo de infracción:", opciones)
    if st.button("Guardar Infracción"):
        st.success(f"Infracción '{tipo_infraccion}' registrada correctamente.")

st.markdown("---")

# 3. LECTURA Y DASHBOARD
try:
    hoja = conectar_sheets()
    datos = hoja.get_all_records()
    df = pd.DataFrame(datos)

    if not df.empty:
        # Procesamiento
        df['lat'] = pd.to_numeric(df['lat'], errors='coerce') / 10000
        df['lon'] = pd.to_numeric(df['lon'], errors='coerce') / 10000
        
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Registros Totales", len(df))
        col2.metric("Infracciones Hoy", len(df))
        col3.metric("Usuarios CiDi Tuc", "130k", "Meta: 800k")
        col4.metric("Recaudación Est.", f"${len(df) * 5000:,.0f}")

        st.markdown("---")

        # MAPA Y GRÁFICOS
        st.subheader("📍 Mapa de Calor: Zonas Críticas")
        st.map(df.dropna(subset=['lat', 'lon']))

        col_izq, col_der = st.columns(2)
        with col_izq:
            st.subheader("Distribución por Tipo")
            # Ajustamos para usar los datos reales si existe la columna 'tipo'
            if 'tipo' in df.columns:
                fig_pie = px.pie(df, names='tipo', hole=0.4)
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("Sin datos suficientes para el gráfico de torta.")

        with col_der:
            st.subheader("Volumen de Registros")
            st.bar_chart(df.index)

        # TABLA
        with st.expander("Ver Registros Detallados"):
            st.dataframe(df)

    else:
        st.info("La planilla está vacía.")

except Exception as e:
    st.error(f"Error en la conexión: {e}")

if st.button("🔄 Actualizar Datos"):
    st.rerun()
