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
    def __init__(self):
        super().__init__(None, title="Sistema POS - Del Sol", size=(800, 600))

        self.SetBackgroundColour(wx.Colour(245, 245, 245))
        panel = wx.Panel(self)

        # Título
        lbl_titulo = wx.StaticText(panel, label="SISTEMA DE PUNTO DE VENTA - DEL SOL")
        fuente_titulo = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        lbl_titulo.SetFont(fuente_titulo)
        lbl_titulo.SetForegroundColour(wx.Colour(0, 70, 140))
        sizer_titulo = wx.BoxSizer(wx.HORIZONTAL)
        sizer_titulo.Add(lbl_titulo, 0, wx.ALIGN_CENTER | wx.ALL, 15)
        panel.SetSizer(sizer_titulo)

        # Botones
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

        grid_sizer = wx.GridSizer(rows=3, cols=3, vgap=20, hgap=20)

        for texto, funcion in opciones:
            btn = wx.Button(panel, label=texto, size=(220, 80))
            btn.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            btn.SetBackgroundColour(wx.Colour(255, 255, 255))
            btn.Bind(wx.EVT_BUTTON, funcion)
            grid_sizer.Add(btn, 0, wx.EXPAND | wx.ALL)

        sizer_principal = wx.BoxSizer(wx.VERTICAL)
        sizer_principal.AddSpacer(50)
        sizer_principal.Add(grid_sizer, 0, wx.CENTER)
        panel.SetSizerAndFit(sizer_principal)

        self.Centre()
        self.Show()

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
        VentaGUI()
        
    def abrir_compras(self, event):
        CompraGUI()

    def en_construccion(self, event):
        wx.MessageBox("Funcionalidad en desarrollo.", "En construcción", wx.OK | wx.ICON_INFORMATION)

    def cerrar_sesion(self, event):
        confirmacion = wx.MessageBox("¿Está seguro que desea cerrar sesión?", "Cerrar Sesión",
                                     wx.YES_NO | wx.ICON_QUESTION)
        if confirmacion == wx.YES:
            self.Close()


if __name__ == "__main__":
    app = wx.App()
    MenuPrincipal()
    app.MainLoop()