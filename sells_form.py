import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from pyuiWidgets.imageLabel import ImageLabel
from tkinter import ttk, messagebox
from datetime import date
from general_processes import *
from appointments_form import appointment_db
from tkinter import simpledialog
import random
import datetime

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    center_x = (screen_width // 2) - (ancho // 2)
    center_y = (screen_height // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{center_x}+{center_y}")

class DataBase_Sells(DataBaseX):
    def c_in_c(self, nit, name):
        con = self._get_conn()
        cur = con.cursor()
        client_id = id_creation("C")
        if nit == "":
            nit = "CF"
            cur.execute(
                "INSERT INTO b_clients (id, c_nit, client_name) VALUES (%s, %s, %s)",
                (client_id, nit, name)
            )
            con.commit()
        else:
            cur.execute("SELECT id FROM b_clients WHERE c_nit = %s", (nit,))
            cliente_existente = cur.fetchone()
            if cliente_existente:
                client_id = cliente_existente[0]
            else:
                client_id = id_creation("C")
                cur.execute(
                    "INSERT INTO b_clients (id, c_nit, client_name) VALUES (%s, %s, %s)",
                    (client_id, nit, name)
                )
                con.commit()

        con.close()
        return client_id

    def cobro(self, carrito, sale_id, client_id, fecha, total):
        con = self._get_conn()
        cur = con.cursor()

        cur.execute("INSERT INTO barbershop_sales (id, client_b) VALUES (%s, %s)", (sale_id, client_id))

        for idx, item in enumerate(carrito):
            tipo, item_id, nombre, precio, cantidad, subtotal = item

            if tipo == "P":
                cur.execute("""
                                    INSERT INTO sales_details (sale_id, client_id, product_id, service_id, sale_date, quantity_sold, service_price)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                                """, (sale_id, client_id, item_id, None, fecha, cantidad, precio))
                cur.execute("""
                               UPDATE barbershop_products
                               SET stock_quantity = stock_quantity - %s
                               WHERE id = %s
                           """, (cantidad, item_id))
            else:
                cur.execute("""
                                    INSERT INTO sales_details (sale_id, client_id, product_id, service_id, sale_date, quantity_sold, service_price)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                                """, (sale_id, client_id, None, item_id, fecha, 1, precio))

        con.commit()
        con.close()
        messagebox.showinfo("Éxito", f"Venta registrada exitosamente.\nTotal: Q{total:.2f}")


sales_db = DataBase_Sells()

def sells_menu():
    def obtener_client_info():
        cliente = tk.Toplevel()
        cliente.title("Datos del Cliente")
        cliente.geometry("400x250")
        cliente.config(bg="#ffffff")
        centrar_ventana(cliente,500,350)

        tk.Label(cliente, text="NIT del Cliente:", bg="#ffffff").pack(pady=5)
        nit_entry = tk.Entry(cliente)
        nit_entry.pack(pady=5)

        tk.Label(cliente, text="Nombre del Cliente:", bg="#ffffff").pack(pady=5)
        name_entry = tk.Entry(cliente)
        name_entry.pack(pady=5)

        def continuar():
            nit = nit_entry.get().strip()
            nombre = name_entry.get().strip()

            if not nombre:
                messagebox.showwarning("Advertencia", "Debe ingresar el nombre del cliente.")
                return

            try:
                client_id = sales_db.c_in_c(nit, nombre)
                cliente.destroy()
                abrir_ventana_ventas(client_id, nombre)

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar el cliente:\n{e}")

        tk.Button(cliente, text="Continuar", command=continuar, bg="#4CAF50", fg="white").pack(pady=20)

    def abrir_ventana_ventas(client_id, client_name):
        ventas = tk.Toplevel()
        ventas.title("Registro de Ventas")
        ventas.geometry("800x500")
        ventas.config(bg="#ffffff")
        centrar_ventana(ventas,800,500)

        tk.Label(ventas, text=f"Cliente: {client_name}", bg="#ffffff", font=("Arial", 12, "bold")).pack(pady=10)

        productos = appointment_db.iterable_db("SELECT id, product_name, price FROM barbershop_products")

        servicios = appointment_db.iterable_db("SELECT id, name, price FROM b_services")

        tipo_var = tk.StringVar()
        tipo_combo = ttk.Combobox(ventas, textvariable=tipo_var, values=["Producto", "Servicio"], state="readonly")
        tipo_combo.set("Producto")
        tipo_combo.pack(pady=10)


        item_var = tk.StringVar()
        item_combo = ttk.Combobox(ventas, textvariable=item_var, width=50)
        item_combo.pack(pady=10)

        def actualizar_items(*args):
            if tipo_var.get() == "Producto":
                item_combo["values"] = [f"{p[1]} - Q{p[2]}" for p in productos]
            else:
                item_combo["values"] = [f"{s[1]} - Q{s[2]}" for s in servicios]

        tipo_combo.bind("<<ComboboxSelected>>", actualizar_items)
        actualizar_items()

        tk.Label(ventas, text="Cantidad:").pack()
        cantidad_entry = tk.Entry(ventas)
        cantidad_entry.pack(pady=5)
        cantidad_entry.insert(0, "1")


        tabla = ttk.Treeview(ventas, columns=("item", "precio", "cantidad", "subtotal"), show="headings")
        tabla.heading("item", text="Producto/Servicio")
        tabla.heading("precio", text="Precio Unitario")
        tabla.heading("cantidad", text="Cantidad")
        tabla.heading("subtotal", text="Subtotal")
        tabla.pack(pady=10, fill="x")

        carrito = []

        def agregar_item():
            seleccion = item_combo.get()
            cantidad = cantidad_entry.get()

            if not seleccion or not cantidad.isdigit():
                messagebox.showwarning("Advertencia", "Seleccione un ítem y una cantidad válida.")
                return

            cantidad = int(cantidad)

            if tipo_var.get() == "Producto":
                index = item_combo.current()
                item_id, nombre, precio = productos[index]
                subtotal = precio * cantidad
                carrito.append(("P", item_id, nombre, precio, cantidad, subtotal))
            else:
                index = item_combo.current()
                item_id, nombre, precio = servicios[index]
                subtotal = precio
                carrito.append(("S", item_id, nombre, precio, 1, subtotal))

            tabla.insert("", "end", values=(nombre, f"Q{precio}", cantidad, f"Q{subtotal}"))
            item_combo.set("")

        tk.Button(ventas, text="Agregar", command=agregar_item, bg="#2196F3", fg="white").pack(pady=5)

        def cobrar():
            if not carrito:
                messagebox.showwarning("Advertencia", "No hay productos ni servicios agregados.")
                return

            total = sum(item[5] for item in carrito)
            sale_id = id_creation("V")
            fecha = datetime.date.today()

            try:
                sales_db.cobro(carrito, sale_id, client_id, fecha, total)
                ventas.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar la venta:\n{e}")

        tk.Button(ventas, text="Cobrar", command=cobrar, bg="#4CAF50", fg="white").pack(pady=10)

    obtener_client_info()