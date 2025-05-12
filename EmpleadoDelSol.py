import wx
import mysql.connector
from mysql.connector import Error

# Función para conectar a la base de datos
def conectar():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            database='tu_base_de_datos',
            user='tu_usuario',
            password='tu_contraseña'
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        wx.MessageBox(f"Error al conectar a la base de datos: {e}", "Error", wx.OK | wx.ICON_ERROR)
        return None

# Función para crear un empleado
def crear_empleado(id_empleado, nombre, apellidos, telefono, correo, contrasena):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO empleados (id_empleado, nombre, apellidos, telefono, correo, contrasena) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (id_empleado, nombre, apellidos, telefono, correo, contrasena))
            conn.commit()
            cursor.close()
            conn.close()
            wx.MessageBox("Empleado creado exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al crear empleado: {e}", "Error", wx.OK | wx.ICON_ERROR)
    else:
        wx.MessageBox("No se pudo conectar a la base de datos", "Error", wx.OK | wx.ICON_ERROR)

# Función para buscar un empleado
def buscar_empleado(id_empleado):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM empleados WHERE id_empleado = %s"
            cursor.execute(query, (id_empleado,))
            resultado = cursor.fetchone()
            if resultado:
                return resultado
            else:
                wx.MessageBox("Empleado no encontrado", "Error", wx.OK | wx.ICON_ERROR)
                return None
            cursor.close()
            conn.close()
        except Error as e:
            wx.MessageBox(f"Error al buscar empleado: {e}", "Error", wx.OK | wx.ICON_ERROR)
    else:
        wx.MessageBox("No se pudo conectar a la base de datos", "Error", wx.OK | wx.ICON_ERROR)

# Función para actualizar un empleado
def actualizar_empleado(id_empleado, nombre, apellidos, telefono, correo, contrasena):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            query = "UPDATE empleados SET nombre = %s, apellidos = %s, telefono = %s, correo = %s, contrasena = %s WHERE id_empleado = %s"
            cursor.execute(query, (nombre, apellidos, telefono, correo, contrasena, id_empleado))
            conn.commit()
            cursor.close()
            conn.close()
            wx.MessageBox("Empleado actualizado exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al actualizar empleado: {e}", "Error", wx.OK | wx.ICON_ERROR)
    else:
        wx.MessageBox("No se pudo conectar a la base de datos", "Error", wx.OK | wx.ICON_ERROR)

