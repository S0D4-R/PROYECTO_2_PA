import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from pyuiWidgets.imageLabel import ImageLabel
from tkinter import ttk, messagebox
from general_processes import *
from datetime import date

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
            conn = get_conn()
            cur = conn.cursor()
            # 🔹 Cargamos el ID y el nombre del servicio
            cur.execute("SELECT id, name, price FROM b_services ORDER BY name ASC;")
            servicios = cur.fetchall()
            win.servicios_dict = {nombre: (id_serv, precio) for id_serv, nombre, precio in servicios}
            combo_servicios["values"] = list(win.servicios_dict.keys())
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los servicios: {e}")
        finally:
            if conn:
                conn.close()

    def mostrar_precio(event):
        nombre_servicio = combo_servicios.get()
        if nombre_servicio in win.servicios_dict:
            precio = win.servicios_dict[nombre_servicio][1]
            precio_var.set(f"Q{precio:.2f}")

    combo_servicios.bind("<<ComboboxSelected>>", mostrar_precio)

    def cobrar_servicio():
        nombre = combo_servicios.get()
        if not nombre:
            messagebox.showwarning("Atención", "Seleccione un servicio antes de cobrar.")
            return

        service_id, precio = win.servicios_dict[nombre]
        venta_id = id_creation("V")
        fecha = date.today()
        cantidad = 1

        try:
            conn = get_conn()
            cur = conn.cursor()

            # 🔹 Insertamos los datos en la tabla barbershop_sales
            cur.execute("""
                        INSERT INTO barbershop_sales
                        (id, sale_date, product_id, service_id, quantity, total_amount)
                        VALUES (%s, %s, NULL, %s, %s, %s);
                    """, (venta_id, fecha, service_id, cantidad, precio))

            conn.commit()

            messagebox.showinfo(
                "Cobro realizado",
                f"Venta registrada con éxito.\n\nCódigo de venta: {venta_id}\n"
                f"Servicio: {nombre}\nTotal: Q{precio:.2f}"
            )

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la venta: {e}")
        finally:
            if conn:
                conn.close()

    ttk.Button(win, text="Cobrar", command=cobrar_servicio).place(x=200, y=180)

    ttk.Button(win, text="Cobrar", command=cobrar_servicio).place(x=200, y=180)

    cargar_servicios()

    win.mainloop()

