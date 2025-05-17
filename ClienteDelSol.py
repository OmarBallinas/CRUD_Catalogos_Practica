# clientes.py
import wx
from conexion import conectar

# Función para mostrar mensajes emergentes
def mostrar_mensaje(titulo, mensaje):
    wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

# Crear cliente
def crear_cliente(telefono, nombre, apellido, correo):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            cursor.execute("INSERT INTO cliente (telefono_cliente, nombre, apellido, correo_electronico) VALUES (%s, %s, %s, %s)", 
                           (telefono, nombre, apellido, correo))
            conn.commit()
            mostrar_mensaje("Éxito", "Cliente creado exitosamente.")
        except Exception as e:
            mostrar_mensaje("Error", f"Error al crear cliente: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos.")

# Buscar cliente
def buscar_cliente(telefono):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            cursor.execute("SELECT telefono_cliente, nombre, apellido, correo_electronico FROM cliente WHERE telefono_cliente = %s", 
                           (telefono,))
            resultado = cursor.fetchone()
            return resultado
        except Exception as e:
            mostrar_mensaje("Error", f"Error al buscar cliente: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos.")
    return None

# Actualizar cliente
def actualizar_cliente(telefono, nombre, apellido, correo):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            cursor.execute("UPDATE cliente SET nombre = %s, apellido = %s, correo_electronico = %s WHERE telefono_cliente = %s", 
                           (nombre, apellido, correo, telefono))
            conn.commit()
            mostrar_mensaje("Éxito", "Cliente actualizado exitosamente.")
        except Exception as e:
            mostrar_mensaje("Error", f"Error al actualizar cliente: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos.")

# Eliminar cliente
def eliminar_cliente(telefono):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            cursor.execute("DELETE FROM cliente WHERE telefono_cliente = %s", (telefono,))
            conn.commit()
            mostrar_mensaje("Éxito", "Cliente eliminado exitosamente.")
        except Exception as e:
            mostrar_mensaje("Error", f"Error al eliminar cliente: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos.")

# Interfaz gráfica
app = wx.App()
ventana = wx.Frame(None, title='Catálogo de Clientes', size=(600, 450))
panel = wx.Panel(ventana)

lbl_titulo = wx.Panel(panel, pos=(0, 0), size=(600, 40))
lbl_titulo = wx.StaticText(lbl_titulo, label="CATÁLOGO DE CLIENTES", pos=(220, 10))
lbl_titulo.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

tamano_texto = (200, -1)

# Entradas
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

# Botones
btn_crear = wx.Button(panel, label=" Crear ", pos=(50, 300), size=(120, 40))
btn_buscar = wx.Button(panel, label=" Buscar ", pos=(180, 300), size=(120, 40))
btn_actualizar = wx.Button(panel, label=" Actualizar ", pos=(310, 300), size=(120, 40))
btn_eliminar = wx.Button(panel, label=" Eliminar ", pos=(440, 300), size=(120, 40))

# Eventos
def on_crear(event):
    if txt_telefono.GetValue() and txt_nombre.GetValue() and txt_apellido.GetValue() and txt_correo.GetValue():
        crear_cliente(txt_telefono.GetValue(), txt_nombre.GetValue(), txt_apellido.GetValue(), txt_correo.GetValue())
    else:
        mostrar_mensaje("Advertencia", "Por favor, complete todos los campos.")

def on_buscar(event):
    if txt_telefono.GetValue():
        cliente = buscar_cliente(txt_telefono.GetValue())
        if cliente:
            txt_nombre.SetValue(cliente[1])
            txt_apellido.SetValue(cliente[2])
            txt_correo.SetValue(cliente[3])
    else:
        mostrar_mensaje("Advertencia", "Por favor, ingrese un teléfono de cliente.")

def on_actualizar(event):
    if txt_telefono.GetValue() and txt_nombre.GetValue() and txt_apellido.GetValue() and txt_correo.GetValue():
        actualizar_cliente(txt_telefono.GetValue(), txt_nombre.GetValue(), txt_apellido.GetValue(), txt_correo.GetValue())
    else:
        mostrar_mensaje("Advertencia", "Por favor, complete todos los campos.")

def on_eliminar(event):
    if txt_telefono.GetValue():
        eliminar_cliente(txt_telefono.GetValue())
        txt_telefono.Clear()
        txt_nombre.Clear()
        txt_apellido.Clear()
        txt_correo.Clear()
    else:
        mostrar_mensaje("Advertencia", "Por favor, ingrese un teléfono de cliente.")

btn_crear.Bind(wx.EVT_BUTTON, on_crear)
btn_buscar.Bind(wx.EVT_BUTTON, on_buscar)
btn_actualizar.Bind(wx.EVT_BUTTON, on_actualizar)
btn_eliminar.Bind(wx.EVT_BUTTON, on_eliminar)

ventana.Centre()
ventana.Show()
app.MainLoop()
