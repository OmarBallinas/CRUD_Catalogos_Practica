# archivo: conexion.py
import mysql.connector

def conectar():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="#2005Omar",
            database="delsol",
            # auth_plugin='mysql_native_password'  Solo si se usa native verificar con: SELECT user, host, plugin FROM mysql.user WHERE user = 'root';
        )
        
        cursor = conn.cursor()
        return conn, cursor
    
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return None, None
