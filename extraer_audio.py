import os
from moviepy import VideoFileClip

# Carpetas de entrada y salida
# input_folder = "videos"
# output_folder = "audios"

def extraer_audio(input_folder, output_folder, progress_callback=None):

    os.makedirs(output_folder, exist_ok=True)

    videos = [f for f in os.listdir(input_folder) if f.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.wmv', '.mpeg'))]
    total_videos = len(videos)

    # Procesar cada archivo en la carpeta de entrada
    # for index, filename in os.listdir(input_folder):
    for index, filename in enumerate(videos, 1):
        input_path = os.path.join(input_folder, filename)

        if os.path.isfile(input_path):  # Comprobar que la ruta tenga un archivo
            try:
                # Llamar al callback de progreso, si está definido
                if progress_callback:
                    progress_callback(index, total_videos, filename)
                print(f"Procesando: {filename}")
                # Cargar el archivo de video
                video_clip = VideoFileClip(input_path)
                # Obtener la ruta de salida del audio
                audio_output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.mp3')
                # Extraer el audio y guardarlo
                video_clip.audio.write_audiofile(audio_output_path)
                # Cerrar el clip
                video_clip.close()
                print(f"Audio extraído: {audio_output_path}")

            except Exception as e:
                print(f"Error al procesar {filename}: {e}")

    print("Extracción masiva de audios completada.")