# Función para eliminar un empleado
def eliminar_empleado(id_empleado):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM empleados WHERE id_empleado = %s"
            cursor.execute(query, (id_empleado,))
            conn.commit()
            cursor.close()
            conn.close()
            wx.MessageBox("Empleado eliminado exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Error as e:
            wx.MessageBox(f"Error al eliminar empleado: {e}", "Error", wx.OK | wx.ICON_ERROR)
    else:
        wx.MessageBox("No se pudo conectar a la base de datos", "Error", wx.OK | wx.ICON_ERROR)

# Función para mostrar un mensaje
def mostrar_mensaje(titulo, mensaje):
    wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

# Funciones de eventos con validaciones
def on_crear(event):
    id_empleado = txt_id_empleado.GetValue()
    nombre = txt_nombre.GetValue()
    apellidos = txt_apellidos.GetValue()
    telefono = txt_telefono.GetValue()
    correo = txt_correo.GetValue()
    contrasena = txt_contrasena.GetValue()
    conf_contrasena = txt_conf_contrasena.GetValue()

    if not id_empleado or not nombre or not apellidos or not telefono or not correo or not contrasena or not conf_contrasena:
        mostrar_mensaje("Advertencia", "Por favor, complete todos los campos obligatorios.")
    elif contrasena != conf_contrasena:
        mostrar_mensaje("Advertencia", "Las contraseñas no coinciden.")
    else:
        crear_empleado(id_empleado, nombre, apellidos, telefono, correo, contrasena)

def on_buscar(event):
    id_empleado = txt_id_empleado.GetValue()
    if not id_empleado:
        mostrar_mensaje("Advertencia", "Por favor, ingrese un ID de empleado para buscar.")
    else:
        empleado = buscar_empleado(id_empleado)
        if empleado:
            txt_nombre.SetValue(empleado[1])  # Completar el nombre
            txt_apellidos.SetValue(empleado[2])  # Completar apellidos
            txt_telefono.SetValue(empleado[3])  # Completar teléfono
            txt_correo.SetValue(empleado[4])  # Completar correo

def on_actualizar(event):
    id_empleado = txt_id_empleado.GetValue()
    nombre = txt_nombre.GetValue()
    apellidos = txt_apellidos.GetValue()
    telefono = txt_telefono.GetValue()
    correo = txt_correo.GetValue()
    contrasena = txt_contrasena.GetValue()
    conf_contrasena = txt_conf_contrasena.GetValue()

    if not id_empleado or not nombre or not apellidos or not telefono or not correo or not contrasena or not conf_contrasena:
        mostrar_mensaje("Advertencia", "Por favor, complete todos los campos obligatorios.")
    elif contrasena != conf_contrasena:
        mostrar_mensaje("Advertencia", "Las contraseñas no coinciden.")
    else:
        actualizar_empleado(id_empleado, nombre, apellidos, telefono, correo, contrasena)

def on_eliminar(event):
    id_empleado = txt_id_empleado.GetValue()
    if not id_empleado:
        mostrar_mensaje("Advertencia", "Por favor, ingrese un ID de empleado para eliminar.")
    else:
        eliminar_empleado(id_empleado)

# Interfaz gráfica
app = wx.App()

ventana = wx.Frame(None, title='Catálogo de Empleados', size=(600, 550))  # Aumentando la altura de la ventana
panel = wx.Panel(ventana)

lbl_titulo = wx.Panel(panel, pos=(0, 0), size=(600, 40))  # Título
lbl_titulo = wx.StaticText(lbl_titulo, label="CATÁLOGO DE EMPLEADOS", pos=(220, 10))
fuente_titulo = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
lbl_titulo.SetFont(fuente_titulo)

tamano_texto = (200, -1)  # Definir un tamaño estándar para los campos de texto

# ID Empleado
lbl_id_empleado = wx.StaticText(panel, label="ID Empleado:", pos=(50, 50))
txt_id_empleado = wx.TextCtrl(panel, pos=(200, 50), size=tamano_texto)
txt_id_empleado.SetBackgroundColour(wx.Colour(255, 255, 230))

# Nombre
lbl_nombre = wx.StaticText(panel, label="Nombre:", pos=(50, 100))
txt_nombre = wx.TextCtrl(panel, pos=(200, 100), size=tamano_texto)
txt_nombre.SetBackgroundColour(wx.Colour(255, 255, 230))

# Apellidos
lbl_apellidos = wx.StaticText(panel, label="Apellidos:", pos=(50, 150))
txt_apellidos = wx.TextCtrl(panel, pos=(200, 150), size=tamano_texto)
txt_apellidos.SetBackgroundColour(wx.Colour(255, 255, 230))

# Teléfono
lbl_telefono = wx.StaticText(panel, label="Teléfono:", pos=(50, 200))
txt_telefono = wx.TextCtrl(panel, pos=(200, 200), size=tamano_texto)
txt_telefono.SetBackgroundColour(wx.Colour(255, 255, 230))

# Correo Electrónico
lbl_correo = wx.StaticText(panel, label="Correo Electrónico:", pos=(50, 250))
txt_correo = wx.TextCtrl(panel, pos=(200, 250), size=tamano_texto)
txt_correo.SetBackgroundColour(wx.Colour(255, 255, 230))

# Contraseña
lbl_contrasena = wx.StaticText(panel, label="Contraseña:", pos=(50, 300))
txt_contrasena = wx.TextCtrl(panel, pos=(200, 300), size=tamano_texto, style=wx.TE_PASSWORD)
txt_contrasena.SetBackgroundColour(wx.Colour(255, 255, 230))

# Confirmar Contraseña
lbl_conf_contrasena = wx.StaticText(panel, label="Confirmar Contraseña:", pos=(50, 350))
txt_conf_contrasena = wx.TextCtrl(panel, pos=(200, 350), size=tamano_texto, style=wx.TE_PASSWORD)
txt_conf_contrasena.SetBackgroundColour(wx.Colour(255, 255, 230))

# Botones CRUD
button_crear = wx.Button(panel, label=" Crear ", pos=(50, 420), size=(120, 40))
button_buscar = wx.Button(panel, label=" Buscar ", pos=(180, 420), size=(120, 40))
button_actualizar = wx.Button(panel, label=" Actualizar ", pos=(310, 420), size=(120, 40))
button_eliminar = wx.Button(panel, label=" Eliminar ", pos=(440, 420), size=(120, 40))

# Asociar eventos
button_crear.Bind(wx.EVT_BUTTON, on_crear)
button_buscar.Bind(wx.EVT_BUTTON, on_buscar)
button_actualizar.Bind(wx.EVT_BUTTON, on_actualizar)
button_eliminar.Bind(wx.EVT_BUTTON, on_eliminar)

ventana.Centre()  # Centrar ventana
ventana.Show()  # Mostrar ventana

app.MainLoop()  # Mantener ventana abierta