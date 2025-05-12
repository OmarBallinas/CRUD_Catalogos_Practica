# conexion.py
import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="DelSol"
        )
        cursor = conn.cursor()
        return conn, cursor
    except Error as e:
        print("Error al conectar a la base de datos:", e)
        return None, None
