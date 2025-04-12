import wx 

app = wx.App() #Instancia del objeto wx

ventana = wx.Frame(None, title='Catalogo de Categorías', size=(600, 250)) #Creacion de la ventana 
panel = wx.Panel(ventana) #Crear panel dentro de la ventana


lbl_titulo = wx.Panel(panel, pos=(0, 0), size=(600, 40))  # titulo
lbl_titulo = wx.StaticText(lbl_titulo, label="CATALOGO DE CATEGORÍAS", pos=(220, 10))
fuente_titulo = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD) # Fuente más grande y en negrita para el título
lbl_titulo.SetFont(fuente_titulo)


tamano_texto = (200, -1) # Definir un tamaño estándar para los campos de texto

# ID Categoría
lbl_id_categoria = wx.StaticText(panel, label="ID Categoría:", pos=(50, 50)) #Texto
txt_id_categoria = wx.TextCtrl(panel, pos=(200, 50), size=tamano_texto) #Input
txt_id_categoria.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Nombre
lbl_nombre = wx.StaticText(panel, label="Nombre:", pos=(50, 100)) #Texto
txt_nombre = wx.TextCtrl(panel, pos=(200, 100), size=tamano_texto)  #Input
txt_nombre.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

#BOTONES DEL CRUD 
# Create
button_crear = wx.Button(panel, label=" Crear ", pos=(50, 150), size=(120, 40))
# Read
button_buscar = wx.Button(panel, label=" Buscar ", pos=(180, 150), size=(120, 40))
# Update
button_actualizar = wx.Button(panel, label=" Actualizar ", pos=(310, 150), size=(120, 40))
# Delete
button_eliminar = wx.Button(panel, label=" Eliminar ", pos=(440, 150), size=(120, 40))


ventana.Centre() # Ventana en el centro de pantalla

ventana.Show() # Mostrar la ventana

app.MainLoop() #Mantener ventana hasta que el usuario cierre