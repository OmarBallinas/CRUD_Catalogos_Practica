import wx
from conexion import conectar
from mysql.connector import Error


# Función para mostrar mensajes
def mostrar_mensaje(titulo, mensaje):
    wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

# Función para validar campos
def validar_campos(idempleado, nombre, apellidos, telefono, correo_electronico, contraseña, conf_contraseña):
    if not idempleado.isdigit():
        return "El ID del empleado debe ser un número entero"
    if len(nombre) == 0 or len(apellidos) == 0:
        return "Nombre y apellidos son campos obligatorios"
    if telefono and (not telefono.isdigit() or len(telefono) != 10):
        return "El teléfono debe tener 10 dígitos numéricos"
    if correo_electronico and '@' not in correo_electronico:
        return "Ingrese un correo electrónico válido"
    if len(contraseña) < 6:
        return "La contraseña debe tener al menos 6 caracteres"
    if contraseña != conf_contraseña:
        return "Las contraseñas no coinciden"
    return None

# Función para crear un empleado
def crear_empleado(idempleado, nombre, apellidos, telefono, correo_electronico, contraseña):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            query = """INSERT INTO empleado 
                       (idempleado, nombre, apellidos, telefono, correo_electronico, contraseña) 
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (idempleado, nombre, apellidos, 
                                 telefono if telefono else None, 
                                 correo_electronico if correo_electronico else None, 
                                 contraseña))
            conn.commit()
            mostrar_mensaje("Éxito", "Empleado creado exitosamente")
            return True
        except Error as e:
            mostrar_mensaje("Error", f"Error al crear empleado: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos")
    return False

# Función para buscar un empleado
def buscar_empleado(idempleado):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            query = "SELECT * FROM empleado WHERE idempleado = %s"
            cursor.execute(query, (idempleado,))
            resultado = cursor.fetchone()
            return resultado
        except Error as e:
            mostrar_mensaje("Error", f"Error al buscar empleado: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos")
    return None

# Función para actualizar un empleado
def actualizar_empleado(idempleado, nombre, apellidos, telefono, correo_electronico, contraseña):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            query = """UPDATE empleado SET 
                      nombre = %s, 
                      apellidos = %s, 
                      telefono = %s, 
                      correo_electronico = %s, 
                      contraseña = %s 
                      WHERE idempleado = %s"""
            cursor.execute(query, (nombre, apellidos, 
                                 telefono if telefono else None, 
                                 correo_electronico if correo_electronico else None, 
                                 contraseña, 
                                 idempleado))
            conn.commit()
            mostrar_mensaje("Éxito", "Empleado actualizado exitosamente")
            return True
        except Error as e:
            mostrar_mensaje("Error", f"Error al actualizar empleado: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos")
    return False

# Función para eliminar un empleado
def eliminar_empleado(idempleado):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            query = "DELETE FROM empleado WHERE idempleado = %s"
            cursor.execute(query, (idempleado,))
            conn.commit()
            mostrar_mensaje("Éxito", "Empleado eliminado exitosamente")
            return True
        except Error as e:
            mostrar_mensaje("Error", f"Error al eliminar empleado: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos")
    return False

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