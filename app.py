import streamlit as st
import time

# Configuración adaptada para celulares
st.set_page_config(page_title="ISAAC Agente", page_icon="📱", layout="centered")

st.title("🚓 ISAAC - Terminal Móvil")
st.markdown("**Agente en calle:** Operativo Activo")
st.divider()

# Widget nativo para activar la cámara del celular o PC
foto = st.camera_input("📸 Capturar Acta o Patente")

if foto:
    st.success("✅ Imagen capturada con alta calidad.")
    
    # Botón para activar el motor de Inteligencia Artificial
    if st.button("🤖 Procesar y Extraer Datos (OCR)"):
        with st.spinner("Analizando imagen con visión computacional..."):
            time.sleep(3) # Simulamos los 3 segundos que tarda la IA real
            
            # Resultado simulado de la extracción
            st.info("📋 **Datos extraídos automáticamente:**")
            
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Dominio (Patente):", "AB 123 CD")
                st.text_input("DNI Infractor:", "34.567.890")
            with col2:
                st.text_input("Tipo de Infracción:", "Mal estacionamiento")
                st.text_input("Ubicación GPS:", "-26.8300, -65.2050")
            
            st.success("🚀 ¡Infracción enviada al Tablero Central y a Google Sheets!")
