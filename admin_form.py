import os
import tkinter as tk
from tkinter.messagebox import showerror
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import json
from pyuiWidgets.imageLabel import ImageLabel
import psycopg2
from general_processes import *
import datetime
import random

PASSWORD_FILE = "password.json"
DEFAULT_PASSWORD = "123"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Lord:
    def __init__(self):
        try:
            with open(PASSWORD_FILE, 'r') as f:
                data = json.load(f)
                self.__password = data.get("password", DEFAULT_PASSWORD)
        except (FileNotFoundError, json.JSONDecodeError):
            self.__password = DEFAULT_PASSWORD
            self._save_password()

    def _save_password(self):
        with open(PASSWORD_FILE, 'w') as p_file:
            json.dump({"password": self.__password}, p_file)

    @property
    def contra(self):
        return self.__password

    @contra.setter
    def contra(self, new_password):
        if new_password == self.__password:
            messagebox.showinfo("Error", "La contraseña no puede ser igual a la anterior")
        else:
            self.__password = new_password
            messagebox.showinfo("Éxito", "El cambio ha sido exitoso")


lord = Lord()



def get_info(frame, entry):
    temp_pass = entry.get()
    if temp_pass == lord.contra:
        frame.destroy()
        return admin_menu()
    else:
        frame.destroy()
        return login()


def login():
    login_form = tk.Tk()
    login_form.geometry("400x100")
    login_form.title("LOGIN")
    login_form.config(bg="#ffffff")

    gen_style = ttk.Style(login_form)
    gen_style.theme_use("clam")
    gen_style.configure("Custom.TButton",
                        background="#000000",
                        foreground="#ffffff",
                        font=('Arial', 10),
                        bordercolor="#000000",
                        darkcolor="#000000",
                        lightcolor="#333333",
                        padding=3)

    pass_label = tk.Label(login_form, text="CONTRASEÑA:", background="#ffffff", foreground="#000000")
    pass_label.grid(row=0, column=0, padx=10, pady=30, sticky="w")

    pass_text = tk.Entry(login_form, background="#000000", foreground="#ffffff", show="*")
    pass_text.grid(row=0, column=0, padx=100, pady=30, sticky="w")

    button_get = ttk.Button(login_form, text="Log In",
                            style="Custom.TButton",
                            command=lambda: get_info(login_form, pass_text))
    button_get.grid(row=0, column=0, padx=290, pady=(50, 10), sticky="ew")


def gen_report(fdate, sdate, treeview):
    if check_date(fdate.get()) and check_date(sdate.get()):
        gen_db_x.reports("SELECT * FROM sales_details WHERE sale_date BETWEEN %s AND %s;", (fdate.get(), sdate.get()), treeview)
    else:
        messagebox.showerror("ERROR", "Fecha inválida")


