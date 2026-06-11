import gspread
import json
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- CONFIGURACIÓN DE CONEXIÓN ---
# Asegúrate de tener tu archivo 'credenciales.json' en la misma carpeta que este script
def get_sheets_client():
    with open('credenciales.json') as f:
        credenciales_dict = json.load(f)
        
    creds = Credentials.from_service_account_info(
        credenciales_dict, 
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets", 
            "https://www.googleapis.com/auth/drive"
        ]
    )
    return gspread.authorize(creds)

# --- LÓGICA DE GUARDADO ---
def guardar_infraccion(lat, lon, tipo_infraccion):
    """
    Inserta una nueva fila en Google Sheets.
    Debe coincidir exactamente con el orden: [fecha, lat, lon, tipo]
    """
    try:
        cliente = get_sheets_client()
        archivo = cliente.open("ISAAC - Monitoreo")
        hoja = archivo.worksheet("Hoja 1")
        
        # Obtenemos fecha y hora actual
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Guardamos en la hoja
        hoja.append_row([fecha, lat, lon, tipo_infraccion])
        return True
    except Exception as e:
        print(f"Error al guardar en Google Sheets: {e}")
        return False

# --- LÓGICA DEL AGENTE ---
def procesar_reporte(data):
    """
    Función principal para procesar los datos recibidos (ej: desde un bot).
    'data' debe ser un diccionario con claves: lat, lon, tipo.
    """
    lat = data.get("lat")
    lon = data.get("lon")
    tipo = data.get("tipo")
    
    # Validamos que los datos existen
    if lat and lon and tipo:
        resultado = guardar_infraccion(lat, lon, tipo)
        if resultado:
            print(f"ÉXITO: Reporte de '{tipo}' guardado en posición {lat}, {lon}")
        else:
            print("ERROR: No se pudo guardar el reporte.")
    else:
        print("ERROR: Datos incompletos.")

# --- EJECUCIÓN DE PRUEBA ---
if __name__ == "__main__":
    # Simulación de un dato que llega desde el campo
    dato_recibido = {
        "lat": -26.8241, 
        "lon": -65.2226, 
        "tipo": "Mal estacionamiento"
    }
    procesar_reporte(dato_recibido)
