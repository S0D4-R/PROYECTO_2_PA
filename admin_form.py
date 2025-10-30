import os
import tkinter as tk
from tkinter.messagebox import showerror

from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import json
from pyuiWidgets.imageLabel import ImageLabel
import  psycopg2
from general_processes import *
from tkcalendar import DateEntry
import datetime
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

#LOGIN----------------------------------------------------------------------------------------------------------
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

    #Style
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


    #label
    pass_label = tk.Label(login_form, text="CONTRASEÑA:", background="#ffffff", foreground="#000000")
    pass_label.grid(row=0, column=0, padx=10, pady=30, sticky="w")
    #textbox
    pass_text = tk.Entry(login_form, background="#000000", foreground="#ffffff", show="*")
    pass_text.grid(row=0, column=0, padx=100, pady=30, sticky="w")

    #Botón get

    button_get = ttk.Button(login_form, text="Log In",
                           style="Custom.TButton",
                           command=lambda: get_info(login_form, pass_text))
    button_get.grid(row=0, column=0, padx=290, pady=(50, 10), sticky="ew")



#REPORTES-----------------------------------------------------------------------------------------------------------

def gen_report(fdate, sdate, treeview):
    if check_date(fdate.get()) and check_date(sdate.get()):
        gen_db_x.reports("SELECT * FROM sales_details WHERE sale_date BETWEEN %s AND %s;", (fdate.get(), sdate.get()))
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


    #Tabla de labels
    report_table = ttk.Treeview(frame_reportes, columns=("1", "2", "3", "4", "5", "6"), show="headings")
    column_map = {"1": "ID", "2": "Fecha", "3": "Producto", "4": "Servicio", "5": "Total"}
    for col_id, text in column_map.items():
        report_table.heading(col_id, text=text, anchor=tk.CENTER)

    # Configuración de Ancho (CRUCIAL para que se muestren)
    report_table.column("1", width=30, anchor=tk.CENTER, stretch=tk.NO)
    report_table.column("2", width=100, anchor=tk.CENTER)
    report_table.column("3", width=120, anchor=tk.W)
    report_table.column("4", width=120, anchor=tk.W)
    report_table.column("5", width=60, anchor=tk.E)


    # ¡Añadir el Treeview al grid! Ocupará ambas columnas y se estirará horizontalmente.
    # Usamos sticky="nsew" para que se estire en las 4 direcciones dentro de la celda.
    report_table.grid(row=2, column=0, columnspan=2, padx=10, pady=15, sticky="nsew")

    # ---------------------------------------------------------------------
    # 3. CONFIGURACIÓN DE ESPACIO Y BOTONES

    frame_reportes.grid_rowconfigure(3, weight=1)

    # BOTONES
    save_button = ttk.Button(frame_reportes, text="GENERAR", style="Custom.TButton",
                             command=lambda: gen_report(first_date_entry, second_date_entry, report_table))
    save_button.grid(row=4, column=0, columnspan=2, padx=200, pady=(10, 50), sticky="ew")

    # Salir
    exit_button = ttk.Button(frame_reportes, text="SALIR", style="Custom.TButton",
                             command=lambda: close_tabs(menu, main_frame, frame_reportes))
    # Mantenemos los botones juntos, por ejemplo, en la fila 5
    exit_button.grid(row=5, column=0, columnspan=2, padx=200, pady=(10, 50), sticky="ew")

    menu.add(frame_reportes, text="REPORTES")
    menu.select(frame_reportes)


