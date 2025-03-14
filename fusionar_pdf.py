import os
from PyPDF2 import PdfMerger
from pathlib import Path

def fusionar_pdf(carpeta_entrada, archivo_salida='pdfs_fusionados.pdf'):
    """
    Fusiona todos los archivos PDF en una carpeta específica

    Args:
        carpeta_entrada (str): Ruta de la carpeta que contiene los PDF
        archivo_salida (str): Nombre del archivo PDF de salida
    """
    try:
        # Crear el merger
        merger = PdfMerger()
        #Verificar si la carpeta existe
        if not os.path.exists(carpeta_entrada):
            print(f"La carpeta {carpeta_entrada} no existe")
            return
        # Obtener todos los PDF de la carpeta
        pdfs = [f for f in Path(carpeta_entrada).glob('*.pdf')]
        if not pdfs:
            print(f"No se encontraron archivos PDF en la carpeta {carpeta_entrada}")
            return
        print(f"Se encontraron {len(pdfs)} archivos PDF")
        # Agregar cada PDF al merger
        for pdf in pdfs:
            print(f"Agregando: {pdf.name}")
            merger.append(str(pdf))
        # Guardar el PDF fusionado
        merger.write(archivo_salida)
        merger.close()
        print(f"\nPDFs fusionados exitosamente en: {archivo_salida}")
    except Exception as e:
        print(f"Error al fusionar los PDFs: {str(e)}")

if __name__ == '__main__':
    ruta = r"C:\Users\seiya\Desktop\automatizacion_de_tareas\pdf"
    fusionar_pdf(ruta)