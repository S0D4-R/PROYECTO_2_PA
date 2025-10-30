import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from admin_form import *
from general_processes import *
from pyuiWidgets.imageLabel import ImageLabel

def products_menu():
    products_form = tk.Tk()
    products_form.title("PRODUCTOS")
    products_form.geometry("1780x720")
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

    #Configurar el estilo de los ENCABEZADOS (T.Heading)
    admin_style.configure("Treeview.Heading",
                          background="#333333",
                          foreground="#ffffff",
                          font=('Arial', 10, 'bold'))


    admin_style.map('Treeview',
                    background=[('selected', '#333333')],
                    foreground=[('selected', '#ffffff')])

    #Crear el Treeview
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

    main_table.column("1", width=30, anchor=tk.CENTER, stretch=tk.NO)

    main_table.column("2", width=150, anchor=tk.W, stretch=tk.YES)

    main_table.column("3", width=80, anchor=tk.W)
    main_table.column("4", width=80, anchor=tk.W)
    main_table.column("5", width=60, anchor=tk.CENTER)
    main_table.column("6", width=50, anchor=tk.CENTER)
    main_table.column("7", width=120, anchor=tk.W)
    main_table.column("8", width=100, anchor=tk.CENTER)
    main_table.column("9", width=100, anchor=tk.CENTER)

    main_table.pack(expand=True, fill='both')

    # Mostrar productos
    gen_db_x.displayDB("SELECT id, product_name, brand, category, price, stock_quantity, supplier, date_added, last_updated FROM barbershop_products;", main_table)

    boton_salir = ttk.Button(
        master=products_form,
        text="Volver al Menu",
        style="salir.TButton",
        command=lambda: products_form.destroy()
    )
    boton_salir.place(x=20, y=320, width=100, height=35)