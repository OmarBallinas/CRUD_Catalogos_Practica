# categorias.py
import wx
from conexion import conectar

def mostrar_mensaje(titulo, mensaje):
    wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

# Crear
def crear_categoria(id_categoria, nombre):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            cursor.execute("INSERT INTO categoria (idcategoria, nombre) VALUES (%s, %s)", (id_categoria, nombre))
            conn.commit()
            mostrar_mensaje("Éxito", "Categoría creada exitosamente.")
        except Exception as e:
            mostrar_mensaje("Error", f"Error al crear categoría: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos.")

# Buscar
def buscar_categoria(id_categoria):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            cursor.execute("SELECT idcategoria, nombre FROM categoria WHERE idcategoria = %s", (id_categoria,))
            resultado = cursor.fetchone()
            return resultado
        except Exception as e:
            mostrar_mensaje("Error", f"Error al buscar categoría: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos.")
    return None

# Actualizar
def actualizar_categoria(id_categoria, nombre):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            cursor.execute("UPDATE categoria SET nombre = %s WHERE idcategoria = %s", (nombre, id_categoria))
            conn.commit()
            mostrar_mensaje("Éxito", "Categoría actualizada exitosamente.")
        except Exception as e:
            mostrar_mensaje("Error", f"Error al actualizar categoría: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos.")

# Eliminar
def eliminar_categoria(id_categoria):
    conn, cursor = conectar()
    if conn and cursor:
        try:
            cursor.execute("DELETE FROM categoria WHERE idcategoria = %s", (id_categoria,))
            conn.commit()
            mostrar_mensaje("Éxito", "Categoría eliminada exitosamente.")
        except Exception as e:
            mostrar_mensaje("Error", f"Error al eliminar categoría: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        mostrar_mensaje("Error", "No se pudo conectar a la base de datos.")

# Interfaz gráfica
app = wx.App()
ventana = wx.Frame(None, title='Catálogo de Categoría', size=(600, 250))
panel = wx.Panel(ventana)

lbl_titulo = wx.Panel(panel, pos=(0, 0), size=(600, 40))
lbl_titulo = wx.StaticText(lbl_titulo, label="CATÁLOGO DE CATEGORÍAS", pos=(220, 10))
lbl_titulo.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

tamano_texto = (200, -1)

# Entradas
lbl_id_categoria = wx.StaticText(panel, label="ID Categoría:", pos=(50, 50))
txt_id_categoria = wx.TextCtrl(panel, pos=(200, 50), size=tamano_texto)
txt_id_categoria.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_nombre = wx.StaticText(panel, label="Nombre:", pos=(50, 100))
txt_nombre = wx.TextCtrl(panel, pos=(200, 100), size=tamano_texto)
txt_nombre.SetBackgroundColour(wx.Colour(255, 255, 230))

# Botones
btn_crear = wx.Button(panel, label=" Crear ", pos=(50, 150), size=(120, 40))
btn_buscar = wx.Button(panel, label=" Buscar ", pos=(180, 150), size=(120, 40))
btn_actualizar = wx.Button(panel, label=" Actualizar ", pos=(310, 150), size=(120, 40))
btn_eliminar = wx.Button(panel, label=" Eliminar ", pos=(440, 150), size=(120, 40))

# Eventos
def on_crear(event):
    if txt_id_categoria.GetValue() and txt_nombre.GetValue():
        crear_categoria(txt_id_categoria.GetValue(), txt_nombre.GetValue())
    else:
        mostrar_mensaje("Advertencia", "Por favor, complete todos los campos.")

def on_buscar(event):
    if txt_id_categoria.GetValue():
        categoria = buscar_categoria(txt_id_categoria.GetValue())
        if categoria:
            txt_nombre.SetValue(categoria[1])
    else:
        mostrar_mensaje("Advertencia", "Por favor, ingrese un ID de categoría.")

def on_actualizar(event):
    if txt_id_categoria.GetValue() and txt_nombre.GetValue():
        actualizar_categoria(txt_id_categoria.GetValue(), txt_nombre.GetValue())
    else:
        mostrar_mensaje("Advertencia", "Por favor, complete todos los campos.")

def on_eliminar(event):
    if txt_id_categoria.GetValue():
        eliminar_categoria(txt_id_categoria.GetValue())
        txt_id_categoria.Clear()
        txt_nombre.Clear()
    else:
        mostrar_mensaje("Advertencia", "Por favor, ingrese un ID de categoría.")

btn_crear.Bind(wx.EVT_BUTTON, on_crear)
btn_buscar.Bind(wx.EVT_BUTTON, on_buscar)
btn_actualizar.Bind(wx.EVT_BUTTON, on_actualizar)
btn_eliminar.Bind(wx.EVT_BUTTON, on_eliminar)

ventana.Centre()
ventana.Show()
app.MainLoop()