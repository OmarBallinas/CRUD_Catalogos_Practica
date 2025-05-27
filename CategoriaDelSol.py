import wx
from conexion import conectar

class CategoriaCRUD(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title='Catálogo de Categorías', size=(1200, 800))
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
            self.txt_id_categoria.GetValue(),
            self.txt_nombre.GetValue()
        ]):
            respuesta = wx.MessageBox(
                "Hay datos no guardados. ¿Desea salir de todas formas?",
                "Advertencia",
                wx.YES_NO | wx.ICON_WARNING
            )
            return respuesta == wx.YES
        return True

    def validar_campos(self):
        """Verifica que los campos obligatorios no estén vacíos."""
        return all([
            self.txt_id_categoria.GetValue(),
            self.txt_nombre.GetValue()
        ])

    def crear_interfaz(self):
        sizer_principal = wx.BoxSizer(wx.VERTICAL)

        # Título
        lbl_titulo = wx.StaticText(self.panel, label="CATÁLOGO DE CATEGORÍAS", style=wx.ALIGN_CENTER)
        fuente_titulo = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        lbl_titulo.SetFont(fuente_titulo)
        lbl_titulo.SetForegroundColour(wx.Colour(44, 62, 80))  # Azul oscuro
        sizer_principal.Add(lbl_titulo, 0, wx.EXPAND | wx.ALL, 20)

        # Campos de entrada
        grid_sizer = wx.FlexGridSizer(rows=7, cols=2, vgap=15, hgap=10)
        grid_sizer.AddGrowableCol(1)


        # Campo ID Categoría
        grid_sizer.Add(wx.StaticText(self.panel, label="ID Categoría:"), flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_id_categoria = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.txt_id_categoria.SetBackgroundColour(wx.Colour(255, 255, 230))
        grid_sizer.Add(self.txt_id_categoria, flag=wx.EXPAND)

        # Campo Nombre
        grid_sizer.Add(wx.StaticText(self.panel, label="Nombre:"), flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_nombre = wx.TextCtrl(self.panel)
        self.txt_nombre.SetBackgroundColour(wx.Colour(255, 255, 230))
        grid_sizer.Add(self.txt_nombre, flag=wx.EXPAND)

        # Añadimos el grid al sizer principal
        sizer_principal.Add(grid_sizer, 0, wx.CENTER | wx.ALL, 20)

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

        sizer_principal.Add(btn_sizer, 0, wx.CENTER | wx.TOP, 10)

        # Tabla de resultados
        self.lista_resultados = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, size=(-1, 200))
        columnas = ["ID Categoría", "Nombre"]
        for i, col in enumerate(columnas):
            self.lista_resultados.InsertColumn(i, col, width=300)
        sizer_principal.Add(self.lista_resultados, 0, wx.EXPAND | wx.ALL, 20)

        self.panel.SetSizer(sizer_principal)

        # Eventos
        self.btn_crear.Bind(wx.EVT_BUTTON, self.on_crear)
        self.btn_buscar.Bind(wx.EVT_BUTTON, self.on_buscar)
        self.btn_actualizar.Bind(wx.EVT_BUTTON, self.on_actualizar)
        self.btn_eliminar.Bind(wx.EVT_BUTTON, self.on_eliminar)
        self.btn_limpiar.Bind(wx.EVT_BUTTON, self.limpiar_campos)
        self.btn_regresar.Bind(wx.EVT_BUTTON, self.on_regresar)

        # Búsqueda dinámica mientras escribe
        self.txt_id_categoria.Bind(wx.EVT_TEXT, self.busqueda_rapida_id)

        # Doble clic en tabla para rellenar campos
        self.lista_resultados.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.rellenar_desde_tabla)

    def on_crear(self, event):
        if self.validar_campos():
            try:
                id_categoria = int(self.txt_id_categoria.GetValue())
            except ValueError:
                self.mensaje("Error", "El ID debe ser un número entero.")
                return

            self.crear_categoria(id_categoria, self.txt_nombre.GetValue())
        else:
            self.mensaje("Advertencia", "Por favor, complete todos los campos.")

    def on_buscar(self, event):
        id_categoria = self.txt_id_categoria.GetValue().strip()
        if not id_categoria.isdigit():
            self.mensaje("Advertencia", "Ingrese un ID válido.")
            return

        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("SELECT * FROM categoria WHERE idcategoria = %s", (int(id_categoria),))
                resultado = cursor.fetchone()

                if resultado:
                    self.lista_resultados.DeleteAllItems()
                    idx = self.lista_resultados.InsertItem(0, str(resultado[0]))
                    self.lista_resultados.SetItem(idx, 1, resultado[1])
                    self.txt_nombre.SetValue(resultado[1])
                else:
                    self.lista_resultados.DeleteAllItems()
                    self.mensaje("Información", "Categoría no encontrada.")
            except Exception as e:
                self.mensaje("Error", f"No se pudo buscar la categoría: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def busqueda_rapida_id(self, event):
        valor = self.txt_id_categoria.GetValue().strip()
        if not valor:
            self.lista_resultados.DeleteAllItems()
            return

        conn, cursor = conectar()
        if conn and cursor:
            try:
                if valor.isdigit():
                    cursor.execute("SELECT * FROM categoria WHERE idcategoria = %s", (int(valor),))
                    resultados = cursor.fetchall()
                else:
                    cursor.execute("SELECT * FROM categoria WHERE nombre LIKE %s LIMIT 10", (f"%{valor}%",))
                    resultados = cursor.fetchall()

                self.lista_resultados.DeleteAllItems()
                for row in resultados:
                    idx = self.lista_resultados.InsertItem(self.lista_resultados.GetItemCount(), str(row[0]))
                    self.lista_resultados.SetItem(idx, 1, row[1])
            except Exception as e:
                self.mensaje("Error", f"Error al buscar categoría: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def rellenar_desde_tabla(self, event):
        index = self.lista_resultados.GetFirstSelected()
        if index >= 0:
            confirmacion = wx.MessageBox(
                "¿Desea rellenar los campos con esta categoría?",
                "Confirmar",
                wx.YES_NO | wx.ICON_QUESTION
            )
            if confirmacion == wx.YES:
                id_categoria = self.lista_resultados.GetItem(index, 0).GetText()
                resultado = self.buscar_categoria(int(id_categoria))
                if resultado:
                    self.txt_id_categoria.SetValue(str(resultado[0]))
                    self.txt_nombre.SetValue(resultado[1])

    def on_actualizar(self, event):
        if self.validar_campos():
            try:
                id_categoria = int(self.txt_id_categoria.GetValue())
            except ValueError:
                self.mensaje("Error", "El ID debe ser un número entero.")
                return

            self.actualizar_categoria(id_categoria, self.txt_nombre.GetValue())
        else:
            self.mensaje("Advertencia", "Por favor, complete todos los campos.")

    def on_eliminar(self, event):
        id_categoria = self.txt_id_categoria.GetValue().strip()
        if not id_categoria.isdigit():
            self.mensaje("Advertencia", "Ingrese un ID válido.")
            return

        confirmacion = wx.MessageBox(
            f"¿Está seguro de eliminar la categoría '{id_categoria}'? Se eliminarán artículos e inventario.",
            "Confirmar eliminación",
            wx.YES_NO | wx.ICON_WARNING
        )
        if confirmacion == wx.YES:
            self.eliminar_categoria(int(id_categoria))
            self.limpiar_campos(None)

    def limpiar_campos(self, event):
        self.txt_id_categoria.Clear()
        self.txt_nombre.Clear()
        self.lista_resultados.DeleteAllItems()

    def on_regresar(self, event):
        if self.advertencia_salir():
            self.Close()

    def crear_categoria(self, id_categoria, nombre):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    INSERT INTO categoria (idcategoria, nombre)
                    VALUES (%s, %s)
                """, (int(id_categoria), nombre))
                conn.commit()
                self.mensaje("Éxito", "Categoría creada exitosamente.")
            except Exception as e:
                self.mensaje("Error", f"Error al crear categoría: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def buscar_categoria(self, id_categoria):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("SELECT * FROM categoria WHERE idcategoria = %s", (id_categoria,))
                return cursor.fetchone()
            except Exception as e:
                self.mensaje("Error", f"Error al buscar categoría: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")
        return None

    def actualizar_categoria(self, id_categoria, nombre):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    UPDATE categoria SET nombre = %s WHERE idcategoria = %s
                """, (nombre, int(id_categoria)))
                conn.commit()
                self.mensaje("Éxito", "Categoría actualizada exitosamente.")
            except Exception as e:
                self.mensaje("Error", f"Error al actualizar categoría: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def eliminar_categoria(self, id_categoria):
        conn, cursor = conectar()
        if not conn or not cursor:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")
            return

        try:
            cursor.execute("SELECT COUNT(*) FROM articulo WHERE idcategoria = %s", (id_categoria,))
            cantidad = cursor.fetchone()[0]
            if cantidad > 0:
                mensaje = f"La categoría tiene {cantidad} artículo(s) asociado(s).\n¿Eliminar todo junto con artículos e inventario?"
                confirmacion = wx.MessageBox(mensaje, "Confirmar eliminación", wx.YES_NO | wx.ICON_WARNING)
                if confirmacion != wx.YES:
                    return

                # Eliminar artículos relacionados
                cursor.execute("""
                    DELETE inventario FROM inventario
                    INNER JOIN articulo ON inventario.codigo_barras = articulo.codigo_barras
                    WHERE articulo.idcategoria = %s
                """, (id_categoria,))
                cursor.execute("DELETE FROM articulo WHERE idcategoria = %s", (id_categoria,))

            # Eliminar categoría
            cursor.execute("DELETE FROM categoria WHERE idcategoria = %s", (id_categoria,))
            conn.commit()
            self.mensaje("Éxito", "Categoría eliminada correctamente.")

        except Exception as e:
            conn.rollback()
            self.mensaje("Error", f"Error al eliminar categoría: {e}")
        finally:
            cursor.close()
            conn.close()