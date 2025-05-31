import wx
from conexion import conectar

class InventarioCRUD(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title='Catálogo de Inventario', size=(1200, 800))
        self.panel = wx.Panel(self)
        self.lista_resultados = None
        self.txt_codigo_barras = None
        self.txt_fecha = None
        self.crear_interfaz()
        self.Centre()
        self.Show()

    def mensaje(self, titulo, mensaje):
        """Muestra un mensaje emergente."""
        wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

    def advertencia_salir(self):
        """Pregunta si desea salir si hay datos ingresados."""
        if any([
            self.txt_codigo_barras.GetValue(),
            self.txt_existencia.GetValue(),
            self.txt_minimo.GetValue(),
            self.combo_temporada.GetValue()
        ]):
            respuesta = wx.MessageBox(
                "Hay datos no guardados. ¿Desea salir de todas formas?",
                "Advertencia",
                wx.YES_NO | wx.ICON_WARNING
            )
            return respuesta == wx.YES
        return True

    def validar_campos(self):
        """Valida que los campos obligatorios no estén vacíos."""
        return all([
            self.txt_codigo_barras.GetValue(),
            self.txt_existencia.GetValue(),
            self.txt_minimo.GetValue(),
            self.combo_temporada.GetValue()
        ])

    def crear_interfaz(self):
        sizer_principal = wx.BoxSizer(wx.VERTICAL)

        # Título
        lbl_titulo = wx.StaticText(self.panel, label="CATÁLOGO DE INVENTARIO", style=wx.ALIGN_CENTER)
        fuente_titulo = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        lbl_titulo.SetFont(fuente_titulo)
        lbl_titulo.SetForegroundColour(wx.Colour(44, 62, 80))  # Azul oscuro
        sizer_principal.Add(lbl_titulo, 0, wx.EXPAND | wx.ALL, 20)

        # Campos de entrada
        grid_sizer = wx.FlexGridSizer(rows=6, cols=2, vgap=15, hgap=10)
        grid_sizer.AddGrowableCol(1)

        # Campo Código de Barras
        grid_sizer.Add(wx.StaticText(self.panel, label="Código de Barras:"), flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_codigo_barras = wx.TextCtrl(self.panel, size=(300, -1), style=wx.TE_PROCESS_ENTER)
        self.txt_codigo_barras.SetBackgroundColour(wx.Colour(255, 255, 230))
        grid_sizer.Add(self.txt_codigo_barras, flag=wx.EXPAND)

        # Campo Existencia Actual
        grid_sizer.Add(wx.StaticText(self.panel, label="Existencia Actual:"), flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_existencia = wx.TextCtrl(self.panel, size=(300, -1))
        self.txt_existencia.SetBackgroundColour(wx.Colour(255, 255, 230))
        grid_sizer.Add(self.txt_existencia, flag=wx.EXPAND)

        # Campo Mínimo Requerido
        grid_sizer.Add(wx.StaticText(self.panel, label="Mínimo Requerido:"), flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_minimo = wx.TextCtrl(self.panel, size=(300, -1))
        self.txt_minimo.SetBackgroundColour(wx.Colour(255, 255, 230))
        grid_sizer.Add(self.txt_minimo, flag=wx.EXPAND)

        # Campo Temporada (ComboBox)
        grid_sizer.Add(wx.StaticText(self.panel, label="Temporada:"), flag=wx.ALIGN_CENTER_VERTICAL)
        temporadas = ['Todo el año', 'Verano', 'Otoño', 'Invierno', 'Primavera',
                      'Día de las Madres', 'Navidad', 'Día de Muertos']
        self.combo_temporada = wx.ComboBox(self.panel, choices=temporadas,
                                           style=wx.CB_READONLY, size=(300, -1))
        self.combo_temporada.SetBackgroundColour(wx.Colour(255, 255, 230))
        grid_sizer.Add(self.combo_temporada, flag=wx.EXPAND)

        # Campo Último Reabastecimiento (Solo lectura)
        grid_sizer.Add(wx.StaticText(self.panel, label="Último Reabastecimiento:"), flag=wx.ALIGN_CENTER_VERTICAL)
        self.lbl_ultimo_reabastecimiento = wx.StaticText(self.panel, label="")
        grid_sizer.Add(self.lbl_ultimo_reabastecimiento, flag=wx.EXPAND)

        sizer_principal.Add(grid_sizer, 0, wx.CENTER | wx.ALL, 20)

        # Botones
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_crear = wx.Button(self.panel, label=" Crear ", size=(120, 40))
        self.btn_buscar = wx.Button(self.panel, label=" Buscar ", size=(120, 40))
        self.btn_actualizar = wx.Button(self.panel, label=" Actualizar / Agregar ", size=(120, 40))
        self.btn_eliminar = wx.Button(self.panel, label=" Eliminar ", size=(120, 40))
        self.btn_limpiar = wx.Button(self.panel, label=" Limpiar ", size=(120, 40))
        self.btn_regresar = wx.Button(self.panel, label=" Regresar ", size=(120, 40))

        for btn in [self.btn_crear, self.btn_buscar, self.btn_actualizar,
                    self.btn_eliminar, self.btn_limpiar, self.btn_regresar]:
            btn.SetBackgroundColour(wx.Colour(44, 62, 80))
            btn.SetForegroundColour(wx.WHITE)
            btn.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))  # Fuente más pequeña

        btn_sizer.Add(self.btn_crear, 0, wx.ALL, 5)
        btn_sizer.Add(self.btn_buscar, 0, wx.ALL, 5)
        btn_sizer.Add(self.btn_actualizar, 0, wx.ALL, 5)
        btn_sizer.Add(self.btn_eliminar, 0, wx.ALL, 5)
        btn_sizer.Add(self.btn_limpiar, 0, wx.ALL, 5)
        btn_sizer.Add(self.btn_regresar, 0, wx.ALL, 5)
        sizer_principal.Add(btn_sizer, 0, wx.CENTER | wx.TOP, 10)

        # Tabla de resultados
        self.lista_resultados = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, size=(-1, 200))
        columnas = ["Código", "Existencia", "Mínimo", "Temporada", "Último Reabastecimiento"]
        for i, col in enumerate(columnas):
            self.lista_resultados.InsertColumn(i, col, width=200)
        sizer_principal.Add(self.lista_resultados, 0, wx.EXPAND | wx.ALL, 20)

        self.panel.SetSizer(sizer_principal)

        # Eventos
        self.btn_crear.Bind(wx.EVT_BUTTON, self.on_crear)
        self.btn_buscar.Bind(wx.EVT_BUTTON, self.on_buscar)
        self.btn_actualizar.Bind(wx.EVT_BUTTON, self.on_actualizar_agregar)
        self.btn_eliminar.Bind(wx.EVT_BUTTON, self.on_eliminar)
        self.btn_limpiar.Bind(wx.EVT_BUTTON, self.limpiar_campos)
        self.btn_regresar.Bind(wx.EVT_BUTTON, self.on_regresar)

        # Búsqueda automática mientras escribe
        self.txt_codigo_barras.Bind(wx.EVT_TEXT, self.busqueda_rapida)

        # Doble clic en tabla
        self.lista_resultados.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.rellenar_desde_tabla)

    def on_crear(self, event):
        if not self.validar_campos():
            self.mensaje("Advertencia", "Por favor, complete todos los campos obligatorios.")
            return

        try:
            existencia = int(self.txt_existencia.GetValue())
            minimo = int(self.txt_minimo.GetValue())
        except ValueError:
            self.mensaje("Error", "Los campos de cantidad deben ser números enteros.")
            return

        temporada = self.combo_temporada.GetValue()
        codigo = self.txt_codigo_barras.GetValue().strip()

        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    INSERT INTO inventario (codigo_barras, existencia_actual, minimo_requerido, temporada, ultimo_reabastecimiento)
                    VALUES (%s, %s, %s, %s, NOW())
                """, (codigo, existencia, minimo, temporada))
                conn.commit()
                self.mensaje("Éxito", "Producto creado correctamente.")
                self.limpiar_campos(None)
                self.busqueda_rapida(None)
            except Exception as e:
                self.mensaje("Error", f"No se pudo crear el producto:\n{e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def on_buscar(self, event):
        codigo = self.txt_codigo_barras.GetValue().strip()
        if not codigo:
            self.mensaje("Advertencia", "Ingrese un código de barras.")
            return

        resultado = self.buscar_producto(codigo)
        if resultado:
            self.txt_existencia.SetValue(str(resultado[1]))
            self.txt_minimo.SetValue(str(resultado[2]))
            self.combo_temporada.SetValue(resultado[3])
            self.lbl_ultimo_reabastecimiento.SetLabel(str(resultado[4]) if resultado[4] else "")
        else:
            self.mensaje("Información", "Producto no encontrado.")

    def busqueda_rapida(self, event):
        valor = self.txt_codigo_barras.GetValue().strip()
        if not valor:
            self.lista_resultados.DeleteAllItems()
            return

        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    SELECT * FROM inventario 
                    WHERE codigo_barras LIKE %s LIMIT 10
                """, (f"%{valor}%",))
                resultados = cursor.fetchall()
                self.lista_resultados.DeleteAllItems()
                for row in resultados:
                    idx = self.lista_resultados.InsertItem(self.lista_resultados.GetItemCount(), row[0])
                    self.lista_resultados.SetItem(idx, 1, str(row[1]))
                    self.lista_resultados.SetItem(idx, 2, str(row[2]))
                    self.lista_resultados.SetItem(idx, 3, row[3])
                    self.lista_resultados.SetItem(idx, 4, str(row[4]) if row[4] else "")
            except Exception as e:
                self.mensaje("Error", f"Error al buscar producto:\n{e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def rellenar_desde_tabla(self, event):
        index = self.lista_resultados.GetFirstSelected()
        if index >= 0:
            confirmacion = wx.MessageBox(
                "¿Desea rellenar los campos con este producto?",
                "Confirmar",
                wx.YES_NO | wx.ICON_QUESTION
            )
            if confirmacion == wx.YES:
                codigo = self.lista_resultados.GetItem(index, 0).GetText()
                resultado = self.buscar_producto(codigo)
                if resultado:
                    self.txt_codigo_barras.SetValue(str(resultado[0]))
                    self.txt_existencia.SetValue(str(resultado[1]))
                    self.txt_minimo.SetValue(str(resultado[2]))
                    self.combo_temporada.SetValue(str(resultado[3]))
                    self.lbl_ultimo_reabastecimiento.SetLabel(str(resultado[4]) if resultado[4] else "")

    def on_actualizar_agregar(self, event):
        if not self.validar_campos():
            self.mensaje("Advertencia", "Por favor, complete todos los campos obligatorios.")
            return

        try:
            existencia = int(self.txt_existencia.GetValue())
            minimo = int(self.txt_minimo.GetValue())
        except ValueError:
            self.mensaje("Error", "Los campos de cantidad deben ser números enteros.")
            return

        temporada = self.combo_temporada.GetValue()
        codigo = self.txt_codigo_barras.GetValue().strip()

        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    UPDATE inventario SET 
                        existencia_actual = %s, 
                        minimo_requerido = %s, 
                        temporada = %s, 
                        ultimo_reabastecimiento = NOW()
                    WHERE codigo_barras = %s
                """, (existencia, minimo, temporada, codigo))

                if cursor.rowcount == 0:
                    # Si no se encontró, lo creamos
                    cursor.execute("""
                        INSERT INTO inventario (codigo_barras, existencia_actual, minimo_requerido, temporada, ultimo_reabastecimiento)
                        VALUES (%s, %s, %s, %s, NOW())
                    """, (codigo, existencia, minimo, temporada))

                conn.commit()
                self.mensaje("Éxito", "Producto actualizado o creado exitosamente.")
                self.limpiar_campos(None)
                self.busqueda_rapida(None)
            except Exception as e:
                conn.rollback()
                self.mensaje("Error", f"No se pudo actualizar el producto:\n{e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def on_eliminar(self, event):
        codigo = self.txt_codigo_barras.GetValue().strip()
        if not codigo:
            self.mensaje("Advertencia", "Ingrese un código de barras.")
            return

        confirmacion = wx.MessageBox(
            f"¿Está seguro de eliminar el producto '{codigo}'? Se eliminarán artículos e inventario.",
            "Confirmar eliminación",
            wx.YES_NO | wx.ICON_WARNING
        )
        if confirmacion == wx.YES:
            conn, cursor = conectar()
            if conn and cursor:
                try:
                    cursor.execute("DELETE FROM inventario WHERE codigo_barras = %s", (codigo,))
                    conn.commit()
                    self.mensaje("Éxito", "Producto eliminado correctamente.")
                    self.limpiar_campos(None)
                except Exception as e:
                    conn.rollback()
                    self.mensaje("Error", f"No se pudo eliminar el producto:\n{e}")
                finally:
                    cursor.close()
                    conn.close()
            else:
                self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def limpiar_campos(self, event):
        self.txt_codigo_barras.Clear()
        self.txt_existencia.Clear()
        self.txt_minimo.Clear()
        self.combo_temporada.SetValue("")
        self.lbl_ultimo_reabastecimiento.SetLabel("")
        self.lista_resultados.DeleteAllItems()

    def on_regresar(self, event):
        if self.advertencia_salir():
            self.Close()

    def buscar_producto(self, codigo):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("SELECT * FROM inventario WHERE codigo_barras = %s", (codigo,))
                return cursor.fetchone()
            except Exception as e:
                self.mensaje("Error", f"No se pudo buscar el producto:\n{e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")
        return None

    def on_buscar(self, event):
        codigo = self.txt_codigo_barras.GetValue().strip()
        if not codigo:
            self.mensaje("Advertencia", "Ingrese el código de barras.")
            return

        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("SELECT * FROM inventario WHERE codigo_barras = %s", (codigo,))
                resultado = cursor.fetchone()
                if resultado:
                    # Mostrar en tabla
                    self.lista_resultados.DeleteAllItems()
                    idx = self.lista_resultados.InsertItem(0, resultado[0])
                    self.lista_resultados.SetItem(idx, 1, str(resultado[1]))
                    self.lista_resultados.SetItem(idx, 2, str(resultado[2]))
                    self.lista_resultados.SetItem(idx, 3, resultado[3])
                    self.lista_resultados.SetItem(idx, 4, str(resultado[4]) if resultado[4] else "")

                    # Rellenar campos
                    self.txt_existencia.SetValue(str(resultado[1]))
                    self.txt_minimo.SetValue(str(resultado[2]))
                    self.combo_temporada.SetValue(resultado[3])
                    self.lbl_ultimo_reabastecimiento.SetLabel(str(resultado[4]) if resultado[4] else "")
                else:
                    self.lista_resultados.DeleteAllItems()
                    self.mensaje("Información", "Producto no encontrado.")
            except Exception as e:
                self.mensaje("Error", f"No se pudo buscar el producto: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")
            
    def on_actualizar(self, event):
        self.on_actualizar_agregar(event)

    def on_eliminar(self, event):
        self.on_eliminar(event)