import tkinter as tk
from tkinter import ttk, messagebox
from general_processes import gen_db_x, id_creation
import datetime

def centrar_ventana(ventana, ancho, alto):

    ventana.update_idletasks()
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    center_x = (screen_width // 2) - (ancho // 2)
    center_y = (screen_height // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{center_x}+{center_y}")

def categories_menu():
    cat = tk.Toplevel()
    cat.title("Gestión de Categorías")
    cat.geometry("500x350")
    cat.config(bg="#ffffff")
    centrar_ventana(cat, 500, 350)

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
                "INSERT INTO product_categories (id, category_name, description) VALUES (%s, %s, %s)",
                (id_categoria, nombre, descripcion)
            )
            con.commit()
            con.close()

            messagebox.showinfo("Éxito", f"Categoría agregada correctamente.\nID generado: {id_categoria}")
            name_entry.delete(0, tk.END)
            desc_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la categoría:\n{e}")

    ttk.Button(cat, text="Guardar", command=guardar_categoria).pack(pady=10)
    ttk.Button(cat, text="Editar/Eliminar registros", command=manage_categories).pack(pady=5)
    ttk.Button(cat, text="Volver al menú", command= cat.destroy).pack(pady=5)

    cat.mainloop()
def manage_categories():
    cat = tk.Toplevel()
    cat.title("Editar / Eliminar Categorías")
    cat.geometry("600x400")
    cat.config(bg="#ffffff")
    centrar_ventana(cat, 600, 400)

    columnas = ("ID", "Nombre", "Descripción")
    tabla = ttk.Treeview(cat, columns=columnas, show="headings", height=10)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=180, anchor="center")
    tabla.pack(padx=10, pady=10, fill="both", expand=True)

    def cargar_categorias():
        for item in tabla.get_children():
            tabla.delete(item)
        try:
            con = gen_db_x._get_conn()
            cur = con.cursor()
            cur.execute("SELECT id, category_name, description FROM product_categories ORDER BY category_name ASC;")
            filas = cur.fetchall()
            con.close()
            for fila in filas:
                tabla.insert("", tk.END, values=fila)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las categorías:\n{e}")

    def editar_categoria():
        seleccionado = tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona una categoría para editar.")
            return
        valores = tabla.item(seleccionado, "values")
        id_cat = valores[0]

        edit = tk.Toplevel(cat)
        edit.title("Editar Categoría")
        edit.geometry("400x250")
        edit.config(bg="#ffffff")

        tk.Label(edit, text="Nombre:", bg="#ffffff").pack(pady=5)
        name_e = tk.Entry(edit, width=40)
        name_e.pack(pady=5)
        name_e.insert(0, valores[1])

        tk.Label(edit, text="Descripción:", bg="#ffffff").pack(pady=5)
        desc_e = tk.Entry(edit, width=40)
        desc_e.pack(pady=5)
        desc_e.insert(0, valores[2])

        def guardar_cambios():
            try:
                con = gen_db_x._get_conn()
                cur = con.cursor()
                cur.execute(
                    "UPDATE product_categories SET category_name=%s, description=%s WHERE id=%s;",
                    (name_e.get(), desc_e.get(), id_cat)
                )
                con.commit()
                con.close()
                messagebox.showinfo("Éxito", "Categoría actualizada correctamente.")
                edit.destroy()
                cargar_categorias()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar la categoría:\n{e}")

        ttk.Button(edit, text="Guardar", command=guardar_cambios).pack(pady=10)

    def eliminar_categoria():
        seleccionado = tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona una categoría para eliminar.")
            return
        valores = tabla.item(seleccionado, "values")
        id_cat = valores[0]
        if messagebox.askyesno("Confirmar", f"¿Eliminar la categoría '{valores[1]}'?"):
            try:
                con = gen_db_x._get_conn()
                cur = con.cursor()
                cur.execute("DELETE FROM product_categories WHERE id=%s;", (id_cat,))
                con.commit()
                con.close()
                messagebox.showinfo("Éxito", "Categoría eliminada correctamente.")
                cargar_categorias()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la categoría:\n{e}")

    frame_btn = tk.Frame(cat, bg="#ffffff")
    frame_btn.pack(pady=10)

    ttk.Button(frame_btn, text="Editar", command=editar_categoria).pack(side="left", padx=5)
    ttk.Button(frame_btn, text="Eliminar", command=eliminar_categoria).pack(side="left", padx=5)
    ttk.Button(frame_btn, text="Actualizar", command=cargar_categorias).pack(side="left", padx=5)
    ttk.Button(frame_btn, text="Cerrar", command=cat.destroy).pack(side="left", padx=5)

    cargar_categorias()


