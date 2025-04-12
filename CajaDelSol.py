import wx 

app = wx.App() #Instancia del objeto wx

ventana = wx.Frame(None, title='Catalogo de Cajas', size=(600, 400)) #Creacion de la ventana 
panel = wx.Panel(ventana) #Crear panel dentro de la ventana


lbl_titulo = wx.Panel(panel, pos=(0, 0), size=(600, 40))  # titulo
lbl_titulo = wx.StaticText(lbl_titulo, label="CATALOGO DE CAJAS", pos=(220, 10))
fuente_titulo = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD) # Fuente más grande y en negrita para el título
lbl_titulo.SetFont(fuente_titulo)


tamano_texto = (200, -1) # Definir un tamaño estándar para los campos de texto

# ID Caja
lbl_id_caja = wx.StaticText(panel, label="ID Caja:", pos=(50, 50)) #Texto
txt_id_caja = wx.TextCtrl(panel, pos=(200, 50), size=tamano_texto) #Input
txt_id_caja.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Estatus
lbl_estatus = wx.StaticText(panel, label="Estatus:", pos=(50, 100)) #Texto
opciones_estatus = ["Disponible", "No Disponible"]
cmb_estatus = wx.Choice(panel, pos=(200, 100), size=tamano_texto, choices=opciones_estatus) #Selector
cmb_estatus.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Numero Caja
lbl_numero_caja = wx.StaticText(panel, label="Numero Caja:", pos=(50, 150)) #Texto
txt_numero_caja = wx.TextCtrl(panel, pos=(200, 150), size=tamano_texto) #Input
txt_numero_caja.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Modelo
lbl_modelo = wx.StaticText(panel, label="Modelo:", pos=(50, 200)) #Texto
txt_modelo = wx.TextCtrl(panel, pos=(200, 200), size=tamano_texto) #Input
txt_modelo.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

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