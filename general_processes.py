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
    temp_date = date.split("/")
    if (int(temp_date[0]) > 31 or int(temp_date[0]) < 0) or (int(temp_date[1]) > 12 or int(temp_date[1]) < 0) or (int(temp_date[2]) > 9999 or int(temp_date[2]) < 0):
        messagebox.showerror("ERROR", "Fecha inválida")
        return  False
    else:
        return True