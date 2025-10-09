import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from pyuiWidgets.imageLabel import ImageLabel
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def reportes():
    reportes_form = tk.Tk()


def agregar_producto(menu, frame_add_prods):
    menu.select(frame_add_prods)


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
#Botones--------------------------------------------------------------------------------------------------------
    button_ap = ttk.Button(frame_menu_inicial, text="AGREGAR PRODUCTO",
                           style="Custom.TButton",
                           command=lambda: agregar_producto(inside_menu, frame_add_prods))
    button_ap.grid(row=0, column=0, padx=250, pady=(50, 10), sticky="ew")

    button_rep = ttk.Button(frame_menu_inicial, text="REPORTES",
                            style="Custom.TButton",
                            command=lambda: reportes())
    button_rep.grid(row=1, column=0, padx=250, pady=10, sticky="ew")

    button_exit = ttk.Button(frame_menu_inicial, text="SALIR",
                             style="Custom.TButton",
                             command=lambda: admin_form.destroy())
    button_exit.grid(row=2, column=0, padx=250, pady=10, sticky="ew")
# Botones--------------------------------------------------------------------------------------------------------
    admin_style.configure("label.TLabel", background="#E4E2E2", foreground="#000", anchor="center")
    #label = ImageLabel(master=admin_form, image_path=os.path.join(BASE_DIR, "assets", "images","pngwing.com.png"),
                       #text="Label", compound=tk.TOP, mode="cover")
    #label.configure(anchor="center")
    #label.place(x=50, y=15, width=403, height=319)
""" 
    #Botón de salida
    button = ttk.Button(master=admin_form, text="SALIR", style="button.TButton", command=lambda: admin_form.destroy())
    button.place(x=500, y=340, width=175, height=48)
    admin_style.configure("button.TButton", background="#000000", foreground="#ffffff")
    admin_style.map("button.TButton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

#Botón de Agregar Producto
    button_ap = ttk.Button(master=admin_form, text="AGREGAR PRODUCTO", style="button.TButton", command=lambda: agregar_producto())
    button_ap.place(x=300, y=340, width=175, height=48)
    admin_style.configure("button_ap.TButton", background="#000000", foreground="#ffffff")
    admin_style.map("button_ap.TButton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

#Botón de reportes
    button_rep = ttk.Button(master=admin_form, text="REPORTES", style="button.TButton", command=lambda: agregar_producto())
    button_rep.place(x=100, y=340, width=175, height=48)
    admin_style.configure("button_rep.TButton", background="#000000", foreground="#ffffff")
    admin_style.map("button_rep.TButton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])
"""