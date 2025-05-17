# articulo_crud.py
import wx
from conexion import conectar

# Función para mostrar mensajes
def mostrar_mensaje(titulo, mensaje):
    wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

# Crear artículo
def agregar_articulo(codigo, nombre, descripcion, precio, unidad, descuento, id_categoria):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            cursor.execute("""
                INSERT INTO articulo (codigo_barras, nombre, descripcion, precio, unidad, descuento, idcategoria)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (codigo, nombre, descripcion, float(precio), unidad, float(descuento), int(id_categoria)))
            conn.commit()
            mostrar_mensaje("Éxito", "Artículo creado exitosamente.")
        except Exception as e:
            mostrar_mensaje("Error", f"Error al crear el artículo: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos.")

# Buscar artículo
def buscar_articulo(codigo):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            cursor.execute("SELECT * FROM articulo WHERE codigo_barras = %s", (codigo,))
            resultado = cursor.fetchone()
            return resultado
        except Exception as e:
            mostrar_mensaje("Error", f"Error al buscar el artículo: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos.")
    return None

# Actualizar artículo
def actualizar_articulo(codigo, nombre, descripcion, precio, unidad, descuento, id_categoria):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            cursor.execute("""
                UPDATE articulo
                SET nombre = %s, descripcion = %s, precio = %s, unidad = %s, descuento = %s, idcategoria = %s
                WHERE codigo_barras = %s
            """, (nombre, descripcion, float(precio), unidad, float(descuento), int(id_categoria), codigo))
            conn.commit()
            mostrar_mensaje("Éxito", "Artículo actualizado exitosamente.")
        except Exception as e:
            mostrar_mensaje("Error", f"Error al actualizar el artículo: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos.")

# Eliminar artículo
def eliminar_articulo(codigo):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            cursor.execute("DELETE FROM articulo WHERE codigo_barras = %s", (codigo,))
            conn.commit()
            mostrar_mensaje("Éxito", "Artículo eliminado exitosamente.")
        except Exception as e:
            mostrar_mensaje("Error", f"Error al eliminar el artículo: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos.")

# Interfaz gráfica
app = wx.App()
ventana = wx.Frame(None, title='Catálogo de Artículos', size=(600, 450))
panel = wx.Panel(ventana)

lbl_titulo = wx.Panel(panel, pos=(0, 0), size=(600, 40))
lbl_titulo = wx.StaticText(lbl_titulo, label="CATÁLOGO DE ARTÍCULOS", pos=(220, 10))
lbl_titulo.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

tamano_texto = (200, -1)

# Entradas
lbl_codigo = wx.StaticText(panel, label="Código de Barras:", pos=(50, 50))
txt_codigo = wx.TextCtrl(panel, pos=(200, 50), size=tamano_texto)
txt_codigo.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_nombre = wx.StaticText(panel, label="Nombre:", pos=(50, 90))
txt_nombre = wx.TextCtrl(panel, pos=(200, 90), size=tamano_texto)
txt_nombre.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_descripcion = wx.StaticText(panel, label="Descripción:", pos=(50, 130))
txt_descripcion = wx.TextCtrl(panel, pos=(200, 130), size=(200, 60), style=wx.TE_MULTILINE)
txt_descripcion.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_precio = wx.StaticText(panel, label="Precio:", pos=(50, 200))
txt_precio = wx.TextCtrl(panel, pos=(200, 200), size=tamano_texto)
txt_precio.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_unidad = wx.StaticText(panel, label="Unidad:", pos=(50, 240))
txt_unidad = wx.TextCtrl(panel, pos=(200, 240), size=tamano_texto)
txt_unidad.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_descuento = wx.StaticText(panel, label="Descuento:", pos=(50, 280))
txt_descuento = wx.TextCtrl(panel, pos=(200, 280), size=tamano_texto)
txt_descuento.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_id_categoria = wx.StaticText(panel, label="ID Categoría:", pos=(50, 320))
txt_id_categoria = wx.TextCtrl(panel, pos=(200, 320), size=tamano_texto)
txt_id_categoria.SetBackgroundColour(wx.Colour(255, 255, 230))

# Botones
btn_crear = wx.Button(panel, label=" Crear ", pos=(50, 360), size=(120, 40))
btn_buscar = wx.Button(panel, label=" Buscar ", pos=(180, 360), size=(120, 40))
btn_actualizar = wx.Button(panel, label=" Actualizar ", pos=(310, 360), size=(120, 40))
btn_eliminar = wx.Button(panel, label=" Eliminar ", pos=(440, 360), size=(120, 40))

# Eventos
def on_crear(event):
    if all([
        txt_codigo.GetValue(), txt_nombre.GetValue(), txt_descripcion.GetValue(),
        txt_precio.GetValue(), txt_unidad.GetValue(), txt_descuento.GetValue(),
        txt_id_categoria.GetValue()
    ]):
        agregar_articulo(
            txt_codigo.GetValue(),
            txt_nombre.GetValue(),
            txt_descripcion.GetValue(),
            txt_precio.GetValue(),
            txt_unidad.GetValue(),
            txt_descuento.GetValue(),
            txt_id_categoria.GetValue()
        )
    else:
        mostrar_mensaje("Advertencia", "Por favor, complete todos los campos.")

def on_buscar(event):
    if txt_codigo.GetValue():
        articulo = buscar_articulo(txt_codigo.GetValue())
        if articulo:
            txt_nombre.SetValue(articulo[1])
            txt_descripcion.SetValue(articulo[2])
            txt_precio.SetValue(str(articulo[3]))
            txt_unidad.SetValue(articulo[4])
            txt_descuento.SetValue(str(articulo[5]))
            txt_id_categoria.SetValue(str(articulo[6]))
    else:
        mostrar_mensaje("Advertencia", "Por favor, ingrese el código de barras.")

def on_actualizar(event):
    if all([
        txt_codigo.GetValue(), txt_nombre.GetValue(), txt_descripcion.GetValue(),
        txt_precio.GetValue(), txt_unidad.GetValue(), txt_descuento.GetValue(),
        txt_id_categoria.GetValue()
    ]):
        actualizar_articulo(
            txt_codigo.GetValue(),
            txt_nombre.GetValue(),
            txt_descripcion.GetValue(),
            txt_precio.GetValue(),
            txt_unidad.GetValue(),
            txt_descuento.GetValue(),
            txt_id_categoria.GetValue()
        )
    else:
        mostrar_mensaje("Advertencia", "Por favor, complete todos los campos.")

def on_eliminar(event):
    if txt_codigo.GetValue():
        eliminar_articulo(txt_codigo.GetValue())
        txt_codigo.Clear()
        txt_nombre.Clear()
        txt_descripcion.Clear()
        txt_precio.Clear()
        txt_unidad.Clear()
        txt_descuento.Clear()
        txt_id_categoria.Clear()
    else:
        mostrar_mensaje("Advertencia", "Por favor, ingrese el código de barras.")

# Asociar eventos
btn_crear.Bind(wx.EVT_BUTTON, on_crear)
btn_buscar.Bind(wx.EVT_BUTTON, on_buscar)
btn_actualizar.Bind(wx.EVT_BUTTON, on_actualizar)
btn_eliminar.Bind(wx.EVT_BUTTON, on_eliminar)

ventana.Centre()
ventana.Show()
app.MainLoop()
