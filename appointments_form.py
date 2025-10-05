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