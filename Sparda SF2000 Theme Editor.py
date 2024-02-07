import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar  # Importar Progressbar desde ttk
from PIL import Image, ImageTk
import struct
import threading

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sparda SF2000 Theme Editor")

        # Ajustar el tamaño de la ventana principal
        self.root.geometry("350x200")  # Ajusta el tamaño según tus preferencias

        self.input_folder_path = tk.StringVar()
        self.output_folder_path = tk.StringVar()

        self.progress_bar = Progressbar(self.root, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack(pady=10)

        # Crear la ventana flotante y elementos una vez al inicio
        self.image_viewer = tk.Toplevel(root)
        self.scrollbar = tk.Scrollbar(self.image_viewer, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas = tk.Canvas(self.image_viewer, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.image_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.image_frame, anchor=tk.NW)
        self.scrollbar.config(command=self.canvas.yview)
        self.image_frame.bind("<Configure>", lambda event, canvas=self.canvas: self.on_frame_configure(event, canvas))
        self.image_frame.bind("<MouseWheel>", self.on_mousewheel)

        # Botones de siguiente y anterior en la ventana flotante
        self.prev_page_button_popup = tk.Button(self.image_viewer, text="Previous", command=self.prev_page)
        self.prev_page_button_popup.pack(side=tk.LEFT)

        self.next_page_button_popup = tk.Button(self.image_viewer, text="Next", command=self.next_page)
        self.next_page_button_popup.pack(side=tk.RIGHT)

        # Botones de selección de carpetas
        self.input_folder_button = tk.Button(root, text="Input Folder", command=self.select_input_folder)
        self.input_folder_button.pack(pady=10)  # Ajusta pady según tu preferencia

        self.output_folder_button = tk.Button(root, text="Output Folder", command=self.select_output_folder)
        self.output_folder_button.pack(pady=10)  # Ajusta pady según tu preferencia

        # Diccionario para almacenar las referencias a los tk_image originales
        self.original_tk_images = {}

        # Inicializar la visualización de imágenes
        self.load_images()

        # Botón para grabar cambios
        self.save_button = tk.Button(root, text="Save", command=self.save_changes)
        self.save_button.pack(pady=10)  # Ajusta pady según tu preferencia

        self.bgra_files = [
            "aepic.nec", "appvc.ikb", "awusa.tax", "bttlve.kbp", "certlm.msa", "djctq.rsd", "djoin.nec", "dxdiag.bin",
            "dxkgi.ctp", "ectte.bke", "esent.bvs", "exaxz.hsp", "fvecpl.ai", "gakne.ctp", "gkavc.ers", "htui.kcc",
            "icm32.dll", "igc64.dll", "irmon.tax", "itiss.ers", "ke89a.bvs", "lk7tc.bvs", "msgsm.dll", "mssvp.nec",
            "normidna.bin", "ntdll.bvs", "nvinf.hsp", "okcg2.old", "pcadm.nec", "rmapi.tax", "sensc.bvs", "sfcdr.cpl", "subst.tax",
            "ucby4.aax", "vidca.bvs", "vssvc.nec", "wshrm.nec"            
        ]

        # Lista para almacenar imágenes y tamaños de miniatura
        self.images = [
            {"name": "aepic.nec", "size": (1008, 164)},
            {"name": "apisa.dlk", "size": (640, 480)},
            {"name": "appvc.ikb", "size": (150, 214)},
            {"name": "awusa.tax", "size": (1008, 164)},
            {"name": "bisrv.nec", "size": (640, 480)},
            {"name": "bttlve.kbp", "size": (60, 144)},
            {"name": "c1eac.pal", "size": (640, 480)},
            {"name": "cero.phl", "size": (640, 480)},
            {"name": "certlm.msa", "size": (40, 24)},
            {"name": "cketp.bvs", "size": (640, 816)},
            {"name": "d2d1.hgp", "size": (640, 480)},
            {"name": "dism.cef", "size": (640, 480)},
            {"name": "djctq.rsd", "size": (40, 24)},
            {"name": "djoin.nec", "size": (1008, 164)},
            {"name": "dpskc.ctp", "size": (640, 320)},
            {"name": "drivr.ers", "size": (640, 480)},
            {"name": "dsuei.cpl", "size": (640, 480)},
            {"name": "dxdiag.bin", "size": (40, 24)},            
            {"name": "dxva2.nec", "size": (640, 480)},
            {"name": "dxkgi.ctp", "size": (1008, 164)},
            {"name": "ectte.bke", "size": (161, 126)},
            {"name": "efsui.stc", "size": (640, 480)},
            {"name": "esent.bvs", "size": (1008, 164)},
            {"name": "exaxz.hsp", "size": (152, 1224)},
            {"name": "fixas.ctp", "size": (640, 480)},
            {"name": "fltmc.sta", "size": (640, 480)},
            {"name": "fvecpl.ai", "size": (40, 24)},
            {"name": "gakne.ctp", "size": (576, 256)},
            {"name": "gkavc.ers", "size": (576, 256)},
            {"name": "hctml.ers", "size": (640, 480)},
            {"name": "hlink.bvs", "size": (640, 480)},
            {"name": "htui.kcc", "size": (40, 24)},
            {"name": "icm32.dll", "size": (40, 24)},
            {"name": "icuin.cpl", "size": (640, 480)},
            {"name": "igc64.dll", "size": (217, 37)},
            {"name": "ihdsf.bke", "size": (640, 480)},
            {"name": "irftp.ctp", "size": (640, 480)},
            {"name": "irmon.tax", "size": (1008, 164)},
            {"name": "itiss.ers", "size": (1008, 164)},
            {"name": "jccatm.kbp", "size": (640, 480)},
            {"name": "ke89a.bvs", "size": (1008, 164)},
            {"name": "kmbcj.acp", "size": (640, 480)},
            {"name": "lfsvc.dll", "size": (640, 480)},
            {"name": "lk7tc.bvs", "size": (52, 192)},
            {"name": "lkvax.aef", "size": (640, 480)},
            {"name": "mkhbc.rcv", "size": (640, 1440)},
            {"name": "mksh.rcv", "size": (640, 480)},
            {"name": "msgsm.dll", "size": (40, 24)},
            {"name": "mssvp.nec", "size": (1008, 164)},
            {"name": "normidna.bin", "size": (40, 24)},
            {"name": "ntdll.bvs", "size": (1008, 164)},
            {"name": "nvinf.hsp", "size": (16, 240)},
            {"name": "okcg2.old", "size": (32, 32)},
            {"name": "pcadm.nec", "size": (1008, 164)},
            {"name": "pwsso.occ", "size": (640, 480)},
            {"name": "qasf.bel", "size": (640, 480)},
            {"name": "qwave.bke", "size": (640, 480)},
            {"name": "rmapi.tax", "size": (640, 480)},
            {"name": "sdclt.occ", "size": (120, 240)},
            {"name": "sensc.bvs", "size": (1008, 164)},
            {"name": "sfcdr.cpl", "size": (576, 1344)},
            {"name": "subst.tax", "size": (1008, 164)},
            {"name": "ucby4.aax", "size": (1008, 164)},
            {"name": "urlkp.bvs", "size": (640, 480)},
            {"name": "uyhbc.dck", "size": (640, 480)},
            {"name": "vidca.bvs", "size": (1008, 164)},
            {"name": "vssvc.nec", "size": (1008, 164)},
            {"name": "wshrm.nec", "size": (217, 37)},
            {"name": "xajkg.hsp", "size": (640, 480)},
            {"name": "ztrba.nec", "size": (64, 320)},
        ]

        # Cantidad de imágenes por página
        imagenes_por_pagina = 1

        # Dividir las imágenes en páginas
        self.paginas = [self.images[i:i + imagenes_por_pagina] for i in range(0, len(self.images), imagenes_por_pagina)]

        # Página actual (inicialmente la primera)
        self.pagina_actual = 0

        # Inicializar la visualización de imágenes
        self.display_images()

    def on_frame_configure(self, event, canvas):
        # Ajustar el área de desplazamiento al tamaño del lienzo interior
        canvas.config(scrollregion=canvas.bbox("all"))

    def on_mousewheel(self, event):
        # Desplazar el lienzo verticalmente con la rueda del ratón
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def select_input_folder(self):
        folder_path = filedialog.askdirectory()
        self.input_folder_path.set(folder_path)
        self.load_images()  # Llamar a load_images() para cargar las imágenes desde la carpeta seleccionada
        self.update_images()

    def select_output_folder(self):
        folder_path = filedialog.askdirectory()
        self.output_folder_path.set(folder_path)

    def load_images(self):
        input_folder = self.input_folder_path.get()

        # Verificar si la carpeta de entrada está seleccionada
        if not input_folder:
            return

        supported_files = [
            "apisa.dlk", "bisrv.nec", "c1eac.pal", "cero.phl", "cketp.bvs", "d2d1.hgp", "dism.cef", "dpskc.ctp",
            "drivr.ers", "dsuei.cpl", "dxva2.nec", "efsui.stc", "fixas.ctp", "fltmc.sta", "hctml.ers", "hlink.bvs",
            "icuin.cpl", "ihdsf.bke", "irftp.ctp", "jccatm.kbp", "kmbcj.acp", "lfsvc.dll", "lkvax.aef", "mkhbc.rcv",
            "mksh.rcv", "pwsso.occ", "qasf.bel", "qwave.bke", "sdclt.occ", "urlkp.bvs", "uyhbc.dck", "xajkg.hsp", "ztrba.nec"
        ]

        bgra_files = [
            "aepic.nec", "appvc.ikb", "awusa.tax", "bttlve.kbp", "certlm.msa", "djctq.rsd", "djoin.nec", "dxdiag.bin",
            "dxkgi.ctp", "ectte.bke", "esent.bvs", "exaxz.hsp", "fvecpl.ai", "gakne.ctp", "gkavc.ers", "htui.kcc",
            "icm32.dll", "igc64.dll", "irmon.tax", "itiss.ers", "ke89a.bvs", "lk7tc.bvs", "msgsm.dll", "mssvp.nec",
            "normidna.bin", "ntdll.bvs", "nvinf.hsp", "okcg2.old", "pcadm.nec", "rmapi.tax", "sensc.bvs", "sfcdr.cpl", "subst.tax",
            "ucby4.aax", "vidca.bvs", "vssvc.nec", "wshrm.nec"            
        ]

        for image_data in self.images:
            file_name = image_data["name"]
            size = image_data["size"]

            file_path = f"{input_folder}/{file_name}"

            try:
                # Verificar si el nombre de archivo está en la lista de archivos compatibles
                if file_name in supported_files:
                    # Leer el archivo y convertir los datos BGRA a imagen PIL
                    with open(file_path, 'rb') as file:
                        raw_data = file.read()
                        image = Image.frombytes('RGB', (size[0], size[1]), raw_data, 'raw', 'BGR;16', 0, -1)
                    image = image.transpose(Image.FLIP_TOP_BOTTOM)
                elif file_name in bgra_files:
                    # Leer el archivo y convertir los datos BGRA a imagen PIL
                    with open(file_path, 'rb') as file:
                        raw_data = file.read()
                        image = Image.frombytes('RGBA', (size[0], size[1]), raw_data, 'raw', 'BGRA', 0, -1)
                    image = image.transpose(Image.FLIP_TOP_BOTTOM)
                else:
                    # Si no es un archivo de los seleccionados, cargar la imagen como antes
                    image = Image.open(file_path)

                # Escalar la imagen a miniatura
                image.thumbnail(size)

                # Crear PhotoImage y almacenarlo en el diccionario image_data
                tk_image = ImageTk.PhotoImage(image)
                image_data["tk_image"] = tk_image

                # Almacenar una referencia al tk_image original
                self.original_tk_images[file_name] = tk_image.copy()
            except Exception as e:
                print(f"Could not load image {file_name}: {str(e)}")

    def display_images(self):
        # Establecer el tamaño deseado para la ventana flotante
        self.image_viewer.geometry("1280x600")

        # Limpiar el contenido actual del lienzo
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        # Mostrar imágenes en la cuadrícula en el lienzo existente
        row, col = 0, 0
        for image_data in self.paginas[self.pagina_actual]:
            image_name = image_data["name"]
            tk_image = self.original_tk_images.get(image_name, None)  # Obtener el tk_image original del diccionario

            if tk_image:
                # Si hay un tk_image original, utilizarlo
                image_label = tk.Label(self.image_frame, image=tk_image, text=image_name, compound=tk.TOP)
            else:
                # Si no hay un tk_image original, utilizar el tk_image actualizado o el texto
                tk_image = image_data.get("tk_image")
                if tk_image:
                    image_label = tk.Label(self.image_frame, image=tk_image, text=image_name, compound=tk.TOP)
                else:
                    image_label = tk.Label(self.image_frame, text=image_name)

            image_label.grid(row=row, column=col)

            change_button = tk.Button(self.image_frame, text="Cambiar", command=lambda data=image_data: self.change_image(data))
            change_button.grid(row=row + 1, column=col)

            col += 1
            if col > 5:
                col = 0
                row += 2

        # Ajustar el área de desplazamiento al tamaño del lienzo interior
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Añadir el botón de descarga debajo de la imagen actual en la cuadrícula
        for widget in self.image_frame.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("text") == self.paginas[self.pagina_actual][0]["name"]:
                download_button = tk.Button(self.image_frame, text="Descargar", command=self.download_image)
                download_button.grid(row=widget.grid_info()["row"] + 2, column=widget.grid_info()["column"])
                break


    def download_image(self):
        output_folder = self.output_folder_path.get()

        # Verificar si se ha seleccionado "Output Folder"
        if not output_folder:
            self.show_error_message("Select the output folder.")
            return

        # Obtener la imagen actual
        current_image_data = self.paginas[self.pagina_actual][0]
        image_name = current_image_data["name"]
        tk_image = current_image_data.get("tk_image")

        # Verificar si la imagen actual tiene una representación en PhotoImage
        if tk_image:
            # Convertir PhotoImage a Image
            image = ImageTk.getimage(tk_image)

            # Guardar la imagen en la carpeta de salida
            try:
                image.save(f"{output_folder}/{image_name}.png", format="PNG")
                self.show_success_message(f"Image '{image_name}' downloaded successfully.")
            except Exception as e:
                self.show_error_message(f"Could not save image {image_name}: {str(e)}")

    def change_image(self, image_data):
        new_image_path = filedialog.askopenfilename()
        if new_image_path:
            new_image = Image.open(new_image_path)
            new_image = new_image.resize(image_data["size"])  # Redimensionar la imagen al tamaño esperado
            tk_new_image = ImageTk.PhotoImage(new_image)
            image_data["tk_image"] = tk_new_image

            # Actualizar el tk_image original en el diccionario
            self.original_tk_images[image_data["name"]] = tk_new_image

            # Buscar la etiqueta de la imagen actual en la cuadrícula en el lienzo
            for widget in self.image_frame.winfo_children():
                if isinstance(widget, tk.Label) and widget.cget("text") == image_data["name"]:
                    # Actualizar la etiqueta de la imagen en el lienzo
                    widget.configure(image=tk_new_image)
                    break


    def update_images(self):
        # Actualizar las imágenes cuando sea necesario
        if self.root.winfo_exists():
            self.display_images()

    def save_changes(self):
        output_folder = self.output_folder_path.get()

        # Verificar si se ha seleccionado "Output Folder"
        if not output_folder:
            self.show_error_message("Select the output folder.")
            return

        # Iniciar un hilo para realizar la operación de grabación
        threading.Thread(target=self.save_changes_thread, args=(output_folder,)).start()

    def save_changes_thread(self, output_folder):
        # Lógica para guardar las imágenes en la carpeta de salida
        total_images = len(self.images)
        progress_step = 100 / total_images
        progress = 0

        for index, image_data in enumerate(self.images, start=1):
            image_name = image_data["name"]
            tk_image = image_data.get("tk_image")

            if tk_image:
                # Convertir PhotoImage a Image
                image = ImageTk.getimage(tk_image)

                # Verificar si el archivo actual es uno de los que requiere conversión a RGB565
                if image_name in self.bgra_files:  # Aquí se corrige
                    # Convertir la imagen PIL a datos BGRA
                    raw_data = image.tobytes('raw', 'BGRA')
                else:
                    # Realizar la conversión a RGB565 Little Endian
                    raw_data = self.convert_to_rgb565(image)

                # Guardar la imagen en la carpeta de salida
                try:
                    with open(f"{output_folder}/{image_name}", 'wb') as file:
                        file.write(raw_data)
                except Exception as e:
                    self.show_error_message(f"Could not save image {image_name}: {str(e)}")
                    return
            
            # Actualizar la barra de progreso
            progress += progress_step
            self.update_progress(progress)

        # Mostrar mensaje de éxito
        self.show_success_message("Changes saved successfully.")

    def update_progress(self, value):
        # Actualizar la barra de progreso
        self.progress_bar["value"] = value
        self.root.update_idletasks()

    def convert_to_rgb565(self, image):
        # Obtener los datos de píxeles RGB
        rgb_data = list(image.getdata())

        # Convertir a formato RGB565 Little Endian
        rgb565_data = []
        for pixel in rgb_data:
            r, g, b = pixel[:3]  # Tomar solo los primeros tres valores (R, G, B)
            rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            rgb565_data.extend(struct.pack('<H', rgb565))

        return bytes(rgb565_data)

    def show_error_message(self, message):
        tk.messagebox.showerror("Error", message)

    def show_success_message(self, message):
        tk.messagebox.showinfo("Success", message)

    def prev_page(self):
        if self.pagina_actual > 0:
            self.pagina_actual -= 1
            self.display_images()

    def next_page(self):
        if self.pagina_actual < len(self.paginas) - 1:
            self.pagina_actual += 1
            self.display_images()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
