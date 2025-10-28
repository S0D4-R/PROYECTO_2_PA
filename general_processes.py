from admin_form import  *
from tkinter import messagebox
import random


PG_CONFIG = {
    "host": "ep-spring-field-adn3pad6-pooler.c-2.us-east-1.aws.neon.tech",
    "dbname": "neondb",
    "user": "neondb_owner",
    "password": "npg_oWvxAFjh8d0R",
    "sslmode": "require"
}

#DB_CONN----------------------------------------------------------------------------------------------------------------
def get_conn():
    try:
        return psycopg2.connect(**PG_CONFIG)
    except Exception as e:
        messagebox.showerror("DB ERROR", "Error in DB")
def init_db():
    try:
        con = get_conn()
        cur = con.cursor()
        # Productos
        cur.execute("""
            CREATE TABLE IF NOT EXISTS barbershop_products (
                id SERIAL PRIMARY KEY,
                product_name VARCHAR(100) NOT NULL,
                brand VARCHAR(50),
                category VARCHAR(50),
                price DECIMAL(10, 2) NOT NULL,
                stock_quantity INTEGER NOT NULL,
                supplier VARCHAR(100),
                date_added DATE DEFAULT CURRENT_DATE,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS b_services (
                id VARCHAR(10) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price NUMERIC(10, 2) NOT NULL
            );
        """)

        cur.execute("""
                CREATE TABLE IF NOT EXISTS barbershop_appointments (
                    id VARCHAR(10) PRIMARY KEY,
                    client_name VARCHAR(100) NOT NULL,
                    service_id VARCHAR(10) REFERENCES b_services(id),
                    appointment_date DATE NOT NULL,
                    appointment_time TIME NOT NULL,
                    status VARCHAR(20) DEFAULT 'Scheduled'
                );
                """)

        cur.execute("""
                CREATE TABLE IF NOT EXISTS barbershop_sales (
                    id VARCHAR(10) PRIMARY KEY,
                    sale_date DATE NOT NULL,
                    product_id INTEGER REFERENCES barbershop_products(id),
                    service_id VARCHAR(10) REFERENCES b_services(id),
                    quantity INTEGER NOT NULL,
                    total_amount NUMERIC(10,2) NOT NULL
                );
                """)

        con.commit()
        con.close()
    except Exception as e:
        messagebox.showerror("Error de BD", f"No se pudo inicializar la BD:\n{e}")


#AUTOGENERADOR_ID's-----------------------------------------------------------------------------------------------------
def id_creation(typeP):
    ran_code1 = random.randint(10000, 99999)
    ran_code2 = random.randint(10, 99)

    if typeP == "S":
        id_gen = "SVC" + str(ran_code1) + str(ran_code2)
        return id_gen
    elif typeP == "A":
        id_gen = "APM" + str(ran_code1) + str(ran_code2)
        return id_gen
    elif typeP == "V":
        return "VNT" + str(ran_code1) + str(ran_code2)
    else:
        return None

#TABS-------------------------------------------------------------------------------------------------------------------
def close_tabs(menu, frame1, frame2):
    menu.select(frame1)
    menu.hide(frame2)

def check_date(date):
    temp_date = date.split("-")
    if (int(temp_date[2]) > 31 or int(temp_date[2]) < 0) or (int(temp_date[1]) > 12 or int(temp_date[1]) < 0) or (int(temp_date[0]) > 9999 or int(temp_date[0]) < 0):
        messagebox.showerror("ERROR", "Fecha inválida")
        return  False
    else:
        return True


#Modify Elimate---------------------------------------------------------------------------------------------------------
def get_selected_item_data(treeview):
    selected_item_id = treeview.focus()

    if not selected_item_id:
        messagebox.showwarning("Selección Requerida", "Por favor, selecciona un producto de la lista.")
        return None, None

    values = treeview.item(selected_item_id, 'values')

    db_id = values[0] if values else None

    return selected_item_id, db_id, values


def edit_product(treeview):
    item_id, db_id, values = get_selected_item_data(treeview)

    if item_id:
        # Aquí puedes abrir una nueva ventana con un formulario prellenado con 'values'
        print(f"Editando producto ID: {db_id} con datos: {values}")
        # Lógica para abrir ventana de edición...


