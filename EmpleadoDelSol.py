import wx
from conexion import conectar

# Función para mostrar mensajes
def mostrar_mensaje(titulo, mensaje):
    wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

# Validar campos
def validar_campos(idempleado, nombre, apellidos, telefono, correo_electronico, contrasena, conf_contrasena):
    if not idempleado.isdigit():
        return "El ID del empleado debe ser un número entero."
    if not nombre or not apellidos:
        return "Nombre y apellidos son obligatorios."
    if telefono and (not telefono.isdigit() or len(telefono) != 10):
        return "El teléfono debe tener 10 dígitos numéricos."
    if correo_electronico and '@' not in correo_electronico:
        return "Correo electrónico no válido."
    if len(contrasena) < 6:
        return "La contraseña debe tener al menos 6 caracteres."
    if contrasena != conf_contrasena:
        return "Las contraseñas no coinciden."
    return None

# Crear empleado
def agregar_empleado(idempleado, nombre, apellidos, telefono, correo_electronico, contrasena):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            cursor.execute("""
                INSERT INTO empleado (idempleado, nombre, apellidos, telefono, correo_electronico, contraseña)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (int(idempleado), nombre, apellidos,
                  telefono if telefono else None,
                  correo_electronico if correo_electronico else None,
                  contrasena))
            conn.commit()
            mostrar_mensaje("Éxito", "Empleado creado exitosamente.")
        except Exception as e:
            mostrar_mensaje("Error", f"Error al crear el empleado: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos.")

# Buscar empleado
def buscar_empleado(idempleado):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            cursor.execute("SELECT * FROM empleado WHERE idempleado = %s", (int(idempleado),))
            resultado = cursor.fetchone()
            return resultado
        except Exception as e:
            mostrar_mensaje("Error", f"Error al buscar el empleado: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos.")
    return None

# Actualizar empleado
def actualizar_empleado(idempleado, nombre, apellidos, telefono, correo_electronico, contrasena):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            cursor.execute("""
                UPDATE empleado SET
                    nombre = %s,
                    apellidos = %s,
                    telefono = %s,
                    correo_electronico = %s,
                    contraseña = %s
                WHERE idempleado = %s
            """, (nombre, apellidos,
                  telefono if telefono else None,
                  correo_electronico if correo_electronico else None,
                  contrasena, int(idempleado)))
            conn.commit()
            mostrar_mensaje("Éxito", "Empleado actualizado exitosamente.")
        except Exception as e:
            mostrar_mensaje("Error", f"Error al actualizar el empleado: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos.")

# Eliminar empleado
def eliminar_empleado(idempleado):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            cursor.execute("DELETE FROM empleado WHERE idempleado = %s", (int(idempleado),))
            conn.commit()
            mostrar_mensaje("Éxito", "Empleado eliminado exitosamente.")
        except Exception as e:
            mostrar_mensaje("Error", f"Error al eliminar el empleado: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos.")

# Interfaz gráfica
app = wx.App()
ventana = wx.Frame(None, title='Catálogo de Empleados', size=(600, 470))
panel = wx.Panel(ventana)

lbl_titulo = wx.Panel(panel, pos=(0, 0), size=(600, 40))
lbl_titulo = wx.StaticText(lbl_titulo, label="CATÁLOGO DE EMPLEADOS", pos=(220, 10))
lbl_titulo.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

tamano_texto = (200, -1)

# Entradas
lbl_idempleado = wx.StaticText(panel, label="ID Empleado:", pos=(50, 50))
txt_idempleado = wx.TextCtrl(panel, pos=(200, 50), size=tamano_texto)
txt_idempleado.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_nombre = wx.StaticText(panel, label="Nombre:", pos=(50, 90))
txt_nombre = wx.TextCtrl(panel, pos=(200, 90), size=tamano_texto)
txt_nombre.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_apellidos = wx.StaticText(panel, label="Apellidos:", pos=(50, 130))
txt_apellidos = wx.TextCtrl(panel, pos=(200, 130), size=tamano_texto)
txt_apellidos.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_telefono = wx.StaticText(panel, label="Teléfono:", pos=(50, 170))
txt_telefono = wx.TextCtrl(panel, pos=(200, 170), size=tamano_texto)
txt_telefono.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_correo = wx.StaticText(panel, label="Correo Electrónico:", pos=(50, 210))
txt_correo = wx.TextCtrl(panel, pos=(200, 210), size=tamano_texto)
txt_correo.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_contrasena = wx.StaticText(panel, label="Contraseña:", pos=(50, 250))
txt_contrasena = wx.TextCtrl(panel, pos=(200, 250), size=tamano_texto, style=wx.TE_PASSWORD)
txt_contrasena.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_conf_contrasena = wx.StaticText(panel, label="Confirmar Contraseña:", pos=(50, 290))
txt_conf_contrasena = wx.TextCtrl(panel, pos=(200, 290), size=tamano_texto, style=wx.TE_PASSWORD)
txt_conf_contrasena.SetBackgroundColour(wx.Colour(255, 255, 230))

# Botones
btn_crear = wx.Button(panel, label=" Crear ", pos=(50, 350), size=(120, 40))
btn_buscar = wx.Button(panel, label=" Buscar ", pos=(180, 350), size=(120, 40))
btn_actualizar = wx.Button(panel, label=" Actualizar ", pos=(310, 350), size=(120, 40))
btn_eliminar = wx.Button(panel, label=" Eliminar ", pos=(440, 350), size=(120, 40))

# Eventos
def on_crear(event):
    campos = [
        txt_idempleado.GetValue(),
        txt_nombre.GetValue(),
        txt_apellidos.GetValue(),
        txt_telefono.GetValue(),
        txt_correo.GetValue(),
        txt_contrasena.GetValue(),
        txt_conf_contrasena.GetValue(),
    ]
    error = validar_campos(*campos)
    if error:
        mostrar_mensaje("Advertencia", error)
    else:
        agregar_empleado(*campos[:-1])

def on_buscar(event):
    idemp = txt_idempleado.GetValue()
    if not idemp:
        mostrar_mensaje("Advertencia", "Por favor, ingrese el ID del empleado.")
        return
    empleado = buscar_empleado(idemp)
    if empleado:
        txt_nombre.SetValue(empleado[1])
        txt_apellidos.SetValue(empleado[2])
        txt_telefono.SetValue(empleado[3] if empleado[3] else "")
        txt_correo.SetValue(empleado[4] if empleado[4] else "")
        txt_contrasena.SetValue(empleado[5])
        txt_conf_contrasena.SetValue(empleado[5])
    else:
        mostrar_mensaje("Información", "Empleado no encontrado.")

def on_actualizar(event):
    campos = [
        txt_idempleado.GetValue(),
        txt_nombre.GetValue(),
        txt_apellidos.GetValue(),
        txt_telefono.GetValue(),
        txt_correo.GetValue(),
        txt_contrasena.GetValue(),
        txt_conf_contrasena.GetValue(),
    ]
    error = validar_campos(*campos)
    if error:
        mostrar_mensaje("Advertencia", error)
    else:
        actualizar_empleado(*campos[:-1])

def on_eliminar(event):
    idemp = txt_idempleado.GetValue()
    if not idemp:
        mostrar_mensaje("Advertencia", "Por favor, ingrese el ID del empleado.")
    else:
        eliminar_empleado(idemp)
        txt_idempleado.Clear()
        txt_nombre.Clear()
        txt_apellidos.Clear()
        txt_telefono.Clear()
        txt_correo.Clear()
        txt_contrasena.Clear()
        txt_conf_contrasena.Clear()

# Asociar eventos
btn_crear.Bind(wx.EVT_BUTTON, on_crear)
btn_buscar.Bind(wx.EVT_BUTTON, on_buscar)
btn_actualizar.Bind(wx.EVT_BUTTON, on_actualizar)
btn_eliminar.Bind(wx.EVT_BUTTON, on_eliminar)

ventana.Centre()
ventana.Show()
app.MainLoop()