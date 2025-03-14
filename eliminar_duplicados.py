import os
import hashlib

def hash_file(filename):
    h = hashlib.md5()
    with open(filename, 'rb') as file:
        while chunk := file.read(8192): # equivale a 8 KB
            h.update(chunk)
    return h.hexdigest()    # Devuelve el hash en hexadecimal (32 caracteres)

def find_duplicates(folder):
    hashes = {}
    duplicates = []
    for dirpath, _, filenames in os.walk(folder):
        # print(filenames)  # Para ver los nombres de los archivos
        # print(dirpath)    # Para ver los nombres de las carpetas, en este caso la carpeta raíz
        for f in filenames:
            full_path = os.path.join(dirpath, f)
            file_hash = hash_file(full_path)
            # print(full_path)
            # print(file_hash)
            if file_hash in hashes:
                # print(f"Se encontraron duplicados: {full_path} = {hashes[file_hash]}")
                # delete = input(f"¿Quieres eliminar el archivo duplicado {full_path}? (s/n): ").strip().lower()
                duplicates.append((full_path, hashes[file_hash])) # Agrega los duplicados a la lista, se utiliza en la aplicación en Flet
                # if delete == "s":
                #     os.remove(full_path)
                #     print(f"Archivo {full_path} eliminado.")
                # else:
                #     print(f"Archivo {full_path} no eliminado.")
            else:
                hashes[file_hash] = full_path
    return duplicates

def delete_file(filepath):
    try:
        os.remove(filepath)
        return True
    except Exception as e:
        return False
    
# def handle_folder_picker(e: ft.FilePickerResultEvent):  # Evento seleccionar carpeta
#         if e.path:
#             selected_dir_text.value = f"Carpeta seleccionada: {e.path}"
#             selected_dir_text.update()

find_duplicates("archivos")






"""
archivo = "archivos/casa.jpg"
print(hash_file(archivo))
archivo = "archivos/foto1.png"
print(hash_file(archivo))
archivo = "archivos/foto1 - copia.png"
print(hash_file(archivo))
archivo = "archivos/Wallpaper 3 - copia.jpg"
print(hash_file(archivo))
archivo = "archivos/Wallpaper 3.jpg"
print(hash_file(archivo))
archivo = "archivos/duplicado.txt"
print(hash_file(archivo))
archivo = "archivos/este es un texto - copia.txt"
print(hash_file(archivo))
archivo = "archivos/este es un texto - copia (2).txt"
print(hash_file(archivo))
archivo = "archivos/este es un texto.txt"
print(hash_file(archivo))
archivo = "archivos/otro texto.txt"
print(hash_file(archivo))
"""