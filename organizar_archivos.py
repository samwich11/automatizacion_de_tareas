import os
import shutil

def organize_folder(folder):
    file_types = {
        'Imágenes': ['.jpeg', '.jpg', '.png', '.gif', '.svg'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.mpeg'],
        'Documentos': ['.pdf', '.docx', '.txt', '.doc', '.md', '.rtf'],
        'Datasets': ['.xlsx', '.xls','.csv', '.sav', '.dat', '.raw', '.json', '.xml'],
        'Comprimidos': ['.zip', '.rar', '.7z', '.rar5'],
        'Diapositivas': ['.pptx', '.ppt']
    }
    # Bucle que itera entre todos los archivos y carpetas de una misma carpeta, pero no dentro de las carpetas dentro de la carpeta
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            for folder_name, extensions in file_types.items():
                if ext in extensions:
                    target_folder = os.path.join(folder, folder_name)
                    os.makedirs(target_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(target_folder, filename))
                    print(f'Archivo {filename} movido a {folder_name}')

# organize_folder('archivos')
