import wx
from ArticuloDelSol import ArticuloCRUD
from CategoriaDelSol import CategoriaCRUD
from ClienteDelSol import ClienteCRUD
from EmpleadoDelSol import EmpleadoCRUD
from InventarioDelSol import InventarioCRUD
from ProveedorDelSol import ProveedorCRUD
from ventas_gui import VentaGUI
from compras_gui import CompraGUI
import os

class MenuPrincipal(wx.Frame):
    def __init__(self, idempleado=None, nombre_empleado=None):
        super().__init__(None, title="Sistema POS - Del Sol", size=(1200, 800))
        self.idempleado = idempleado
        self.nombre_empleado = nombre_empleado  # Nombre del empleado logueado
        self.panel = wx.Panel(self)
        self.SetBackgroundColour(wx.Colour(245, 247, 250))  # Fondo muy claro

        # Cargar imagen del logo (asegúrate de tener un logo.png en la carpeta)
        logo_path = os.path.join(os.path.dirname(__file__), "logo_del_sol.png")
        if os.path.exists(logo_path):
            self.logo = wx.Image(logo_path).Scale(80, 80).ConvertToBitmap()
        else:
            self.logo = None

        self.crear_interfaz()
        self.Centre()
        self.Show()

    def crear_interfaz(self):
        sizer_principal = wx.BoxSizer(wx.VERTICAL)

        # Panel superior: Logo + Título + Info Usuario
        panel_superior = wx.Panel(self.panel)
        panel_superior.SetBackgroundColour(wx.Colour(230, 236, 240))  # Fondo suave azulado
        sizer_superior = wx.BoxSizer(wx.HORIZONTAL)

        # Logo
        if self.logo:
            img_logo = wx.StaticBitmap(panel_superior, bitmap=self.logo)
            sizer_superior.Add(img_logo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        # Título
        lbl_titulo = wx.StaticText(panel_superior, label="PUNTO DE VENTA")
        font_titulo = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        lbl_titulo.SetFont(font_titulo)
        lbl_titulo.SetForegroundColour(wx.Colour(44, 62, 80))  # Azul oscuro
        sizer_superior.Add(lbl_titulo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        # Espaciador flexible
        sizer_superior.AddStretchSpacer()

        # Información del usuario activo
        info_usuario = wx.StaticText(panel_superior,
                                     label=f"Usuario Activo: {self.idempleado} - {self.nombre_empleado}")
        font_info = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        info_usuario.SetFont(font_info)
        info_usuario.SetForegroundColour(wx.Colour(45, 52, 54))  # Negro grisáceo
        sizer_superior.Add(info_usuario, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        panel_superior.SetSizer(sizer_superior)
        sizer_principal.Add(panel_superior, 0, wx.EXPAND)

        # Título del menú principal
        lbl_menu = wx.StaticText(self.panel, label="Menú Principal")
        font_menu = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        lbl_menu.SetFont(font_menu)
        lbl_menu.SetForegroundColour(wx.Colour(44, 62, 80))
        sizer_principal.Add(lbl_menu, 0, wx.ALIGN_CENTER | wx.TOP, 20)

        # Botones del menú (en grid)
        opciones = [
            ("Gestionar Artículos", self.abrir_articulos),
            ("Gestionar Categorías", self.abrir_categorias),
            ("Gestionar Clientes", self.abrir_clientes),
            ("Gestionar Empleados", self.abrir_empleados),
            ("Gestionar Inventario", self.abrir_inventario),
            ("Gestionar Proveedores", self.abrir_proveedores),
            ("Registrar Venta", self.abrir_ventas),
            ("Registrar Compra", self.abrir_compras),
            ("Cerrar Sesión", self.cerrar_sesion),
        ]

        grid_sizer = wx.GridSizer(rows=3, cols=3, vgap=30, hgap=30)

        for texto, funcion in opciones:
            btn = wx.Button(self.panel, label=texto, size=(250, 100))
            btn.SetBackgroundColour(wx.Colour(44, 62, 80))  # Azul oscuro
            btn.SetForegroundColour(wx.Colour(255, 255, 255))  # Blanco
            btn.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            btn.Bind(wx.EVT_BUTTON, funcion)
            grid_sizer.Add(btn, 0, wx.EXPAND | wx.ALL, 5)

        sizer_principal.Add(grid_sizer, 0, wx.CENTER | wx.ALL, 30)

        # Pie de página
        pie = wx.StaticText(self.panel, label="Tienda del Sol © 2025")
        pie.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_LIGHT))
        pie.SetForegroundColour(wx.Colour(127, 140, 141))  # Gris plata
        sizer_principal.Add(pie, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)

        self.panel.SetSizer(sizer_principal)

    # Funciones para abrir módulos
    def abrir_articulos(self, event):
        ArticuloCRUD(parent=self)

    def abrir_categorias(self, event):
        CategoriaCRUD()

    def abrir_clientes(self, event):
        ClienteCRUD()

    def abrir_empleados(self, event):
        EmpleadoCRUD()

    def abrir_inventario(self, event):
        InventarioCRUD()

    def abrir_proveedores(self, event):
        ProveedorCRUD()

    def abrir_ventas(self, event):
        from ventas_gui import VentaGUI
        VentaGUI(parent=self, idempleado=self.idempleado, nombre_empleado=self.nombre_empleado)

    def abrir_compras(self, event):
        CompraGUI(idempleado=self.idempleado)

    def cerrar_sesion(self, event):
        confirmacion = wx.MessageBox("¿Está seguro que desea cerrar sesión?", "Cerrar Sesión",
                                     wx.YES_NO | wx.ICON_QUESTION)
        if confirmacion == wx.YES:
            self.Close()
            from LoginGUI import LoginGUI
            LoginGUI()