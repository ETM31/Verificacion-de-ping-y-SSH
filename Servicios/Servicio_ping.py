"""Este archivo lo que hace es contener la funcion que realiza el ping al dispositivo"""


import os

class Servicioping:
    def __init__(self):
        pass

    def verificar_ping(self, ip):
        """Realiza un ping nativo en Windows de 1 solo paquete."""
        # En Windows usamos '-n 1'. Redirigimos la salida a NUL para mantener limpia la consola.
        comando = f"ping -n 1 {ip} > NUL 2>&1"
        respuesta = os.system(comando)
        # os.system devuelve 0 si el comando fue exitoso (hubo respuesta)
        return "OK" if respuesta == 0 else "FALLÓ"
