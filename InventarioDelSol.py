import wx
from conexion import conectar

class Inventario(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(600, 400))
        panel = wx.Panel(self)

        wx.StaticText(panel, label="CATÁLOGO DE INVENTARIO", pos=(200, 10)).SetFont(
            wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        )

        self.tamano = (200, -1)

        wx.StaticText(panel, label="Código de Barras:", pos=(50, 50))
        self.txt_codigo_barras = wx.TextCtrl(panel, pos=(200, 50), size=self.tamano)
        self.txt_codigo_barras.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(panel, label="Existencia Actual:", pos=(50, 100))
        self.txt_existencia = wx.TextCtrl(panel, pos=(200, 100), size=self.tamano)
        self.txt_existencia.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(panel, label="Capacidad Máxima:", pos=(50, 150))
        self.txt_capacidad = wx.TextCtrl(panel, pos=(200, 150), size=self.tamano)
        self.txt_capacidad.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(panel, label="Temporada:", pos=(50, 200))
        temporadas = ['Verano', 'Otoño', 'Invierno', 'Primavera','Todo el Año','Dia de las Madres','Navidad','Dia de Muertos']
        self.combo_temporada = wx.ComboBox(panel, pos=(200, 200), size=self.tamano,
                                           choices=temporadas, style=wx.CB_READONLY)
        self.combo_temporada.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(panel, label="Fecha de Caducidad:", pos=(50, 250))
        self.txt_fecha = wx.TextCtrl(panel, pos=(200, 250), size=(200, 30), style=wx.TE_MULTILINE)
        self.txt_fecha.SetBackgroundColour(wx.Colour(255, 255, 230))
        self.txt_fecha.SetValue("AAAA/MM/DD")

        self.btn_no_aplica = wx.Button(panel, label="No Aplica", pos=(420, 250), size=(120, 30))
        self.btn_crear = wx.Button(panel, label=" Crear ", pos=(50, 300), size=(120, 40))
        self.btn_buscar = wx.Button(panel, label=" Buscar ", pos=(180, 300), size=(120, 40))
        self.btn_actualizar = wx.Button(panel, label=" Actualizar ", pos=(310, 300), size=(120, 40))
        self.btn_eliminar = wx.Button(panel, label=" Eliminar ", pos=(440, 300), size=(120, 40))

        self.Bind(wx.EVT_BUTTON, self.no_aplica, self.btn_no_aplica)
        self.Bind(wx.EVT_BUTTON, self.crear, self.btn_crear)
        self.Bind(wx.EVT_BUTTON, self.buscar, self.btn_buscar)
        self.Bind(wx.EVT_BUTTON, self.actualizar, self.btn_actualizar)
        self.Bind(wx.EVT_BUTTON, self.eliminar, self.btn_eliminar)

        self.Centre()
        self.Show()

    def mensaje(self, titulo, mensaje):
        wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

    def crear(self, event):
        codigo = self.txt_codigo_barras.GetValue()
        existencia = self.txt_existencia.GetValue()
        capacidad = self.txt_capacidad.GetValue()
        temporada = self.combo_temporada.GetValue()
        fecha = self.txt_fecha.GetValue() if self.txt_fecha.GetValue() != "AAAA/MM/DD" else None

        if not codigo or not existencia or not capacidad or not temporada:
            self.mensaje("Advertencia", "Complete todos los campos obligatorios.")
            return

        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    INSERT INTO inventario (codigo_barras, existencia_actual, capacidad_maxima, temporada, fecha_caducidad)
                    VALUES (%s, %s, %s, %s, %s)
                """, (codigo, existencia, capacidad, temporada, fecha))
                conn.commit()
                self.mensaje("Éxito", "Producto creado correctamente.")
            except Exception as e:
                self.mensaje("Error", f"Error al insertar: {e}")
            finally:
                cursor.close()
                conn.close()

    def buscar(self, event):
        codigo = self.txt_codigo_barras.GetValue()
        if not codigo:
            self.mensaje("Advertencia", "Ingrese el código de barras a buscar.")
            return

        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("SELECT existencia_actual, capacidad_maxima, temporada, fecha_caducidad FROM inventario WHERE codigo_barras = %s", (codigo,))
                datos = cursor.fetchone()
                if datos:
                    self.txt_existencia.SetValue(str(datos[0]))
                    self.txt_capacidad.SetValue(str(datos[1]))
                    self.combo_temporada.SetValue(datos[2])
                    
                    if datos[3]:  # Si la fecha no es NULL
                        fecha_str = datos[3].strftime("%Y-%m-%d")  # o "%d/%m/%Y" si prefieres ese formato
                        self.txt_fecha.SetValue(fecha_str)
                    else:
                        self.txt_fecha.SetValue("AAAA/MM/DD")

                    self.mensaje("Éxito", "Producto encontrado.")
                else:
                    self.mensaje("No encontrado", "No se encontró un producto con ese código.")
            except Exception as e:
                self.mensaje("Error", f"Error al buscar: {e}")
            finally:
                cursor.close()
                conn.close()

    def actualizar(self, event):
        codigo = self.txt_codigo_barras.GetValue()
        existencia = self.txt_existencia.GetValue()
        capacidad = self.txt_capacidad.GetValue()
        temporada = self.combo_temporada.GetValue()
        
        fecha_str = self.txt_fecha.GetValue()
        fecha = None if fecha_str == "AAAA/MM/DD" else fecha_str

        if not codigo:
            self.mensaje("Advertencia", "Ingrese el código de barras a actualizar.")
            return

        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    UPDATE inventario 
                    SET existencia_actual=%s, capacidad_maxima=%s, temporada=%s, fecha_caducidad=%s
                    WHERE codigo_barras=%s
                """, (existencia, capacidad, temporada, fecha, codigo))
                conn.commit()
                self.mensaje("Éxito", "Producto actualizado correctamente.")
            except Exception as e:
                self.mensaje("Error", f"Error al actualizar: {e}")
            finally:
                cursor.close()
                conn.close()


    def eliminar(self, event):
        codigo = self.txt_codigo_barras.GetValue()
        if not codigo:
            self.mensaje("Advertencia", "Ingrese el código de barras a eliminar.")
            return

        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("DELETE FROM inventario WHERE codigo_barras = %s", (codigo,))
                conn.commit()
                self.txt_existencia.SetValue("")
                self.txt_capacidad.SetValue("")
                self.combo_temporada.SetValue("")
                self.txt_fecha.SetValue("AAAA/MM/DD")
                self.mensaje("Éxito", "Producto eliminado correctamente.")
            except Exception as e:
                self.mensaje("Error", f"Error al eliminar: {e}")
            finally:
                cursor.close()
                conn.close()

    def no_aplica(self, event):
        self.txt_fecha.SetValue("AAAA/MM/DD")
        self.mensaje("Información", "Fecha de caducidad no aplica. Se dejará como 'AAAA/MM/DD'.")

if __name__ == "__main__":
    app = wx.App()
    Inventario(None, title="Inventario")
    app.MainLoop()