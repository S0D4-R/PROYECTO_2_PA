import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from pyuiWidgets.imageLabel import ImageLabel
from tkinter import ttk, messagebox
from general_processes import get_conn

def services_menu():
    win = tk.Toplevel()
    win.title("Servicios - Cobro")
    win.geometry("500x300")
    win.config(bg="#ffffff")

    tk.Label(win, text="Seleccionar Servicio:", bg="#ffffff", font=("Arial", 12)).place(x=50, y=50)
    tk.Label(win, text="Precio:", bg="#ffffff", font=("Arial", 12)).place(x=50, y=120)

    combo_servicios = ttk.Combobox(win, width=30, state="readonly")
    combo_servicios.place(x=220, y=50)

    precio_var = tk.StringVar()
    entry_precio = tk.Entry(win, textvariable=precio_var, state="readonly", width=15, justify="center")
    entry_precio.place(x=220, y=120)

    def cargar_servicios():
        try:
            connection = get_conn()
            cursor = connection.cursor()
            cursor.execute("SELECT name, price FROM b_services ORDER BY name ASC;")
            servicios = cursor.fetchall()

            win.servicios_dict = {nombre: precio for nombre, precio in servicios}
            combo_servicios["values"] = list(win.servicios_dict.keys())

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los servicios: {e}")
        finally:
            if connection:
                connection.close()

    def mostrar_precio(event):
        nombre_servicio = combo_servicios.get()
        if nombre_servicio in win.servicios_dict:
            precio_var.set(f"Q{win.servicios_dict[nombre_servicio]:.2f}")

    combo_servicios.bind("<<ComboboxSelected>>", mostrar_precio)

    def cobrar_servicio():
        nombre = combo_servicios.get()
        if not nombre:
            messagebox.showwarning("Atención", "Seleccione un servicio antes de cobrar.")
            return

        precio = win.servicios_dict.get(nombre)
        messagebox.showinfo("Cobro realizado", f"Servicio: {nombre}\nTotal a pagar: Q{precio:.2f}")

    ttk.Button(win, text="Cobrar", command=cobrar_servicio).place(x=200, y=180)

    cargar_servicios()

    win.mainloop()

