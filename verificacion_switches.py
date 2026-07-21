import os
import platform
import sys
import pandas as pd
import time
import unicodedata
from dotenv import load_dotenv
from Servicios.Servicio_ping import Servicioping
from Servicios.Servicio_SSH import ServicioSSH

# Traigno el archivo con las credenciales
load_dotenv()

# Credenciales temporales para la prueba de acceso SSH
SSH_USER = os.getenv("SSH_USER")
SSH_PASSWORD = os.getenv("SSH_PASSWORD")

# --- CONFIGURACIÓN ---
nombre_archivo = str(input("Introduce el nombre de tu archivo "))
EXCEL_ENTRADA = f"Inventarios/{nombre_archivo}.xlsx"  # Archivo con el inventario en excel
EXCEL_SALIDA = f"Reportes/reporte_dispositivos_{nombre_archivo}.xlsx"
serv_ping = Servicioping()
serv_SSH = ServicioSSH(SSH_USER, SSH_PASSWORD)


#se verifica si se pudieron leer las credenciales o no
if not SSH_PASSWORD or not SSH_USER:
    print("ALERTA!!! No se pudieron leer las credenciales del archivo .env")
    sys.exit(1) # Alerta que el programa paró debido a un error y para todo

def limpiar_texto(texto):
    # Limpiar espacios en blanco en columna
    if pd.isna(texto):
        return ""

    # Minusculas y adios espacios
    texto = str(texto).strip().lower()

    # Normaliza a NFD y descarta los caracteres de la categoría 'Mn' (Nonspacing Mark)
    nfkd_form = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def main():
    print("Cargando archivo de Excel...")
    try:
        df = pd.read_excel(EXCEL_ENTRADA) #el archivo de excel está en la variable 'df'
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{EXCEL_ENTRADA}' en esta carpeta.")
        return
    
    # Limpiar acentuación y mayúsculas en la columna del excel
    df.columns = [limpiar_texto(col) for col in df.columns]

    # Verificar que exista la columna llamada IP
    if "direccion ip" not in df.columns:
        print("Error: Tu Excel debe tener una columna llamada exactamente 'Direccion IP' o esto explota :D.")
        return

    resultados_ping = []
    resultados_ssh = []

    total_switches = len(df) # calculamos el tamaño del archivo
    print(f"Iniciando escaneo de {total_switches} dispositivos...")

    for index, fila in df.iterrows():   
        ip = str(fila["direccion ip"]).strip()
        print(f"[{index + 1}/{total_switches}] Evaluando {ip}...", end="", flush=True)
        
        # 1. Probar Ping
        estado_ping = str(serv_ping.verificar_ping(ip))
        resultados_ping.append(estado_ping)

        time.sleep(1) # Lo ponemos a domrir un ratito al programa que sino se satura todo

        # 2. Probar SSH (solo si el ping respondió, para no perder tiempo esperando timeouts futiles)
        if estado_ping == "OK":
            estado_ssh = str(serv_SSH.verificar_ssh(ip))
        else:
            estado_ssh = "N/A (Sin Ping)"
        resultados_ssh.append(estado_ssh)
        
        print(f" -> Ping: {estado_ping} | SSH: {estado_ssh}")

    # Agregar las nuevas columnas al contenido del Excel original
    df["Resultado Ping"] = resultados_ping
    df["Resultado SSH"] = resultados_ssh

    # Guardar todo en un Excel nuevo
    df.to_excel(EXCEL_SALIDA, index=False)
    print(f"\n¡Proceso terminado con éxito! Reporte guardado en: {EXCEL_SALIDA}")


if __name__ == "__main__":
    main()
