import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from admin_form import *
from pyuiWidgets.imageLabel import ImageLabel

get_conn()
init_db()

def products_menu():
    products_form = tk.Tk()
    products_form.title("PRODUCTOS")
    products_form.geometry("700x400")
    products_form.config(bg="#ffffff")


    #Treeview
    admin_style = ttk.Style(products_form)
    admin_style.theme_use("clam")
    admin_style.configure("Treeview",
                          background="#000000",
                          foreground="#ffffff",
                          fieldbackground="#000000",
                          bordercolor="#000000",
                          rowheight=25)

    # 2. Configurar el estilo de los ENCABEZADOS (T.Heading)
    admin_style.configure("Treeview.Heading",
                          background="#333333",
                          foreground="#ffffff",
                          font=('Arial', 10, 'bold'))


    admin_style.map('Treeview',
                    background=[('selected', '#333333')],
                    foreground=[('selected', '#ffffff')])

    # 4. Crear el Treeview
    main_table = ttk.Treeview(products_form,
                              columns=("1", "2", "3", "4", "5", "6", "7", "8","9"), show="headings")
    main_table.heading("1", text="ID")
    main_table.heading("2", text="Producto")
    main_table.heading("3", text="Marca")
    main_table.heading("4", text="Tipo")
    main_table.heading("5", text="Precio")
    main_table.heading("6", text="Stock")
    main_table.heading("7", text="Proveedor")
    main_table.heading("8", text="Agregado")
    main_table.heading("9", text="Modificado")
    main_table.pack(expand=True, fill='both')
    #Mostrar productos
    try:
        con = get_conn()
        cur = con.cursor()
        cur.execute("SELECT id, product_name, brand, category, price, stock_quantity, supplier, date_added, last_updated FROM barbershop_products;")
        products_in_db = cur.fetchall()
        con.close()
        """ 
        text_area.delete("1.0", tk.END)
        for p in pacientes:
            text_area.insert(
                tk.END,
                f"ID: {p[0]} | Nombre: {p[1]} | Estado: {p[2]} | Edad: {p[3]} | DPI: {p[4]}\n"
            )
        """
    except Exception as e:
        messagebox.showerror("Error de BD", str(e))



    boton_salir = ttk.Button(
        master=products_form,
        text="Volver al Menu",
        style="salir.TButton",
        command=lambda: products_form.destroy()
    )
    boton_salir.place(x=20, y=320, width=100, height=35)