def reportes(menu, main_frame, frame_reportes, style, form):
    menu.select(frame_reportes)
    form.geometry("700x600")
    style.configure("Custom.TButton")

    frame_reportes.grid_columnconfigure(0, weight=0)
    frame_reportes.grid_columnconfigure(1, weight=1)

    first_date_label = tk.Label(frame_reportes, text="Fecha de inicio:", background="#000000", foreground="#ffffff")
    first_date_label.grid(row=0, column=0, padx=10, pady=5, sticky="nw")
    first_date_entry = tk.Entry(frame_reportes, background="#000000", foreground="#ffffff")
    first_date_entry.grid(row=0, column=1, padx=10, pady=5, sticky="new")
    first_date_entry.insert(0, "AAAA-MM-DD")

    second_date_label = tk.Label(frame_reportes, text="Fecha Final:", background="#000000", foreground="#ffffff")
    second_date_label.grid(row=1, column=0, padx=10, pady=5, sticky="nw")
    second_date_entry = tk.Entry(frame_reportes, background="#000000", foreground="#ffffff")
    second_date_entry.grid(row=1, column=1, padx=10, pady=5, sticky="new")
    second_date_entry.insert(0, "AAAA-MM-DD")

    report_table = ttk.Treeview(frame_reportes, columns=("1", "2", "3", "4", "5", "6", "7", "8"), show="headings")
    column_map = {"1": "ID", "2": "Venta", "3": "Cliente", "4": "Producto", "5": "Servicio", "6": "Fecha", "7": "Cantidad", "8": "Precio"}
    for col_id, text in column_map.items():
        report_table.heading(col_id, text=text, anchor=tk.CENTER)

    report_table.column("1", width=30, anchor=tk.CENTER, stretch=tk.NO)
    report_table.column("2", width=100, anchor=tk.CENTER)
    report_table.column("3", width=120, anchor=tk.W)
    report_table.column("4", width=120, anchor=tk.W)
    report_table.column("5", width=60, anchor=tk.E)
    report_table.column("6", width=60, anchor=tk.E)
    report_table.column("7", width=60, anchor=tk.E)
    report_table.column("8", width=60, anchor=tk.E)

    report_table.grid(row=2, column=0, columnspan=2, padx=10, pady=15, sticky="nsew")
    frame_reportes.grid_rowconfigure(3, weight=1)

    save_button = ttk.Button(frame_reportes, text="GENERAR", style="Custom.TButton",
                             command=lambda: gen_report(first_date_entry, second_date_entry, report_table))
    save_button.grid(row=4, column=0, columnspan=2, padx=200, pady=(10, 50), sticky="ew")

    exit_button = ttk.Button(frame_reportes, text="SALIR", style="Custom.TButton",
                             command=lambda: close_tabs(menu, main_frame, frame_reportes))
    exit_button.grid(row=5, column=0, columnspan=2, padx=200, pady=(10, 50), sticky="ew")

    menu.add(frame_reportes, text="REPORTES")
    menu.select(frame_reportes)


def close_tabs(menu, frame1, frame2):
    menu.select(frame1)
    menu.hide(frame2)


def check_date(date_str):
    try:
        temp_date = date_str.split("-")
        if len(temp_date) != 3:
            return False
        dd, mm, yyyy = temp_date[2], temp_date[1], temp_date[0]
        if (int(dd) > 31 or int(dd) < 1) or (int(mm) > 12 or int(mm) < 1) or (int(yyyy) > 9999 or int(yyyy) < 1):
            messagebox.showerror("ERROR", "Fecha inválida")
            return False
        return True
    except Exception:
        messagebox.showerror("ERROR", "Fecha inválida")
        return False



def add_new_prod(name_e, brand_e, categ_e, price_e, stock_e, supp_e):
    try:
        prod_name = name_e.get()
        prod_brand = brand_e.get()
        prod_category = categ_e.get()
        prod_price = float(price_e.get())
        prod_stock = int(stock_e.get())
        prod_supplier = supp_e.get()

        gen_db_x.execute("""
            INSERT INTO barbershop_products 
            (product_name, brand, category, price, stock_quantity, supplier) 
            VALUES (%s, %s, %s, %s, %s, %s); 
        """, (prod_name, prod_brand, prod_category, prod_price, prod_stock, prod_supplier))
        messagebox.showinfo("ÉXITO", f"Producto '{prod_name}' guardado con éxito.")
    except ValueError:
        messagebox.showerror("ERROR DE DATOS", "El Precio y la Cantidad deben ser números válidos.")
    except Exception as e:
        messagebox.showerror("ERROR AL AGREGAR PRODUCTOS", f"Error en la base de datos: {e}")


