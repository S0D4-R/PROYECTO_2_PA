import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from pyuiWidgets.imageLabel import ImageLabel


def sells_menu():
    sells_form = tk.Tk()
    sells_form.title("VENTAS")
    sells_form.geometry("1000x700")
    sells_form.config(bg="#ffffff")

    style = ttk.Style()
    style.configure("salir.TButton", background="#000000", foreground="#ffffff")
    style.map("salir.TButton", background=[("active", "#CC0000")])

    boton_salir = ttk.Button(
        master=sells_form,
        text="Volver al Menu ",
        style="salir.TButton",
        command=lambda: sells_form.destroy()
    )
    boton_salir.place(x=20, y=320, width=100, height=35)