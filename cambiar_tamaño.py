from PIL import Image
import os

def batch_resize(folder_in, folder_out, width, height):
    for filename in os.listdir(folder_in):
        if filename.endswith(('.jpeg', '.jpg', '.png', '.gif', '.svg')):
            img = Image.open(os.path.join(folder_in, filename))
            img = img.resize((width, height))
            img.save(os.path.join(folder_out, f"resized_{filename}"))
            # print(f'{filename} Redimensionado')

if __name__ == "__main__":
    batch_resize('images', 'images_resized', 800, 600)


# folder_in = r"c:\Users\seiya\Desktop\automatizacion_de_tareas\images"
# filename = "casa - copia (2) copy 2.jpg"
# Image.open(os.path.join(folder_in, filename))