def agregar_producto(menu, main_frame, frame_add_prods, style):
    menu.select(frame_add_prods)
    style.configure("Custom.TButton")
    frame_add_prods.grid_columnconfigure(0, weight=0)
    frame_add_prods.grid_columnconfigure(1, weight=1)

    prodname_label = tk.Label(frame_add_prods, text="Nombre del producto:", background="#000000", foreground="#ffffff")
    prodname_label.grid(row=0, column=0, padx=10, pady=5, sticky="nw")
    prodname_entry = tk.Entry(frame_add_prods, background="#000000", foreground="#ffffff")
    prodname_entry.grid(row=0, column=1, padx=10, pady=5, sticky="new")

    brand_label = tk.Label(frame_add_prods, text="Marca:", background="#000000", foreground="#ffffff")
    brand_label.grid(row=1, column=0, padx=10, pady=5, sticky="nw")
    brand_entry = tk.Entry(frame_add_prods, background="#000000", foreground="#ffffff")
    brand_entry.grid(row=1, column=1, padx=10, pady=5, sticky="new")

    cat_label = tk.Label(frame_add_prods, text="Categoría:", background="#000000", foreground="#ffffff")
    cat_label.grid(row=2, column=0, padx=10, pady=5, sticky="nw")
    cat_entry = tk.Entry(frame_add_prods, background="#000000", foreground="#ffffff")
    cat_entry.grid(row=2, column=1, padx=10, pady=5, sticky="new")

    price_label = tk.Label(frame_add_prods, text="Precio:", background="#000000", foreground="#ffffff")
    price_label.grid(row=3, column=0, padx=10, pady=5, sticky="nw")
    price_entry = tk.Entry(frame_add_prods, background="#000000", foreground="#ffffff")
    price_entry.grid(row=3, column=1, padx=10, pady=5, sticky="new")

    stock_label = tk.Label(frame_add_prods, text="Cantidad:", background="#000000", foreground="#ffffff")
    stock_label.grid(row=4, column=0, padx=10, pady=5, sticky="nw")
    stock_entry = tk.Entry(frame_add_prods, background="#000000", foreground="#ffffff")
    stock_entry.grid(row=4, column=1, padx=10, pady=5, sticky="new")

    sup_label = tk.Label(frame_add_prods, text="Proveedor:", background="#000000", foreground="#ffffff")
    sup_label.grid(row=5, column=0, padx=10, pady=5, sticky="nw")
    sup_entry = tk.Entry(frame_add_prods, background="#000000", foreground="#ffffff")
    sup_entry.grid(row=5, column=1, padx=10, pady=5, sticky="new")

    frame_add_prods.grid_rowconfigure(6, weight=1)

    save_button = ttk.Button(frame_add_prods, text="GUARDAR", style="Custom.TButton",
                             command=lambda: add_new_prod(prodname_entry, brand_entry, cat_entry, price_entry, stock_entry, sup_entry))
    save_button.grid(row=7, column=0, columnspan=2, padx=200, pady=(10, 50), sticky="ew")

    exit_button = ttk.Button(frame_add_prods, text="SALIR", style="Custom.TButton",
                             command=lambda: close_tabs(menu, main_frame, frame_add_prods))
    exit_button.grid(row=8, column=0, columnspan=2, padx=200, pady=(10, 50), sticky="ew")

    menu.add(frame_add_prods, text="AGREGAR PRODUCTOS")
    menu.select(frame_add_prods)


def save_pass(entry1, entry2):
    if entry1.get() == entry2.get():
        lord.contra = entry1.get()
        lord._save_password()


def change_pass(menu, main_frame, password_frame, style):
    menu.select(password_frame)
    style.configure("Custom.TButton")
    password_frame.grid_columnconfigure(0, weight=0)
    password_frame.grid_columnconfigure(1, weight=1)

    pass_label = tk.Label(password_frame, text="Nueva Contraseña:", background="#000000", foreground="#ffffff")
    pass_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    pass_text = tk.Entry(password_frame, background="#000000", foreground="#ffffff", show="*")
    pass_text.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    c_pass_label = tk.Label(password_frame, text="Confirmación de Contraseña:", background="#000000", foreground="#ffffff")
    c_pass_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    c_pass_entry = tk.Entry(password_frame, background="#000000", foreground="#ffffff", show="*")
    c_pass_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    password_frame.grid_rowconfigure(2, weight=1)

    save_button = ttk.Button(password_frame, text="GUARDAR", style="Custom.TButton",
                             command=lambda: save_pass(pass_text, c_pass_entry))
    save_button.grid(row=3, column=0, padx=10, pady=(10, 10), sticky="w")

    exit_button = ttk.Button(password_frame, text="SALIR", style="Custom.TButton",
                             command=lambda: close_tabs(menu, main_frame, password_frame))
    exit_button.grid(row=3, column=1, padx=10, pady=(10, 10), sticky="e")



