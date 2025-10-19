import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import json
from pyuiWidgets.imageLabel import ImageLabel
PASSWORD_FILE = "password.json"
DEFAULT_PASSWORD = "123"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
class Lord:
    def __init__(self):
        try:
            with open(PASSWORD_FILE, 'r') as f:
                data = json.load(f)
                self.__password = data.get("password", DEFAULT_PASSWORD)
        except (FileNotFoundError, json.JSONDecodeError):
            self.__password = DEFAULT_PASSWORD
            self._save_password()

    def _save_password(self):
        with open(PASSWORD_FILE, 'w') as p_file:
            json.dump({"password": self.__password}, p_file)

    @property
    def contra(self):
        return self.__password
    @contra.setter
    def contra(self, new_password):
        if new_password == self.__password:
            messagebox.showinfo("La contraseña no puede ser igual a la anterior")
        else:
            self.__password = new_password
            messagebox.showinfo("La contraseña ha sido actualizada exitosamente")


lord = Lord()


#LOGIN----------------------------------------------------------------------------------------------------------
def get_info(frame, entry):
    temp_pass = entry.get()
    if temp_pass == lord.contra:
        frame.destroy()
        return admin_menu()
    else:
        frame.destroy()
        return login()

def login():
    login_form = tk.Tk()
    login_form.geometry("400x100")
    login_form.title("LOGIN")
    login_form.config(bg="#ffffff")

    #Style
    gen_style = ttk.Style(login_form)
    gen_style.theme_use("clam")
    gen_style.configure("Custom.TButton",
                          background="#000000",
                          foreground="#ffffff",
                          font=('Arial', 10),
                          bordercolor="#000000",
                          darkcolor="#000000",
                          lightcolor="#333333",
                          padding=3)


    #label
    pass_label = tk.Label(login_form, text="CONTRASEÑA:", background="#ffffff", foreground="#000000")
    pass_label.grid(row=0, column=0, padx=10, pady=30, sticky="w")
    #textbox
    pass_text = tk.Entry(login_form, background="#000000", foreground="#ffffff")
    pass_text.grid(row=0, column=0, padx=100, pady=30, sticky="w")

    #Botón get

    button_get = ttk.Button(login_form, text="Log In",
                           style="Custom.TButton",
                           command=lambda: get_info(login_form, pass_text))
    button_get.grid(row=0, column=0, padx=290, pady=(50, 10), sticky="ew")



#TABS-----------------------------------------------------------------------------------------------------------
def close_tabs(menu, frame1, frame2):
    menu.select(frame1)
    menu.hide(frame2)


def reportes(menu, main_frame, frame_reportes, style):
    menu.select(frame_reportes)
    style.configure("Custom.TButton")
    exit_button = ttk.Button(frame_reportes, text="SALIR", style="Custom.TButton", command=lambda: close_tabs(menu, main_frame, frame_reportes))
    exit_button.grid(row=0, column=0, padx=550, pady=(300, 50), sticky="ew")


def agregar_producto(menu,main_frame,  frame_add_prods, style):
    menu.select(frame_add_prods)
    style.configure("Custom.TButton")
    exit_button = ttk.Button(frame_add_prods, text="SALIR", style="Custom.TButton", command=lambda: close_tabs(menu,main_frame, frame_add_prods))
    exit_button.grid(row=0, column=0, padx=550, pady=(300, 50), sticky="ew")



#Password
def save_pass(entry1, entry2):
    if entry1.get() == entry2.get():
        lord.contra = entry1.get()
        lord._save_password()


def change_pass(menu, main_frame, password_frame, style):
    #Select tabs------------------------------------------------------------------------------
    menu.select(password_frame)
    style.configure("Custom.TButton")
    # label
    password_frame.grid_columnconfigure(0, weight=0)
    password_frame.grid_columnconfigure(1, weight=1)

    # --- FORMULARIO (Fila 0) ---
    # Etiqueta: Fila 0, Columna 0
    pass_label = tk.Label(password_frame, text="Nueva Contraseña:", background="#000000", foreground="#ffffff")
    pass_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Campo de Entrada: Fila 0, Columna 1
    pass_text = tk.Entry(password_frame, background="#000000", foreground="#ffffff", show="*")
    pass_text.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    c_pass_label = tk.Label(password_frame, text="Confirmación de Contraseña:", background="#000000", foreground="#ffffff")
    c_pass_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    c_pass_entry = tk.Entry(password_frame, background="#000000", foreground="#ffffff", show="*")
    c_pass_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    password_frame.grid_rowconfigure(2, weight=1)

    #Exit Tabs---------------------------------------------------------------------------------

    save_button = ttk.Button(password_frame, text="GUARDAR", style="Custom.TButton", command=lambda: save_pass(pass_text, c_pass_entry))
    save_button.grid(row=3, column=0, padx=10, pady=(10, 10), sticky="w")  # Sticky W para alinearlo a la izquierda

    exit_button = ttk.Button(password_frame, text="SALIR", style="Custom.TButton", command=lambda: close_tabs(menu, main_frame, password_frame))
    exit_button.grid(row=3, column=1, padx=10, pady=(10, 10), sticky="e")  # Sticky E para alinearlo a la derecha


