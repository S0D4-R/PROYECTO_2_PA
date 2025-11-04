import os
import tkinter as tk
from tkinter import ttk, messagebox
from general_processes import gen_db_x

def services_menu():
    servicios = tk.Toplevel()
    servicios.title("Servicios disponibles")
    servicios.geometry("600x400")
    servicios.config(bg="#ffffff")


    tk.Label(servicios, text="Lista de Servicios Disponibles", bg="#ffffff", font=("Arial", 14, "bold")).pack(pady=15)

    columnas = ("ID", "Servicio", "Precio")
    tabla = ttk.Treeview(servicios, columns=columnas, show="headings", height=12)
    tabla.pack(padx=15, pady=10, fill="both", expand=True)

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=130)

    def cargar_servicios():
        try:
            tabla.delete(*tabla.get_children())

            con = gen_db_x._get_conn()
            if con is None:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                return

            cur = con.cursor()
            cur.execute("SELECT id, name, price FROM b_services ORDER BY name ASC;")
            servicios = cur.fetchall()
            con.close()

            for svc in servicios:
                tabla.insert("", tk.END, values=svc)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los servicios:\n{e}")

    frame_botones = tk.Frame(servicios, bg="#ffffff")
    frame_botones.pack(pady=10)

    ttk.Button(frame_botones, text="Actualizar lista", command=cargar_servicios).grid(row=0, column=0, padx=10)
    ttk.Button(frame_botones, text="Volver al menú", command=servicios.destroy).grid(row=0, column=1, padx=10)

    cargar_servicios()

    servicios.mainloop()
