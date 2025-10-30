import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from pyuiWidgets.imageLabel import ImageLabel
from tkinter import ttk, messagebox
from datetime import date
from general_processes import get_conn, id_creation
from tkinter import simpledialog
import random
import datetime


def sells_menu():
    def obtener_client_info():
        """Solicita NIT y nombre del cliente antes de abrir la ventana de ventas"""
        client_win = tk.Toplevel()
        client_win.title("Datos del Cliente")
        client_win.geometry("400x250")
        client_win.config(bg="#ffffff")

        tk.Label(client_win, text="NIT del Cliente:", bg="#ffffff").pack(pady=5)
        nit_entry = tk.Entry(client_win)
        nit_entry.pack(pady=5)

        tk.Label(client_win, text="Nombre del Cliente:", bg="#ffffff").pack(pady=5)
        name_entry = tk.Entry(client_win)
        name_entry.pack(pady=5)

        def continuar():
            nit = nit_entry.get().strip()
            nombre = name_entry.get().strip()

            if not nombre:
                messagebox.showwarning("Advertencia", "Debe ingresar el nombre del cliente.")
                return

            try:
                con = get_conn()
                cur = con.cursor()

                if nit == "":
                    nit = "CF"
                    client_id = id_creation("C")
                    cur.execute(
                        "INSERT INTO b_clients (id, c_nit, client_name) VALUES (%s, %s, %s)",
                        (client_id, nit, nombre)
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
                            (client_id, nit, nombre)
                        )
                        con.commit()

                con.close()
                client_win.destroy()
                abrir_ventana_ventas(client_id, nombre)

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar el cliente:\n{e}")

        tk.Button(client_win, text="Continuar", command=continuar, bg="#4CAF50", fg="white").pack(pady=20)

    def abrir_ventana_ventas(client_id, client_name):
        """Abre la ventana de ventas y permite agregar productos o servicios"""
        ventas_win = tk.Toplevel()
        ventas_win.title("Registro de Ventas")
        ventas_win.geometry("800x500")
        ventas_win.config(bg="#ffffff")

        tk.Label(ventas_win, text=f"Cliente: {client_name}", bg="#ffffff", font=("Arial", 12, "bold")).pack(pady=10)


        con = get_conn()
        cur = con.cursor()
        cur.execute("SELECT id, product_name, price FROM barbershop_products")
        productos = cur.fetchall()

        cur.execute("SELECT id, name, price FROM b_services")
        servicios = cur.fetchall()
        con.close()


        tipo_var = tk.StringVar()
        tipo_combo = ttk.Combobox(ventas_win, textvariable=tipo_var, values=["Producto", "Servicio"], state="readonly")
        tipo_combo.set("Producto")
        tipo_combo.pack(pady=10)


        item_var = tk.StringVar()
        item_combo = ttk.Combobox(ventas_win, textvariable=item_var, width=50)
        item_combo.pack(pady=10)

        def actualizar_items(*args):
            if tipo_var.get() == "Producto":
                item_combo["values"] = [f"{p[1]} - Q{p[2]}" for p in productos]
            else:
                item_combo["values"] = [f"{s[1]} - Q{s[2]}" for s in servicios]

        tipo_combo.bind("<<ComboboxSelected>>", actualizar_items)
        actualizar_items()

        tk.Label(ventas_win, text="Cantidad:").pack()
        cantidad_entry = tk.Entry(ventas_win)
        cantidad_entry.pack(pady=5)
        cantidad_entry.insert(0, "1")


        tabla = ttk.Treeview(ventas_win, columns=("item", "precio", "cantidad", "subtotal"), show="headings")
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

        tk.Button(ventas_win, text="Agregar", command=agregar_item, bg="#2196F3", fg="white").pack(pady=5)

        def cobrar():
            if not carrito:
                messagebox.showwarning("Advertencia", "No hay productos ni servicios agregados.")
                return

            total = sum(item[5] for item in carrito)
            sale_id = id_creation("V")
            fecha = datetime.date.today()

            try:
                con = get_conn()
                cur = con.cursor()


                cur.execute("INSERT INTO barbershop_sales (id, client_b) VALUES (%s, %s)", (sale_id, client_id))


                for idx, item in enumerate(carrito):
                    tipo, item_id, nombre, precio, cantidad, subtotal = item


                    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
                    detail_id = f"DV{timestamp}{idx}"

                    if tipo == "P":
                        cur.execute("""
                            INSERT INTO sales_details (id, sale_id, client_id, product_id, service_id, sale_date, quantity_sold, service_price)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (detail_id, sale_id, client_id, item_id, None, fecha, cantidad, precio))
                    else:
                        cur.execute("""
                            INSERT INTO sales_details (id, sale_id, client_id, product_id, service_id, sale_date, quantity_sold, service_price)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (detail_id, sale_id, client_id, None, item_id, fecha, 1, precio))

                con.commit()
                con.close()
                messagebox.showinfo("Éxito", f"Venta registrada exitosamente.\nTotal: Q{total:.2f}")
                ventas_win.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar la venta:\n{e}")

        tk.Button(ventas_win, text="Cobrar", command=cobrar, bg="#4CAF50", fg="white").pack(pady=10)

    obtener_client_info()