def add_svc(svcname_e, svcprice_e):
    try:
        svc_name = svcname_e.get()
        svc_price = float(svcprice_e.get())
        svc_id = id_creation("S")

        gen_db_x.execute("""
            INSERT INTO b_services 
            (id, name, price) 
            VALUES (%s, %s, %s); 
        """, (svc_id, svc_name, svc_price))
        messagebox.showinfo("ÉXITO", f"El servicio '{svc_name}' guardado con éxito.")
    except ValueError:
        messagebox.showerror("ERROR DE DATOS", "El Precio debe ser un número válido.")
    except Exception as e:
        messagebox.showerror("ERROR AL AGREGAR SERVICIOS", f"Error en la base de datos: {e}")


def add_service(menu, main_frame, new_service_frame, style):
    menu.select(new_service_frame)
    style.configure("Custom.TButton")

    new_service_frame.grid_columnconfigure(0, weight=0)
    new_service_frame.grid_columnconfigure(1, weight=1)

    svc_name_label = tk.Label(new_service_frame, text="Nombre del Servicio:", background="#000000", foreground="#ffffff")
    svc_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="nw")
    svc_name_entry = tk.Entry(new_service_frame, background="#000000", foreground="#ffffff")
    svc_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="new")

    svc_price_label = tk.Label(new_service_frame, text="Precio:", background="#000000", foreground="#ffffff")
    svc_price_label.grid(row=1, column=0, padx=10, pady=5, sticky="nw")
    svc_price_entry = tk.Entry(new_service_frame, background="#000000", foreground="#ffffff")
    svc_price_entry.grid(row=1, column=1, padx=10, pady=5, sticky="new")

    new_service_frame.grid_rowconfigure(6, weight=1)

    save_button = ttk.Button(new_service_frame, text="GUARDAR", style="Custom.TButton",
                             command=lambda: add_svc(svc_name_entry, svc_price_entry))
    save_button.grid(row=7, column=0, columnspan=2, padx=200, pady=(10, 50), sticky="ew")

    exit_button = ttk.Button(new_service_frame, text="SALIR", style="Custom.TButton",
                             command=lambda: close_tabs(menu, main_frame, new_service_frame))
    exit_button.grid(row=8, column=0, columnspan=2, padx=200, pady=(10, 50), sticky="ew")

    menu.add(new_service_frame, text="AGREGAR SERVICIO")
    menu.select(new_service_frame)



def cargar_productos(tabla):
    try:
        for item in tabla.get_children():
            tabla.delete(item)
        con = gen_db_x._get_conn()
        if con is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return
        cur = con.cursor()
        cur.execute("SELECT id, product_name, brand, category, price, stock_quantity, supplier FROM barbershop_products ORDER BY product_name ASC;")
        filas = cur.fetchall()
        con.close()
        for fila in filas:
            tabla.insert("", tk.END, values=fila)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los productos:\n{e}")


def cargar_servicios(tabla):
    try:
        for item in tabla.get_children():
            tabla.delete(item)
        con = gen_db_x._get_conn()
        if con is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return
        cur = con.cursor()
        cur.execute("SELECT id, name, price FROM b_services ORDER BY name ASC;")
        filas = cur.fetchall()
        con.close()
        for fila in filas:
            tabla.insert("", tk.END, values=fila)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los servicios:\n{e}")


