import wx 

app = wx.App() #Instancia del objeto wx

ventana = wx.Frame(None, title='Catalogo de Proveedores', size=(600, 500)) #Creacion de la ventana 
panel = wx.Panel(ventana) #Crear panel dentro de la ventana


lbl_titulo = wx.Panel(panel, pos=(0, 0), size=(600, 40))  # titulo
lbl_titulo = wx.StaticText(lbl_titulo, label="CATALOGO DE PROVEEDORES", pos=(220, 10))
fuente_titulo = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD) # Fuente más grande y en negrita para el título
lbl_titulo.SetFont(fuente_titulo)


tamano_texto = (200, -1) # Definir un tamaño estándar para los campos de texto

# ID Proveedor
lbl_id_proveedor = wx.StaticText(panel, label="ID Proveedor:", pos=(50, 50)) #Texto
txt_id_proveedor = wx.TextCtrl(panel, pos=(200, 50), size=tamano_texto) #Input
txt_id_proveedor.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Nombre
lbl_nombre = wx.StaticText(panel, label="Nombre:", pos=(50, 100)) #Texto
txt_nombre = wx.TextCtrl(panel, pos=(200, 100), size=tamano_texto)  #Input
txt_nombre.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Contacto
lbl_contacto = wx.StaticText(panel, label="Contacto:", pos=(50, 150)) #Texto
txt_contacto = wx.TextCtrl(panel, pos=(200, 150), size=tamano_texto) #Input
txt_contacto.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Teléfono
lbl_telefono = wx.StaticText(panel, label="Teléfono:", pos=(50, 200)) #Texto
txt_telefono = wx.TextCtrl(panel, pos=(200, 200), size=tamano_texto) #Input
txt_telefono.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Correo Electrónico
lbl_correo = wx.StaticText(panel, label="Correo Electrónico:", pos=(50, 250)) #Texto
txt_correo = wx.TextCtrl(panel, pos=(200, 250), size=tamano_texto) #Input
txt_correo.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Dirección
lbl_direccion = wx.StaticText(panel, label="Dirección:", pos=(50, 300)) #Texto
txt_direccion = wx.TextCtrl(panel, pos=(200, 300), size=tamano_texto) #Input
txt_direccion.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

#BOTONES DEL CRUD 
# Create
button_crear = wx.Button(panel, label=" Crear ", pos=(50, 370), size=(120, 40))
# Read
button_buscar = wx.Button(panel, label=" Buscar ", pos=(180, 370), size=(120, 40))
# Update
button_actualizar = wx.Button(panel, label=" Actualizar ", pos=(310, 370), size=(120, 40))
# Delete
button_eliminar = wx.Button(panel, label=" Eliminar ", pos=(440, 370), size=(120, 40))


ventana.Centre() # Ventana en el centro de pantalla

ventana.Show() # Mostrar la ventana

app.MainLoop() #Mantener ventana hasta que el usuario cierre