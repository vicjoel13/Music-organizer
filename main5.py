import os
import shutil
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from mutagen.easyid3 import EasyID3
from tqdm import tqdm
import pyautogui

desktop_folder = os.path.expanduser('~/Desktop')
documents_folder = os.path.expanduser('~/Documents')
destination_folder = 'D:\Music'

# Función para mostrar un indicador de progreso
def show_progress(future):
    print('.', end='', flush=True)

# Función para ordenar un archivo mp3 en la carpeta de destino
def sort_mp3_file(file_path, destination_folder):
    mp3 = EasyID3(file_path)
    year = mp3.get('date', [''])[0]
    album = mp3.get('album', ['Unknown Album'])[0]

    year_folder = os.path.join(destination_folder, year)
    album_folder = os.path.join(year_folder, album)

    os.makedirs(year_folder, exist_ok=True)
    os.makedirs(album_folder, exist_ok=True)

    destination = os.path.join(album_folder, os.path.basename(file_path))
    shutil.copy(file_path, destination)

# Función para procesar y ordenar los archivos mp3 de una carpeta fuente
def process_mp3_files(source_folder, destination_folder):
    mp3_files = []
    for directory in [source_folder]:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.mp3'):
                    file_path = os.path.join(root, file)
                    mp3_files.append(file_path)

    with tqdm(total=len(mp3_files), desc='Progress', unit='file') as pbar:
        for file_path in mp3_files:
            sort_mp3_file(file_path, destination_folder)
            pbar.update(1)

# Función para tomar capturas de pantalla y guardarlas en la carpeta de destino
def take_screenshots(dest_folder):
    while True:
        screenshot = pyautogui.screenshot()

        timestamp = time.strftime('%Y%m%d%H%M%S')
        screenshot_name = f'screenshot_{timestamp}.png'
        file_path = os.path.join(dest_folder, screenshot_name)
        screenshot.save(file_path)

        if stop_thread:
            break

stop_thread = True
screenshot_thread = threading.Thread(target=take_screenshots, args=(destination_folder,))
screenshot_thread.start()

# Ordenar archivos mp3 en la carpeta de escritorio y documentos
process_mp3_files(desktop_folder, destination_folder)
process_mp3_files(documents_folder, destination_folder)

stop_thread = False
screenshot_thread.join()