def mod_elm_prods(menu, main_mod_m, m_e_p, style):
    menu.select(m_e_p)
    style.configure("Custom.TButton")

    m_e_p.grid_columnconfigure(0, weight=1)
    m_e_p.grid_rowconfigure(0, weight=1)

    columnas = ("ID", "Nombre", "Marca", "Categoría", "Precio", "Cantidad", "Proveedor")
    tabla = ttk.Treeview(m_e_p, columns=columnas, show="headings", height=14)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=110)
    tabla.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    frame_btn = tk.Frame(m_e_p, bg="#ffffff")
    frame_btn.grid(row=1, column=0, pady=10)

    def editar_producto():
        seleccionado = tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un producto para editar.")
            return
        valores = tabla.item(seleccionado, "values")
        id_prod = valores[0]

        edit_win = tk.Toplevel(m_e_p)
        edit_win.title("Editar producto")
        edit_win.geometry("420x360")
        edit_win.config(bg="#ffffff")

        campos = ["Nombre", "Marca", "Categoría", "Precio", "Cantidad", "Proveedor"]
        entries = {}
        for i, campo in enumerate(campos):
            tk.Label(edit_win, text=campo + ":", bg="#ffffff").grid(row=i, column=0, padx=10, pady=6, sticky="w")
            e = tk.Entry(edit_win, bg="#000000", fg="#ffffff", width=30)
            e.grid(row=i, column=1, padx=10, pady=6, sticky="w")
            e.insert(0, valores[i+1])
            entries[campo] = e

        def guardar_cambios():
            try:
                con = gen_db_x._get_conn()
                cur = con.cursor()
                cur.execute("""
                    UPDATE barbershop_products
                    SET product_name=%s, brand=%s, category=%s, price=%s, stock_quantity=%s, supplier=%s
                    WHERE id=%s;
                """, (
                    entries["Nombre"].get(),
                    entries["Marca"].get(),
                    entries["Categoría"].get(),
                    float(entries["Precio"].get()),
                    int(entries["Cantidad"].get()),
                    entries["Proveedor"].get(),
                    id_prod
                ))
                con.commit()
                con.close()
                messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
                edit_win.destroy()
                cargar_productos(tabla)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el producto:\n{e}")

        ttk.Button(edit_win, text="Guardar cambios", style="Custom.TButton", command=guardar_cambios).grid(row=len(campos), column=0, columnspan=2, pady=15)

    def eliminar_producto():
        seleccionado = tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un producto para eliminar.")
            return
        valores = tabla.item(seleccionado, "values")
        id_prod = valores[0]
        if messagebox.askyesno("Confirmar", f"¿Eliminar el producto '{valores[1]}'?"):
            try:
                con = gen_db_x._get_conn()
                cur = con.cursor()
                cur.execute("DELETE FROM barbershop_products WHERE id=%s;", (id_prod,))
                con.commit()
                con.close()
                messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
                cargar_productos(tabla)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el producto:\n{e}")

    ttk.Button(frame_btn, text="Editar", style="Custom.TButton", command=editar_producto).pack(side="left", padx=8)
    ttk.Button(frame_btn, text="Eliminar", style="Custom.TButton", command=eliminar_producto).pack(side="left", padx=8)
    ttk.Button(frame_btn, text="Actualizar lista", style="Custom.TButton", command=lambda: cargar_productos(tabla)).pack(side="left", padx=8)
    ttk.Button(frame_btn, text="Volver", style="Custom.TButton", command=lambda: close_tabs(menu, main_mod_m, m_e_p)).pack(side="left", padx=8)

    cargar_productos(tabla)


