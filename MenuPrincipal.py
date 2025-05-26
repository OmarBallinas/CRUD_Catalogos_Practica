# MenuPrincipal.py
import wx
from ArticuloDelSol import ArticuloCRUD
from CategoriaDelSol import CategoriaCRUD
from ClienteDelSol import ClienteCRUD
from EmpleadoDelSol import EmpleadoCRUD
from InventarioDelSol import InventarioCRUD
from ProveedorDelSol import ProveedorCRUD
from ventas_gui import VentaGUI
from compras_gui import CompraGUI

class MenuPrincipal(wx.Frame):
    def __init__(self, idempleado=None):
        super().__init__(None, title="Sistema POS - Del Sol", size=(1000, 700))
        self.idempleado = idempleado  # Guardamos el ID del empleado logueado
        self.panel = wx.Panel(self)
        self.SetBackgroundColour(wx.Colour(240, 245, 255))  # Fondo suave

        self.crear_interfaz()
        self.Centre()
        self.Show()

    def crear_interfaz(self):
        sizer_principal = wx.BoxSizer(wx.VERTICAL)

        # Título
        lbl_titulo = wx.StaticText(self.panel, label="SISTEMA DE PUNTO DE VENTA - DEL SOL")
        fuente_titulo = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        lbl_titulo.SetFont(fuente_titulo)
        lbl_titulo.SetForegroundColour(wx.Colour(0, 56, 119))  # Azul oscuro
        sizer_principal.Add(lbl_titulo, 0, wx.ALIGN_CENTER | wx.ALL, 30)

        # Subtítulo con info del usuario
        self.lbl_usuario = wx.StaticText(self.panel, label=f"Usuario activo: {self.idempleado}")
        fuente_subtitulo = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL)
        self.lbl_usuario.SetFont(fuente_subtitulo)
        self.lbl_usuario.SetForegroundColour(wx.Colour(80, 80, 80))
        sizer_principal.Add(self.lbl_usuario, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)

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

        grid_sizer = wx.GridSizer(rows=3, cols=3, vgap=40, hgap=40)

        for texto, funcion in opciones:
            btn = wx.Button(self.panel, label=texto)
            btn.SetMinSize((250, 80))
            btn.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            btn.SetBackgroundColour(wx.Colour(255, 255, 255))
            btn.Bind(wx.EVT_BUTTON, funcion)
            grid_sizer.Add(btn, 0, wx.EXPAND | wx.ALL, 5)

        sizer_principal.Add(grid_sizer, 0, wx.CENTER)

        # Pie de página
        pie = wx.StaticText(self.panel, label="© 2025 Del Sol - Sistema de Gestión Comercial")
        pie.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_LIGHT))
        pie.SetForegroundColour(wx.Colour(100, 100, 100))
        sizer_principal.Add(pie, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 20)

        self.panel.SetSizer(sizer_principal)

    # Funciones para abrir módulos
    def abrir_articulos(self, event):
        ArticuloCRUD()

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
        VentaGUI(idempleado=self.idempleado)

    def abrir_compras(self, event):
        CompraGUI(idempleado=self.idempleado)

    def cerrar_sesion(self, event):
        confirmacion = wx.MessageBox("¿Está seguro que desea cerrar sesión?", "Cerrar Sesión",
                                     wx.YES_NO | wx.ICON_QUESTION)
        if confirmacion == wx.YES:
            self.Close()
            from LoginGUI import LoginGUI
            LoginGUI()