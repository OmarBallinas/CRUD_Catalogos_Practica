import wx
from conexion import conectar

class ProveedorCRUD(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title="Catálogo de Proveedores", size=(1200, 800))
        self.panel = wx.Panel(self)
        self.lista_resultados = None
        self.txt_id = None
        self.txt_nombre = None
        self.txt_contacto = None
        self.txt_telefono = None
        self.txt_correo = None
        self.txt_direccion = None
        self.crear_interfaz()
        self.Centre()
        self.Show()

    def mensaje(self, titulo, mensaje):
        """Muestra un mensaje emergente."""
        wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

    def advertencia_salir(self):
        """Pregunta si desea salir si hay datos ingresados."""
        if any([
            self.txt_id.GetValue(),
            self.txt_nombre.GetValue(),
            self.txt_contacto.GetValue(),
            self.txt_telefono.GetValue(),
            self.txt_correo.GetValue(),
            self.txt_direccion.GetValue()
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
            self.txt_id.GetValue(),
            self.txt_nombre.GetValue(),
            self.txt_contacto.GetValue(),
            self.txt_telefono.GetValue()
        ])

    def crear_interfaz(self):
        sizer_principal = wx.BoxSizer(wx.VERTICAL)

        # Título
        lbl_titulo = wx.StaticText(self.panel, label="CATÁLOGO DE PROVEEDORES", style=wx.ALIGN_CENTER)
        fuente_titulo = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        lbl_titulo.SetFont(fuente_titulo)
        lbl_titulo.SetForegroundColour(wx.Colour(44, 62, 80))  # Azul oscuro
        sizer_principal.Add(lbl_titulo, 0, wx.EXPAND | wx.ALL, 20)

        # Campos de entrada
        grid_sizer = wx.FlexGridSizer(rows=6, cols=2, vgap=15, hgap=10)
        grid_sizer.AddGrowableCol(1)

        # ID Proveedor
        grid_sizer.Add(wx.StaticText(self.panel, label="ID Proveedor:"), flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_id = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.txt_id.SetBackgroundColour(wx.Colour(255, 255, 230))
        grid_sizer.Add(self.txt_id, flag=wx.EXPAND)

        # Nombre
        grid_sizer.Add(wx.StaticText(self.panel, label="Nombre:"), flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_nombre = wx.TextCtrl(self.panel)
        self.txt_nombre.SetBackgroundColour(wx.Colour(255, 255, 230))
        grid_sizer.Add(self.txt_nombre, flag=wx.EXPAND)

        # Contacto
        grid_sizer.Add(wx.StaticText(self.panel, label="Contacto:"), flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_contacto = wx.TextCtrl(self.panel)
        self.txt_contacto.SetBackgroundColour(wx.Colour(255, 255, 230))
        grid_sizer.Add(self.txt_contacto, flag=wx.EXPAND)

        # Teléfono
        grid_sizer.Add(wx.StaticText(self.panel, label="Teléfono:"), flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_telefono = wx.TextCtrl(self.panel)
        self.txt_telefono.SetBackgroundColour(wx.Colour(255, 255, 230))
        grid_sizer.Add(self.txt_telefono, flag=wx.EXPAND)

        # Correo + botones autocompletar
        sizer_correo = wx.BoxSizer(wx.HORIZONTAL)
        self.txt_correo = wx.TextCtrl(self.panel, size=(180, -1))
        self.txt_correo.SetBackgroundColour(wx.Colour(255, 255, 230))
        btn_gmail = wx.Button(self.panel, label="gmail.com", size=(90, 25))
        btn_hotmail = wx.Button(self.panel, label="hotmail.com", size=(90, 25))
        btn_outlook = wx.Button(self.panel, label="outlook.com", size=(90, 25))
        for btn in [btn_gmail, btn_hotmail, btn_outlook]:
            btn.SetBackgroundColour(wx.Colour(44, 62, 80))
            btn.SetForegroundColour(wx.WHITE)
            btn.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        sizer_correo.Add(self.txt_correo, flag=wx.EXPAND)
        sizer_correo.Add(btn_gmail, flag=wx.LEFT, border=5)
        sizer_correo.Add(btn_hotmail, flag=wx.LEFT, border=5)
        sizer_correo.Add(btn_outlook, flag=wx.LEFT, border=5)
        grid_sizer.Add(wx.StaticText(self.panel, label="Correo Electrónico:"), flag=wx.ALIGN_CENTER_VERTICAL)
        grid_sizer.Add(sizer_correo, flag=wx.EXPAND)

        # Dirección (multilínea)
        grid_sizer.Add(wx.StaticText(self.panel, label="Dirección:"), flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_direccion = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE, size=(-1, 80))
        self.txt_direccion.SetBackgroundColour(wx.Colour(255, 255, 230))
        grid_sizer.Add(self.txt_direccion, flag=wx.EXPAND)

        sizer_principal.Add(grid_sizer, 0, wx.CENTER | wx.ALL, 20)

        # Botones principales
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
        columnas = ["ID", "Nombre", "Contacto", "Teléfono", "Correo"]
        for i, col in enumerate(columnas):
            self.lista_resultados.InsertColumn(i, col, width=200)
        sizer_principal.Add(self.lista_resultados, 0, wx.EXPAND | wx.ALL, 20)

        self.panel.SetSizer(sizer_principal)

        # Eventos
        self.btn_crear.Bind(wx.EVT_BUTTON, self.on_crear)
        self.btn_buscar.Bind(wx.EVT_BUTTON, self.on_buscar)
        self.btn_actualizar.Bind(wx.EVT_BUTTON, self.on_actualizar)
        self.btn_eliminar.Bind(wx.EVT_BUTTON, self.on_eliminar)
        self.btn_limpiar.Bind(wx.EVT_BUTTON, self.limpiar_campos)
        self.btn_regresar.Bind(wx.EVT_BUTTON, self.on_regresar)
        self.txt_id.Bind(wx.EVT_TEXT, self.busqueda_rapida)
        self.txt_id.Bind(wx.EVT_TEXT_ENTER, self.on_buscar)
        self.lista_resultados.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.rellenar_desde_tabla)

        # Autocompletado de correo
        btn_gmail.Bind(wx.EVT_BUTTON, lambda e: self.autocompletar_correo("gmail.com"))
        btn_hotmail.Bind(wx.EVT_BUTTON, lambda e: self.autocompletar_correo("hotmail.com"))
        btn_outlook.Bind(wx.EVT_BUTTON, lambda e: self.autocompletar_correo("outlook.com"))

    def autocompletar_correo(self, dominio):
        texto = self.txt_correo.GetValue().strip()
        if "@" in texto:
            partes = texto.split("@")
            self.txt_correo.SetValue(f"{partes[0]}@{dominio}")
        else:
            self.txt_correo.SetValue(f"{texto}@{dominio}")

    def on_crear(self, event):
        if not self.validar_campos():
            self.mensaje("Advertencia", "Por favor, complete todos los campos obligatorios.")
            return

        try:
            idproveedor = int(self.txt_id.GetValue())
        except ValueError:
            self.mensaje("Error", "El ID debe ser un número entero.")
            return

        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    INSERT INTO proveedor (idproveedor, nombre, contacto, telefono, correo_electronico, direccion)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    idproveedor,
                    self.txt_nombre.GetValue(),
                    self.txt_contacto.GetValue(),
                    self.txt_telefono.GetValue(),
                    self.txt_correo.GetValue(),
                    self.txt_direccion.GetValue()
                ))
                conn.commit()
                self.mensaje("Éxito", "Proveedor creado correctamente.")
                self.limpiar_campos(None)
                self.busqueda_rapida(None)
            except Exception as e:
                self.mensaje("Error", f"No se pudo crear el proveedor:\n{e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def on_buscar(self, event):
        idproveedor = self.txt_id.GetValue().strip()
        if not idproveedor.isdigit():
            self.mensaje("Advertencia", "Ingrese un ID válido.")
            return

        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("SELECT * FROM proveedor WHERE idproveedor = %s", (int(idproveedor),))
                resultado = cursor.fetchone()
                self.lista_resultados.DeleteAllItems()
                if resultado:
                    idx = self.lista_resultados.InsertItem(0, str(resultado[0]))
                    self.lista_resultados.SetItem(idx, 1, resultado[1])
                    self.lista_resultados.SetItem(idx, 2, resultado[2])
                    self.lista_resultados.SetItem(idx, 3, resultado[3])
                    self.lista_resultados.SetItem(idx, 4, resultado[4] or "")
                    self.txt_nombre.SetValue(str(resultado[1]))
                    self.txt_contacto.SetValue(str(resultado[2]))
                    self.txt_telefono.SetValue(str(resultado[3]))
                    self.txt_correo.SetValue(str(resultado[4] or ""))
                    self.txt_direccion.SetValue(str(resultado[5] or ""))
                else:
                    self.mensaje("Información", "Proveedor no encontrado.")
            except Exception as e:
                self.mensaje("Error", f"No se pudo buscar el proveedor:\n{e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def busqueda_rapida(self, event):
        valor = self.txt_id.GetValue().strip()
        if not valor:
            self.lista_resultados.DeleteAllItems()
            return

        conn, cursor = conectar()
        if conn and cursor:
            try:
                if valor.isdigit():
                    cursor.execute("SELECT * FROM proveedor WHERE idproveedor = %s", (int(valor),))
                else:
                    cursor.execute("SELECT * FROM proveedor WHERE nombre LIKE %s OR contacto LIKE %s LIMIT 10",
                                   (f"%{valor}%", f"%{valor}%"))
                resultados = cursor.fetchall()
                self.lista_resultados.DeleteAllItems()
                for row in resultados:
                    idx = self.lista_resultados.InsertItem(self.lista_resultados.GetItemCount(), str(row[0]))
                    self.lista_resultados.SetItem(idx, 1, row[1])
                    self.lista_resultados.SetItem(idx, 2, row[2])
                    self.lista_resultados.SetItem(idx, 3, row[3])
                    self.lista_resultados.SetItem(idx, 4, row[4] or "")
            except Exception as e:
                self.mensaje("Error", f"No se pudo recuperar el proveedor:\n{e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def rellenar_desde_tabla(self, event):
        index = self.lista_resultados.GetFirstSelected()
        if index >= 0:
            confirmacion = wx.MessageBox(
                "¿Desea rellenar los campos con este proveedor?",
                "Confirmar",
                wx.YES_NO | wx.ICON_QUESTION
            )
            if confirmacion == wx.YES:
                idproveedor = self.lista_resultados.GetItem(index, 0).GetText()
                resultado = self.buscar_proveedor(int(idproveedor))
                if resultado:
                    self.txt_id.SetValue(str(resultado[0]))
                    self.txt_nombre.SetValue(resultado[1])
                    self.txt_contacto.SetValue(resultado[2])
                    self.txt_telefono.SetValue(str(resultado[3]))
                    self.txt_correo.SetValue(str(resultado[4] or ""))
                    self.txt_direccion.SetValue(str(resultado[5] or ""))

    def on_actualizar(self, event):
        if not self.validar_campos():
            self.mensaje("Advertencia", "Por favor, complete todos los campos obligatorios.")
            return

        try:
            idproveedor = int(self.txt_id.GetValue())
        except ValueError:
            self.mensaje("Error", "El ID debe ser un número entero.")
            return

        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    UPDATE proveedor SET 
                        nombre=%s, contacto=%s, telefono=%s, 
                        correo_electronico=%s, direccion=%s 
                    WHERE idproveedor=%s
                """, (
                    self.txt_nombre.GetValue(),
                    self.txt_contacto.GetValue(),
                    self.txt_telefono.GetValue(),
                    self.txt_correo.GetValue(),
                    self.txt_direccion.GetValue(),
                    idproveedor
                ))
                conn.commit()
                if cursor.rowcount == 0:
                    self.mensaje("Error", "Proveedor no encontrado. No se realizó la actualización.")
                else:
                    self.mensaje("Éxito", "Proveedor actualizado correctamente.")
                    self.limpiar_campos(None)
                    self.busqueda_rapida(None)
            except Exception as e:
                conn.rollback()
                self.mensaje("Error", f"No se pudo actualizar el proveedor:\n{e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def on_eliminar(self, event):
        idproveedor = self.txt_id.GetValue().strip()
        if not idproveedor.isdigit():
            self.mensaje("Advertencia", "Ingrese un ID válido.")
            return

        confirmacion = wx.MessageBox(
            f"¿Está seguro de eliminar al proveedor '{idproveedor}'?",
            "Confirmar eliminación",
            wx.YES_NO | wx.ICON_WARNING
        )
        if confirmacion != wx.YES:
            return

        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("DELETE FROM proveedor WHERE idproveedor = %s", (int(idproveedor),))
                conn.commit()
                if cursor.rowcount == 0:
                    self.mensaje("Error", "Proveedor no encontrado.")
                else:
                    self.mensaje("Éxito", "Proveedor eliminado correctamente.")
                    self.limpiar_campos(None)
            except Exception as e:
                conn.rollback()
                self.mensaje("Error", f"No se pudo eliminar el proveedor:\n{e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def limpiar_campos(self, event):
        self.txt_id.Clear()
        self.txt_nombre.Clear()
        self.txt_contacto.Clear()
        self.txt_telefono.Clear()
        self.txt_correo.Clear()
        self.txt_direccion.Clear()
        self.lista_resultados.DeleteAllItems()
        self.txt_id.SetFocus()

    def on_regresar(self, event):
        if self.advertencia_salir():
            self.Close()

    def buscar_proveedor(self, idproveedor):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("SELECT * FROM proveedor WHERE idproveedor = %s", (idproveedor,))
                return cursor.fetchone()
            except Exception as e:
                self.mensaje("Error", f"No se pudo recuperar el proveedor:\n{e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")
        return None