def mod_elm_svcs(menu, main_mod_m, m_e_s, style):
    menu.select(m_e_s)
    style.configure("Custom.TButton")

    m_e_s.grid_columnconfigure(0, weight=1)
    m_e_s.grid_rowconfigure(0, weight=1)

    columnas = ("ID", "Servicio", "Precio")
    tabla = ttk.Treeview(m_e_s, columns=columnas, show="headings", height=14)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=150)
    tabla.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    frame_btn = tk.Frame(m_e_s, bg="#ffffff")
    frame_btn.grid(row=1, column=0, pady=10)

    def editar_servicio():
        seleccionado = tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un servicio para editar.")
            return
        valores = tabla.item(seleccionado, "values")
        id_svc = valores[0]

        edit_win = tk.Toplevel(m_e_s)
        edit_win.title("Editar servicio")
        edit_win.geometry("360x220")
        edit_win.config(bg="#ffffff")

        tk.Label(edit_win, text="Nombre:", bg="#ffffff").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        name_e = tk.Entry(edit_win, bg="#000000", fg="#ffffff", width=30)
        name_e.grid(row=0, column=1, padx=10, pady=8, sticky="w")
        name_e.insert(0, valores[1])

        tk.Label(edit_win, text="Precio:", bg="#ffffff").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        price_e = tk.Entry(edit_win, bg="#000000", fg="#ffffff", width=30)
        price_e.grid(row=1, column=1, padx=10, pady=8, sticky="w")
        price_e.insert(0, valores[2])

        def guardar_svc():
            try:
                con = gen_db_x._get_conn()
                cur = con.cursor()
                cur.execute("UPDATE b_services SET name=%s, price=%s WHERE id=%s;", (name_e.get(), float(price_e.get()), id_svc))
                con.commit()
                con.close()
                messagebox.showinfo("Éxito", "Servicio actualizado correctamente.")
                edit_win.destroy()
                cargar_servicios(tabla)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el servicio:\n{e}")

        ttk.Button(edit_win, text="Guardar cambios", style="Custom.TButton", command=guardar_svc).grid(row=2, column=0, columnspan=2, pady=12)

    def eliminar_servicio():
        seleccionado = tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Selecciona un servicio para eliminar.")
            return
        valores = tabla.item(seleccionado, "values")
        id_svc = valores[0]
        if messagebox.askyesno("Confirmar", f"¿Eliminar el servicio '{valores[1]}'?"):
            try:
                gen_db_x.execute("DELETE FROM b_services WHERE id=%s;", (id_svc,))
                messagebox.showinfo("Éxito", "Servicio eliminado correctamente.")
                cargar_servicios(tabla)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el servicio:\n{e}")

    ttk.Button(frame_btn, text="Editar", style="Custom.TButton", command=editar_servicio).pack(side="left", padx=8)
    ttk.Button(frame_btn, text="Eliminar", style="Custom.TButton", command=eliminar_servicio).pack(side="left", padx=8)
    ttk.Button(frame_btn, text="Actualizar lista", style="Custom.TButton", command=lambda: cargar_servicios(tabla)).pack(side="left", padx=8)
    ttk.Button(frame_btn, text="Volver", style="Custom.TButton", command=lambda: close_tabs(menu, main_mod_m, m_e_s)).pack(side="left", padx=8)

    cargar_servicios(tabla)


def modify_eliminate(menu, main_frame, style):
    mod_prods = ttk.Frame(menu)
    mod_prods.pack(expand=True, fill="both")
    menu.add(mod_prods, text="MODIFICAR/ELIMINAR", state="hidden")

    prod_mod_e = ttk.Frame(menu)
    prod_mod_e.pack(expand=True, fill="both")
    menu.add(prod_mod_e, text="PRODUCTOS MODIFICAR/ELIMINAR", state="hidden")

    svc_mod_e = ttk.Frame(menu)
    svc_mod_e.pack(expand=True, fill="both")
    menu.add(svc_mod_e, text="SERVICIOS MODIFICAR/ELIMINAR", state="hidden")

    menu.select(mod_prods)
    style.configure("Custom.TButton")

    mod_prods.grid_columnconfigure(0, weight=0)
    mod_prods.grid_columnconfigure(1, weight=1)
    mod_prods.grid_rowconfigure(6, weight=1)

    ttk.Button(mod_prods, text="PRODUCTOS", style="Custom.TButton",
               command=lambda: mod_elm_prods(menu, main_frame, prod_mod_e, style)).grid(row=1, column=0, columnspan=2, padx=200, pady=(10, 50), sticky="ew")

    ttk.Button(mod_prods, text="SERVICIOS", style="Custom.TButton",
               command=lambda: mod_elm_svcs(menu, main_frame, svc_mod_e, style)).grid(row=2, column=0, columnspan=2, padx=200, pady=(10, 50), sticky="ew")

    ttk.Button(mod_prods, text="SALIR", style="Custom.TButton",
               command=lambda: close_tabs(menu, main_frame, mod_prods)).grid(row=3, column=0, columnspan=2, padx=200, pady=(10, 50), sticky="ew")