#New Prod--------------------------------------------------------------------------------------------------------
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
                        """, (prod_name, prod_brand, prod_category, prod_price, prod_stock, prod_supplier)
                         )
        messagebox.showinfo("ÉXITO", f"Producto '{prod_name}' guardado con éxito.")


    except ValueError:
        messagebox.showerror("ERROR DE DATOS", "El Precio y la Cantidad deben ser números válidos.")
    except Exception as e:
        messagebox.showerror("ERROR", f"Error en la base de datos: {e}")


def agregar_producto(menu,main_frame,  frame_add_prods, style):
    menu.select(frame_add_prods)
    style.configure("Custom.TButton")

    frame_add_prods.grid_columnconfigure(0, weight=0)
    frame_add_prods.grid_columnconfigure(1, weight=1)

    # NOmbre producto (ROW 0)
    prodname_label = tk.Label(frame_add_prods, text="Nombre del producto:", background="#000000", foreground="#ffffff")
    prodname_label.grid(row=0, column=0, padx=10, pady=5, sticky="nw")
    prodname_entry = tk.Entry(frame_add_prods, background="#000000", foreground="#ffffff")
    prodname_entry.grid(row=0, column=1, padx=10, pady=5, sticky="new")

    # Brand (ROW 1)
    brand_label = tk.Label(frame_add_prods, text="Marca:", background="#000000", foreground="#ffffff")
    brand_label.grid(row=1, column=0, padx=10, pady=5, sticky="nw")
    brand_entry = tk.Entry(frame_add_prods, background="#000000", foreground="#ffffff")
    brand_entry.grid(row=1, column=1, padx=10, pady=5, sticky="new")

    # Category (ROW 2)
    cat_label = tk.Label(frame_add_prods, text="Categoría:", background="#000000", foreground="#ffffff")
    cat_label.grid(row=2, column=0, padx=10, pady=5, sticky="nw")
    cat_entry = tk.Entry(frame_add_prods, background="#000000", foreground="#ffffff")
    cat_entry.grid(row=2, column=1, padx=10, pady=5, sticky="new")

    #Price (ROW 3)
    price_label = tk.Label(frame_add_prods, text="Precio:", background="#000000", foreground="#ffffff")
    price_label.grid(row=3, column=0, padx=10, pady=5, sticky="nw")
    price_entry = tk.Entry(frame_add_prods, background="#000000", foreground="#ffffff")
    price_entry.grid(row=3, column=1, padx=10, pady=5, sticky="new")

    #Stock (ROW 4)
    stock_label = tk.Label(frame_add_prods, text="Cantidad:", background="#000000", foreground="#ffffff")
    stock_label.grid(row=4, column=0, padx=10, pady=5, sticky="nw")
    stock_entry = tk.Entry(frame_add_prods, background="#000000", foreground="#ffffff")
    stock_entry.grid(row=4, column=1, padx=10, pady=5, sticky="new")

    #Supplier (ROW 5)
    sup_label = tk.Label(frame_add_prods, text="Proveedor:", background="#000000", foreground="#ffffff")
    sup_label.grid(row=5, column=0, padx=10, pady=5, sticky="nw")
    sup_entry = tk.Entry(frame_add_prods, background="#000000", foreground="#ffffff")
    sup_entry.grid(row=5, column=1, padx=10, pady=5, sticky="new")

    # ---------------------------------------------------------------------------------------------------

    frame_add_prods.grid_rowconfigure(6, weight=1)

    save_button = ttk.Button(frame_add_prods, text="GUARDAR", style="Custom.TButton", command=lambda: add_new_prod(prodname_entry, brand_entry, cat_entry, price_entry, stock_entry, sup_entry))
    save_button.grid(row=7, column=0, columnspan=2, padx=200, pady=(10, 50), sticky="ew")

    exit_button = ttk.Button(frame_add_prods, text="SALIR", style="Custom.TButton", command=lambda: close_tabs(menu, main_frame, frame_add_prods))
    exit_button.grid(row=8, column=0, columnspan=2, padx=200, pady=(10, 50), sticky="ew")


    menu.add(frame_add_prods, text="AGREGAR PRODUCTOS")
    menu.select(frame_add_prods)



#Password---------------------------------------------------------------------------------------------------------------
def save_pass(entry1, entry2):
    if entry1.get() == entry2.get():
        lord.contra = entry1.get()
        lord._save_password()


def change_pass(menu, main_frame, password_frame, style):
    #Select tabs------------------------------------------------------------------------------
    menu.select(password_frame)
    style.configure("Custom.TButton")
    # label
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

    #Exit Tabs---------------------------------------------------------------------------------

    save_button = ttk.Button(password_frame, text="GUARDAR", style="Custom.TButton", command=lambda: save_pass(pass_text, c_pass_entry))
    save_button.grid(row=3, column=0, padx=10, pady=(10, 10), sticky="w")  # Sticky W para alinearlo a la izquierda

    exit_button = ttk.Button(password_frame, text="SALIR", style="Custom.TButton", command=lambda: close_tabs(menu, main_frame, password_frame))
    exit_button.grid(row=3, column=1, padx=10, pady=(10, 10), sticky="e")  # Sticky E para alinearlo a la derecha

#ADD SERVICES-----------------------------------------------------------------------------------------------------------
def add_svc(svcname_e, svcprice_e):
    try:
        svc_name = svcname_e.get()
        svc_price = float(svcprice_e.get())
        svc_id = id_creation("S")

        gen_db_x.execute("""
                INSERT INTO b_services 
                (id, name, price) 
                VALUES (%s, %s, %s); 
                """,(svc_id, svc_name, svc_price))
        messagebox.showinfo("ÉXITO", f"El servicio '{svc_name}' guardado con éxito.")

    except ValueError:
        messagebox.showerror("ERROR DE DATOS", "El Precio debe ser un número válido.")
    except Exception as e:
        messagebox.showerror("ERROR", f"Error en la base de datos: {e}")




def add_service(menu, main_frame, new_service_frame, style):
    menu.select(new_service_frame)
    style.configure("Custom.TButton")

    new_service_frame.grid_columnconfigure(0, weight=0)
    new_service_frame.grid_columnconfigure(1, weight=1)

    # Nombre del servicio (ROW 0)
    svc_name_label = tk.Label(new_service_frame, text="Nombre del Servicio:", background="#000000", foreground="#ffffff")
    svc_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="nw")
    svc_name_entry = tk.Entry(new_service_frame, background="#000000", foreground="#ffffff")
    svc_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="new")

    # Precio (ROW 1)
    svc_price_label = tk.Label(new_service_frame, text="Precio:", background="#000000", foreground="#ffffff")
    svc_price_label.grid(row=1, column=0, padx=10, pady=5, sticky="nw")
    svc_price_entry = tk.Entry(new_service_frame, background="#000000", foreground="#ffffff")
    svc_price_entry.grid(row=1, column=1, padx=10, pady=5, sticky="new")



    # ---------------------------------------------------------------------------------------------------

    new_service_frame.grid_rowconfigure(6, weight=1)

    save_button = ttk.Button(new_service_frame, text="GUARDAR", style="Custom.TButton",
                             command=lambda: add_svc(svc_name_entry, svc_price_entry))
    save_button.grid(row=7, column=0, columnspan=2, padx=200, pady=(10, 50), sticky="ew")

    exit_button = ttk.Button(new_service_frame, text="SALIR", style="Custom.TButton",
                             command=lambda: close_tabs(menu, main_frame, new_service_frame))
    exit_button.grid(row=8, column=0, columnspan=2, padx=200, pady=(10, 50), sticky="ew")

    menu.add(new_service_frame, text="AGREGAR PRODUCTOS")
    menu.select(new_service_frame)

#
#ADMIN MENU----------------------------------------------------------------------------------------------------
def admin_menu():
    admin_form = tk.Tk()
    admin_form.title("Administrador")
    admin_form.geometry("700x600")
    admin_form.config(bg="#ffffff")
    admin_style = ttk.Style(admin_form)
    admin_style.theme_use("clam")

    admin_style.configure("Custom.TButton",
                          background="#000000",
                          foreground="#ffffff",
                          font=('Arial', 10),
                          bordercolor="#000000",
                          darkcolor="#000000",
                          lightcolor="#333333",
                          padding=10)


    inside_menu = ttk.Notebook(admin_form)
    inside_menu.pack(expand=True, fill="both", padx=10, pady=10)
    #Frame del menú principal
    frame_menu_inicial = ttk.Frame(inside_menu)
    frame_menu_inicial.pack(expand=True, fill="both")
    inside_menu.add(frame_menu_inicial, text=" Menú Principal ")

    #Frame del menú de agregar productos
    frame_add_prods = ttk.Frame(inside_menu)
    frame_add_prods.pack(expand=True, fill="both")
    inside_menu.add(frame_add_prods, text="AGREGAR PRODUCTOS", state="hidden")

    #Frame para agregar servicios
    frame_add_svc = ttk.Frame(inside_menu)
    frame_add_svc.pack(expand=True, fill="both")
    inside_menu.add(frame_add_svc, text="AGREGAR SERVICIO", state="hidden")

    # Frame del reporte
    frame_reports = ttk.Frame(inside_menu)
    frame_reports.pack(expand=True, fill="both")
    inside_menu.add(frame_reports, text="REPORTES", state="hidden")

    #Frame de cambio de contraseña
    frame_cambio_c = ttk.Frame(inside_menu)
    frame_cambio_c.pack(expand=True, fill="both")
    inside_menu.add(frame_cambio_c, text="CAMBIAR CONTRASEÑA", state="hidden")
#Botones--------------------------------------------------------------------------------------------------------
    button_ap = ttk.Button(frame_menu_inicial, text="AGREGAR PRODUCTO",
                           style="Custom.TButton",
                           command=lambda: agregar_producto(inside_menu,frame_menu_inicial, frame_add_prods, admin_style))
    button_ap.grid(row=0, column=0, padx=250, pady=(50, 10), sticky="ew")

    button_rep = ttk.Button(frame_menu_inicial, text="REPORTES",
                            style="Custom.TButton",
                            command=lambda: reportes(inside_menu,frame_menu_inicial, frame_reports, admin_style, admin_form))
    button_rep.grid(row=3, column=0, padx=250, pady=10, sticky="ew")

    button_exit = ttk.Button(frame_menu_inicial, text="SALIR",
                             style="Custom.TButton",
                             command=lambda: admin_form.destroy())
    button_exit.grid(row=5, column=0, padx=250, pady=10, sticky="ew")


    button_change_p = ttk.Button(frame_menu_inicial, text="CAMBIAR CONTRASEÑA",
                            style="Custom.TButton",
                            command=lambda: change_pass(inside_menu,frame_menu_inicial, frame_cambio_c, admin_style))

    button_change_p.grid(row=2, column=0, padx=250, pady=10, sticky="ew")

    button_add_service = ttk.Button(frame_menu_inicial, text="AGREGAR SERVICIO",
                                 style="Custom.TButton",
                                 command=lambda: add_service(inside_menu,frame_menu_inicial,frame_add_svc,admin_style))
    button_add_service.grid(row=1, column=0, padx=250, pady=10, sticky="ew")

    button_add_service = ttk.Button(frame_menu_inicial, text="MODIFICAR/ELIMINAR REGISTROS",
                                    style="Custom.TButton",
                                    command=lambda: modify_eliminate(inside_menu, frame_menu_inicial, admin_style))
    button_add_service.grid(row=4, column=0, padx=250, pady=10, sticky="ew")


# Botones--------------------------------------------------------------------------------------------------------
    admin_style.configure("label.TLabel", background="#E4E2E2", foreground="#000", anchor="center")