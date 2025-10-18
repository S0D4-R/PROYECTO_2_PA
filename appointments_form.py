import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from pyuiWidgets.imageLabel import ImageLabel


def appointments_menu():
    appointments_form = tk.Tk()
    appointments_form.title("CITAS")
    appointments_form.geometry("700x400")
    appointments_form.config(bg="#ffffff")


    style = ttk.Style()
    style.configure("salir.TButton", background="#FF0000", foreground="#ffffff")
    style.map("salir.TButton", background=[("active", "#CC0000")])

    boton_salir = ttk.Button(
        master=appointments_form,
        text="Volver al Menu",
        style="salir.TButton",
        command=lambda: appointments_form.destroy()
    )
    boton_salir.place(x=20, y=320, width=100, height=35)