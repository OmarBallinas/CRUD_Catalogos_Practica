import wx 

app = wx.App() #Instancia del objeto wx

ventana = wx.Frame(None, title='Catalogo de Promociones', size=(600, 600)) #Creacion de la ventana con altura aumentada
panel = wx.Panel(ventana) #Crear panel dentro de la ventana


lbl_titulo = wx.Panel(panel, pos=(0, 0), size=(600, 40))  # titulo
lbl_titulo = wx.StaticText(lbl_titulo, label="CATALOGO DE PROMOCIONES", pos=(220, 10))
fuente_titulo = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD) # Fuente más grande y en negrita para el título
lbl_titulo.SetFont(fuente_titulo)


tamano_texto = (200, -1) # Definir un tamaño estándar para los campos de texto

# ID Promocion
lbl_id_promocion = wx.StaticText(panel, label="ID Promoción:", pos=(50, 50)) #Texto
txt_id_promocion = wx.TextCtrl(panel, pos=(200, 50), size=tamano_texto) #Input
txt_id_promocion.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Nombre
lbl_nombre = wx.StaticText(panel, label="Nombre:", pos=(50, 100)) #Texto
txt_nombre = wx.TextCtrl(panel, pos=(200, 100), size=tamano_texto)  #Input
txt_nombre.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Descripción
lbl_descripcion = wx.StaticText(panel, label="Descripción:", pos=(50, 150)) #Texto
txt_descripcion = wx.TextCtrl(panel, pos=(200, 150), size=tamano_texto) #Input
txt_descripcion.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Fecha Inicio
lbl_fecha_inicio = wx.StaticText(panel, label="Fecha Inicio:", pos=(50, 200)) #Texto
txt_fecha_inicio = wx.TextCtrl(panel, pos=(200, 200), size=tamano_texto) #Input
txt_fecha_inicio.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Fecha Fin
lbl_fecha_fin = wx.StaticText(panel, label="Fecha Fin:", pos=(50, 250)) #Texto
txt_fecha_fin = wx.TextCtrl(panel, pos=(200, 250), size=tamano_texto) #Input
txt_fecha_fin.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Valor
lbl_valor = wx.StaticText(panel, label="Valor:", pos=(50, 300)) #Texto
txt_valor = wx.TextCtrl(panel, pos=(200, 300), size=tamano_texto) #Input
txt_valor.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Status
lbl_status = wx.StaticText(panel, label="Status:", pos=(50, 350)) #Texto
opciones_status = ["Activo", "Inactivo"]
cmb_status = wx.Choice(panel, pos=(200, 350), size=tamano_texto, choices=opciones_status) #Selector
cmb_status.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

# Condiciones
lbl_condiciones = wx.StaticText(panel, label="Condiciones:", pos=(50, 400)) #Texto
txt_condiciones = wx.TextCtrl(panel, pos=(200, 400), size=(200, 60), style=wx.TE_MULTILINE) #Input más grande y multilinea
txt_condiciones.SetBackgroundColour(wx.Colour(255, 255, 230)) #Color input

#BOTONES DEL CRUD 
# Create
button_crear = wx.Button(panel, label=" Crear ", pos=(50, 480), size=(120, 40))
# Read
button_buscar = wx.Button(panel, label=" Buscar ", pos=(180, 480), size=(120, 40))
# Update
button_actualizar = wx.Button(panel, label=" Actualizar ", pos=(310, 480), size=(120, 40))
# Delete
button_eliminar = wx.Button(panel, label=" Eliminar ", pos=(440, 480), size=(120, 40))


ventana.Centre() # Ventana en el centro de pantalla

ventana.Show() # Mostrar la ventana

app.MainLoop() #Mantener ventana hasta que el usuario cierre