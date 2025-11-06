from admin_form import  *
from tkinter import messagebox
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#DB_CONN----------------------------------------------------------------------------------------------------------------
class DataBaseX():
    def __init__(self):
        self._get_conn()
        self.__init_db()
        self.__PGCONFIG = {
                "host": "ep-spring-field-adn3pad6-pooler.c-2.us-east-1.aws.neon.tech",
                "dbname": "neondb",
                "user": "neondb_owner",
                "password": "npg_oWvxAFjh8d0R",
                "sslmode": "require"
                }

    def _get_conn(self):
        try:
            return psycopg2.connect(**self.__PGCONFIG)
        except Exception as e:
            #messagebox.showerror("DB ERROR", "Error al conectar a la BD")
            return None
    def __init_db(self):
        try:
            con = self._get_conn()
            if con is None:
                return
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
                        client_b VARCHAR(10) REFERENCES b_clients(id)
                    );
                    """)

            cur.execute("""
                    CREATE TABLE IF NOT EXISTS b_clients (
                        id VARCHAR(10) PRIMARY KEY,
                        c_nit VARCHAR(9) NOT NULL,
                        client_name VARCHAR(100) NOT NULL
                    );
            """)

            cur.execute(""" 
                    CREATE TABLE  IF NOT EXISTS sales_details (
                        id SERIAL PRIMARY KEY,
                        sale_id VARCHAR(10) REFERENCES barbershop_sales(id),
                        client_id VARCHAR(10) REFERENCES b_clients(id),
                        product_id INTEGER REFERENCES barbershop_products(id),
                        service_id VARCHAR(10) REFERENCES b_services(id),
                        sale_date DATE DEFAULT CURRENT_DATE,
                        quantity_sold INTEGER,
                        service_price NUMERIC(10,2)
                        );
            """)

            con.commit()
            con.close()
        except Exception as e:
            messagebox.showerror("Error de BD", f"No se pudo inicializar la BD:\n{e}")

    def displayDB(self, query, table):
        try:
            con = self._get_conn()
            cur = con.cursor()
            cur.execute(query)
            products_in_db = cur.fetchall()

            for product in products_in_db:
                table.insert(parent="", index=tk.END, values=product)

            con.close()

        except Exception as e:
            messagebox.showerror("Error al desplegar la BD", str(e))

    def execute(self, query, parameters):
        try:
            con = self._get_conn()
            cur = con.cursor()
            cur.execute(query, parameters)

            con.commit()
            con.close()

        except Exception as e:
            messagebox.showerror("Error al ejecutar comando", str(e))

class DataBase_For_Reports(DataBaseX):
    def reports(self,query, parameter, table):
        sales_total = 0
        try:
            con = self._get_conn()
            cur = con.cursor()
            cur.execute(query, parameter)
            sales_in_db = cur.fetchall()

            counter = 0
            for sale in sales_in_db:
                quantity = sale[6]
                unit_price = sale[7]
                subtotal = quantity * unit_price
                counter += 1
                sales_total += subtotal
                table.insert(parent="", index=tk.END, values=(sale[0], sale[1], sale[2], sale[3], sale[4], sale[5], sale[6], sale[7]))
            con.close()
        except Exception as e:
            messagebox.showerror("Error al generar reporte", str(e))
        table.insert(parent="", index=tk.END, values=(" ", " ", " ", " ", " ", " ", "TOTAL: ", f"Q{sales_total:.2f}"))

class DataBase_For_Services(DataBaseX):
    def cargar_servicios(self, window, combobox):
        try:
            conn = self._get_conn()
            cur = conn.cursor()
            cur.execute("SELECT id, name, price FROM b_services ORDER BY name ASC;")
            servicios = cur.fetchall()
            window.servicios_dict = {nombre: (id_serv, precio) for id_serv, nombre, precio in servicios}
            combobox["values"] = list(window.servicios_dict.keys())
            conn.close()
        except Exception as e:
            messagebox.showerror("Error de servicios", f"No se pudieron cargar los servicios: {e}")




class Appointments_DB(DataBaseX):
    def iterable_db(self, query):
        con = self._get_conn()
        cur = con.cursor()
        cur.execute(query)
        new_list = cur.fetchall()
        con.close()
        return new_list


gen_db_x = DataBase_For_Reports()



#Main menu



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
    elif typeP == "C":
        return "IDC" + str(ran_code1) + str(ran_code2)
    elif typeP == "DV":
        return "DTV" + str(ran_code1) + str(ran_code2)
    elif typeP == "P":
        return "PVD" + str(ran_code1) + str(ran_code2)
    elif typeP  == "B":
        return "CTG" + str(ran_code1) + str(ran_code2)
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



def delete_product(treeview, query):
    item_id, db_id, values = get_selected_item_data(treeview)

    if item_id:
        if messagebox.askyesno("Confirmar Eliminación",
                               f"¿Estás seguro de que quieres eliminar el producto ID {db_id}?"):
            gen_db_x.execute(query, (db_id,))
            treeview.delete(item_id)
            messagebox.showinfo("Éxito", "Producto eliminado.")



#PRODUCTOS------------------------------------------------------------------------------------------------------------
def mod_elm_prods(menu, main_mod_m, m_e_p, style):
    menu.select(m_e_p)
    style.configure("Custom.TButton")
    m_e_p.grid_columnconfigure(0, weight=1)
    m_e_p.grid_columnconfigure(1, weight=0)

    # --- TREEVIEW (Columna 0) ---
    products_display = ttk.Treeview(m_e_p,
                                    columns=("1", "2", "3", "4", "5", "6", "7", "8", "9"), show="headings")

    gen_db_x.displayDB("SELECT * FROM barbershop_products;", products_display)

    products_display.grid(row=0, column=0, rowspan=10, padx=10, pady=10, sticky="nsew")


    m_e_p.grid_rowconfigure(0, weight=1)




    delete_button = ttk.Button(m_e_p, text="ELIMINAR", style="Custom.TButton",
                               command=lambda: delete_product(products_display, "DELETE FROM barbershop_products WHERE id = %s;"))
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

    #Menu selection----------------------------------------------------------------------
    menu.select(mod_prods)
    style.configure("Custom.TButton")

    mod_prods.grid_columnconfigure(0, weight=0)
    mod_prods.grid_columnconfigure(1, weight=1)

    mod_prods.grid_rowconfigure(4, weight=1)

    m_e_prods_button = ttk.Button(mod_prods, text="PRODUCTOS", style="Custom.TButton",
                             command=lambda: mod_elm_prods(menu, main_frame, prod_mod_e, style))
    m_e_prods_button.grid(row=1, column=0, columnspan=2, padx=200, pady=(10, 50), sticky="ew")



    exit_button = ttk.Button(mod_prods, text="SALIR", style="Custom.TButton",
                             command=lambda: close_tabs(menu, main_frame, mod_prods))
    exit_button.grid(row=2, column=0, columnspan=2, padx=200, pady=(10, 50), sticky="ew")

#close window------------------------------------------------------------------------------------------------------------
def manipulate_window(first_window, second_window, op_type):
    if op_type == "C":
        first_window.destroy()
    elif op_type == "O":
        pass
    elif op_type == "CO":
        second_window.destroy()