#ADMIN MENU----------------------------------------------------------------------------------------------------



def admin_menu():
    admin_form = tk.Tk()
    admin_form.title("Administrador")
    admin_form.geometry("700x400")
    admin_form.config(bg="#ffffff")
    admin_style = ttk.Style(admin_form)
    admin_style.theme_use("clam")

    admin_style.configure("Custom.TButton",
                          background="#000000",  # Color de fondo principal (estado normal)
                          foreground="#ffffff",  # Color del texto
                          font=('Arial', 10),
                          # Esto es importante para el estilo 'clam':
                          bordercolor="#000000",  # Color del borde del botón
                          darkcolor="#000000",  # Color usado para sombras/bordes oscuros
                          lightcolor="#333333",  # Color usado para bordes claros (poco visible en clam)
                          padding=10)


    inside_menu = ttk.Notebook(admin_form)
    inside_menu.pack(expand=True, fill="both", padx=10, pady=10)
    #Frame del menú principal
    frame_menu_inicial = ttk.Frame(inside_menu)
    frame_menu_inicial.pack(expand=True, fill="both")
    inside_menu.add(frame_menu_inicial, text=" Menú Principal ")

    #Frame del menú de agregar productos
    frame_add_prods = ttk.Frame(inside_menu)
    frame_add_prods.pack(expand=True, fill="both")
    inside_menu.add(frame_add_prods, text="AGREGAR PRODUCTOS", state="hidden")

    # Frame del reporte
    frame_reports = ttk.Frame(inside_menu)
    frame_reports.pack(expand=True, fill="both")
    inside_menu.add(frame_reports, text="REPORTES", state="hidden")

    #Frame de cambio de contraseña
    frame_cambio_c = ttk.Frame(inside_menu)
    frame_cambio_c.pack(expand=True, fill="both")
    inside_menu.add(frame_cambio_c, text="CAMBIAR CONTRASEÑA", state="hidden")
#Botones--------------------------------------------------------------------------------------------------------
    button_ap = ttk.Button(frame_menu_inicial, text="AGREGAR PRODUCTO",
                           style="Custom.TButton",
                           command=lambda: agregar_producto(inside_menu,frame_menu_inicial, frame_add_prods, admin_style))
    button_ap.grid(row=0, column=0, padx=250, pady=(50, 10), sticky="ew")

    button_rep = ttk.Button(frame_menu_inicial, text="REPORTES",
                            style="Custom.TButton",
                            command=lambda: reportes(inside_menu,frame_menu_inicial, frame_reports, admin_style))
    button_rep.grid(row=1, column=0, padx=250, pady=10, sticky="ew")

    button_exit = ttk.Button(frame_menu_inicial, text="SALIR",
                             style="Custom.TButton",
                             command=lambda: admin_form.destroy())
    button_exit.grid(row=3, column=0, padx=250, pady=10, sticky="ew")

    button_change_p = ttk.Button(frame_menu_inicial, text="CAMBIAR CONTRASEÑA",
                            style="Custom.TButton",
                            command=lambda: change_pass(inside_menu,frame_menu_inicial, frame_cambio_c, admin_style))
    button_change_p.grid(row=2, column=0, padx=250, pady=10, sticky="ew")


# Botones--------------------------------------------------------------------------------------------------------
    admin_style.configure("label.TLabel", background="#E4E2E2", foreground="#000", anchor="center")
    #label = ImageLabel(master=admin_form, image_path=os.path.join(BASE_DIR, "assets", "images","pngwing.com.png"),
                       #text="Label", compound=tk.TOP, mode="cover")
    #label.configure(anchor="center")
    #label.place(x=50, y=15, width=403, height=319)
