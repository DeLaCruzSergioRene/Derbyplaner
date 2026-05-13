import mysql.connector
from mysql.connector import Error

class BD:
    def __init__(self):
        try:
            self.conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="derby_planer"
            )
            self.cursor = self.conexion.cursor(dictionary=True)
        except Error as e:
            print(f"Error de conexión: {e}")
    
    def ejecutar(self, consulta, parametros=None):
        try:
            if parametros:
                self.cursor.execute(consulta, parametros)
            else:
                self.cursor.execute(consulta)
            self.conexion.commit()
        except Error as e:
            print(f"Error: {e}")
    
    def obtener_uno(self, consulta, parametros=None):
        try:
            if parametros:
                self.cursor.execute(consulta, parametros)
            else:
                self.cursor.execute(consulta)
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error: {e}")
            return None
    
    def cerrar(self):
        self.cursor.close()
        self.conexion.close()
