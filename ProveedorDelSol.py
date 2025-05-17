import wx
from conexion import conectar

app = wx.App()
ventana = wx.Frame(None, title="Catálogo de Proveedores", size=(600, 500))
panel = wx.Panel(ventana)

# Título
titulo_panel = wx.Panel(panel, pos=(0, 0), size=(600, 40))
lbl_titulo = wx.StaticText(titulo_panel, label="CATÁLOGO DE PROVEEDORES", pos=(220, 10))
fuente_titulo = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
lbl_titulo.SetFont(fuente_titulo)

# Tamaño estándar para campos
tamano_texto = (200, -1)

# Labels y TextCtrl globales
lbl_id = wx.StaticText(panel, label="ID Proveedor:", pos=(50, 50))
txt_id = wx.TextCtrl(panel, pos=(200, 50), size=tamano_texto)
txt_id.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_nombre = wx.StaticText(panel, label="Nombre:", pos=(50, 100))
txt_nombre = wx.TextCtrl(panel, pos=(200, 100), size=tamano_texto)
txt_nombre.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_contacto = wx.StaticText(panel, label="Contacto:", pos=(50, 150))
txt_contacto = wx.TextCtrl(panel, pos=(200, 150), size=tamano_texto)
txt_contacto.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_telefono = wx.StaticText(panel, label="Teléfono:", pos=(50, 200))
txt_telefono = wx.TextCtrl(panel, pos=(200, 200), size=tamano_texto)
txt_telefono.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_correo = wx.StaticText(panel, label="Correo Electrónico:", pos=(50, 250))
txt_correo = wx.TextCtrl(panel, pos=(200, 250), size=tamano_texto)
txt_correo.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_direccion = wx.StaticText(panel, label="Dirección:", pos=(50, 300))
txt_direccion = wx.TextCtrl(panel, pos=(200, 300), size=tamano_texto)
txt_direccion.SetBackgroundColour(wx.Colour(255, 255, 230))

# Botones
btn_crear = wx.Button(panel, label=" Crear ", pos=(50, 370), size=(120, 40))
btn_buscar = wx.Button(panel, label=" Buscar ", pos=(180, 370), size=(120, 40))
btn_actualizar = wx.Button(panel, label=" Actualizar ", pos=(310, 370), size=(120, 40))
btn_eliminar = wx.Button(panel, label=" Eliminar ", pos=(440, 370), size=(120, 40))

def mostrar_mensaje(titulo, mensaje):
    wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

def limpiar_campos():
    txt_id.SetValue("")
    txt_nombre.SetValue("")
    txt_contacto.SetValue("")
    txt_telefono.SetValue("")
    txt_correo.SetValue("")
    txt_direccion.SetValue("")

def crear(event):
    idproveedor = txt_id.GetValue()
    nombre = txt_nombre.GetValue()
    contacto = txt_contacto.GetValue()
    telefono = txt_telefono.GetValue()
    correo = txt_correo.GetValue()
    direccion = txt_direccion.GetValue()

    if not idproveedor or not nombre or not contacto or not telefono:
        mostrar_mensaje("Advertencia", "Los campos ID, Nombre, Contacto y Teléfono son obligatorios.")
        return

    conn, cursor = conectar()
    if conn and cursor:
        try:
            cursor.execute("""
                INSERT INTO proveedor (idproveedor, nombre, contacto, telefono, correo_electronico, direccion)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (idproveedor, nombre, contacto, telefono, correo, direccion))
            conn.commit()
            mostrar_mensaje("Éxito", "Proveedor creado correctamente.")
        except Exception as e:
            mostrar_mensaje("Error", f"No se pudo crear el proveedor:\n{e}")
        finally:
            cursor.close()
            conn.close()

def buscar(event):
    idproveedor = txt_id.GetValue()
    if not idproveedor:
        mostrar_mensaje("Advertencia", "Ingrese el ID del proveedor a buscar.")
        return

    conn, cursor = conectar()
    if conn and cursor:
        try:
            cursor.execute("SELECT * FROM proveedor WHERE idproveedor = %s", (idproveedor,))
            resultado = cursor.fetchone()
            if resultado:
                txt_nombre.SetValue(str(resultado[1]))
                txt_contacto.SetValue(str(resultado[2]))
                txt_telefono.SetValue(str(resultado[3]))
                txt_correo.SetValue(str(resultado[4]))
                txt_direccion.SetValue(str(resultado[5]))
                mostrar_mensaje("Proveedor encontrado", f"Datos cargados para ID {idproveedor}.")
            else:
                mostrar_mensaje("No encontrado", "No se encontró el proveedor.")
        except Exception as e:
            mostrar_mensaje("Error", f"No se pudo recuperar el proveedor:\n{e}")
        finally:
            cursor.close()
            conn.close()

def actualizar(event):
    idproveedor = txt_id.GetValue()
    nombre = txt_nombre.GetValue()
    contacto = txt_contacto.GetValue()
    telefono = txt_telefono.GetValue()
    correo = txt_correo.GetValue()
    direccion = txt_direccion.GetValue()

    if not idproveedor:
        mostrar_mensaje("Advertencia", "Ingrese el ID del proveedor a actualizar.")
        return

    conn, cursor = conectar()
    if conn and cursor:
        try:
            cursor.execute("""
                UPDATE proveedor SET 
                    nombre=%s, contacto=%s, telefono=%s, 
                    correo_electronico=%s, direccion=%s 
                WHERE idproveedor=%s
            """, (nombre, contacto, telefono, correo, direccion, idproveedor))
            conn.commit()
            mostrar_mensaje("Actualizado", f"Proveedor {idproveedor} actualizado correctamente.")
        except Exception as e:
            mostrar_mensaje("Error", f"No se pudo actualizar el proveedor:\n{e}")
        finally:
            cursor.close()
            conn.close()

def eliminar(event):
    idproveedor = txt_id.GetValue()
    if not idproveedor:
        mostrar_mensaje("Advertencia", "Ingrese el ID del proveedor a eliminar.")
        return

    conn, cursor = conectar()
    if conn and cursor:
        try:
            cursor.execute("DELETE FROM proveedor WHERE idproveedor = %s", (idproveedor,))
            conn.commit()
            mostrar_mensaje("Eliminado", f"Proveedor {idproveedor} eliminado correctamente.")
            limpiar_campos()
        except Exception as e:
            mostrar_mensaje("Error", f"No se pudo eliminar el proveedor:\n{e}")
        finally:
            cursor.close()
            conn.close()

# Bind de eventos
btn_crear.Bind(wx.EVT_BUTTON, crear)
btn_buscar.Bind(wx.EVT_BUTTON, buscar)
btn_actualizar.Bind(wx.EVT_BUTTON, actualizar)
btn_eliminar.Bind(wx.EVT_BUTTON, eliminar)

ventana.Centre()
ventana.Show()
app.MainLoop()