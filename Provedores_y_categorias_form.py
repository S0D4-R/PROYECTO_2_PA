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


def categories_menu():
    win = tk.Toplevel()
    win.title("Gestión de Categorías")
    win.geometry("500x400")
    win.config(bg="#ffffff")

    tk.Label(win, text="Gestión de Categorías", bg="#ffffff", font=("Arial", 14, "bold")).pack(pady=10)

    frame = tk.Frame(win, bg="#ffffff")
    frame.pack(pady=15)

    tk.Label(frame, text="Nombre de Categoría:", bg="#ffffff").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    entry_name = tk.Entry(frame, width=40)
    entry_name.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame, text="Descripción:", bg="#ffffff").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_desc = tk.Entry(frame, width=40)
    entry_desc.grid(row=1, column=1, padx=5, pady=5)

    def agregar_categoria():
        try:
            nombre = entry_name.get().strip()
            desc = entry_desc.get().strip()
            if not nombre:
                messagebox.showwarning("Atención", "Debe ingresar un nombre para la categoría.")
                return

            id_cat = id_creation("B")

            con = gen_db_x._get_conn()
            cur = con.cursor()
            cur.execute("INSERT INTO b_categories (id, category_name, description, created_at) VALUES (%s, %s, %s, NOW());",
                        (id_cat, nombre, desc))
            con.commit()
            con.close()

            messagebox.showinfo("Éxito", "Categoría agregada correctamente.")
            entry_name.delete(0, tk.END)
            entry_desc.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la categoría:\n{e}")

    ttk.Button(win, text="Agregar Categoría", command=agregar_categoria).pack(pady=10)
    ttk.Button(win, text="Cerrar", command=win.destroy).pack(pady=5)
