import flet as ft
from eliminar_duplicados import find_duplicates, delete_file
from organizar_archivos import organize_folder
from cambiar_tamaño import batch_resize
from convertidor_imagenes import convertir_imagen
from extraer_audio import extraer_audio
from fusionar_pdf import fusionar_pdf
from cambiar_nombre import cambiar_nombre
import os

def main(page: ft.Page):
    # Configuración de la ventana
    page.title = "Automatización de Tareas"
    page.window.width = 1000
    page.window.height = 700
    page.padding = 0
    page.bgcolor = ft.Colors.SURFACE_CONTAINER_HIGHEST
    page.theme_mode = ft.ThemeMode.DARK

    # Agregar tema personalizado
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE,
        visual_density=ft.VisualDensity.COMFORTABLE,
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.BLUE,
            secondary=ft.Colors.ORANGE,
            background=ft.Colors.GREY_900,
            surface=ft.Colors.GREY_800  # Todo lo que esté por encima del background
        )
    )

    # Variables de estado
    state = {
        "current_duplicates": [],
        "current_view": "duplicates",
        "resize_input_folder": "",          # Carpeta de estado de entrada
        "resize_output_folder": "",         # Carpeta de estado de salida
        "selecting_resize_output": False,
        "convert_input_file": "",
        "audio_input_folder": "",
        "audio_extraction_progress": 0,
        "total_videos": 0,
        "current_video": "",
        "pdf_input_folder": "",
        "rename_input_folder": "",
        "rename_option": "",
        "rename_value": ""
    }

    # Controles para la vista de eliminar duplicados
    selected_dir_text = ft.Text(
        value="No se ha seleccionado niguna carpeta",
        size=14,
        color=ft.Colors.BLUE_200,
    )
    result_text = ft.Text(size=14, weight=ft.FontWeight.BOLD)   # Inicialmente está vacío

    duplicates_list = ft.ListView(
        expand=1,
        spacing=10,
        height=200,
    )

    delete_all_button = ft.ElevatedButton(
        text="Eliminar todos los duplicados",
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.RED_900,
        icon=ft.Icons.DELETE_SWEEP,
        icon_color=ft.Colors.WHITE,
        visible=False,
        on_click=lambda e: delete_all_duplicates()
    )

    # Controles para la vista de organizar archivos
    organize_dir_text = ft.Text(
        value="No se ha seleccionado ninguna carpeta",
        size=14,
        color=ft.Colors.BLUE_200
    )
    organize_result_text = ft.Text(size=14, weight=ft.FontWeight.BOLD)

    # Controles para la vista de redimensionar imágenes
    resize_input_text = ft.Text(
        value="Carpeta de entrada: No seleccionada",
        size=14,
        color=ft.Colors.BLUE_200
    )
    resize_output_text = ft.Text(
        value="Carpeta de salida: No seleccionada",
        size=14,
        color=ft.Colors.BLUE_200
    )

    resize_result_text = ft.Text(size=14, weight=ft.FontWeight.BOLD)    # Inicialmente está vacío

    width_field = ft.TextField(
        label="Ancho",
        value=800,
        width=100,
        text_align=ft.TextAlign.RIGHT,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    height_field = ft.TextField(
        label="Alto",
        value=600,
        width=100,
        text_align=ft.TextAlign.RIGHT,
        keyboard_type=ft.KeyboardType.NUMBER
    )

    # Controles para la vista de convertir imágenes
    convert_input_text = ft.Text(
        value="No se ha seleccionado ninguna imagen",
        size=14,
        color=ft.Colors.BLUE_200
    )

    convert_result_text = ft.Text(size=14, weight=ft.FontWeight.BOLD)    # Inicialmente está vacío
    format_dropdown = ft.Dropdown(
        label="Formato de salida",
        width=200,
        options=[
            ft.dropdown.Option("PNG"),
            ft.dropdown.Option("JPEG"),
            ft.dropdown.Option("WEBP"),
            ft.dropdown.Option("BMP"),
            ft.dropdown.Option("GIF"),
        ],
        value="PNG"
    )

    # Controles para la vista de extracción de audio
    audio_input_text = ft.Text(
        value="No se ha seleccionado ninguna carpeta",
        size=14,
        color=ft.Colors.BLUE_200
    )

    audio_result_text = ft.Text(size=14, weight=ft.FontWeight.BOLD)    # Inicialmente está vacío
    audio_progress = ft.ProgressBar(width=400, visible=False)
    current_video_text = ft.Text(size=14, weight=ft.FontWeight.BOLD)

    def extract_audio():
        try:
            if not state["audio_input_folder"]:
                audio_result_text.value = "Error: Seleccione una carpeta con videos"
                audio_result_text.color = ft.Colors.RED_400
                audio_result_text.update()
                return
            
            # Crear la carpeta de audios si no existe
            input_folder = state["audio_input_folder"]
            output_folder = os.path.join(input_folder, "audios")
            os.makedirs(output_folder, exist_ok=True)

            audio_progress.value = 0
            audio_progress.visible = True
            audio_progress.update()

            def progress_callback(current, total, archivo):     # 2:35:50
                progress = current / total
                audio_progress.value = progress
                audio_progress.update()
                current_video_text.value = f"Procesando {archivo}: {current}/{total}"
                current_video_text.update()

            # Llamar a la función extraer_audio con el callback de progreso
            extraer_audio(input_folder, output_folder, progress_callback)

            audio_result_text.value = "Extracción completada. Los archivos de audio se guardaron en la carpeta 'audios'."
            audio_result_text.color = ft.Colors.GREEN_400
            current_video_text.value = "Proceso finalizado"
            
        except Exception as e:
            audio_result_text.value = f"Error durante la extracción: {str(e)}"
            audio_result_text.color = ft.Colors.RED_400
        finally:
            audio_progress.visible = False  # Ocultar la barra de progrso la finalizar
            audio_progress.update()

        audio_result_text.update()
        current_video_text.update()

    #Controles para la vista de fusión de PDFs
    pdf_input_text = ft.Text(
        value="No se ha seleccionado ninguna carpeta",
        size=14,
        color=ft.Colors.BLUE_200
    )
    pdf_result_text = ft.Text(size=14, weight=ft.FontWeight.BOLD)

    def merge_pdfs():
        try:
            if not state["pdf_input_folder"]:
                pdf_result_text.value = "Error: Seleccione una carpeta con PDFs"
                pdf_result_text.color = ft.Colors.RED_400
                pdf_result_text.update()
                return
            
            output_file = os.path.join(state["pdf_input_folder"], "pdf_fusionados.pdf")
            fusionar_pdf(state["pdf_input_folder"], output_file)
            pdf_result_text.value = f"PDFs fusionados exitosamente en: {output_file}"
            pdf_result_text.color = ft.Colors.GREEN_400
            pdf_result_text.update()
        except Exception as e:
            pdf_result_text.value = f"Error durante la fusión: {str(e)}"
            pdf_result_text.color = ft.Colors.RED_400
            pdf_result_text.update()

    # Controles para la vista de renombrar archivos
    rename_input_text = ft.Text(
        value="Carpeta de entrada: No seleccionada",
        size=14,
        color=ft.Colors.BLUE_200
    )

    def on_rename_option_change(e):
        is_cambiar = e.control.value.lower() == "cambiar"
        rename_search_text.visible = is_cambiar
        rename_replace_text.visible = is_cambiar
        rename_prefix_text.visible = not is_cambiar
        rename_search_text.update()
        rename_replace_text.update()
        rename_prefix_text.update()

    rename_option_dropdown = ft.Dropdown(
            label="Opción de renombrado",
            options=[
                ft.dropdown.Option("Cambiar"),
                ft.dropdown.Option("Prefijo")
            ],
            value="cambiar",
            on_change=on_rename_option_change,
            # width=page.width
            width=400,
        # expand=True
    )

    rename_search_text = ft.TextField(
        label="Palabra a buscar",
        width=200,
        visible=True
    )

    rename_replace_text = ft.TextField(
        label="Reemplazar por",
        width=200,
        visible=True
    )

    rename_prefix_text = ft.TextField(
        label="Prefijo a agregar",
        width=200,
        visible=False
    )

    rename_result_text = ft.Text(size=14, weight=ft.FontWeight.BOLD)

    def rename_files():
        try:
            if not state["rename_input_folder"]:
                rename_result_text.value = "Error: Seleccione una carpeta"
                rename_result_text.color = ft.Colors.RED_400
                rename_result_text.update()
                return
            
            option = rename_option_dropdown.value.lower()
            # option = rename_option_dropdown.value
            
            if option == "cambiar":
                if not rename_search_text.value:
                    rename_result_text.value = "Error: Ingrese la palabra a buscar"
                    rename_result_text.color = ft.Colors.RED_400
                    rename_result_text.update()
                    return 
                value = [rename_search_text.value, rename_replace_text.value]
            else:
                if not rename_prefix_text.value:
                    rename_result_text.value = "Error: Ingrese el prefijo"
                    rename_result_text.color = ft.Colors.RED_400
                    rename_result_text.update()
                    return
                value = rename_prefix_text.value

            cambiar_nombre(state["rename_input_folder"], option, value)
            rename_result_text.value = "Archivos renombrados exitosamente"
            rename_result_text.color = ft.Colors.GREEN_400
            rename_result_text.update()

        except Exception as e:
            rename_result_text.value = f"Error al renombrar: {str(e)}"
            rename_result_text.color = ft.Colors.RED_400
            rename_result_text.update()

    def change_view(e):
        selected = e.control.selected_index
        if selected == 0:
            state["current_view"] = "duplicates"
            content_area.content = duplicate_files_view
        elif selected == 1:
            state["current_view"] = "organize"
            content_area.content = organize_files_view
        elif selected == 2:
            state["current_view"] = "resize"
            content_area.content = resize_files_view
        elif selected == 3:
            state["current_view"] = "convert"
            content_area.content = convert_images_view
        elif selected == 4:
            state["current_view"] = "audio"
            content_area.content = extract_audio_view
        elif selected == 5:
            state["current_view"] = "merge_pdfs"
            content_area.content = merge_pdfs_view
        elif selected == 6:
            state["current_view"] = "rename"
            content_area.content = rename_files_view
        elif selected == 7:
            state["current_view"] = "coming_soon"
            content_area.content = ft.Text(value="Próximamente...", size=24)
        content_area.update()

    def handle_file_picker(e: ft.FilePickerResultEvent):    # Evento para seleccionar archivo
        if e.files and len(e.files) > 0:
            file_path = e.files[0].path
            state["convert_input_file"] = file_path
            convert_input_text.value = f"Imagen seleccionada: {file_path}"
            convert_input_text.update()

    def handle_folder_picker(e: ft.FilePickerResultEvent):  # Evento para seleccionar carpeta
        if e.path:
            if state["current_view"] == "duplicates":
                selected_dir_text.value = f"Carpeta seleccionada: {e.path}"
                selected_dir_text.update()
                scan_directory(e.path)
            elif state["current_view"] == "organize":
                organize_dir_text.value = f"Carpeta seleccionada: {e.path}"
                organize_dir_text.update()
                organize_directory(e.path)
            elif state["current_view"] == "resize":
                if state["selecting_resize_output"]:
                    state["resize_output_folder"] = e.path
                    resize_output_text.value = f"Carpeta de salida: {e.path}"
                    resize_output_text.update()
                else:
                    state["resize_input_folder"] = e.path
                    resize_input_text.value = f"Carpeta de entrada: {e.path}"
                    resize_input_text.update()
            elif state["current_view"] == "audio":
                state["audio_input_folder"] = e.path
                audio_input_text.value = f"Carpeta seleccionada: {e.path}"
                audio_input_text.update()
            elif state["current_view"] == "merge_pdfs":
                state["pdf_input_folder"] = e.path
                pdf_input_text.value = f"Carpeta seleccionada: {e.path}"
                pdf_input_text.update()
            elif state["current_view"] == "rename":
                state["rename_input_folder"] = e.path
                rename_input_text.value = f"Carpeta seleccionada: {e.path}"
                rename_input_text.update()
    
    def select_input_folder():
        state["selecting_resize_output"] = False
        folder_picker.get_directory_path()
    
    def select_output_folder():
        state["selecting_resize_output"] = True
        folder_picker.get_directory_path()

    def convert_image():
        try:
            if not state["convert_input_file"]:
                convert_result_text.value = "Error: Seleccione una imagen"
                convert_result_text.color = ft.Colors.RED_400
                convert_result_text.update()
                return
            if not format_dropdown.value:
                convert_result_text.value = "Error: Selecciona un formato de salida"
                convert_result_text.color = ft.Colors.RED_400
                convert_result_text.update()
                return
            convertir_imagen(state["convert_input_file"], format_dropdown.value)
            convert_result_text.value = "Imagen convertida exitosamente"
            convert_result_text.color = ft.Colors.GREEN_400
            convert_result_text.update()

        except Exception as e:
            convert_result_text.value = f"Error al convertir la imagen: {str(e)}"
            convert_result_text.color = ft.Colors.RED_400
            convert_result_text.update()

    def resize_images():
        try:
            if not state["resize_input_folder"] or not state["resize_output_folder"]:
                resize_result_text.value = "Error: Selecciona las carpetas de entrada y salida"
                resize_result_text.color = ft.Colors.RED_400
                resize_result_text.update()
                return

            width = int(width_field.value)
            height = int(height_field.value)

            if width <= 0 or height <= 0:
                resize_result_text.value = "Error: Las dimensiones deben ser mayores a 0"
                resize_result_text.color = ft.Colors.RED_400
                resize_result_text.update()
                return
            
            batch_resize(state["resize_input_folder"], state["resize_output_folder"], width, height)
            resize_result_text.value = "Imágenes redimensionadas exitosamente"
            resize_result_text.color = ft.Colors.GREEN_400
            resize_result_text.update()
            
        except ValueError:
            resize_result_text.value = "Error: Ingresa dimensiones válidas"
            resize_result_text.color = ft.Colors.RED_400
            resize_result_text.update()
        except Exception as e:
            resize_result_text.value = f"Error al redimensionar: {str(e)}"
            resize_result_text.color = ft.Colors.RED_400
            resize_result_text.update()
    
    def organize_directory(directory):
        try:
            organize_folder(directory)
            organize_result_text.value = "Archivos organizados exitosamente"
            organize_result_text.color = ft.Colors.GREEN_400
        except Exception as e:
            organize_result_text.value = f"Error al organizar los archivos: {str(e)}"
            organize_result_text.color = ft.Colors.RED_400
        organize_result_text.update()

    def scan_directory(directory):
        duplicates_list.controls.clear()
        state["current_duplicates"] = find_duplicates(directory)

        if not state["current_duplicates"]:
            result_text.value = "No se encontraron duplicados"
            result_text.color = ft.Colors.GREEN_400
            delete_all_button.visible = False
        else:
            result_text.value = f"Se encontraron {len(state['current_duplicates'])} archivos duplicados"
            result_text.color = ft.Colors.ORANGE_400
            delete_all_button.visible = True

            for dup_file, original in state["current_duplicates"]:
                dup_row = ft.Row([
                    ft.Text(
                        value=f"Duplicado: {dup_file}\nOriginal: {original}",
                        size=12,
                        expand=True,
                        color=ft.Colors.BLUE_200,
                    ),
                    ft.ElevatedButton(
                        text="Eliminar",
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.RED_900,
                        on_click=lambda e, path = dup_file: delete_duplicate(path)
                    ),
                ])
                duplicates_list.controls.append(dup_row)
        duplicates_list.update()
        result_text.update()
        delete_all_button.update()

    def delete_duplicate(filepath):
        if delete_file(filepath):
            result_text.value = f"Archivo eliminado: {filepath}"
            result_text.color = ft.Colors.GREEN_400
            for control in duplicates_list.controls[:]:
                if filepath in control.controls[0].value:
                    duplicates_list.controls.remove(control)
            state["current_duplicates"] = [(dup, orig) for dup, orig in state["current_duplicates"] if dup != filepath]
            if not state["current_duplicates"]:
                delete_all_button.visible = False
        else:
            result_text.value = f"Error al eliminar: {filepath}"
            result_text.color = ft.Colors.RED_400

        duplicates_list.update()
        result_text.update()
        delete_all_button.update()

    def delete_all_duplicates():
        deleted_count = 0
        failed_count = 0

        for dup_file, _ in state["current_duplicates"][:]:
            if delete_file(dup_file):
                deleted_count += 1
            else:
                failed_count += 1
        
        duplicates_list.controls.clear()
        state["current_duplicates"] = []
        delete_all_button.visible = False

        if failed_count == 0:
            result_text.value = f"Se eliminaron exitosamente {deleted_count} archivos duplicados."
            result_text.color = ft.Colors.GREEN_400
        else:
            result_text.value = f"Se eliminaron {deleted_count} archivos. Fallaron {failed_count} archivos."
            result_text.color = ft.Colors.RED_400
        
        duplicates_list.update()
        result_text.update()
        delete_all_button.update()

    # Configurar los selectores de archivos
    file_picker = ft.FilePicker(
        on_result=handle_file_picker
    )
    file_picker.file_type = ft.FilePickerFileType.IMAGE
    file_picker.allowed_extensions = ["png", "jpg", "jpeg", "gif", "bmp", "webp"]



    # Configurar el selector de carpetas
    folder_picker = ft.FilePicker(on_result=handle_folder_picker)
    page.overlay.extend([folder_picker, file_picker])  # Para que se muestre sobre la ventana principal de Flet

    # Vista de archivos duplicados
    duplicate_files_view = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(
                    value="Eliminar Archivos Duplicados",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_200
                ),
                margin=ft.margin.only(bottom=20)
            ),
            ft.Row([
                ft.ElevatedButton(
                text="Seleccionar Carpeta",
                icon=ft.Icons.FOLDER_OPEN,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_900,
                on_click=lambda _: folder_picker.get_directory_path()
            ),
            delete_all_button,
            ]),
            ft.Container(
                content=selected_dir_text,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            result_text,
            ft.Container(
                content=duplicates_list,
                border=ft.border.all(2, ft.Colors.BLUE_400),
                border_radius=10,
                padding=20,
                margin=ft.margin.only(top=10),
                bgcolor=ft.Colors.GREY_800,
                expand=True,
            )
        ]),
        padding=30,
        expand=True,
    )

    # Vista de organizar archivos
    organize_files_view = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(
                    value="Organizar Archivos por Tipo",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_200
                ),
                margin=ft.margin.only(bottom=20)
            ),
            ft.ElevatedButton(
                text="Seleccionar Carpeta",
                icon=ft.Icons.FOLDER_OPEN,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_900,
                on_click=lambda _: folder_picker.get_directory_path()
            ),
            ft.Container(
                content=organize_dir_text,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            organize_result_text,
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        value="Los archivos serán organizados en las siguientes carpetas:",
                        size=14,
                        color=ft.Colors.BLUE_200
                    ),
                    ft.Text(value="  • Imágenes (.jpeg, .jpg, .png, .gif, .svg)", size=14),
                    ft.Text(value="  • Videos (.mp4, .avi, .mkv, .mov, .wmv, .mpeg)", size=14),
                    ft.Text(value="  • Documentos (.pdf, .docx, .txt, .doc, .md, .rtf)", size=14),
                    ft.Text(value="  • Diapositivas (.pptx, .ppt)", size=14),
                    ft.Text(value="  • Datasets (.xlsx, .xls,.csv, .sav, .dat, .raw, .json, .xml)", size=14),
                    ft.Text(value="  • Comprimidos (.zip, .rar, .7z, .rar5)", size=14),
                ]),
                border=ft.border.all(2, ft.Colors.BLUE_400),
                border_radius=10,
                padding=20,
                margin=ft.margin.only(top=10),
                bgcolor=ft.Colors.GREY_800,
            )
        ]),
        padding=30, 
        expand=True
    )

    # Vista de redimensionar archivos
    resize_files_view = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(
                    value="Redimensionar Imágenes",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_200
                ),
                margin=ft.margin.only(bottom=20)
            ),
            ft.Row([
                ft.ElevatedButton(
                    text="Seleccionar carpeta de entrada",
                    icon=ft.Icons.FOLDER_OPEN,
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.BLUE_900,
                    on_click=lambda _: select_input_folder()
                ),
                ft.ElevatedButton(
                    text="Seleccionar carpeta de salida",
                    icon=ft.Icons.FOLDER_OPEN,
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.BLUE_900,
                    on_click=lambda _: select_output_folder()
                ),
            ]),
            ft.Container(
                content=ft.Column([
                    resize_input_text,
                    resize_output_text,
                ]),
                margin=ft.margin.only(top=10, bottom=10)
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        value="Dimensiones de la imagen:",
                        size=14,
                        color=ft.Colors.BLUE_200
                    ),
                    ft.Row([
                        width_field,
                        ft.Text(value="x", size=20),
                        height_field,
                        ft.Text(value="pixeles", size=14),
                    ]),
                ]),
                margin=ft.margin.only(bottom=10)
            ),
            ft.ElevatedButton(
                text="Redimensionar Imágenes",
                icon=ft.Icons.PHOTO_SIZE_SELECT_LARGE,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_900,
                on_click=lambda _: resize_images()
            ),
            resize_result_text,
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        value="Información",
                        size=14,
                        color=ft.Colors.BLUE_200
                    ),
                    ft.Text(value="  • Se procesarán los archivos .jpeg, .jpg, .png, .gif, .svg", size=14),
                    ft.Text(value="  • Las imágenes originales no serán modificadas", size=14),
                    ft.Text(value="  • Las imágenes redimensionadas se guardarán en la carpeta de salida con el prefijo 'resized_'", size=14),
                ]),
                border=ft.border.all(2, ft.Colors.BLUE_200),
                border_radius=10,
                padding=20,
                margin=ft.margin.only(top=10),
                bgcolor=ft.Colors.GREY_800,
            )
        ]),
        padding=30,
        expand=True,
    )

    content_area = ft.Container(
        content=duplicate_files_view,
        expand=True,
    )

    # Vista de convertir imágenes
    convert_images_view = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(
                    "Convertir Formato de Imagen",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_200,
                ),
                margin=ft.margin.only(bottom=20)
            ),
            ft.ElevatedButton(
                text="Seleccionar Imagen",
                icon=ft.Icons.FOLDER_OPEN,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_900,
                on_click=lambda _: file_picker.pick_files() 
            ),
            ft.Container(
                content=convert_input_text,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            format_dropdown,
            ft.Container(
                margin=ft.margin.only(top=10),
                content=ft.ElevatedButton(
                    text="Convertir Imagen",
                    icon=ft.Icons.TRANSFORM,
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.BLUE_900,
                    on_click=lambda _: convert_image()
                ),
            ),
            convert_result_text,
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        value="Información:",
                        size=14,
                        color=ft.Colors.BLUE_200
                    ),
                    ft.Text(value="  • Formatos soportados: PNG, JPEG,WEBP, BMP, GIF", size=14),
                    ft.Text(value="  • La imagen original no será modificada", size=14),
                    ft.Text(value="  • La imagen convertida se guardará en la misma carpeta", size=14),
                    ft.Text(value="  • Al convertir a JPEG, las imágenes con transparencia se convertirán a fondo blanco", size=14),
                ]),
                border=ft.border.all(2, ft.Colors.BLUE_200),
                border_radius=10,
                padding=20,
                margin=ft.margin.only(top=10),
                bgcolor=ft.Colors.GREY_800
            )
        ]),
        padding=30,
        expand=True
    )

    # Vista de extracción de audio
    extract_audio_view = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(
                    value="Extraer Audio de Videos",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_200,
                ),
                margin=ft.margin.only(bottom=20)
            ),
            ft.ElevatedButton(
                text="Seleccionar Carpeta con Videos",
                icon=ft.Icons.FOLDER_OPEN,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_900,
                on_click=lambda _: folder_picker.get_directory_path()
            ),
            ft.Container(
                content=audio_input_text,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            ft.ElevatedButton(
                text="Extraer Audio",
                icon=ft.Icons.AUDIOTRACK,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_900,
                on_click=lambda _: extract_audio()
            ),
            current_video_text,
            audio_progress,
            audio_result_text,
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        value="Información:",
                        size=14,
                        color=ft.Colors.BLUE_200
                    ),
                    ft.Text(value="  • Formatos soportados: MP4, AVI, MKV, MOV", size=14),
                    ft.Text(value="  • Los archivos de audio se extraerán en formato MP3", size=14),
                    ft.Text(value="  • Los audios extraídos se guardarán en una carpeta 'audios dentro de la carpeta seleccionada", size=14),
                    ft.Text(value="  • Los archivos de video originales no serán modificados", size=14),
                ]),
                border=ft.border.all(2, ft.Colors.BLUE_400),
                border_radius=10,
                padding=20,
                margin=ft.margin.only(top=10),
                bgcolor=ft.Colors.GREY_800
            )
        ]),
        padding=30, 
        expand=True
    )

    # Vista  de fusión de PDFs
    merge_pdfs_view = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text(
                    value="Fusionar Archivos PDF",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_200
                ),
                margin=ft.margin.only(bottom=20)
            ),
            ft.ElevatedButton(
                text="Seleccionar Carpeta con PDFs",
                icon=ft.Icons.FOLDER_OPEN,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_900,
                on_click=lambda _: folder_picker.get_directory_path()
            ),
            ft.Container(
                content=pdf_input_text,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            ft.ElevatedButton(
                text="Fusionar PDFs",
                icon=ft.Icons.MERGE_TYPE,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_900,
                on_click=lambda _: merge_pdfs()
            ),
            pdf_result_text,
        ]),
        padding=30,
        expand=True 
    )

    # Vista de renombrar archivos
    rename_files_view = ft.Container(
        ft.Column([
            ft.Container(
                content=ft.Text(
                    value="Renombrar Archivos",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_200
                ),
                margin=ft.margin.only(bottom=20)
            ),
            ft.ElevatedButton(
                text="Seleccionar Carpeta",
                icon=ft.Icons.FOLDER_OPEN,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_900,
                on_click=lambda _: folder_picker.get_directory_path()
            ),
            ft.Container(
                content=rename_input_text,
                margin=ft.margin.only(top=10, bottom=10)
            ),
            ft.Container(
                content=ft.Column([
                    rename_option_dropdown,
                    rename_search_text,
                    rename_replace_text,
                    rename_prefix_text
                ]),
                margin=ft.margin.only(top=10, bottom=10),
                expand=True
            ),
            ft.ElevatedButton(
                text="Renombrar Archivos",
                icon=ft.Icons.EDIT,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_900,
                on_click=lambda _: rename_files()
            ),
            rename_result_text
        ]),
        padding=30,
        expand=True 
    )

    # Menú lateral
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.DELETE_FOREVER,
                selected_icon=ft.Icons.DELETE_FOREVER,
                label="Duplicados"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.FOLDER_COPY,
                selected_icon=ft.Icons.FOLDER_COPY,
                label="Organizar"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.PHOTO_SIZE_SELECT_LARGE,
                selected_icon=ft.Icons.PHOTO_SIZE_SELECT_LARGE,
                label="Redimensionar"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.TRANSFORM,
                selected_icon=ft.Icons.TRANSFORM,
                label="Convertir"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.AUDIOTRACK,
                selected_icon=ft.Icons.AUDIOTRACK,
                label="Extraer Audio"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.MERGE_TYPE,
                selected_icon=ft.Icons.MERGE_TYPE,
                label="Fusionar PDFs"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.EDIT,
                selected_icon=ft.Icons.EDIT,
                label="Renombrar"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                selected_icon=ft.Icons.ADD_CIRCLE,
                label="Próximamente"
            ),
        ],
        on_change=change_view,
        bgcolor=ft.Colors.GREY_900,
    )

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                content_area,
            ],
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)