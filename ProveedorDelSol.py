# proveedores.py
import wx
from conexion import conectar

class ProveedorCRUD(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title="Catálogo de Proveedores", size=(600, 500))
        self.panel = wx.Panel(self)
        self.crear_interfaz()
        self.Centre()
        self.Show()

    def mensaje(self, titulo, mensaje):
        """Muestra un mensaje emergente."""
        wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

    def validar_campos(self):
        """Valida que los campos obligatorios no estén vacíos."""
        return all([
            self.txt_id.GetValue(),
            self.txt_nombre.GetValue(),
            self.txt_contacto.GetValue(),
            self.txt_telefono.GetValue()
        ])

    def crear_interfaz(self):
        """Construye la interfaz gráfica."""
        # Título
        titulo_panel = wx.Panel(self.panel, pos=(0, 0), size=(600, 40))
        lbl_titulo = wx.StaticText(titulo_panel, label="CATÁLOGO DE PROVEEDORES", pos=(220, 10))
        fuente_titulo = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        lbl_titulo.SetFont(fuente_titulo)

        tamano_texto = (200, -1)

        # Labels y TextCtrl
        wx.StaticText(self.panel, label="ID Proveedor:", pos=(50, 50))
        self.txt_id = wx.TextCtrl(self.panel, pos=(200, 50), size=tamano_texto)
        self.txt_id.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Nombre:", pos=(50, 100))
        self.txt_nombre = wx.TextCtrl(self.panel, pos=(200, 100), size=tamano_texto)
        self.txt_nombre.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Contacto:", pos=(50, 150))
        self.txt_contacto = wx.TextCtrl(self.panel, pos=(200, 150), size=tamano_texto)
        self.txt_contacto.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Teléfono:", pos=(50, 200))
        self.txt_telefono = wx.TextCtrl(self.panel, pos=(200, 200), size=tamano_texto)
        self.txt_telefono.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Correo Electrónico:", pos=(50, 250))
        self.txt_correo = wx.TextCtrl(self.panel, pos=(200, 250), size=tamano_texto)
        self.txt_correo.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Dirección:", pos=(50, 300))
        self.txt_direccion = wx.TextCtrl(self.panel, pos=(200, 300), size=tamano_texto)
        self.txt_direccion.SetBackgroundColour(wx.Colour(255, 255, 230))

        # Botones
        self.btn_crear = wx.Button(self.panel, label=" Crear ", pos=(50, 370), size=(120, 40))
        self.btn_buscar = wx.Button(self.panel, label=" Buscar ", pos=(180, 370), size=(120, 40))
        self.btn_actualizar = wx.Button(self.panel, label=" Actualizar ", pos=(310, 370), size=(120, 40))
        self.btn_eliminar = wx.Button(self.panel, label=" Eliminar ", pos=(440, 370), size=(120, 40))

        # Eventos
        self.btn_crear.Bind(wx.EVT_BUTTON, self.on_crear)
        self.btn_buscar.Bind(wx.EVT_BUTTON, self.on_buscar)
        self.btn_actualizar.Bind(wx.EVT_BUTTON, self.on_actualizar)
        self.btn_eliminar.Bind(wx.EVT_BUTTON, self.on_eliminar)

    def on_crear(self, event):
        if self.validar_campos():
            self.crear(
                self.txt_id.GetValue(),
                self.txt_nombre.GetValue(),
                self.txt_contacto.GetValue(),
                self.txt_telefono.GetValue(),
                self.txt_correo.GetValue(),
                self.txt_direccion.GetValue()
            )
        else:
            self.mensaje("Advertencia", "Los campos ID, Nombre, Contacto y Teléfono son obligatorios.")

    def on_buscar(self, event):
        idproveedor = self.txt_id.GetValue()
        if not idproveedor:
            self.mensaje("Advertencia", "Ingrese el ID del proveedor a buscar.")
            return

        resultado = self.buscar(idproveedor)
        if resultado:
            self.txt_nombre.SetValue(str(resultado[1]))
            self.txt_contacto.SetValue(str(resultado[2]))
            self.txt_telefono.SetValue(str(resultado[3]))
            self.txt_correo.SetValue(str(resultado[4]))
            self.txt_direccion.SetValue(str(resultado[5]))
            self.mensaje("Proveedor encontrado", f"Datos cargados para ID {idproveedor}.")
        else:
            self.mensaje("No encontrado", "No se encontró el proveedor.")

    def on_actualizar(self, event):
        idproveedor = self.txt_id.GetValue()
        if not idproveedor:
            self.mensaje("Advertencia", "Ingrese el ID del proveedor a actualizar.")
            return

        self.actualizar(
            idproveedor,
            self.txt_nombre.GetValue(),
            self.txt_contacto.GetValue(),
            self.txt_telefono.GetValue(),
            self.txt_correo.GetValue(),
            self.txt_direccion.GetValue()
        )

    def on_eliminar(self, event):
        idproveedor = self.txt_id.GetValue()
        if not idproveedor:
            self.mensaje("Advertencia", "Ingrese el ID del proveedor a eliminar.")
            return

        self.eliminar(idproveedor)
        self.limpiar_campos()

    def limpiar_campos(self):
        self.txt_id.Clear()
        self.txt_nombre.Clear()
        self.txt_contacto.Clear()
        self.txt_telefono.Clear()
        self.txt_correo.Clear()
        self.txt_direccion.Clear()

    def crear(self, idproveedor, nombre, contacto, telefono, correo, direccion):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    INSERT INTO proveedor (idproveedor, nombre, contacto, telefono, correo_electronico, direccion)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (idproveedor, nombre, contacto, telefono, correo, direccion))
                conn.commit()
                self.mensaje("Éxito", "Proveedor creado correctamente.")
            except Exception as e:
                self.mensaje("Error", f"No se pudo crear el proveedor:\n{e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def buscar(self, idproveedor):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("SELECT * FROM proveedor WHERE idproveedor = %s", (idproveedor,))
                resultado = cursor.fetchone()
                return resultado
            except Exception as e:
                self.mensaje("Error", f"No se pudo recuperar el proveedor:\n{e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")
        return None

    def actualizar(self, idproveedor, nombre, contacto, telefono, correo, direccion):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    UPDATE proveedor SET 
                        nombre=%s, contacto=%s, telefono=%s, 
                        correo_electronico=%s, direccion=%s 
                    WHERE idproveedor=%s
                """, (nombre, contacto, telefono, correo, direccion, idproveedor))
                conn.commit()
                self.mensaje("Actualizado", f"Proveedor {idproveedor} actualizado correctamente.")
            except Exception as e:
                self.mensaje("Error", f"No se pudo actualizar el proveedor:\n{e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def eliminar(self, idproveedor):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("DELETE FROM proveedor WHERE idproveedor = %s", (idproveedor,))
                conn.commit()
                self.mensaje("Eliminado", f"Proveedor {idproveedor} eliminado correctamente.")
            except Exception as e:
                self.mensaje("Error", f"No se pudo eliminar el proveedor:\n{e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")