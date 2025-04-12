import wx 

app = wx.App() #Instancia del objeto wx

ventana = wx.Frame(None, title='Catalogo de Usuarios', size=(600, 450)) #Creacion de la ventana 
panel = wx.Panel(ventana) #Crear panel dentro de la ventana


lbl_titulo = wx.Panel(panel, pos=(0, 0), size=(600, 40))  # titulo
lbl_titulo = wx.StaticText(lbl_titulo, label="CATALOGO DE USUARIOS", pos=(220, 10))
fuente_titulo = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD) # Fuente más grande y en negrita para el título
lbl_titulo.SetFont(fuente_titulo)


tamano_texto = (200, -1) # Definir un tamaño estándar para los campos de texto

# ID Empleado
lbl_id_empleado = wx.StaticText(panel, label="ID Empleado:", pos=(50, 50)) #Texto
txt_id_empleado = wx.TextCtrl(panel, pos=(200, 50), size=tamano_texto) #Input
txt_id_empleado.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Nombre
lbl_nombre = wx.StaticText(panel, label="Nombre:", pos=(50, 100)) #Texto
txt_nombre = wx.TextCtrl(panel, pos=(200, 100), size=tamano_texto)  #Input
txt_nombre.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Contraseña
lbl_contrasena = wx.StaticText(panel, label="Contraseña:", pos=(50, 150)) #Texto
txt_contrasena = wx.TextCtrl(panel, pos=(200, 150), size=tamano_texto, style=wx.TE_PASSWORD) #Input oculto
txt_contrasena.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Confirmar Contraseña
lbl_conf_contrasena = wx.StaticText(panel, label="Confirmar Contraseña:", pos=(50, 200)) #Texto
txt_conf_contrasena = wx.TextCtrl(panel, pos=(200, 200), size=tamano_texto, style=wx.TE_PASSWORD) #Input oculto
txt_conf_contrasena.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Último Acceso
lbl_ultimo_acceso = wx.StaticText(panel, label="Último Acceso:", pos=(50, 250)) #Texto
txt_ultimo_acceso = wx.TextCtrl(panel, pos=(200, 250), size=tamano_texto) #Input
txt_ultimo_acceso.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Estatus
lbl_estatus = wx.StaticText(panel, label="Estatus:", pos=(50, 300)) #Texto
opciones_estatus = ["Activo", "Inactivo"]
cmb_estatus = wx.Choice(panel, pos=(200, 300), size=tamano_texto, choices=opciones_estatus) #Selector
cmb_estatus.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

#BOTONES DEL CRUD 
# Create
button_crear = wx.Button(panel, label=" Crear ", pos=(50, 350), size=(120, 40))
# Read
button_buscar = wx.Button(panel, label=" Buscar ", pos=(180, 350), size=(120, 40))
# Update
button_actualizar = wx.Button(panel, label=" Actualizar ", pos=(310, 350), size=(120, 40))
# Delete
button_eliminar = wx.Button(panel, label=" Eliminar ", pos=(440, 350), size=(120, 40))


ventana.Centre() # Ventana en el centro de pantalla

ventana.Show() # Mostrar la ventana

app.MainLoop() #Mantener ventana hasta que el usuario cierre