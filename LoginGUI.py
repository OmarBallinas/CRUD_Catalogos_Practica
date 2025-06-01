# LoginGUI.py
import wx
from conexion import conectar
from MenuPrincipal import MenuPrincipal
from EmpleadoDelSol import EmpleadoCRUD

class LoginGUI(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Inicio de Sesión - Del Sol", size=(500, 400))
        self.SetBackgroundColour(wx.Colour(240, 245, 255))  # Fondo claro
        self.panel = wx.Panel(self)
        self.crear_interfaz()
        self.Centre()
        self.Show()

    def crear_interfaz(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Título
        lbl_titulo = wx.StaticText(self.panel, label="Sistema POS - Del Sol")
        fuente_titulo = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        lbl_titulo.SetFont(fuente_titulo)
        lbl_titulo.SetForegroundColour(wx.Colour(0, 56, 119))  # Azul oscuro
        sizer.Add(lbl_titulo, 0, wx.ALIGN_CENTER | wx.ALL, 20)

        # Campos en grid
        grid_sizer = wx.FlexGridSizer(rows=2, cols=2, vgap=10, hgap=10)
        grid_sizer.AddGrowableCol(1)

        # Usuario
        lbl_usuario = wx.StaticText(self.panel, label="ID Empleado:")
        self.txt_id = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        grid_sizer.Add(lbl_usuario, 0, wx.ALIGN_CENTER_VERTICAL)
        grid_sizer.Add(self.txt_id, 1, wx.EXPAND)

        # Contraseña
        lbl_pass = wx.StaticText(self.panel, label="Contraseña:")
        self.txt_pass = wx.TextCtrl(self.panel, style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        grid_sizer.Add(lbl_pass, 0, wx.ALIGN_CENTER_VERTICAL)
        grid_sizer.Add(self.txt_pass, 1, wx.EXPAND)

        sizer.Add(grid_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 40)
        sizer.AddSpacer(10)

        # Botones
        btn_login = wx.Button(self.panel, label="Iniciar Sesión", size=(200, 35))
        btn_registro = wx.Button(self.panel, label="Registrar Nuevo Empleado", size=(200, 35))

        sizer.Add(btn_login, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        sizer.Add(btn_registro, 0, wx.ALIGN_CENTER | wx.TOP, 5)

        self.panel.SetSizer(sizer)

        # Eventos
        btn_login.Bind(wx.EVT_BUTTON, self.verificar_login)
        btn_registro.Bind(wx.EVT_BUTTON, self.registrar_nuevo_empleado)

        # Permitir Enter en los campos
        self.txt_id.Bind(wx.EVT_TEXT_ENTER, self.verificar_login)
        self.txt_pass.Bind(wx.EVT_TEXT_ENTER, self.verificar_login)
        self.txt_id.SetFocus()

    def verificar_login(self, event):
        idempleado = self.txt_id.GetValue().strip()
        contrasena = self.txt_pass.GetValue().strip()

        if not idempleado or not contrasena:
            wx.MessageBox("Por favor, ingrese ambos campos.", "Advertencia", wx.OK | wx.ICON_WARNING)
            return

        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("SELECT nombre, apellidos FROM empleado WHERE idempleado = %s AND contraseña = %s",
                               (idempleado, contrasena))
                resultado = cursor.fetchone()
                if resultado:
                    wx.MessageBox(f"Bienvenido, {resultado[0]} {resultado[1]}", "Éxito", wx.OK | wx.ICON_INFORMATION)
                    self.Close()
                    MenuPrincipal(idempleado=idempleado)
                else:
                    wx.MessageBox("ID o contraseña incorrectos.", "Error", wx.OK | wx.ICON_ERROR)
            except Exception as e:
                wx.MessageBox(f"Error al iniciar sesión: {e}", "Error", wx.OK | wx.ICON_ERROR)
            finally:
                cursor.close()
                conn.close()
        else:
            wx.MessageBox("No se pudo conectar a la base de datos.", "Error", wx.OK | wx.ICON_ERROR)

    def registrar_nuevo_empleado(self, event):
        # Pedimos la clave del gerente
        dlg = wx.TextEntryDialog(
            self, 
            "Ingrese la clave del gerente:",  # mensaje
            "Autenticación Requerida",        # título
            "",                               # valor por defecto
            style=wx.TE_PASSWORD | wx.OK | wx.CANCEL
        )

        if dlg.ShowModal() == wx.ID_OK:
            clave = dlg.GetValue()
            dlg.Destroy()

            if clave != "1234":
                wx.MessageBox("Clave incorrecta. Acceso denegado.", "Error", wx.OK | wx.ICON_ERROR)
            else:
                self.Close()  # Cierra la ventana de Login
                from EmpleadoDelSol import EmpleadoCRUD
                EmpleadoCRUD(es_gerente=True)  # Abre el CRUD completo de empleados
        else:
            dlg.Destroy()