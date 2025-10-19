import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from admin_form import *
from pyuiWidgets.imageLabel import ImageLabel

get_conn()
init_db()

def products_menu():
    products_form = tk.Tk()
    products_form.title("PRODUCTOS")
    products_form.geometry("700x400")
    products_form.config(bg="#ffffff")

    style = ttk.Style()
    style.configure("salir.TButton", background="#FF0000", foreground="#ffffff")
    style.map("salir.TButton", background=[("active", "#CC0000")])

    boton_salir = ttk.Button(
        master=products_form,
        text="Volver al Menu",
        style="salir.TButton",
        command=lambda: products_form.destroy()
    )
    boton_salir.place(x=20, y=320, width=100, height=35)