def delete_product(treeview):
    item_id, db_id, values = get_selected_item_data(treeview)

    if item_id:
        if messagebox.askyesno("Confirmar Eliminación",
                               f"¿Estás seguro de que quieres eliminar el producto ID {db_id}?"):
            try:
                con = get_conn()
                cur = con.cursor()
                cur.execute(
                    "DELETE FROM barbershop_products WHERE id = %s;", (db_id))

                con.commit()
                con.close()

            except Exception as e:
                messagebox.showerror("Error de BD", str(e))
            treeview.delete(item_id)
            messagebox.showinfo("Éxito", "Producto eliminado.")

def mod_elm_prods(menu, main_mod_m, m_e_p, style):
    menu.select(m_e_p)
    style.configure("Custom.TButton")
    m_e_p.grid_columnconfigure(0, weight=1)
    m_e_p.grid_columnconfigure(1, weight=0)

    # --- TREEVIEW (Columna 0) ---
    products_display = ttk.Treeview(m_e_p,
                                    columns=("1", "2", "3", "4", "5", "6", "7", "8", "9"), show="headings")

    try:
        con = get_conn()
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM barbershop_products;")
        products_in_db = cur.fetchall()


        for product in products_in_db:
            products_display.insert(parent="", index=tk.END, values=product)

        con.close()

    except Exception as e:
        messagebox.showerror("Error de BD", str(e))

    products_display.grid(row=0, column=0, rowspan=10, padx=10, pady=10, sticky="nsew")


    m_e_p.grid_rowconfigure(0, weight=1)


    edit_button = ttk.Button(m_e_p, text="EDITAR", style="Custom.TButton",
                             command=lambda: edit_product(products_display))  # <- Llama a la función
    edit_button.grid(row=1, column=1, padx=10, pady=(10, 5), sticky="n")  # Sticky "n" para pegarse arriba


    delete_button = ttk.Button(m_e_p, text="ELIMINAR", style="Custom.TButton",
                               command=lambda: delete_product(products_display))
    delete_button.grid(row=2, column=1, padx=10, pady=5, sticky="n")


    exit_button = ttk.Button(m_e_p, text="SALIR", style="Custom.TButton",
                             command=lambda: close_tabs(menu, main_mod_m, m_e_p))

    exit_button.grid(row=10, column=1, padx=10, pady=(50, 10), sticky="s")

    m_e_p.grid_rowconfigure(9, weight=1)


def modify_eliminate(menu, main_frame, style):
    #Tabs
    mod_prods = ttk.Frame(menu)
    mod_prods.pack(expand=True, fill="both")
    menu.add(mod_prods, text="MODIFICAR/ELIMINAR", state="hidden")

    prod_mod_e = ttk.Frame(menu)
    prod_mod_e.pack(expand=True, fill="both")
    menu.add(prod_mod_e, text="PRODUCTOS MODIFICAR/ELIMINAR", state="hidden")

    svc_mod_e = ttk.Frame(menu)
    svc_mod_e.pack(expand=True, fill="both")
    menu.add(svc_mod_e, text="PRODUCTOS MODIFICAR/ELIMINAR", state="hidden")

    #Menu selection----------------------------------------------------------------------
    menu.select(mod_prods)
    style.configure("Custom.TButton")

    mod_prods.grid_columnconfigure(0, weight=0)
    mod_prods.grid_columnconfigure(1, weight=1)

    mod_prods.grid_rowconfigure(4, weight=1)

    m_e_prods_button = ttk.Button(mod_prods, text="PRODUCTOS", style="Custom.TButton",
                             command=lambda: mod_elm_prods(menu, main_frame, prod_mod_e, style))
    m_e_prods_button.grid(row=1, column=0, columnspan=2, padx=200, pady=(10, 50), sticky="ew")

    m_e_prods_button = ttk.Button(mod_prods, text="SERVICIOS", style="Custom.TButton",
                                  command=lambda: mod_elm_prods(menu, main_frame, prod_mod_e, style))
    m_e_prods_button.grid(row=2, column=0, columnspan=2, padx=200, pady=(10, 50), sticky="ew")

    exit_button = ttk.Button(mod_prods, text="SALIR", style="Custom.TButton",
                             command=lambda: close_tabs(menu, main_frame, mod_prods))
    exit_button.grid(row=3, column=0, columnspan=2, padx=200, pady=(10, 50), sticky="ew")