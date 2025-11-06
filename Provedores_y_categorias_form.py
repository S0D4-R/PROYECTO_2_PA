import tkinter as tk
from tkinter import ttk, messagebox
from general_processes import gen_db_x, id_creation
import datetime

def categories_menu():
    cat = tk.Toplevel()
    cat.title("Gestión de Categorías")
    cat.geometry("500x350")
    cat.config(bg="#ffffff")

    tk.Label(cat, text="Agregar Nueva Categoría", font=("Arial", 14, "bold"), bg="#F5F1F0").pack(pady=15)
    tk.Label(cat, text="Nombre de categoría:", bg="#F5F1F0", anchor="w").pack(fill="x", padx=20)
    name_entry = tk.Entry(cat)
    name_entry.pack(fill="x", padx=20, pady=5)

    tk.Label(cat, text="Descripción:", bg="#F5F1F0", anchor="w").pack(fill="x", padx=20)
    desc_entry = tk.Entry(cat)
    desc_entry.pack(fill="x", padx=20, pady=5)

    def guardar_categoria():
        nombre = name_entry.get().strip()
        descripcion = desc_entry.get().strip()

        if nombre == "" or descripcion == "":
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        try:
            id_categoria = id_creation("B")
            con = gen_db_x._get_conn()
            cur = con.cursor()
            cur.execute(
                "INSERT INTO b_categories (id, category_name, description, created_at) VALUES (%s, %s, %s, %s)",
                (id_categoria, nombre, descripcion, datetime.datetime.now())
            )
            con.commit()
            con.close()

            messagebox.showinfo("Éxito", f"Categoría agregada correctamente.\nID generado: {id_categoria}")
            name_entry.delete(0, tk.END)
            desc_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la categoría:\n{e}")

    ttk.Button(cat, text="Guardar", command=guardar_categoria).pack(pady=10)
    ttk.Button(cat, text="Volver al menú", command= cat.destroy).pack(pady=5)

    cat.mainloop()


def providers_menu():
    provedores = tk.Toplevel()
    provedores.title("Gestión de Proveedores")
    provedores.geometry("500x400")
    provedores.config(bg="#ffffff")

    tk.Label(provedores, text="Gestión de Proveedores", bg="#F5F1F0", font=("Arial", 14, "bold")).pack(pady=10)

    frame = tk.Frame(provedores, bg="#F5F1F0")
    frame.pack(pady=15)

    tk.Label(frame, text="Nombre del Proveedor:", bg="#F5F1F0").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    entry_name = tk.Entry(frame, width=40)
    entry_name.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame, text="Correo Electrónico:", bg="#F5F1F0").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_email = tk.Entry(frame, width=40)
    entry_email.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame, text="Número de Teléfono:", bg="#F5F1F0").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    entry_phone = tk.Entry(frame, width=40)
    entry_phone.grid(row=2, column=1, padx=5, pady=5)

    def agregar_proveedor():
        try:
            nombre = entry_name.get().strip()
            email = entry_email.get().strip()
            telefono = entry_phone.get().strip()

            if not nombre or not email or not telefono:
                messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
                return
            id_prov = id_creation("P")
            con = gen_db_x._get_conn()
            cur = con.cursor()
            cur.execute("INSERT INTO b_providers (id, provider_name, contact_email, phone_number) VALUES (%s, %s, %s, %s);",
                        (id_prov, nombre, email, telefono))
            con.commit()
            con.close()

            messagebox.showinfo("Éxito", "Proveedor agregado correctamente.")
            entry_name.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            entry_phone.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el proveedor:\n{e}")

    ttk.Button(provedores, text="Agregar Proveedor", command=agregar_proveedor).pack(pady=10)
    ttk.Button(provedores, text="volver al Menu", command=provedores.destroy).pack(pady=5)