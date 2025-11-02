class Cita:
    def __init__(self,name_client, fecha, hora):
        self.__name_client = name_client
        self.__fecha = fecha
        self.__hora = hora

        @property
        def name(self):
            return self.__name_client

        @name.setter
        def name(self, new_name):
            if new_name:
                self.__name_client = new_name
            else:
                print("El nombre no puede quedaer vacio")

        @property
        def fecha(self):
            return self.__fecha

        @fecha.setter
        def fecha(self, new_fecha):
            if new_fecha:
                self.__fecha = new_fecha
            else:
                print("La fecha no puede quedar vacia")
        @property
        def hora(self):
            return self.__hora

        @hora.setter
        def hora(self,new_hora):
            if new_hora:
                self.__hora = new_hora
            else:
                print("La hora no puede queda vacia")

    def guardar_db(self,id_cita,id_services,conn):
        cur = conn.cursor
        cur.execute("""
            INSERT INTO barbershop_appointments (id, client_name, service_id, appointment_date, appointment_time)
                VALUES (%s, %s, %s, %s, %s);
        """, (id_cita,self.__name_client, id_services, self.__fecha, self.__hora) )
        conn.commit()
        cur.close()





