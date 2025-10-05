import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from pyuiWidgets.imageLabel import ImageLabel
def reportes():
    reportes_form = tk.Tk()


def agregar_producto():
    prod_form = tk.Tk()


def admin_menu():
    admin_form = tk.Tk()
    admin_form.title("Administrador")
    admin_form.geometry("700x400")
    admin_form.config(bg="#ffffff")
    admin_style = ttk.Style(admin_form)
    admin_style.theme_use("clam")

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