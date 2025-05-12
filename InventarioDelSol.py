import wx
import mysql.connector
from mysql.connector import Error

# Crear la aplicación wx
app = wx.App()  # Instancia del objeto wx

ventana = wx.Frame(None, title='Catálogo de Inventario', size=(600, 400))  # Creación de la ventana
panel = wx.Panel(ventana)  # Crear panel dentro de la ventana

# Título
lbl_titulo = wx.Panel(panel, pos=(0, 0), size=(600, 40))  
lbl_titulo = wx.StaticText(lbl_titulo, label="CATÁLOGO DE INVENTARIO", pos=(220, 10))
fuente_titulo = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)  # Fuente más grande y en negrita
lbl_titulo.SetFont(fuente_titulo)

# Tamaño estándar para los campos de texto
tamano_texto = (200, -1)

# Campos de entrada para el inventario
lbl_codigo_barras = wx.StaticText(panel, label="Código de Barras:", pos=(50, 50))  # Texto
txt_codigo_barras = wx.TextCtrl(panel, pos=(200, 50), size=tamano_texto)  # Input
txt_codigo_barras.SetBackgroundColour(wx.Colour(255, 255, 230))  # Color input

lbl_existencia = wx.StaticText(panel, label="Existencia Actual:", pos=(50, 100))  # Texto
txt_existencia = wx.TextCtrl(panel, pos=(200, 100), size=tamano_texto)  # Input
txt_existencia.SetBackgroundColour(wx.Colour(255, 255, 230))  # Color input

lbl_capacidad = wx.StaticText(panel, label="Capacidad Máxima:", pos=(50, 150))  # Texto
txt_capacidad = wx.TextCtrl(panel, pos=(200, 150), size=tamano_texto)  # Input
txt_capacidad.SetBackgroundColour(wx.Colour(255, 255, 230))  # Color input

lbl_ubicacion = wx.StaticText(panel, label="Ubicación:", pos=(50, 200))  # Texto
txt_ubicacion = wx.TextCtrl(panel, pos=(200, 200), size=tamano_texto)  # Input
txt_ubicacion.SetBackgroundColour(wx.Colour(255, 255, 230))  # Color input

lbl_fecha = wx.StaticText(panel, label="Fecha Actualización:", pos=(50, 250))  # Texto
txt_fecha = wx.TextCtrl(panel, pos=(200, 250), size=tamano_texto)  # Input
txt_fecha.SetBackgroundColour(wx.Colour(255, 255, 230))  # Color input

# Botones del CRUD
button_crear = wx.Button(panel, label=" Crear ", pos=(50, 300), size=(120, 40))  # Crear
button_buscar = wx.Button(panel, label=" Buscar ", pos=(180, 300), size=(120, 40))  # Buscar
button_actualizar = wx.Button(panel, label=" Actualizar ", pos=(310, 300), size=(120, 40))  # Actualizar
button_eliminar = wx.Button(panel, label=" Eliminar ", pos=(440, 300), size=(120, 40))  # Eliminar

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

# Crear producto
def on_crear(event):
    codigo_barras = txt_codigo_barras.GetValue()
    existencia = txt_existencia.GetValue()
    capacidad = txt_capacidad.GetValue()
    ubicacion = txt_ubicacion.GetValue()
    fecha = txt_fecha.GetValue()

    if not codigo_barras or not existencia or not capacidad or not ubicacion or not fecha:
        mostrar_mensaje("Advertencia", "Por favor, complete todos los campos obligatorios.")
    else:
        conn = conectar_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO inventario (codigo_barras, existencia, capacidad, ubicacion, fecha_actualizacion) VALUES (%s, %s, %s, %s, %s)",
                           (codigo_barras, existencia, capacidad, ubicacion, fecha))
            conn.commit()
            mostrar_mensaje("Éxito", "Inventario creado correctamente.")
            conn.close()

# Buscar producto
def on_buscar(event):
    codigo_barras = txt_codigo_barras.GetValue()
    if not codigo_barras:
        mostrar_mensaje("Advertencia", "Por favor, ingrese un código de barras para buscar.")
    else:
        conn = conectar_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inventario WHERE codigo_barras = %s", (codigo_barras,))
            resultado = cursor.fetchone()
            if resultado:
                txt_existencia.SetValue(str(resultado[1]))
                txt_capacidad.SetValue(str(resultado[2]))
                txt_ubicacion.SetValue(resultado[3])
                txt_fecha.SetValue(str(resultado[4]))
                mostrar_mensaje("Resultado", f"Producto encontrado: {codigo_barras}")
            else:
                mostrar_mensaje("No encontrado", f"No se encontró el producto con el código de barras {codigo_barras}.")
            conn.close()

# Actualizar producto
def on_actualizar(event):
    codigo_barras = txt_codigo_barras.GetValue()
    existencia = txt_existencia.GetValue()
    capacidad = txt_capacidad.GetValue()
    ubicacion = txt_ubicacion.GetValue()
    fecha = txt_fecha.GetValue()

    if not codigo_barras:
        mostrar_mensaje("Advertencia", "Por favor, ingrese un código de barras para actualizar.")
    elif not existencia or not capacidad or not ubicacion or not fecha:
        mostrar_mensaje("Advertencia", "Por favor, complete todos los campos.")
    else:
        conn = conectar_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE inventario
                SET existencia = %s, capacidad = %s, ubicacion = %s, fecha_actualizacion = %s
                WHERE codigo_barras = %s
            """, (existencia, capacidad, ubicacion, fecha, codigo_barras))
            conn.commit()
            mostrar_mensaje("Éxito", f"Producto {codigo_barras} actualizado correctamente.")
            conn.close()

# Eliminar producto
def on_eliminar(event):
    codigo_barras = txt_codigo_barras.GetValue()
    if not codigo_barras:
        mostrar_mensaje("Advertencia", "Por favor, ingrese un código de barras para eliminar.")
    else:
        conn = conectar_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM inventario WHERE codigo_barras = %s", (codigo_barras,))
            conn.commit()
            mostrar_mensaje("Éxito", f"Producto {codigo_barras} eliminado correctamente.")
            conn.close()

# Asociar los eventos de los botones
button_crear.Bind(wx.EVT_BUTTON, on_crear)
button_buscar.Bind(wx.EVT_BUTTON, on_buscar)
button_actualizar.Bind(wx.EVT_BUTTON, on_actualizar)
button_eliminar.Bind(wx.EVT_BUTTON, on_eliminar)

ventana.Centre()  # Centrar ventana
ventana.Show()  # Mostrar la ventana

app.MainLoop()  # Mantener ventana abierta