import wx
from conexion import conectar

# ---------- Funciones de lógica ----------

def mostrar_mensaje(titulo, mensaje):
    wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

def validar_campos(idempleado, nombre, apellidos, telefono, correo_electronico, contraseña, conf_contraseña):
    if not idempleado.isdigit():
        return "El ID del empleado debe ser un número entero"
    if not nombre or not apellidos:
        return "Nombre y apellidos son obligatorios"
    if telefono and (not telefono.isdigit() or len(telefono) != 10):
        return "El teléfono debe tener 10 dígitos numéricos"
    if correo_electronico and '@' not in correo_electronico:
        return "Correo electrónico no válido"
    if len(contraseña) < 6:
        return "La contraseña debe tener al menos 6 caracteres"
    if contraseña != conf_contraseña:
        return "Las contraseñas no coinciden"
    return None

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
        except Exception as e:
            mostrar_mensaje("Error", f"Error al crear empleado:\n{e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos")
    return False

def buscar_empleado(idempleado):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            cursor.execute("SELECT * FROM empleado WHERE idempleado = %s", (idempleado,))
            return cursor.fetchone()
        except Exception as e:
            mostrar_mensaje("Error", f"Error al buscar empleado:\n{e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos")
    return None

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
                                   contraseña, idempleado))
            conn.commit()
            mostrar_mensaje("Éxito", "Empleado actualizado exitosamente")
            return True
        except Exception as e:
            mostrar_mensaje("Error", f"Error al actualizar empleado:\n{e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos")
    return False

def eliminar_empleado(idempleado):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            cursor.execute("DELETE FROM empleado WHERE idempleado = %s", (idempleado,))
            conn.commit()
            mostrar_mensaje("Éxito", "Empleado eliminado exitosamente")
            return True
        except Exception as e:
            mostrar_mensaje("Error", f"Error al eliminar empleado:\n{e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos")
    return False

# ---------- Interfaz gráfica ----------

app = wx.App()
ventana = wx.Frame(None, title='Catálogo de Empleados', size=(600, 530))
panel = wx.Panel(ventana)

wx.StaticText(panel, label="CATÁLOGO DE EMPLEADOS", pos=(210, 15)).SetFont(
    wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
)

# Campos
campos = [
    ("ID Empleado:", "txt_id_empleado"),
    ("Nombre:", "txt_nombre"),
    ("Apellidos:", "txt_apellidos"),
    ("Teléfono:", "txt_telefono"),
    ("Correo Electrónico:", "txt_correo"),
    ("Contraseña:", "txt_contrasena"),
    ("Confirmar Contraseña:", "txt_conf_contrasena")
]

controles = {}
pos_y = 50
for etiqueta, nombre in campos:
    wx.StaticText(panel, label=etiqueta, pos=(50, pos_y))
    estilo = wx.TE_PASSWORD if "contrasena" in nombre else 0
    controles[nombre] = wx.TextCtrl(panel, pos=(200, pos_y), size=(200, -1), style=estilo)
    controles[nombre].SetBackgroundColour(wx.Colour(255, 255, 230))
    pos_y += 50

# Acciones
def on_crear(event):
    datos = [controles[n].GetValue() for n in controles]
    error = validar_campos(*datos)
    if error:
        mostrar_mensaje("Advertencia", error)
    else:
        crear_empleado(*datos[:-1])  # Excluir confirmación

def on_buscar(event):
    idemp = controles["txt_id_empleado"].GetValue()
    if not idemp:
        mostrar_mensaje("Advertencia", "Ingrese ID para buscar")
    else:
        empleado = buscar_empleado(idemp)
        if empleado:
            controles["txt_nombre"].SetValue(empleado[1])
            controles["txt_apellidos"].SetValue(empleado[2])
            controles["txt_telefono"].SetValue(empleado[3] or "")
            controles["txt_correo"].SetValue(empleado[4] or "")
            controles["txt_contrasena"].SetValue(empleado[5])
            controles["txt_conf_contrasena"].SetValue(empleado[5])

def on_actualizar(event):
    datos = [controles[n].GetValue() for n in controles]
    error = validar_campos(*datos)
    if error:
        mostrar_mensaje("Advertencia", error)
    else:
        actualizar_empleado(*datos[:-1])

def on_eliminar(event):
    idemp = controles["txt_id_empleado"].GetValue()
    if not idemp:
        mostrar_mensaje("Advertencia", "Ingrese ID para eliminar")
    else:
        eliminar_empleado(idemp)

# Botones
acciones = [
    ("Crear", on_crear, (50, 420)),
    ("Buscar", on_buscar, (180, 420)),
    ("Actualizar", on_actualizar, (310, 420)),
    ("Eliminar", on_eliminar, (440, 420))
]

for etiqueta, handler, pos in acciones:
    btn = wx.Button(panel, label=f" {etiqueta} ", pos=pos, size=(120, 40))
    btn.Bind(wx.EVT_BUTTON, handler)

ventana.Centre()
ventana.Show()
app.MainLoop()