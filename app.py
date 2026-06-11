import gspread
import json
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- CONFIGURACIÓN ---
# Asegurate de tener tu archivo JSON de credenciales en el servidor
def get_sheets_client():
    # Si usas Streamlit Cloud, podrías cargar esto desde st.secrets
    # Para un script local, podés usar el path al archivo .json
    with open('credenciales.json') as f:
        credenciales_dict = json.load(f)
        
    creds = Credentials.from_service_account_info(
        credenciales_dict, 
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    )
    return gspread.authorize(creds)

def guardar_infraccion(lat, lon, tipo_infraccion):
    """
    Función que el Agente llama al recibir un reporte.
    """
    try:
        cliente = get_sheets_client()
        archivo = cliente.open("ISAAC - Monitoreo")
        hoja = archivo.worksheet("Hoja 1")
        
        # Obtenemos fecha y hora actual
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Guardamos en la hoja
        # Asegurate de que el orden de columnas coincida con tu Hoja 1
        hoja.append_row([fecha, lat, lon, tipo_infraccion])
        return True
    except Exception as e:
        print(f"Error al guardar: {e}")
        return False

# --- LÓGICA DEL AGENTE ---
# Aquí es donde integrarías la lógica de tu bot de WhatsApp (ej: Twilio o API de Meta)
def procesar_mensaje_infraccion(mensaje_recibido):
    """
    Ejemplo: El mensaje llega como "lat: -268241, lon: -652226, tipo: Sin casco"
    El agente parsea esto y llama a guardar_infraccion
    """
    # Lógica de parsing (simplificada)
    # En producción usarías regex o una librería de NLP
    lat = mensaje_recibido.get("lat")
    lon = mensaje_recibido.get("lon")
    tipo = mensaje_recibido.get("tipo")
    
    if guardar_infraccion(lat, lon, tipo):
        print("Infracción procesada y guardada correctamente.")
    else:
        print("Fallo en la comunicación con el sistema.")

# Ejemplo de uso
if __name__ == "__main__":
    datos_prueba = {"lat": -268241, "lon": -652226, "tipo": "Sin casco"}
    procesar_mensaje_infraccion(datos_prueba)
