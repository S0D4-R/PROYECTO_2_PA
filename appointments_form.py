import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from general_processes import *
from datetime import datetime

appointment_db = Appointments_DB()

def appointments_menu():
    citas = tk.Toplevel()
    citas.title("Gestión de Citas")
    citas.geometry("1000x550")
    citas.config(bg="#ffffff")

    columns = ("id", "nombre", "servicio", "fecha", "hora", "estado")
    tabla = ttk.Treeview(citas, columns=columns, show="headings")

    ttk.Label(citas, text="GESTIÓN DE CITAS", background="#ffffff", font=("Arial", 14, "bold")).pack(pady=20)

    contenedor = ttk.Frame(citas)
    contenedor.pack(pady=10)

    frame_form = ttk.Frame(contenedor)
    frame_form.grid(row=0, column=0, padx=20, pady=10, sticky="n")

    ttk.Label(frame_form, text="ID Cita:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_id = ttk.Entry(frame_form, width=25)
    entry_id.grid(row=0, column=1, padx=10, pady=5)
    entry_id.insert(0, id_creation("A"))
    entry_id.config(state="readonly")

    ttk.Label(frame_form, text="Nombre del cliente:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_nombre = ttk.Entry(frame_form, width=35)
    entry_nombre.grid(row=1, column=1, padx=10, pady=5)

    try:
        servicios = appointment_db.iterable_db("SELECT id, name, price FROM b_services;")
        valores_servicio = [f"{s[0]} - {s[1]}" for s in servicios]
    except Exception as e:
        valores_servicio = []
        messagebox.showerror("Error de BD", f"No se pudieron cargar los servicios:\n{e}")

    combo_servicio = ttk.Combobox(frame_form, width=25, values=valores_servicio, state="readonly")
    combo_servicio.grid(row=2, column=1, padx=10, pady=5)
    combo_servicio.set("Seleccione un servicio")

    ttk.Label(frame_form, text="Fecha (DD-MM-AAAA):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry_fecha = ttk.Entry(frame_form, width=25)
    entry_fecha.grid(row=3, column=1, padx=10, pady=5)

    ttk.Label(frame_form, text="Hora (HH:MM):").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    entry_hora = ttk.Entry(frame_form, width=25)
    entry_hora.grid(row=4, column=1, padx=10, pady=5)

    frame_botones = ttk.Frame(contenedor, width=200)
    frame_botones.grid(row=0, column=1, padx=50, pady=10, sticky="n")

    style = ttk.Style()
    style.configure("Accion.TButton", font=("Arial", 10, "bold"), padding=8)

    ttk.Button(frame_botones, text="Registrar", style="Accion.TButton", command=lambda: agregar_cita()).pack(fill="x", pady=6)
    ttk.Button(frame_botones, text="Editar", style="Accion.TButton", command=lambda: editar_cita()).pack(fill="x", pady=6)
    ttk.Button(frame_botones, text="Atender", style="Accion.TButton", command=lambda: atender_cita()).pack(fill="x", pady=6)
    ttk.Button(frame_botones, text="Eliminar", style="Accion.TButton", command=lambda: eliminar_cita()).pack(fill="x", pady=6)
    ttk.Button(frame_botones, text="Actualizar lista", style="Accion.TButton", command=lambda: cargar_citas()).pack(fill="x", pady=6)
    ttk.Button(frame_botones, text="Salir", style="Accion.TButton", command=citas.destroy).pack(fill="x", pady=6)

    for col, text in zip(columns, ["ID", "Cliente", "Servicio", "Fecha", "Hora", "Estado"]):
        tabla.heading(col, text=text)
        tabla.column(col, width=150)
    tabla.pack(pady=20, fill="both", expand=True)

    tabla.bind("<Double-1>", lambda e: seleccionar_cita())

    def cargar_citas():
        tabla.delete(*tabla.get_children())
        try:
            citas_list = appointment_db.iterable_db("SELECT * FROM barbershop_appointments ORDER BY appointment_date;")
            for row in citas_list:
                datos = list(row)
                if len(datos) >= 6:
                    datos[5] = "Pendiente"
                tabla.insert("", tk.END, values=datos)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las citas:\n{e}")

    def agregar_cita():
        id_cita = entry_id.get()
        nombre = entry_nombre.get()
        servicio = combo_servicio.get()
        fecha_input = entry_fecha.get()
        hora = entry_hora.get()

        if not id_cita or not nombre or not servicio or not fecha_input or not hora:
            messagebox.showwarning("Campos incompletos", "Todos los campos son obligatorios.")
            return

        try:
            fecha1 = datetime.strptime(fecha_input, "%d-%m-%Y")
            fecha = fecha1.strftime("%Y-%m-%d")
            servicio_id = servicio.split(" - ")[0].strip()

            consulta = f"""SELECT id FROM barbershop_appointments WHERE appointment_time = '{hora}' AND appointment_date = '{fecha}'"""
            cita_existente = appointment_db.iterable_db(consulta)

            if cita_existente:
                messagebox.showwarning("Conflicto", "Ya existe una cita registrada en esa hora y fecha.")
                return

            gen_db_x.execute("""
                INSERT INTO barbershop_appointments (id, client_name, service_id, appointment_date, appointment_time)
                VALUES (%s, %s, %s, %s, %s);
            """, (id_cita, nombre, servicio_id, fecha, hora))

            messagebox.showinfo("Éxito", "Cita registrada correctamente.")

            entry_nombre.delete(0, tk.END)
            combo_servicio.set('')
            entry_fecha.delete(0, tk.END)
            entry_hora.delete(0, tk.END)

            cargar_citas()
            limpiar_campos()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la cita:\n{e}")


    def editar_cita():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una cita para editar.")
            return

        item = tabla.item(seleccion[0])
        id_cita = item["values"][0]

        nombre = entry_nombre.get()
        servicio = combo_servicio.get()
        fecha_input = entry_fecha.get()
        hora = entry_hora.get()

        if not nombre or not servicio or not fecha_input or not hora:
            messagebox.showwarning("Campos incompletos", "Todos los campos son obligatorios.")
            return

        try:
            fecha1 = datetime.strptime(fecha_input, "%d-%m-%Y")
            fecha = fecha1.strftime("%Y-%m-%d")
            servicio_id = servicio.split(" - ")[0].strip()

            consulta = f"""SELECT id FROM barbershop_appointments WHERE appointment_time = '{hora}' AND appointment_date = '{fecha}'"""
            cita_existente = appointment_db.iterable_db(consulta)

            if cita_existente:
                messagebox.showwarning("Conflicto", "Ya existe una cita registrada en esa hora y fecha.")
                return

            gen_db_x.execute("""
                UPDATE barbershop_appointments 
                SET client_name=%s, service_id=%s, appointment_date=%s, appointment_time=%s
                WHERE id=%s;
            """, (nombre, servicio_id, fecha, hora, id_cita))

            messagebox.showinfo("Éxito", "Cita actualizada correctamente.")
            cargar_citas()
            limpiar_campos()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo editar la cita:\n{e}")



    def eliminar_cita():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una cita para eliminar.")
            return
        item = tabla.item(seleccion[0])
        id_cita = item["values"][0]
        try:
            gen_db_x.execute("DELETE FROM barbershop_appointments WHERE id = %s;", (id_cita,))
            messagebox.showinfo("Éxito", "Cita eliminada correctamente.")
            cargar_citas()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la cita:\n{e}")

    def atender_cita():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una cita para atender.")
            return

        item = tabla.item(seleccion[0])
        id_cita = item["values"][0]

        confirmar = messagebox.askquestion("Atender cita", "¿Marcar esta cita como completada y eliminarla?")
        if confirmar == "yes":
            try:
                gen_db_x.execute("DELETE FROM barbershop_appointments WHERE id = %s;", (id_cita,))
                messagebox.showinfo("Éxito", "Cita atendida y eliminada correctamente.")
                cargar_citas()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la cita:\n{e}")

    def seleccionar_cita():
        seleccion = tabla.selection()
        if not seleccion:
            return
        item = tabla.item(seleccion[0])
        datos = item["values"]

        entry_id.config(state="normal")
        entry_id.delete(0, tk.END)
        entry_id.insert(0, datos[0])
        entry_id.config(state="readonly")

        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, datos[1])

        combo_servicio.set(datos[2])
        entry_fecha.delete(0, tk.END)
        entry_fecha.insert(0, datos[3])
        entry_hora.delete(0, tk.END)
        entry_hora.insert(0, datos[4])


    def limpiar_campos():
        entry_id.config(state="normal")
        entry_id.delete(0, tk.END)
        entry_id.insert(0, id_creation("A"))
        entry_id.config(state="readonly")

        entry_nombre.delete(0, tk.END)
        combo_servicio.set("Seleccione un servicio")
        entry_fecha.delete(0, tk.END)
        entry_hora.delete(0, tk.END)

    cargar_citas()