def admin_menu():
    admin_form = tk.Tk()
    admin_form.title("Administrador")
    admin_form.geometry("700x600")
    admin_form.config(bg="#ffffff")
    admin_style = ttk.Style(admin_form)
    admin_style.theme_use("clam")

    admin_style.configure("Custom.TButton", background="#000000", foreground="#ffffff", font=('Arial', 10), bordercolor="#000000", darkcolor="#000000", lightcolor="#333333", padding=10)

    inside_menu = ttk.Notebook(admin_form)
    inside_menu.pack(expand=True, fill="both", padx=10, pady=10)

    frame_menu_inicial = ttk.Frame(inside_menu)
    frame_menu_inicial.pack(expand=True, fill="both")
    inside_menu.add(frame_menu_inicial, text=" Menú Principal ")

    frame_add_prods = ttk.Frame(inside_menu)
    frame_add_prods.pack(expand=True, fill="both")
    inside_menu.add(frame_add_prods, text="AGREGAR PRODUCTOS", state="hidden")

    frame_add_svc = ttk.Frame(inside_menu)
    frame_add_svc.pack(expand=True, fill="both")
    inside_menu.add(frame_add_svc, text="AGREGAR SERVICIO", state="hidden")

    frame_reports = ttk.Frame(inside_menu)
    frame_reports.pack(expand=True, fill="both")
    inside_menu.add(frame_reports, text="REPORTES", state="hidden")

    frame_cambio_c = ttk.Frame(inside_menu)
    frame_cambio_c.pack(expand=True, fill="both")
    inside_menu.add(frame_cambio_c, text="CAMBIAR CONTRASEÑA", state="hidden")

    admin_style.configure("label.TLabel", background="#E4E2E2", foreground="#000", anchor="center")

    ttk.Button(frame_menu_inicial, text="AGREGAR PRODUCTO", style="Custom.TButton",
               command=lambda: agregar_producto(inside_menu, frame_menu_inicial, frame_add_prods, admin_style)).grid(row=0, column=0, padx=250, pady=(50, 10), sticky="ew")

    ttk.Button(frame_menu_inicial, text="AGREGAR SERVICIO", style="Custom.TButton",
               command=lambda: add_service(inside_menu, frame_menu_inicial, frame_add_svc, admin_style)).grid(row=1, column=0, padx=250, pady=10, sticky="ew")

    ttk.Button(frame_menu_inicial, text="CAMBIAR CONTRASEÑA", style="Custom.TButton",
               command=lambda: change_pass(inside_menu, frame_menu_inicial, frame_cambio_c, admin_style)).grid(row=2, column=0, padx=250, pady=10, sticky="ew")

    ttk.Button(frame_menu_inicial, text="REPORTES", style="Custom.TButton",
               command=lambda: reportes(inside_menu, frame_menu_inicial, frame_reports, admin_style, admin_form)).grid(row=3, column=0, padx=250, pady=10, sticky="ew")

    ttk.Button(frame_menu_inicial, text="MODIFICAR/ELIMINAR REGISTROS", style="Custom.TButton",
               command=lambda: modify_eliminate(inside_menu, frame_menu_inicial, admin_style)).grid(row=4, column=0, padx=250, pady=10, sticky="ew")

    ttk.Button(frame_menu_inicial, text="SALIR", style="Custom.TButton",
               command=lambda: admin_form.destroy()).grid(row=5, column=0, padx=250, pady=10, sticky="ew")

    admin_form.mainloop()

if __name__ == "__main__":
    login()
