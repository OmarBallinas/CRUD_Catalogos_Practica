import wx
from conexion import conectar

class ArticuloCRUD(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title='Catálogo de Artículos', size=(1200, 800))
        self.panel = wx.Panel(self)
        self.crear_interfaz()
        self.Centre()
        self.Show()

    def mensaje(self, titulo, mensaje):
        """Muestra un mensaje emergente."""
        wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

    def advertencia_salir(self):
        """Pregunta si desea salir si hay datos ingresados."""
        if any([
            self.txt_codigo.GetValue(),
            self.txt_nombre.GetValue(),
            self.txt_descripcion.GetValue(),
            self.txt_precio.GetValue(),
            self.txt_unidad.GetValue(),
            self.txt_descuento.GetValue(),
            self.txt_id_categoria.GetValue()
        ]):
            respuesta = wx.MessageBox(
                "Hay datos no guardados. ¿Desea salir de todas formas?",
                "Advertencia",
                wx.YES_NO | wx.ICON_WARNING
            )
            return respuesta == wx.YES
        return True

    def validar_campos(self):
        """Valida que los campos obligatorios tengan datos."""
        return all([
            self.txt_codigo.GetValue(),
            self.txt_nombre.GetValue(),
            self.txt_descripcion.GetValue(),
            self.txt_precio.GetValue(),
            self.txt_unidad.GetValue(),
            self.txt_descuento.GetValue(),
            self.txt_id_categoria.GetValue()
        ])

    def crear_interfaz(self):
        """Construye la interfaz gráfica."""
        sizer_principal = wx.BoxSizer(wx.VERTICAL)

        # Título
        lbl_titulo = wx.StaticText(self.panel, label="CATÁLOGO DE ARTÍCULOS", style=wx.ALIGN_CENTER)
        fuente_titulo = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        lbl_titulo.SetFont(fuente_titulo)
        lbl_titulo.SetForegroundColour(wx.Colour(44, 62, 80))  # Azul oscuro
        sizer_principal.Add(lbl_titulo, 0, wx.EXPAND | wx.ALL, 20)

        # Campos de entrada
        grid_sizer = wx.FlexGridSizer(rows=7, cols=2, vgap=15, hgap=10)
        grid_sizer.AddGrowableCol(1)

        # Campos
        grid_sizer.Add(wx.StaticText(self.panel, label="Código de Barras:"), flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_codigo = wx.TextCtrl(self.panel, size=(300, -1), style=wx.TE_PROCESS_ENTER)
        self.txt_codigo.SetBackgroundColour(wx.Colour(255, 255, 230))
        grid_sizer.Add(self.txt_codigo, flag=wx.EXPAND)

        grid_sizer.Add(wx.StaticText(self.panel, label="Nombre:"), flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_nombre = wx.TextCtrl(self.panel, size=(300, -1))
        self.txt_nombre.SetBackgroundColour(wx.Colour(255, 255, 230))
        grid_sizer.Add(self.txt_nombre, flag=wx.EXPAND)

        grid_sizer.Add(wx.StaticText(self.panel, label="Descripción:"), flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_descripcion = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE, size=(300, 60))
        self.txt_descripcion.SetBackgroundColour(wx.Colour(255, 255, 230))
        grid_sizer.Add(self.txt_descripcion, flag=wx.EXPAND)

        grid_sizer.Add(wx.StaticText(self.panel, label="Precio:"), flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_precio = wx.TextCtrl(self.panel, size=(300, -1))
        self.txt_precio.SetBackgroundColour(wx.Colour(255, 255, 230))
        grid_sizer.Add(self.txt_precio, flag=wx.EXPAND)

        grid_sizer.Add(wx.StaticText(self.panel, label="Unidad:"), flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_unidad = wx.TextCtrl(self.panel, size=(300, -1))
        self.txt_unidad.SetBackgroundColour(wx.Colour(255, 255, 230))
        grid_sizer.Add(self.txt_unidad, flag=wx.EXPAND)

        grid_sizer.Add(wx.StaticText(self.panel, label="Descuento (%):"), flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_descuento = wx.TextCtrl(self.panel, size=(300, -1))
        self.txt_descuento.SetBackgroundColour(wx.Colour(255, 255, 230))
        grid_sizer.Add(self.txt_descuento, flag=wx.EXPAND)

        grid_sizer.Add(wx.StaticText(self.panel, label="ID Categoría:"), flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_id_categoria = wx.TextCtrl(self.panel, size=(300, -1))
        self.txt_id_categoria.SetBackgroundColour(wx.Colour(255, 255, 230))
        grid_sizer.Add(self.txt_id_categoria, flag=wx.EXPAND)

        sizer_principal.Add(grid_sizer, 0, wx.CENTER | wx.ALL, 10)

        # Botones
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_crear = wx.Button(self.panel, label=" Crear ", size=(120, 40))
        self.btn_buscar = wx.Button(self.panel, label=" Buscar ", size=(120, 40))
        self.btn_actualizar = wx.Button(self.panel, label=" Actualizar ", size=(120, 40))
        self.btn_eliminar = wx.Button(self.panel, label=" Eliminar ", size=(120, 40))
        self.btn_limpiar = wx.Button(self.panel, label=" Limpiar ", size=(120, 40))
        self.btn_regresar = wx.Button(self.panel, label=" Regresar ", size=(120, 40))

        for btn in [self.btn_crear, self.btn_buscar, self.btn_actualizar,
                    self.btn_eliminar, self.btn_limpiar, self.btn_regresar]:
            btn.SetBackgroundColour(wx.Colour(44, 62, 80))
            btn.SetForegroundColour(wx.WHITE)
            btn.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        btn_sizer.Add(self.btn_crear, 0, wx.ALL, 5)
        btn_sizer.Add(self.btn_buscar, 0, wx.ALL, 5)
        btn_sizer.Add(self.btn_actualizar, 0, wx.ALL, 5)
        btn_sizer.Add(self.btn_eliminar, 0, wx.ALL, 5)
        btn_sizer.Add(self.btn_limpiar, 0, wx.ALL, 5)
        btn_sizer.Add(self.btn_regresar, 0, wx.ALL, 5)

        sizer_principal.Add(btn_sizer, 0, wx.CENTER)

        # Tabla de resultados
        self.lista_resultados = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, size=(-1, 200))
        columnas = ["Código", "Nombre", "Precio", "Unidad", "Descuento", "ID Categoría"]
        for i, col in enumerate(columnas):
            self.lista_resultados.InsertColumn(i, col, width=180)

        sizer_principal.Add(self.lista_resultados, 0, wx.EXPAND | wx.ALL, 20)

        self.panel.SetSizer(sizer_principal)

        # Eventos
        self.btn_crear.Bind(wx.EVT_BUTTON, self.on_crear)
        self.btn_buscar.Bind(wx.EVT_BUTTON, self.on_buscar)
        self.btn_actualizar.Bind(wx.EVT_BUTTON, self.on_actualizar)
        self.btn_eliminar.Bind(wx.EVT_BUTTON, self.on_eliminar)
        self.btn_limpiar.Bind(wx.EVT_BUTTON, self.limpiar_campos)
        self.btn_regresar.Bind(wx.EVT_BUTTON, self.on_regresar)
        self.txt_codigo.Bind(wx.EVT_TEXT, self.busqueda_rapida)
        self.txt_codigo.Bind(wx.EVT_TEXT_ENTER, self.on_buscar)

        # Doble clic en tabla
        self.lista_resultados.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.rellenar_desde_tabla)

    def on_crear(self, event):
        if self.validar_campos():
            try:
                precio = float(self.txt_precio.GetValue())
                descuento = float(self.txt_descuento.GetValue())
                id_categoria = int(self.txt_id_categoria.GetValue())
            except ValueError:
                self.mensaje("Error", "Datos inválidos en precio, descuento o ID categoría.")
                return

            self.agregar_articulo(
                self.txt_codigo.GetValue(),
                self.txt_nombre.GetValue(),
                self.txt_descripcion.GetValue(),
                precio,
                self.txt_unidad.GetValue(),
                descuento,
                id_categoria
            )
        else:
            self.mensaje("Advertencia", "Por favor, complete todos los campos.")

    def on_buscar(self, event):
        codigo = self.txt_codigo.GetValue()
        if not codigo:
            self.mensaje("Advertencia", "Ingrese el código de barras.")
            return

        resultado = self.buscar_articulo(codigo)
        if resultado:
            self.lista_resultados.DeleteAllItems()
            idx = self.lista_resultados.InsertItem(self.lista_resultados.GetItemCount(), resultado[0])
            self.lista_resultados.SetItem(idx, 1, resultado[1])
            self.lista_resultados.SetItem(idx, 2, f"{resultado[3]:.2f}")
            self.lista_resultados.SetItem(idx, 3, resultado[4])
            self.lista_resultados.SetItem(idx, 4, f"{resultado[5]:.2f}")
            self.lista_resultados.SetItem(idx, 5, str(resultado[6]))
            self.txt_nombre.SetValue(resultado[1])
            self.txt_descripcion.SetValue(resultado[2])
            self.txt_precio.SetValue(str(resultado[3]))
            self.txt_unidad.SetValue(resultado[4])
            self.txt_descuento.SetValue(str(resultado[5]))
            self.txt_id_categoria.SetValue(str(resultado[6]))
        else:
            self.lista_resultados.DeleteAllItems()
            self.mensaje("Información", "Artículo no encontrado.")

    def busqueda_rapida(self, event):
        valor = self.txt_codigo.GetValue().strip()
        if not valor:
            self.lista_resultados.DeleteAllItems()
            return

        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    SELECT * FROM articulo 
                    WHERE codigo_barras LIKE %s OR nombre LIKE %s
                    LIMIT 10
                """, (f"%{valor}%", f"%{valor}%"))
                resultados = cursor.fetchall()
                self.lista_resultados.DeleteAllItems()
                for row in resultados:
                    idx = self.lista_resultados.InsertItem(self.lista_resultados.GetItemCount(), row[0])
                    self.lista_resultados.SetItem(idx, 1, row[1])
                    self.lista_resultados.SetItem(idx, 2, f"{row[3]:.2f}")
                    self.lista_resultados.SetItem(idx, 3, row[4])
                    self.lista_resultados.SetItem(idx, 4, f"{row[5]:.2f}")
                    self.lista_resultados.SetItem(idx, 5, str(row[6]))
            except Exception as e:
                self.mensaje("Error", f"Error al buscar artículo: {e}")
            finally:
                cursor.close()
                conn.close()

    def rellenar_desde_tabla(self, event):
        index = self.lista_resultados.GetFirstSelected()
        if index >= 0:
            confirmacion = wx.MessageBox(
                "¿Desea rellenar los campos con este artículo?",
                "Confirmar",
                wx.YES_NO | wx.ICON_QUESTION
            )
            if confirmacion == wx.YES:
                codigo = self.lista_resultados.GetItem(index, 0).GetText()
                resultado = self.buscar_articulo(codigo)
                if resultado:
                    self.txt_codigo.SetValue(resultado[0])
                    self.txt_nombre.SetValue(resultado[1])
                    self.txt_descripcion.SetValue(resultado[2])
                    self.txt_precio.SetValue(str(resultado[3]))
                    self.txt_unidad.SetValue(resultado[4])
                    self.txt_descuento.SetValue(str(resultado[5]))
                    self.txt_id_categoria.SetValue(str(resultado[6]))

    def on_actualizar(self, event):
        if self.validar_campos():
            self.actualizar_articulo(
                self.txt_codigo.GetValue(),
                self.txt_nombre.GetValue(),
                self.txt_descripcion.GetValue(),
                self.txt_precio.GetValue(),
                self.txt_unidad.GetValue(),
                self.txt_descuento.GetValue(),
                self.txt_id_categoria.GetValue()
            )
        else:
            self.mensaje("Advertencia", "Por favor, complete todos los campos.")

    def on_eliminar(self, event):
        codigo = self.txt_codigo.GetValue()
        if not codigo:
            self.mensaje("Advertencia", "Por favor, ingrese el código de barras.")
            return

        confirmacion = wx.MessageBox(
            f"¿Está seguro de eliminar el artículo '{codigo}'? Se eliminará del inventario.",
            "Confirmar eliminación",
            wx.YES_NO | wx.ICON_WARNING
        )
        if confirmacion != wx.YES:
            return

        self.eliminar_articulo(codigo)
        self.limpiar_campos(None)

    def limpiar_campos(self, event):
        self.txt_codigo.Clear()
        self.txt_nombre.Clear()
        self.txt_descripcion.Clear()
        self.txt_precio.Clear()
        self.txt_unidad.Clear()
        self.txt_descuento.Clear()
        self.txt_id_categoria.Clear()
        self.lista_resultados.DeleteAllItems()

    def on_regresar(self, event):
        if self.advertencia_salir():
            self.Close()

    def agregar_articulo(self, codigo, nombre, descripcion, precio, unidad, descuento, id_categoria):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    INSERT INTO articulo (codigo_barras, nombre, descripcion, precio, unidad, descuento, idcategoria)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (codigo, nombre, descripcion, float(precio), unidad, float(descuento), int(id_categoria)))
                conn.commit()
                self.mensaje("Éxito", "Artículo creado exitosamente.")
            except Exception as e:
                self.mensaje("Error", f"Error al crear el artículo: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def buscar_articulo(self, codigo):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("SELECT * FROM articulo WHERE codigo_barras = %s", (codigo,))
                return cursor.fetchone()
            except Exception as e:
                self.mensaje("Error", f"Error al buscar artículo: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")
        return None

    def actualizar_articulo(self, codigo, nombre, descripcion, precio, unidad, descuento, id_categoria):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    UPDATE articulo
                    SET nombre = %s, descripcion = %s, precio = %s,
                        unidad = %s, descuento = %s, idcategoria = %s
                    WHERE codigo_barras = %s
                """, (nombre, descripcion, float(precio), unidad, float(descuento), int(id_categoria), codigo))
                conn.commit()
                self.mensaje("Éxito", "Artículo actualizado exitosamente.")
            except Exception as e:
                self.mensaje("Error", f"Error al actualizar artículo: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def eliminar_articulo(self, codigo):
        conn, cursor = conectar()
        if not conn or not cursor:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")
            return

        try:
            cursor.execute("SELECT nombre FROM articulo WHERE codigo_barras = %s", (codigo,))
            fila = cursor.fetchone()
            if not fila:
                self.mensaje("Información", "El artículo no existe o ya fue eliminado.")
                return

            nombre_articulo = fila[0]
            cursor.execute("DELETE FROM inventario WHERE codigo_barras = %s", (codigo,))
            cursor.execute("DELETE FROM articulo WHERE codigo_barras = %s", (codigo,))
            conn.commit()
            self.mensaje("Éxito", f"Artículo '{nombre_articulo}' eliminado correctamente.")
        except Exception as e:
            conn.rollback()
            self.mensaje("Error", f"Error al eliminar artículo: {e}")
        finally:
            cursor.close()
            conn.close()

    def on_buscar(self, event):
        codigo = self.txt_codigo.GetValue()
        if not codigo:
            self.mensaje("Advertencia", "Por favor, ingrese el código de barras.")
            return

        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("SELECT * FROM articulo WHERE codigo_barras = %s", (codigo,))
                resultado = cursor.fetchone()

                if resultado:
                    # Mostrar resultados en los campos
                    self.txt_nombre.SetValue(resultado[1])
                    self.txt_descripcion.SetValue(resultado[2])
                    self.txt_precio.SetValue(str(resultado[3]))
                    self.txt_unidad.SetValue(resultado[4])
                    self.txt_descuento.SetValue(str(resultado[5]))
                    self.txt_id_categoria.SetValue(str(resultado[6]))

                    # Mostrar artículo en la tabla
                    self.lista_resultados.DeleteAllItems()
                    idx = self.lista_resultados.InsertItem(self.lista_resultados.GetItemCount(), resultado[0])
                    self.lista_resultados.SetItem(idx, 1, resultado[1])
                    self.lista_resultados.SetItem(idx, 2, f"{resultado[3]:.2f}")
                    self.lista_resultados.SetItem(idx, 3, resultado[4])
                    self.lista_resultados.SetItem(idx, 4, f"{resultado[5]:.2f}")
                    self.lista_resultados.SetItem(idx, 5, str(resultado[6]))
                else:
                    self.lista_resultados.DeleteAllItems()
                    self.mensaje("Información", "Artículo no encontrado.")

            except Exception as e:
                self.mensaje("Error", f"No se pudo buscar el artículo: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")
