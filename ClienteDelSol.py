# clientes.py
import wx
from conexion import conectar

class ClienteCRUD(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title='Catálogo de Clientes', size=(600, 450))
        self.panel = wx.Panel(self)
        self.crear_interfaz()
        self.Centre()
        self.Show()

    def mensaje(self, titulo, mensaje):
        """Muestra un mensaje emergente."""
        wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

    def validar_campos(self):
        """Verifica que los campos obligatorios no estén vacíos."""
        return all([
            self.txt_telefono.GetValue(),
            self.txt_nombre.GetValue(),
            self.txt_apellido.GetValue(),
            self.txt_correo.GetValue()
        ])

    def crear_interfaz(self):
        """Construye la interfaz gráfica."""
        lbl_titulo = wx.StaticText(self.panel, label="CATÁLOGO DE CLIENTES", pos=(220, 10))
        lbl_titulo.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        tamano_texto = (200, -1)

        # Campos de entrada
        wx.StaticText(self.panel, label="Teléfono Cliente:", pos=(50, 50))
        self.txt_telefono = wx.TextCtrl(self.panel, pos=(200, 50), size=tamano_texto)
        self.txt_telefono.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Nombre:", pos=(50, 100))
        self.txt_nombre = wx.TextCtrl(self.panel, pos=(200, 100), size=tamano_texto)
        self.txt_nombre.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Apellido:", pos=(50, 150))
        self.txt_apellido = wx.TextCtrl(self.panel, pos=(200, 150), size=tamano_texto)
        self.txt_apellido.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Correo Electrónico:", pos=(50, 200))
        self.txt_correo = wx.TextCtrl(self.panel, pos=(200, 200), size=tamano_texto)
        self.txt_correo.SetBackgroundColour(wx.Colour(255, 255, 230))

        # Botones
        self.btn_crear = wx.Button(self.panel, label=" Crear ", pos=(50, 300), size=(120, 40))
        self.btn_buscar = wx.Button(self.panel, label=" Buscar ", pos=(180, 300), size=(120, 40))
        self.btn_actualizar = wx.Button(self.panel, label=" Actualizar ", pos=(310, 300), size=(120, 40))
        self.btn_eliminar = wx.Button(self.panel, label=" Eliminar ", pos=(440, 300), size=(120, 40))

        # Eventos
        self.btn_crear.Bind(wx.EVT_BUTTON, self.on_crear)
        self.btn_buscar.Bind(wx.EVT_BUTTON, self.on_buscar)
        self.btn_actualizar.Bind(wx.EVT_BUTTON, self.on_actualizar)
        self.btn_eliminar.Bind(wx.EVT_BUTTON, self.on_eliminar)

    def on_crear(self, event):
        if self.validar_campos():
            self.crear_cliente(
                self.txt_telefono.GetValue(),
                self.txt_nombre.GetValue(),
                self.txt_apellido.GetValue(),
                self.txt_correo.GetValue()
            )
        else:
            self.mensaje("Advertencia", "Por favor, complete todos los campos.")

    def on_buscar(self, event):
        telefono = self.txt_telefono.GetValue()
        if telefono:
            resultado = self.buscar_cliente(telefono)
            if resultado:
                self.txt_nombre.SetValue(resultado[1])
                self.txt_apellido.SetValue(resultado[2])
                self.txt_correo.SetValue(resultado[3])
            else:
                self.mensaje("Información", "Cliente no encontrado.")
        else:
            self.mensaje("Advertencia", "Por favor, ingrese un teléfono de cliente.")

    def on_actualizar(self, event):
        if self.validar_campos():
            self.actualizar_cliente(
                self.txt_telefono.GetValue(),
                self.txt_nombre.GetValue(),
                self.txt_apellido.GetValue(),
                self.txt_correo.GetValue()
            )
        else:
            self.mensaje("Advertencia", "Por favor, complete todos los campos.")

    def on_eliminar(self, event):
        telefono = self.txt_telefono.GetValue()
        if telefono:
            self.eliminar_cliente(telefono)
            self.limpiar_campos()
        else:
            self.mensaje("Advertencia", "Por favor, ingrese un teléfono de cliente.")

    def limpiar_campos(self):
        self.txt_telefono.Clear()
        self.txt_nombre.Clear()
        self.txt_apellido.Clear()
        self.txt_correo.Clear()

    def crear_cliente(self, telefono, nombre, apellido, correo):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    INSERT INTO cliente (telefono_cliente, nombre, apellido, correo_electronico)
                    VALUES (%s, %s, %s, %s)
                """, (telefono, nombre, apellido, correo))
                conn.commit()
                self.mensaje("Éxito", "Cliente creado exitosamente.")
            except Exception as e:
                self.mensaje("Error", f"Error al crear cliente: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def buscar_cliente(self, telefono):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    SELECT telefono_cliente, nombre, apellido, correo_electronico 
                    FROM cliente WHERE telefono_cliente = %s
                """, (telefono,))
                return cursor.fetchone()
            except Exception as e:
                self.mensaje("Error", f"Error al buscar cliente: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")
        return None

    def actualizar_cliente(self, telefono, nombre, apellido, correo):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    UPDATE cliente SET
                        nombre = %s,
                        apellido = %s,
                        correo_electronico = %s
                    WHERE telefono_cliente = %s
                """, (nombre, apellido, correo, telefono))
                conn.commit()
                self.mensaje("Éxito", "Cliente actualizado exitosamente.")
            except Exception as e:
                self.mensaje("Error", f"Error al actualizar cliente: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def eliminar_cliente(self, telefono):
        conn, cursor = conectar()
        if not conn or not cursor:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")
            return

        try:
            cursor.execute("DELETE FROM cliente WHERE telefono_cliente = %s", (telefono,))
            conn.commit()
            self.mensaje("Éxito", "Cliente eliminado exitosamente.")
        except Exception as e:
            conn.rollback()
            self.mensaje("Error", f"Error al eliminar cliente: {e}")
        finally:
            cursor.close()
            conn.close()