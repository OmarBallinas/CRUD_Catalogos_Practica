# clientes.py
import wx
from conexion import conectar
from mysql.connector import Error

# Función para mostrar los mensajes en la ventana de wx
def mostrar_mensaje(titulo, mensaje):
    wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

# Función para crear un cliente
def crear_cliente(telefono, nombre, apellido, correo):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            query = "INSERT INTO cliente (telefono_cliente , nombre, apellido, correo_electronico ) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (telefono, nombre, apellido, correo))
            conn.commit()
            mostrar_mensaje("Éxito", "Cliente creado exitosamente")
        except Error as e:
            mostrar_mensaje("Error", f"Error al crear cliente: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos")

# Función para buscar un cliente por teléfono
def buscar_cliente(telefono):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            query = "SELECT telefono_cliente , nombre, apellido, correo_electronico  FROM cliente WHERE telefono_cliente = %s"
            cursor.execute(query, (telefono,))
            resultado = cursor.fetchone()
            if resultado:
                return resultado
            else:
                mostrar_mensaje("Error", "Cliente no encontrado")
                return None
        except Error as e:
            mostrar_mensaje("Error", f"Error al buscar cliente: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos")
    return None

# Función para actualizar un cliente
def actualizar_cliente(telefono, nombre, apellido, correo):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            query = "UPDATE cliente SET nombre = %s, apellido = %s, correo_electronico = %s WHERE telefono_cliente = %s"
            cursor.execute(query, (nombre, apellido, correo, telefono))
            conn.commit()
            mostrar_mensaje("Éxito", "Cliente actualizado exitosamente")
        except Error as e:
            mostrar_mensaje("Error", f"Error al actualizar cliente: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos")

# Función para eliminar un cliente
def eliminar_cliente(telefono):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            query = "DELETE FROM cliente WHERE telefono_cliente = %s"
            cursor.execute(query, (telefono,))
            conn.commit()
            mostrar_mensaje("Éxito", "Cliente eliminado exitosamente")
        except Error as e:
            mostrar_mensaje("Error", f"Error al eliminar cliente: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos")

# Función para manejar el evento de crear
def on_crear(event):
    telefono = txt_telefono.GetValue()
    nombre = txt_nombre.GetValue()
    apellido = txt_apellido.GetValue()
    correo = txt_correo.GetValue()
    if telefono and nombre and apellido and correo:
        crear_cliente(telefono, nombre, apellido, correo)
    else:
        mostrar_mensaje("Advertencia", "Por favor, complete todos los campos")

# Función para manejar el evento de buscar
def on_buscar(event):
    telefono = txt_telefono.GetValue()
    if telefono:
        cliente = buscar_cliente(telefono)
        if cliente:
            txt_nombre.SetValue(cliente[1])  # Completar el nombre en el campo de texto
            txt_apellido.SetValue(cliente[2])  # Completar el apellido
            txt_correo.SetValue(cliente[3])  # Completar el correo
    else:
        mostrar_mensaje("Advertencia", "Por favor, ingrese un teléfono de cliente")

# Función para manejar el evento de actualizar
def on_actualizar(event):
    telefono = txt_telefono.GetValue()
    nombre = txt_nombre.GetValue()
    apellido = txt_apellido.GetValue()
    correo = txt_correo.GetValue()
    if telefono and nombre and apellido and correo:
        actualizar_cliente(telefono, nombre, apellido, correo)
    else:
        mostrar_mensaje("Advertencia", "Por favor, complete todos los campos")

# Función para manejar el evento de eliminar
def on_eliminar(event):
    telefono = txt_telefono.GetValue()
    if telefono:
        eliminar_cliente(telefono)
        txt_telefono.Clear()
        txt_nombre.Clear()
        txt_apellido.Clear()
        txt_correo.Clear()
    else:
        mostrar_mensaje("Advertencia", "Por favor, ingrese un teléfono de cliente")

# Interfaz gráfica con wxPython
app = wx.App()

ventana = wx.Frame(None, title='Catálogo de Clientes', size=(600, 400))
panel = wx.Panel(ventana)

# Titulo
lbl_titulo = wx.Panel(panel, pos=(0, 0), size=(600, 40))
lbl_titulo = wx.StaticText(lbl_titulo, label="CATÁLOGO DE CLIENTES", pos=(220, 10))
fuente_titulo = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
lbl_titulo.SetFont(fuente_titulo)

tamano_texto = (200, -1)

# Campos de entrada para cliente
lbl_telefono = wx.StaticText(panel, label="Teléfono Cliente:", pos=(50, 50))
txt_telefono = wx.TextCtrl(panel, pos=(200, 50), size=tamano_texto)
txt_telefono.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_nombre = wx.StaticText(panel, label="Nombre:", pos=(50, 100))
txt_nombre = wx.TextCtrl(panel, pos=(200, 100), size=tamano_texto)
txt_nombre.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_apellido = wx.StaticText(panel, label="Apellido:", pos=(50, 150))
txt_apellido = wx.TextCtrl(panel, pos=(200, 150), size=tamano_texto)
txt_apellido.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_correo = wx.StaticText(panel, label="Correo Electrónico:", pos=(50, 200))
txt_correo = wx.TextCtrl(panel, pos=(200, 200), size=tamano_texto)
txt_correo.SetBackgroundColour(wx.Colour(255, 255, 230))

# Botones CRUD
button_crear = wx.Button(panel, label=" Crear ", pos=(50, 300), size=(120, 40))
button_buscar = wx.Button(panel, label=" Buscar ", pos=(180, 300), size=(120, 40))
button_actualizar = wx.Button(panel, label=" Actualizar ", pos=(310, 300), size=(120, 40))
button_eliminar = wx.Button(panel, label=" Eliminar ", pos=(440, 300), size=(120, 40))

# Asociar eventos a los botones
button_crear.Bind(wx.EVT_BUTTON, on_crear)
button_buscar.Bind(wx.EVT_BUTTON, on_buscar)
button_actualizar.Bind(wx.EVT_BUTTON, on_actualizar)
button_eliminar.Bind(wx.EVT_BUTTON, on_eliminar)

ventana.Centre()
ventana.Show()
app.MainLoop()
