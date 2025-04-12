import wx 

app = wx.App() #Instancia del objeto wx

ventana = wx.Frame(None, title='Catalogo de Inventario', size=(600, 400)) #Creacion de la ventana 
panel = wx.Panel(ventana) #Crear panel dentro de la ventana


lbl_titulo = wx.Panel(panel, pos=(0, 0), size=(600, 40))  # titulo
lbl_titulo = wx.StaticText(lbl_titulo, label="CATALOGO DE INVENTARIO", pos=(220, 10))
fuente_titulo = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD) # Fuente más grande y en negrita para el título
lbl_titulo.SetFont(fuente_titulo)


tamano_texto = (200, -1) # Definir un tamaño estándar para los campos de texto

# Código de Barras
lbl_codigo_barras = wx.StaticText(panel, label="Código de Barras:", pos=(50, 50)) #Texto
txt_codigo_barras = wx.TextCtrl(panel, pos=(200, 50), size=tamano_texto) #Input
txt_codigo_barras.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Existencia Actual
lbl_existencia = wx.StaticText(panel, label="Existencia Actual:", pos=(50, 100)) #Texto
txt_existencia = wx.TextCtrl(panel, pos=(200, 100), size=tamano_texto)  #Input
txt_existencia.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Capacidad Máxima
lbl_capacidad = wx.StaticText(panel, label="Capacidad Máxima:", pos=(50, 150)) #Texto
txt_capacidad = wx.TextCtrl(panel, pos=(200, 150), size=tamano_texto) #Input
txt_capacidad.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Ubicación
lbl_ubicacion = wx.StaticText(panel, label="Ubicación:", pos=(50, 200)) #Texto
txt_ubicacion = wx.TextCtrl(panel, pos=(200, 200), size=tamano_texto) #Input
txt_ubicacion.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Fecha Actualización
lbl_fecha = wx.StaticText(panel, label="Fecha Actualización:", pos=(50, 250)) #Texto
txt_fecha = wx.TextCtrl(panel, pos=(200, 250), size=tamano_texto) #Input
txt_fecha.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

#BOTONES DEL CRUD 
# Create
button_crear = wx.Button(panel, label=" Crear ", pos=(50, 300), size=(120, 40))
# Read
button_buscar = wx.Button(panel, label=" Buscar ", pos=(180, 300), size=(120, 40))
# Update
button_actualizar = wx.Button(panel, label=" Actualizar ", pos=(310, 300), size=(120, 40))
# Delete
button_eliminar = wx.Button(panel, label=" Eliminar ", pos=(440, 300), size=(120, 40))


ventana.Centre() # Ventana en el centro de pantalla

ventana.Show() # Mostrar la ventana

app.MainLoop() #Mantener ventana hasta que el usuario cierre