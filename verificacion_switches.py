import os
import platform
import pandas as pd
import paramiko

# --- CONFIGURACIÓN ---
EXCEL_ENTRADA = "CEDIS Obregón Inventario WAN-LAN-WLAN.xlsx"  # Cambia esto por el nombre exacto de tu archivo
EXCEL_SALIDA = "reporte_switches.xlsx"
TIMEOUT_SSH = 50  # Segundos de espera para el SSH antes de darlo por muerto

# Credenciales temporales para la prueba de acceso SSH
SSH_USER = "***ELIMINADO***"
SSH_PASSWORD = "***ELIMINADO***"


def verificar_ping(ip):
    """Realiza un ping nativo en Windows de 1 solo paquete."""
    # En Windows usamos '-n 1'. Redirigimos la salida a NUL para mantener limpia la consola.
    comando = f"ping -n 1 {ip} > NUL 2>&1"
    respuesta = os.system(comando)
    
    # os.system devuelve 0 si el comando fue exitoso (hubo respuesta)
    return "OK" if respuesta == 0 else "FALLÓ"


def verificar_ssh(ip, user, password):
    """Intenta abrir una conexión SSH básica para validar el acceso."""
    ssh = paramiko.SSHClient()
    # Esta línea evita el error de llave desconocida del switch
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # Intentamos conectar. Si conecta bien, el puerto está abierto.
        ssh.connect(ip, username=user, password=password, timeout=TIMEOUT_SSH)
        ssh.close()
        return "ACCESO OK"
    except paramiko.AuthenticationException:
        # Si el switch responde pero rechaza la contraseña, ¡el SSH está activo y accesible!
        return "SSH ACTIVO (Error Auth)"
    except Exception:
        # Si da timeout, conexión rechazada o red inalcanzable
        return "SIN ACCESO SSH o TIMEOUT ALCANZADO"


def main():
    print("Cargando archivo de Excel...")
    try:
        df = pd.read_excel(EXCEL_ENTRADA)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{EXCEL_ENTRADA}' en esta carpeta.")
        return

    # Verificar que exista la columna llamada IP
    if "Direccion IP" not in df.columns:
        print("Error: Tu Excel debe tener una columna llamada exactamente 'Direccion IP'.")
        return

    resultados_ping = []
    resultados_ssh = []

    total_switches = len(df)
    print(f"Iniciando escaneo de {total_switches} dispositivos...")

    for index, fila in df.iterrows():
        ip = str(fila["Direccion IP"]).strip()
        print(f"[{index + 1}/{total_switches}] Evaluando {ip}...", end="", flush=True)

        # 1. Probar Ping
        estado_ping = verificar_ping(ip)
        resultados_ping.append(estado_ping)

        # 2. Probar SSH (solo si el ping respondió, para no perder tiempo esperando timeouts futiles)
        if estado_ping == "OK":
            estado_ssh = verificar_ssh(ip, SSH_USER, SSH_PASSWORD)
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