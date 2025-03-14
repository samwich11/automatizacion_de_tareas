import os
from PIL import Image

def convertir_imagen(ruta_entrada, formato_salida):
    """
    Convierte una imagen al formato especificado.

    Args:
        ruta_entrada (str): Ruta del archivo de imagen original
        formato_salida (str): Formato deseado (por ejemplo: 'PNG', 'JPEG', 'WEBP)
    """
    try:
        # Obtener el nombre del archivo sin la extensión
        nombre_base = os.path.splitext(ruta_entrada)[0]
        
        # Abrir la imagen
        with Image.open(ruta_entrada) as img:
            # Si la imagen está en modo RGBA y convertimos a JPEG, convertir a RGB
            if img.mode in ('RGBA', 'LA') and formato_salida.upper() == 'JPEG':
                img = img.convert('RGB')
            
            # Crear el nombre del archivo de salida
            ruta_salida = f"{nombre_base}.{formato_salida.lower()}"

            # Guarda la imagen en el nuevo formato
            img.save(ruta_salida, formato_salida.upper())
            print(f"Imagen convertida exitosamente: {ruta_salida}")
    except Exception as e:
        print(f"Error al convertir la imagen: {str(e)}")


# nombre_archivo = os.path.splitext(image)[0]
# print(nombre_archivo)
# image = "images/casa - copia (2) copy 2.gif"
# convertir_imagen(image, "PNG")
# convertir_imagen(image, "bmp")