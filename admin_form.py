import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from pyuiWidgets.imageLabel import ImageLabel


def admin_menu():
    admin_form = tk.Tk()
    admin_form.title("Administrador")
    admin_form.geometry("700x400")
    admin_form.config(bg="#ffffff")

    button = ttk.Button(master=admin_form, text="CONSULTAR PRODUCTOS", style="button.TButton")
    button.place(x=56, y=114, width=175, height=48)