# archivo: articulo_crud.py
import wx
from conexion import conectar

# Función para mostrar el cuadro de mensaje emergente
def mostrar_mensaje(titulo, mensaje):
    wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

# Función para agregar un artículo
def agregar_articulo(codigo, nombre, descripcion, precio, unidad, descuento, id_categoria):
    try:
        conn, cursor = conectar()
        query = """
        INSERT INTO articulo (codigo_barras, nombre, descripcion, precio, unidad, descuento, idcategoria)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            codigo,
            nombre,
            descripcion,
            float(precio),
            unidad,
            float(descuento),
            int(id_categoria)
        ))
        conn.commit()
        cursor.close()
        conn.close()
        mostrar_mensaje("Éxito", "Artículo creado exitosamente.")
    except Exception as e:
        mostrar_mensaje("Error", f"Error al crear el artículo: {e}")

# Función para actualizar un artículo
def actualizar_articulo(codigo, nombre, descripcion, precio, unidad, descuento, id_categoria):
    try:
        conn, cursor = conectar()
        query = """
        UPDATE articulo
        SET nombre = %s, descripcion = %s, precio = %s, unidad = %s, descuento = %s, idcategoria = %s
        WHERE codigo_barras = %s
        """
        cursor.execute(query, (
            nombre,
            descripcion,
            float(precio),
            unidad,
            float(descuento),
            int(id_categoria),
            codigo
        ))
        conn.commit()
        cursor.close()
        conn.close()
        mostrar_mensaje("Éxito", "Artículo actualizado exitosamente.")
    except Exception as e:
        mostrar_mensaje("Error", f"Error al actualizar el artículo: {e}")

# Función para eliminar un artículo
def eliminar_articulo(codigo):
    try:
        conn, cursor = conectar()
        query = "DELETE FROM articulo WHERE codigo_barras = %s"
        cursor.execute(query, (codigo,))
        conn.commit()
        cursor.close()
        conn.close()
        mostrar_mensaje("Éxito", "Artículo eliminado exitosamente.")
    except Exception as e:
        mostrar_mensaje("Error", f"Error al eliminar el artículo: {e}")

# Función para buscar un artículo
def buscar_articulo(codigo):
    try:
        conn, cursor = conectar()
        query = "SELECT * FROM articulo WHERE codigo_barras = %s"
        cursor.execute(query, (codigo,))
        articulo = cursor.fetchone()
        cursor.close()
        conn.close()
        if articulo:
            return articulo
        else:
            mostrar_mensaje("No encontrado", "Artículo no encontrado.")
            return None
    except Exception as e:
        mostrar_mensaje("Error", f"Error al buscar el artículo: {e}")
        return None

# Ventana principal
app = wx.App()
ventana = wx.Frame(None, title='Catálogo de Artículos', size=(600, 450))
panel = wx.Panel(ventana)

# Título
lbl_titulo = wx.Panel(panel, pos=(0, 0), size=(600, 40))
lbl_titulo = wx.StaticText(lbl_titulo, label="CATÁLOGO DE ARTÍCULOS", pos=(220, 10))
fuente_titulo = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
lbl_titulo.SetFont(fuente_titulo)

tamano_texto = (200, -1)

# Campos de texto
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
button_crear = wx.Button(panel, label=" Crear ", pos=(50, 360), size=(120, 40))
button_buscar = wx.Button(panel, label=" Buscar ", pos=(180, 360), size=(120, 40))
button_actualizar = wx.Button(panel, label=" Actualizar ", pos=(310, 360), size=(120, 40))
button_eliminar = wx.Button(panel, label=" Eliminar ", pos=(440, 360), size=(120, 40))

# Eventos
def on_crear(event):
    codigo = txt_codigo.GetValue()
    nombre = txt_nombre.GetValue()
    descripcion = txt_descripcion.GetValue()
    precio = txt_precio.GetValue()
    unidad = txt_unidad.GetValue()
    descuento = txt_descuento.GetValue()
    id_categoria = txt_id_categoria.GetValue()
    agregar_articulo(codigo, nombre, descripcion, precio, unidad, descuento, id_categoria)

def on_buscar(event):
    codigo = txt_codigo.GetValue()
    articulo = buscar_articulo(codigo)
    if articulo:
        txt_nombre.SetValue(articulo[1])         # nombre
        txt_descripcion.SetValue(articulo[2])    # descripcion
        txt_precio.SetValue(str(articulo[3]))    # precio
        txt_unidad.SetValue(articulo[4])         # unidad
        txt_descuento.SetValue(str(articulo[5])) # descuento
        txt_id_categoria.SetValue(str(articulo[6])) # idcategoria

def on_actualizar(event):
    codigo = txt_codigo.GetValue()
    nombre = txt_nombre.GetValue()
    descripcion = txt_descripcion.GetValue()
    precio = txt_precio.GetValue()
    unidad = txt_unidad.GetValue()
    descuento = txt_descuento.GetValue()
    id_categoria = txt_id_categoria.GetValue()
    actualizar_articulo(codigo, nombre, descripcion, precio, unidad, descuento, id_categoria)

def on_eliminar(event):
    codigo = txt_codigo.GetValue()
    eliminar_articulo(codigo)

# Asignación de eventos a botones
button_crear.Bind(wx.EVT_BUTTON, on_crear)
button_buscar.Bind(wx.EVT_BUTTON, on_buscar)
button_actualizar.Bind(wx.EVT_BUTTON, on_actualizar)
button_eliminar.Bind(wx.EVT_BUTTON, on_eliminar)

# Mostrar ventana
ventana.Centre()
ventana.Show()
app.MainLoop()