def providers_menu():
    provedores = tk.Toplevel()
    provedores.title("Gestión de Proveedores")
    provedores.geometry("500x400")
    provedores.config(bg="#ffffff")
    centrar_ventana(provedores, 600, 400)

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
            cur.execute("INSERT INTO product_providers (id, provider_name, contact_email, phone_number) VALUES (%s, %s, %s, %s);",
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
    ttk.Button(provedores, text="Editar/Eliminar registros", command=manage_providers).pack(pady=5)
    ttk.Button(provedores, text="volver al Menu", command=provedores.destroy).pack(pady=5)

def manage_providers():
    prov = tk.Toplevel()
    prov.title("Editar / Eliminar Proveedores")
    prov.geometry("700x400")
    prov.config(bg="#ffffff")
    centrar_ventana(prov, 600, 400)

    columnas = ("ID", "Nombre", "Correo", "Teléfono")
    tabla = ttk.Treeview(prov, columns=columnas, show="headings", height=10)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=160, anchor="center")
    tabla.pack(padx=10, pady=10, fill="both", expand=True)

    def cargar_proveedores():
        for item in tabla.get_children():
            tabla.delete(item)
        try:
            con = gen_db_x._get_conn()
            cur = con.cursor()
            cur.execute("SELECT id, provider_name, contact_email, phone_number FROM product_providers ORDER BY provider_name ASC;")
            filas = cur.fetchall()
            con.close()
            for fila in filas:
                tabla.insert("", tk.END, values=fila)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los proveedores:\n{e}")

    def editar_proveedor():
        seleccionado = tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un proveedor para editar.")
            return
        valores = tabla.item(seleccionado, "values")
        id_prov = valores[0]

        edit = tk.Toplevel(prov)
        edit.title("Editar Proveedor")
        edit.geometry("400x300")
        edit.config(bg="#ffffff")

        tk.Label(edit, text="Nombre:", bg="#ffffff").pack(pady=5)
        name_e = tk.Entry(edit, width=40)
        name_e.pack(pady=5)
        name_e.insert(0, valores[1])

        tk.Label(edit, text="Correo electrónico:", bg="#ffffff").pack(pady=5)
        email_e = tk.Entry(edit, width=40)
        email_e.pack(pady=5)
        email_e.insert(0, valores[2])

        tk.Label(edit, text="Teléfono:", bg="#ffffff").pack(pady=5)
        phone_e = tk.Entry(edit, width=40)
        phone_e.pack(pady=5)
        phone_e.insert(0, valores[3])

        def guardar_cambios():
            try:
                con = gen_db_x._get_conn()
                cur = con.cursor()
                cur.execute(
                    "UPDATE product_providers SET provider_name=%s, contact_email=%s, phone_number=%s WHERE id=%s;",
                    (name_e.get(), email_e.get(), phone_e.get(), id_prov)
                )
                con.commit()
                con.close()
                messagebox.showinfo("Éxito", "Proveedor actualizado correctamente.")
                edit.destroy()
                cargar_proveedores()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el proveedor:\n{e}")

        ttk.Button(edit, text="Guardar", command=guardar_cambios).pack(pady=10)

    def eliminar_proveedor():
        seleccionado = tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un proveedor para eliminar.")
            return
        valores = tabla.item(seleccionado, "values")
        id_prov = valores[0]
        if messagebox.askyesno("Confirmar", f"¿Eliminar el proveedor '{valores[1]}'?"):
            try:
                con = gen_db_x._get_conn()
                cur = con.cursor()
                cur.execute("DELETE FROM product_providers WHERE id=%s;", (id_prov,))
                con.commit()
                con.close()
                messagebox.showinfo("Éxito", "Proveedor eliminado correctamente.")
                cargar_proveedores()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el proveedor:\n{e}")

    frame_btn = tk.Frame(prov, bg="#ffffff")
    frame_btn.pack(pady=10)

    ttk.Button(frame_btn, text="Editar", command=editar_proveedor).pack(side="left", padx=5)
    ttk.Button(frame_btn, text="Eliminar", command=eliminar_proveedor).pack(side="left", padx=5)
    ttk.Button(frame_btn, text="Actualizar", command=cargar_proveedores).pack(side="left", padx=5)
    ttk.Button(frame_btn, text="Cerrar", command=prov.destroy).pack(side="left", padx=5)

    cargar_proveedores()

