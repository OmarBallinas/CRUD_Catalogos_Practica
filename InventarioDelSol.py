# inventario.py
import wx
from conexion import conectar

class InventarioCRUD(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title='Catálogo de Inventario', size=(600, 400))
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
            self.txt_codigo_barras.GetValue(),
            self.txt_existencia.GetValue(),
            self.txt_capacidad.GetValue(),
            self.combo_temporada.GetValue()
        ])

    def crear_interfaz(self):
        """Construye la interfaz gráfica."""
        lbl_titulo = wx.StaticText(self.panel, label="CATÁLOGO DE INVENTARIO", pos=(200, 10))
        lbl_titulo.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        tamano = (200, -1)

        # Campos de entrada
        wx.StaticText(self.panel, label="Código de Barras:", pos=(50, 50))
        self.txt_codigo_barras = wx.TextCtrl(self.panel, pos=(200, 50), size=tamano)
        self.txt_codigo_barras.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Existencia Actual:", pos=(50, 100))
        self.txt_existencia = wx.TextCtrl(self.panel, pos=(200, 100), size=tamano)
        self.txt_existencia.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Capacidad Máxima:", pos=(50, 150))
        self.txt_capacidad = wx.TextCtrl(self.panel, pos=(200, 150), size=tamano)
        self.txt_capacidad.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Temporada:", pos=(50, 200))
        temporadas = ['Verano', 'Otoño', 'Invierno', 'Primavera', 'Todo el Año', 'Día de las Madres', 'Navidad', 'Día de Muertos']
        self.combo_temporada = wx.ComboBox(self.panel, pos=(200, 200), size=tamano,
                                           choices=temporadas, style=wx.CB_READONLY)
        self.combo_temporada.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Fecha de Caducidad:", pos=(50, 250))
        self.txt_fecha = wx.TextCtrl(self.panel, pos=(200, 250), size=(200, 30), style=wx.TE_MULTILINE)
        self.txt_fecha.SetBackgroundColour(wx.Colour(255, 255, 230))
        self.txt_fecha.SetValue("AAAA/MM/DD")

        self.btn_no_aplica = wx.Button(self.panel, label="No Aplica", pos=(420, 250), size=(120, 30))
        self.btn_crear = wx.Button(self.panel, label=" Crear ", pos=(50, 300), size=(120, 40))
        self.btn_buscar = wx.Button(self.panel, label=" Buscar ", pos=(180, 300), size=(120, 40))
        self.btn_actualizar = wx.Button(self.panel, label=" Actualizar ", pos=(310, 300), size=(120, 40))
        self.btn_eliminar = wx.Button(self.panel, label=" Eliminar ", pos=(440, 300), size=(120, 40))

        # Eventos
        self.Bind(wx.EVT_BUTTON, self.no_aplica, self.btn_no_aplica)
        self.Bind(wx.EVT_BUTTON, self.crear, self.btn_crear)
        self.Bind(wx.EVT_BUTTON, self.buscar, self.btn_buscar)
        self.Bind(wx.EVT_BUTTON, self.actualizar, self.btn_actualizar)
        self.Bind(wx.EVT_BUTTON, self.eliminar, self.btn_eliminar)

    def no_aplica(self, event):
        self.txt_fecha.SetValue("AAAA/MM/DD")
        self.mensaje("Información", "Fecha de caducidad no aplica.")

    def on_crear(self, event):
        if self.validar_campos():
            self.crear(
                self.txt_codigo_barras.GetValue(),
                self.txt_existencia.GetValue(),
                self.txt_capacidad.GetValue(),
                self.combo_temporada.GetValue(),
                self.txt_fecha.GetValue() if self.txt_fecha.GetValue() != "AAAA/MM/DD" else None
            )
        else:
            self.mensaje("Advertencia", "Complete todos los campos obligatorios.")

    def on_buscar(self, event):
        codigo = self.txt_codigo_barras.GetValue()
        if not codigo:
            self.mensaje("Advertencia", "Ingrese el código de barras a buscar.")
            return

        resultado = self.buscar(codigo)
        if resultado:
            self.txt_existencia.SetValue(str(resultado[1]))
            self.txt_capacidad.SetValue(str(resultado[2]))
            self.combo_temporada.SetValue(str(resultado[3]))
            if resultado[4]:  # fecha_caducidad
                self.txt_fecha.SetValue(resultado[4].strftime("%Y-%m-%d"))
            else:
                self.txt_fecha.SetValue("AAAA/MM/DD")
        else:
            self.mensaje("Información", "Producto no encontrado.")

    def on_actualizar(self, event):
        if self.validar_campos():
            self.actualizar(
                self.txt_codigo_barras.GetValue(),
                self.txt_existencia.GetValue(),
                self.txt_capacidad.GetValue(),
                self.combo_temporada.GetValue(),
                self.txt_fecha.GetValue() if self.txt_fecha.GetValue() != "AAAA/MM/DD" else None
            )
        else:
            self.mensaje("Advertencia", "Complete todos los campos obligatorios.")

    def on_eliminar(self, event):
        codigo = self.txt_codigo_barras.GetValue()
        if not codigo:
            self.mensaje("Advertencia", "Ingrese el código de barras a eliminar.")
            return

        self.eliminar(codigo)
        self.limpiar_campos()

    def limpiar_campos(self):
        self.txt_codigo_barras.Clear()
        self.txt_existencia.Clear()
        self.txt_capacidad.Clear()
        self.combo_temporada.SetValue("")
        self.txt_fecha.SetValue("AAAA/MM/DD")

    def crear(self, codigo, existencia, capacidad, temporada, fecha):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    INSERT INTO inventario (codigo_barras, existencia_actual, capacidad_maxima, temporada, fecha_caducidad)
                    VALUES (%s, %s, %s, %s, %s)
                """, (codigo, int(existencia), int(capacidad), temporada, fecha))
                conn.commit()
                self.mensaje("Éxito", "Producto creado correctamente.")
            except Exception as e:
                self.mensaje("Error", f"Error al insertar: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def buscar(self, codigo):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    SELECT existencia_actual, capacidad_maxima, temporada, fecha_caducidad 
                    FROM inventario WHERE codigo_barras = %s
                """, (codigo,))
                return cursor.fetchone()
            except Exception as e:
                self.mensaje("Error", f"Error al buscar: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")
        return None

    def actualizar(self, codigo, existencia, capacidad, temporada, fecha):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    UPDATE inventario 
                    SET existencia_actual=%s, capacidad_maxima=%s, temporada=%s, fecha_caducidad=%s
                    WHERE codigo_barras=%s
                """, (int(existencia), int(capacidad), temporada, fecha, codigo))
                conn.commit()
                self.mensaje("Éxito", "Producto actualizado correctamente.")
            except Exception as e:
                self.mensaje("Error", f"Error al actualizar: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def eliminar(self, codigo):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("DELETE FROM inventario WHERE codigo_barras = %s", (codigo,))
                conn.commit()
                self.mensaje("Éxito", "Producto eliminado correctamente.")
            except Exception as e:
                self.mensaje("Error", f"Error al eliminar: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")