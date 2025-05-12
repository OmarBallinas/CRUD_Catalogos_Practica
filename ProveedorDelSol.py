import wx
import mysql.connector
from mysql.connector import Error

# Crear la aplicación wx
app = wx.App()  # Instancia del objeto wx

ventana = wx.Frame(None, title='Catálogo de Proveedores', size=(600, 500))  # Creación de la ventana
panel = wx.Panel(ventana)  # Crear panel dentro de la ventana

# Título
lbl_titulo = wx.Panel(panel, pos=(0, 0), size=(600, 40))  
lbl_titulo = wx.StaticText(lbl_titulo, label="CATÁLOGO DE PROVEEDORES", pos=(220, 10))
fuente_titulo = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)  # Fuente más grande y en negrita
lbl_titulo.SetFont(fuente_titulo)

# Tamaño estándar para los campos de texto
tamano_texto = (200, -1)

# Campos de entrada para el proveedor
lbl_id_proveedor = wx.StaticText(panel, label="ID Proveedor:", pos=(50, 50))  # Texto
txt_id_proveedor = wx.TextCtrl(panel, pos=(200, 50), size=tamano_texto)  # Input
txt_id_proveedor.SetBackgroundColour(wx.Colour(255, 255, 230))  # Color input

lbl_nombre = wx.StaticText(panel, label="Nombre:", pos=(50, 100))  # Texto
txt_nombre = wx.TextCtrl(panel, pos=(200, 100), size=tamano_texto)  # Input
txt_nombre.SetBackgroundColour(wx.Colour(255, 255, 230))  # Color input

lbl_contacto = wx.StaticText(panel, label="Contacto:", pos=(50, 150))  # Texto
txt_contacto = wx.TextCtrl(panel, pos=(200, 150), size=tamano_texto)  # Input
txt_contacto.SetBackgroundColour(wx.Colour(255, 255, 230))  # Color input

lbl_telefono = wx.StaticText(panel, label="Teléfono:", pos=(50, 200))  # Texto
txt_telefono = wx.TextCtrl(panel, pos=(200, 200), size=tamano_texto)  # Input
txt_telefono.SetBackgroundColour(wx.Colour(255, 255, 230))  # Color input

lbl_correo = wx.StaticText(panel, label="Correo Electrónico:", pos=(50, 250))  # Texto
txt_correo = wx.TextCtrl(panel, pos=(200, 250), size=tamano_texto)  # Input
txt_correo.SetBackgroundColour(wx.Colour(255, 255, 230))  # Color input

lbl_direccion = wx.StaticText(panel, label="Dirección:", pos=(50, 300))  # Texto
txt_direccion = wx.TextCtrl(panel, pos=(200, 300), size=tamano_texto)  # Input
txt_direccion.SetBackgroundColour(wx.Colour(255, 255, 230))  # Color input

# Botones del CRUD
button_crear = wx.Button(panel, label=" Crear ", pos=(50, 370), size=(120, 40))  # Crear
button_buscar = wx.Button(panel, label=" Buscar ", pos=(180, 370), size=(120, 40))  # Buscar
button_actualizar = wx.Button(panel, label=" Actualizar ", pos=(310, 370), size=(120, 40))  # Actualizar
button_eliminar = wx.Button(panel, label=" Eliminar ", pos=(440, 370), size=(120, 40))  # Eliminar

# Funciones de eventos con validaciones

# Mostrar mensaje
def mostrar_mensaje(titulo, mensaje):
    wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

# Conectar a la base de datos
def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host='localhost',  # Cambia a tu servidor de base de datos
            database='nombre_de_base_de_datos',  # Nombre de tu base de datos
            user='usuario',  # Nombre de usuario de la base de datos
            password='contraseña'  # Contraseña de la base de datos
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        mostrar_mensaje("Error de conexión", f"Error al conectar con la base de datos: {e}")
        return None

# Crear proveedor
def on_crear(event):
    id_proveedor = txt_id_proveedor.GetValue()
    nombre = txt_nombre.GetValue()
    contacto = txt_contacto.GetValue()
    telefono = txt_telefono.GetValue()
    correo = txt_correo.GetValue()
    direccion = txt_direccion.GetValue()

    if not id_proveedor or not nombre or not contacto or not telefono or not correo or not direccion:
        mostrar_mensaje("Advertencia", "Por favor, complete todos los campos obligatorios.")
    else:
        conn = conectar_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO proveedores (id_proveedor, nombre, contacto, telefono, correo, direccion) 
                            VALUES (%s, %s, %s, %s, %s, %s)""",
                           (id_proveedor, nombre, contacto, telefono, correo, direccion))
            conn.commit()
            mostrar_mensaje("Éxito", "Proveedor creado correctamente.")
            conn.close()

# Buscar proveedor
def on_buscar(event):
    id_proveedor = txt_id_proveedor.GetValue()
    if not id_proveedor:
        mostrar_mensaje("Advertencia", "Por favor, ingrese un ID de proveedor para buscar.")
    else:
        conn = conectar_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM proveedores WHERE id_proveedor = %s", (id_proveedor,))
            resultado = cursor.fetchone()
            if resultado:
                txt_nombre.SetValue(resultado[1])
                txt_contacto.SetValue(resultado[2])
                txt_telefono.SetValue(resultado[3])
                txt_correo.SetValue(resultado[4])
                txt_direccion.SetValue(resultado[5])
                mostrar_mensaje("Resultado", f"Proveedor encontrado: {id_proveedor}")
            else:
                mostrar_mensaje("No encontrado", f"No se encontró el proveedor con ID {id_proveedor}.")
            conn.close()

# Actualizar proveedor
def on_actualizar(event):
    id_proveedor = txt_id_proveedor.GetValue()
    nombre = txt_nombre.GetValue()
    contacto = txt_contacto.GetValue()
    telefono = txt_telefono.GetValue()
    correo = txt_correo.GetValue()
    direccion = txt_direccion.GetValue()

    if not id_proveedor:
        mostrar_mensaje("Advertencia", "Por favor, ingrese un ID de proveedor para actualizar.")
    elif not nombre or not contacto or not telefono or not correo or not direccion:
        mostrar_mensaje("Advertencia", "Por favor, complete todos los campos.")
    else:
        conn = conectar_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""UPDATE proveedores SET nombre = %s, contacto = %s, telefono = %s, correo = %s, direccion = %s
                              WHERE id_proveedor = %s""",
                           (nombre, contacto, telefono, correo, direccion, id_proveedor))
            conn.commit()
            mostrar_mensaje("Éxito", f"Proveedor {id_proveedor} actualizado correctamente.")
            conn.close()

# Eliminar proveedor
def on_eliminar(event):
    id_proveedor = txt_id_proveedor.GetValue()
    if not id_proveedor:
        mostrar_mensaje("Advertencia", "Por favor, ingrese un ID de proveedor para eliminar.")
    else:
        conn = conectar_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM proveedores WHERE id_proveedor = %s", (id_proveedor,))
            conn.commit()
            mostrar_mensaje("Éxito", f"Proveedor {id_proveedor} eliminado correctamente.")
            conn.close()

# Asociar los eventos de los botones
button_crear.Bind(wx.EVT_BUTTON, on_crear)
button_buscar.Bind(wx.EVT_BUTTON, on_buscar)
button_actualizar.Bind(wx.EVT_BUTTON, on_actualizar)
button_eliminar.Bind(wx.EVT_BUTTON, on_eliminar)

ventana.Centre()  # Centrar ventana
ventana.Show()  # Mostrar la ventana

app.MainLoop()  # Mantener ventana abierta