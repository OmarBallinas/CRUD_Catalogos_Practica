import wx
from conexion import conectar
from mysql.connector import Error

app = wx.App()
ventana = wx.Frame(None, title='Catálogo de Inventario', size=(600, 400))
panel = wx.Panel(ventana)

lbl_titulo = wx.Panel(panel, pos=(0, 0), size=(600, 40))
lbl_titulo = wx.StaticText(lbl_titulo, label="CATÁLOGO DE INVENTARIO", pos=(220, 10))
lbl_titulo.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

tamano_texto = (200, -1)

# Entradas
lbl_codigo_barras = wx.StaticText(panel, label="Código de Barras:", pos=(50, 50))
txt_codigo_barras = wx.TextCtrl(panel, pos=(200, 50), size=tamano_texto)
txt_codigo_barras.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_existencia = wx.StaticText(panel, label="Existencia Actual:", pos=(50, 100))
txt_existencia = wx.TextCtrl(panel, pos=(200, 100), size=tamano_texto)
txt_existencia.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_capacidad = wx.StaticText(panel, label="Capacidad Máxima:", pos=(50, 150))
txt_capacidad = wx.TextCtrl(panel, pos=(200, 150), size=tamano_texto)
txt_capacidad.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_temporada = wx.StaticText(panel, label="Temporada:", pos=(50, 200))
temporadas = ['Verano', 'Otoño', 'Invierno', 'Primavera']
combo_temporada = wx.ComboBox(panel, pos=(200, 200), size=tamano_texto, choices=temporadas, style=wx.CB_READONLY)
combo_temporada.SetBackgroundColour(wx.Colour(255, 255, 230))

lbl_fecha = wx.StaticText(panel, label="Fecha de Caducidad:", pos=(50, 250))
txt_fecha = wx.TextCtrl(panel, pos=(200, 250), size=(200, 30), style=wx.TE_MULTILINE)
txt_fecha.SetBackgroundColour(wx.Colour(255, 255, 230))
txt_fecha.SetValue("DD/MM/AAAA")

button_no_aplica = wx.Button(panel, label="No Aplica", pos=(420, 250), size=(120, 30))

button_crear = wx.Button(panel, label=" Crear ", pos=(50, 300), size=(120, 40))
button_buscar = wx.Button(panel, label=" Buscar ", pos=(180, 300), size=(120, 40))
button_actualizar = wx.Button(panel, label=" Actualizar ", pos=(310, 300), size=(120, 40))
button_eliminar = wx.Button(panel, label=" Eliminar ", pos=(440, 300), size=(120, 40))

def mostrar_mensaje(titulo, mensaje):
    wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

def on_crear(event):
    codigo_barras = txt_codigo_barras.GetValue()
    existencia = txt_existencia.GetValue()
    capacidad = txt_capacidad.GetValue()
    temporada = combo_temporada.GetValue()
    fecha = txt_fecha.GetValue() if txt_fecha.GetValue() and txt_fecha.GetValue() != "DD/MM/AAAA" else None

    if not codigo_barras or not existencia or not capacidad or not temporada:
        mostrar_mensaje("Advertencia", "Complete todos los campos obligatorios.")
    else:
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    INSERT INTO inventario (codigo_barras, existencia_actual, capacidad_maxima, temporada, fecha_caducidad)
                    VALUES (%s, %s, %s, %s, %s)
                """, (codigo_barras, existencia, capacidad, temporada, fecha))
                conn.commit()
                mostrar_mensaje("Éxito", "Producto creado correctamente.")
            except Error as e:
                mostrar_mensaje("Error", f"Ocurrió un error al insertar: {e}")
            finally:
                cursor.close()
                conn.close()

def on_buscar(event):
    codigo_barras = txt_codigo_barras.GetValue()
    if not codigo_barras:
        mostrar_mensaje("Advertencia", "Ingrese el código de barras a buscar.")
    else:
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("SELECT existencia_actual, capacidad_maxima, temporada, fecha_caducidad FROM inventario WHERE codigo_barras = %s", (codigo_barras,))
                resultado = cursor.fetchone()
                if resultado:
                    txt_existencia.SetValue(str(resultado[0]))
                    txt_capacidad.SetValue(str(resultado[1]))
                    combo_temporada.SetValue(resultado[2])
                    txt_fecha.SetValue(resultado[3] if resultado[3] else "")
                    mostrar_mensaje("Éxito", "Producto encontrado.")
                else:
                    mostrar_mensaje("No encontrado", "No se encontró un producto con ese código.")
            except Error as e:
                mostrar_mensaje("Error", f"Error al buscar: {e}")
            finally:
                cursor.close()
                conn.close()

def on_actualizar(event):
    codigo_barras = txt_codigo_barras.GetValue()
    existencia = txt_existencia.GetValue()
    capacidad = txt_capacidad.GetValue()
    temporada = combo_temporada.GetValue()
    fecha = txt_fecha.GetValue() if txt_fecha.GetValue() and txt_fecha.GetValue() != "DD/MM/AAAA" else None

    if not codigo_barras:
        mostrar_mensaje("Advertencia", "Ingrese el código de barras a actualizar.")
    else:
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    UPDATE inventario SET existencia_actual=%s, capacidad_maxima=%s, temporada=%s, fecha_caducidad=%s
                    WHERE codigo_barras=%s
                """, (existencia, capacidad, temporada, fecha, codigo_barras))
                conn.commit()
                mostrar_mensaje("Éxito", "Producto actualizado correctamente.")
            except Error as e:
                mostrar_mensaje("Error", f"Error al actualizar: {e}")
            finally:
                cursor.close()
                conn.close()

def on_eliminar(event):
    codigo_barras = txt_codigo_barras.GetValue()
    if not codigo_barras:
        mostrar_mensaje("Advertencia", "Ingrese el código de barras a eliminar.")
    else:
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("DELETE FROM inventario WHERE codigo_barras = %s", (codigo_barras,))
                conn.commit()
                txt_existencia.SetValue("")
                txt_capacidad.SetValue("")
                combo_temporada.SetValue("")
                txt_fecha.SetValue("DD/MM/AAAA")
                mostrar_mensaje("Éxito", "Producto eliminado correctamente.")
            except Error as e:
                mostrar_mensaje("Error", f"Error al eliminar: {e}")
            finally:
                cursor.close()
                conn.close()

def on_no_aplica(event):
    txt_fecha.Clear()
    mostrar_mensaje("Información", "Fecha de caducidad no aplica. Se dejará vacía.")

# Asociar botones
button_no_aplica.Bind(wx.EVT_BUTTON, on_no_aplica)
button_crear.Bind(wx.EVT_BUTTON, on_crear)
button_buscar.Bind(wx.EVT_BUTTON, on_buscar)
button_actualizar.Bind(wx.EVT_BUTTON, on_actualizar)
button_eliminar.Bind(wx.EVT_BUTTON, on_eliminar)

ventana.Centre()
ventana.Show()
app.MainLoop()