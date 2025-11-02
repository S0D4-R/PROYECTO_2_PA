import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from general_processes import get_conn
from general_processes import id_creation
from POO import Cita
from datetime import datetime


def appointments_menu():
    citas = tk.Toplevel()
    citas.title("Gestión de Citas")
    citas.geometry("900x500")
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
        con = get_conn()
        cur = con.cursor()
        cur.execute("SELECT id, name, price FROM b_services;")
        servicios = cur.fetchall()
        con.close()

        valores_servicio = [f"{s[0]} - {s[1]}" for s in servicios]

    except Exception as e:
        valores_servicio = []
        messagebox.showerror("Error de BD", f"No se pudieron cargar los servicios:\n{e}")

    ttk.Label(frame_form, text="Servicio:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    combo_servicio = ttk.Combobox(frame_form, width=40, values=valores_servicio, state="readonly")
    combo_servicio.grid(row=2, column=1, padx=10, pady=5)
    combo_servicio.set("Seleccione un servicio")

    ttk.Label(frame_form, text="Fecha (DD-MM-AAAA):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry_fecha = ttk.Entry(frame_form, width=25)
    entry_fecha.grid(row=3, column=1, padx=10, pady=5)

    ttk.Label(frame_form, text="Hora (HH:MM):").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    entry_hora = ttk.Entry(frame_form, width=25)
    entry_hora.grid(row=4, column=1, padx=10, pady=5)

    frame_botones = ttk.Frame(contenedor)
    frame_botones.grid(row=0, column=1, padx=30, pady=10, sticky="n")

    style = ttk.Style()
    style.configure("Accion.TButton", font=("Arial", 10, "bold"), padding=6)

    ttk.Button(frame_botones, text="Registrar", style="Accion.TButton", command=lambda: agregar_cita()).pack(fill="x", pady=5)
    ttk.Button(frame_botones, text="Editar", style="Accion.TButton", command=lambda: editar_cita()).pack(fill="x", pady=5)
    ttk.Button(frame_botones, text="Eliminar", style="Accion.TButton", command=lambda: eliminar_cita()).pack(fill="x", pady=5)
    ttk.Button(frame_botones, text="Actualizar lista", style="Accion.TButton", command=lambda: cargar_citas()).pack(fill="x", pady=5)
    ttk.Button(frame_botones, text="Salir", style="Accion.TButton", command=citas.destroy).pack(fill="x", pady=5)

    for col, text in zip(columns, ["ID", "Cliente", "Servicio", "Fecha", "Hora", "Estado"]):
        tabla.heading(col, text=text)
        tabla.column(col, width=120)
    tabla.pack(pady=20, fill="both", expand=True)

    def cargar_citas():
        tabla.delete(*tabla.get_children())
        try:
            con = get_conn()
            cur = con.cursor()
            cur.execute("SELECT * FROM barbershop_appointments ORDER BY appointment_date;")
            for row in cur.fetchall():
                tabla.insert("", tk.END, values=row)
            con.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las citas:\n{e}")

    def agregar_cita():
        id_cita = entry_id.get()
        name = entry_nombre.get()
        servicio = combo_servicio.get()
        fecha_input = entry_fecha.get()
        hora = entry_hora.get()

        if not id_cita or not name or not servicio or not fecha_input or not hora:
            messagebox.showwarning("Campos incompletos", "Todos los campos son obligatorios.")
            return

        try:
            fecha1 = datetime.strptime(fecha_input, "%d-%m-%Y")
            fecha = fecha1.strftime("%Y-%m-%d")
            servicio_id = servicio.split(" - ")[0]

            nueva_cita = Cita(name,fecha,hora)

            con = get_conn()
            cur = con.cursor()
            cur.execute("""
                INSERT INTO barbershop_appointments (id, client_name, service_id, appointment_date, appointment_time)
                VALUES (%s, %s, %s, %s, %s);
            """, (id_cita, name, servicio_id, fecha, hora))
            con.commit()
            con.close()

            messagebox.showinfo("Éxito", "Cita registrada correctamente.")
            cargar_citas()

            entry_id.config(state="normal")
            entry_id.delete(0, tk.END)
            entry_id.insert(0, id_creation("A"))
            entry_id.config(state="readonly")

        except ValueError:
            messagebox.showerror("Formato incorrecto", "La fecha tiene que ser formato DD-MM-AAAA")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la cita:\n{e}")

    def eliminar_cita():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una cita para eliminar.")
            return
        item = tabla.item(seleccion[0])
        id_cita = item["values"][0]
        try:
            con = get_conn()
            cur = con.cursor()
            cur.execute("DELETE FROM barbershop_appointments WHERE id = %s;", (id_cita,))
            con.commit()
            con.close()
            messagebox.showinfo("Éxito", "Cita eliminada correctamente.")
            cargar_citas()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la cita:\n{e}")

    def editar_cita():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una cita para editar.")
            return
        item = tabla.item(seleccion[0])
        id_cita = item["values"][0]
        nuevo_estado = messagebox.askquestion("Editar estado", "¿Marcar cita como completada?")
        if nuevo_estado == "si":
            try:
                con = get_conn()
                cur = con.cursor()
                cur.execute("UPDATE barbershop_appointments SET status = 'Completada' WHERE id = %s;", (id_cita,))
                con.commit()
                con.close()
                cargar_citas()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo editar la cita:\n{e}")

    cargar_citas()