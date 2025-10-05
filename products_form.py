import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from pyuiWidgets.imageLabel import ImageLabel


def products_menu():
    products_form = tk.Tk()
    products_form.title("PRODUCTOS")
    products_form.geometry("700x400")
    products_form.config(bg="#ffffff")