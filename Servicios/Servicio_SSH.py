"""Este archivo lo que hace es contener la funcion que realiza la verificación de acceso por SSH"""

import os
import paramiko

class ServicioSSH:

    def __init__(self, user, password):
        self.ssh_user = user
        self.ssh_password = password
        self.ssh_timeout = 50

    def verificar_ssh(self, ip):
        """Intenta abrir una conexión SSH básica para validar el acceso."""
        ssh = paramiko.SSHClient()
        # Esta línea evita el error de llave desconocida del switch
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            # Intentamos conectar. Si conecta bien, el puerto está abierto.
            ssh.connect(
                ip, 
                username=self.ssh_user, 
                password=self.ssh_password, 
                timeout= self.ssh_timeout, 
                look_for_keys=False, 
                allow_agent=False
                )
            ssh.close()
            return "ACCESO OK"
        except paramiko.AuthenticationException:
            # Si el switch responde pero rechaza la contraseña, ¡el SSH está activo y accesible!
            return "SSH ACTIVO credenciales erroneas"
        except Exception:
            # Si da timeout, conexión rechazada o red inalcanzable
            return "SIN ACCESO SSH o TIMEOUT ALCANZADO"