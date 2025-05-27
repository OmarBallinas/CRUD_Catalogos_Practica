import wx
from conexion import conectar

class ClienteCRUD(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title='Catálogo de Clientes', size=(1200, 800))
        self.panel = wx.Panel(self)
        self.lista_resultados = None  # Inicialización para evitar errores
        self.txt_telefono = None     # Si no usamos Sizer, puede fallar
        self.crear_interfaz()
        self.Centre()
        self.Show()

    def mensaje(self, titulo, mensaje):
        """Muestra un mensaje emergente."""
        wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

    def advertencia_salir(self):
        """Pregunta si desea salir si hay datos ingresados."""
        if any([
            self.txt_telefono.GetValue(),
            self.txt_nombre.GetValue(),
            self.txt_apellido.GetValue(),
            self.txt_correo.GetValue()
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
            self.txt_telefono.GetValue(),
            self.txt_nombre.GetValue(),
            self.txt_apellido.GetValue(),
            self.txt_correo.GetValue()
        ])

    def crear_interfaz(self):
        sizer_principal = wx.BoxSizer(wx.VERTICAL)

        # Título
        lbl_titulo = wx.StaticText(self.panel, label="CATÁLOGO DE CLIENTES", style=wx.ALIGN_CENTER)
        fuente_titulo = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        lbl_titulo.SetFont(fuente_titulo)
        lbl_titulo.SetForegroundColour(wx.Colour(44, 62, 80))  # Azul oscuro
        sizer_principal.Add(lbl_titulo, 0, wx.EXPAND | wx.ALL, 20)

        # Campos de entrada
        grid_sizer = wx.FlexGridSizer(rows=4, cols=2, vgap=15, hgap=10)
        grid_sizer.AddGrowableCol(1)

        # Campo Teléfono
        grid_sizer.Add(wx.StaticText(self.panel, label="Teléfono:"), flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_telefono = wx.TextCtrl(self.panel, size=(300, -1), style=wx.TE_PROCESS_ENTER)
        self.txt_telefono.SetBackgroundColour(wx.Colour(255, 255, 230))
        grid_sizer.Add(self.txt_telefono, flag=wx.EXPAND)

        # Campo Nombre
        grid_sizer.Add(wx.StaticText(self.panel, label="Nombre:"), flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_nombre = wx.TextCtrl(self.panel, size=(300, -1))
        self.txt_nombre.SetBackgroundColour(wx.Colour(255, 255, 230))
        grid_sizer.Add(self.txt_nombre, flag=wx.EXPAND)

        # Campo Apellido
        grid_sizer.Add(wx.StaticText(self.panel, label="Apellido:"), flag=wx.ALIGN_CENTER_VERTICAL)
        self.txt_apellido = wx.TextCtrl(self.panel, size=(300, -1))
        self.txt_apellido.SetBackgroundColour(wx.Colour(255, 255, 230))
        grid_sizer.Add(self.txt_apellido, flag=wx.EXPAND)

        # Campo Correo + botones de autocompletado
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
        columnas = ["Teléfono", "Nombre", "Apellido", "Correo"]
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

        # Autobusqueda dinámica
        self.txt_telefono.Bind(wx.EVT_TEXT, self.busqueda_rapida)
        self.txt_telefono.Bind(wx.EVT_TEXT_ENTER, self.on_buscar)

        # Doble clic en tabla para rellenar campos
        self.lista_resultados.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.rellenar_desde_tabla)

        # Eventos de autocompletado de correo
        btn_gmail.Bind(wx.EVT_BUTTON, lambda e: self.autocompletar_correo("gmail.com"))
        btn_hotmail.Bind(wx.EVT_BUTTON, lambda e: self.autocompletar_correo("hotmail.com"))
        btn_outlook.Bind(wx.EVT_BUTTON, lambda e: self.autocompletar_correo("outlook.com"))

    def on_crear(self, event):
        if self.validar_campos():
            telefono = self.txt_telefono.GetValue().strip()
            nombre = self.txt_nombre.GetValue().strip()
            apellido = self.txt_apellido.GetValue().strip()
            correo = self.txt_correo.GetValue().strip()
            if len(telefono) != 10 or not telefono.isdigit():
                self.mensaje("Error", "El teléfono debe tener 10 dígitos.")
                return
            if '@' not in correo:
                self.mensaje("Error", "Ingrese un correo electrónico válido.")
                return
            self.crear_cliente(telefono, nombre, apellido, correo)
        else:
            self.mensaje("Advertencia", "Por favor, complete todos los campos.")

    def on_buscar(self, event):
            telefono = self.txt_telefono.GetValue().strip()
            if not telefono:
                self.mensaje("Advertencia", "Ingrese un teléfono de cliente.")
                return

            conn, cursor = conectar()
            if conn and cursor:
                try:
                    cursor.execute("SELECT * FROM cliente WHERE telefono_cliente = %s", (telefono,))
                    resultado = cursor.fetchone()

                    if resultado:
                        self.lista_resultados.DeleteAllItems()
                        idx = self.lista_resultados.InsertItem(self.lista_resultados.GetItemCount(), resultado[0])
                        self.lista_resultados.SetItem(idx, 1, resultado[1])
                        self.lista_resultados.SetItem(idx, 2, resultado[2])
                        self.lista_resultados.SetItem(idx, 3, resultado[3] if resultado[3] else "")

                        # Autocompletar campos
                        self.txt_nombre.SetValue(resultado[1])
                        self.txt_apellido.SetValue(resultado[2])
                        self.txt_correo.SetValue(resultado[3] if resultado[3] else "")
                    else:
                        self.lista_resultados.DeleteAllItems()
                        self.mensaje("Información", "Cliente no encontrado.")
                except Exception as e:
                    self.mensaje("Error", f"Error al buscar cliente: {e}")
                finally:
                    cursor.close()
                    conn.close()
            else:
                self.mensaje("Error", "No se pudo conectar a la base de datos.")

def crear_interfaz(self):
    sizer_principal = wx.BoxSizer(wx.VERTICAL)

    # Título
    lbl_titulo = wx.StaticText(self.panel, label="CATÁLOGO DE EMPLEADOS", style=wx.ALIGN_CENTER)
    fuente_titulo = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
    lbl_titulo.SetFont(fuente_titulo)
    lbl_titulo.SetForegroundColour(wx.Colour(44, 62, 80))  # Azul oscuro
    sizer_principal.Add(lbl_titulo, 0, wx.EXPAND | wx.ALL, 20)

    # Campos de entrada (usamos FlexGridSizer para 6 filas x 2 columnas)
    grid_sizer = wx.FlexGridSizer(rows=6, cols=2, vgap=15, hgap=10)
    grid_sizer.AddGrowableCol(1)

    # Campo ID Empleado
    grid_sizer.Add(wx.StaticText(self.panel, label="ID Empleado:"), flag=wx.ALIGN_CENTER_VERTICAL)
    self.txt_idempleado = wx.TextCtrl(self.panel, size=(300, -1), style=wx.TE_PROCESS_ENTER)
    self.txt_idempleado.SetBackgroundColour(wx.Colour(255, 255, 230))
    grid_sizer.Add(self.txt_idempleado, flag=wx.EXPAND)

    # Campo Nombre
    grid_sizer.Add(wx.StaticText(self.panel, label="Nombre:"), flag=wx.ALIGN_CENTER_VERTICAL)
    self.txt_nombre = wx.TextCtrl(self.panel, size=(300, -1))
    self.txt_nombre.SetBackgroundColour(wx.Colour(255, 255, 230))
    grid_sizer.Add(self.txt_nombre, flag=wx.EXPAND)

    # Campo Apellidos
    grid_sizer.Add(wx.StaticText(self.panel, label="Apellidos:"), flag=wx.ALIGN_CENTER_VERTICAL)
    self.txt_apellidos = wx.TextCtrl(self.panel, size=(300, -1))
    self.txt_apellidos.SetBackgroundColour(wx.Colour(255, 255, 230))
    grid_sizer.Add(self.txt_apellidos, flag=wx.EXPAND)

    # Campo Teléfono
    grid_sizer.Add(wx.StaticText(self.panel, label="Teléfono:"), flag=wx.ALIGN_CENTER_VERTICAL)
    self.txt_telefono = wx.TextCtrl(self.panel, size=(300, -1))
    self.txt_telefono.SetBackgroundColour(wx.Colour(255, 255, 230))
    grid_sizer.Add(self.txt_telefono, flag=wx.EXPAND)

    # Campo Correo
    grid_sizer.Add(wx.StaticText(self.panel, label="Correo Electrónico:"), flag=wx.ALIGN_CENTER_VERTICAL)
    self.txt_correo = wx.TextCtrl(self.panel, size=(180, -1))
    self.txt_correo.SetBackgroundColour(wx.Colour(255, 255, 230))
    grid_sizer.Add(self.txt_correo, flag=wx.EXPAND)

    # Botones de sugerencia de correo
    sizer_correo_btns = wx.BoxSizer(wx.HORIZONTAL)
    btn_gmail = wx.Button(self.panel, label="gmail.com", size=(90, 25))
    btn_hotmail = wx.Button(self.panel, label="hotmail.com", size=(90, 25))
    btn_outlook = wx.Button(self.panel, label="outlook.com", size=(90, 25))

    for btn in [btn_gmail, btn_hotmail, btn_outlook]:
        btn.SetBackgroundColour(wx.Colour(44, 62, 80))
        btn.SetForegroundColour(wx.WHITE)
        btn.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

    sizer_correo_btns.Add(btn_gmail)
    sizer_correo_btns.Add(btn_hotmail, flag=wx.LEFT, border=5)
    sizer_correo_btns.Add(btn_outlook, flag=wx.LEFT, border=5)

    grid_sizer.Add(wx.StaticText(self.panel, label=""), flag=wx.EXPAND)
    grid_sizer.Add(sizer_correo_btns)

    # Campo Contraseña
    grid_sizer.Add(wx.StaticText(self.panel, label="Contraseña:"), flag=wx.ALIGN_CENTER_VERTICAL)
    self.txt_contrasena = wx.TextCtrl(self.panel, size=(300, -1), style=wx.TE_PASSWORD)
    self.txt_contrasena.SetBackgroundColour(wx.Colour(255, 255, 230))
    grid_sizer.Add(self.txt_contrasena, flag=wx.EXPAND)

    # Campo Confirmar Contraseña
    grid_sizer.Add(wx.StaticText(self.panel, label="Confirmar Contraseña:"), flag=wx.ALIGN_CENTER_VERTICAL)
    self.txt_conf_contrasena = wx.TextCtrl(self.panel, size=(300, -1), style=wx.TE_PASSWORD)
    self.txt_conf_contrasena.SetBackgroundColour(wx.Colour(255, 255, 230))
    grid_sizer.Add(self.txt_conf_contrasena, flag=wx.EXPAND)

    # Añadir el grid al principal
    sizer_principal.Add(grid_sizer, 0, wx.CENTER | wx.ALL, 20)

    # Botón Consultar Contraseña (fuera del grid)
    sizer_consulta = wx.BoxSizer(wx.HORIZONTAL)
    self.btn_consultar = wx.Button(self.panel, label="Consultar Contraseña", size=(150, 30))
    self.btn_consultar.SetBackgroundColour(wx.Colour(44, 62, 80))
    self.btn_consultar.SetForegroundColour(wx.WHITE)
    self.btn_consultar.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
    sizer_consulta.Add(self.btn_consultar, 0, wx.ALIGN_CENTER_HORIZONTAL)
    sizer_principal.Add(sizer_consulta, 0, wx.CENTER | wx.TOP, 10)

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
    columnas = ["ID", "Nombre", "Apellidos", "Teléfono", "Correo"]
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

    # Autobúsqueda dinámica mientras escribe
    self.txt_idempleado.Bind(wx.EVT_TEXT, self.busqueda_rapida)
    self.txt_idempleado.Bind(wx.EVT_TEXT_ENTER, self.on_buscar)

    # Doble clic en tabla
    self.lista_resultados.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.rellenar_desde_tabla)

    # Eventos de autocompletado de correo
    btn_gmail.Bind(wx.EVT_BUTTON, lambda e: self.autocompletar_correo("gmail.com"))
    btn_hotmail.Bind(wx.EVT_BUTTON, lambda e: self.autocompletar_correo("hotmail.com"))
    btn_outlook.Bind(wx.EVT_BUTTON, lambda e: self.autocompletar_correo("outlook.com"))

    # Evento consultar contraseña
    self.btn_consultar.Bind(wx.EVT_BUTTON, self.consultar_contrasena)

    def busqueda_rapida(self, event):
        valor = self.txt_telefono.GetValue().strip()
        if not valor:
            self.lista_resultados.DeleteAllItems()
            return

        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    SELECT * FROM cliente 
                    WHERE telefono_cliente LIKE %s OR nombre LIKE %s OR apellido LIKE %s
                    LIMIT 10
                """, (f"%{valor}%", f"%{valor}%", f"%{valor}%"))
                resultados = cursor.fetchall()
                self.lista_resultados.DeleteAllItems()
                for row in resultados:
                    idx = self.lista_resultados.InsertItem(self.lista_resultados.GetItemCount(), row[0])
                    self.lista_resultados.SetItem(idx, 1, row[1])
                    self.lista_resultados.SetItem(idx, 2, row[2])
                    self.lista_resultados.SetItem(idx, 3, row[3] if row[3] else "")
            except Exception as e:
                self.mensaje("Error", f"No se pudo buscar el cliente: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def rellenar_desde_tabla(self, event):
        index = self.lista_resultados.GetFirstSelected()
        if index >= 0:
            confirmacion = wx.MessageBox(
                "¿Desea rellenar los campos con este cliente?",
                "Confirmar",
                wx.YES_NO | wx.ICON_QUESTION
            )
            if confirmacion == wx.YES:
                telefono = self.lista_resultados.GetItem(index, 0).GetText()
                resultado = self.buscar_cliente(telefono)
                if resultado:
                    self.txt_telefono.SetValue(resultado[0])
                    self.txt_nombre.SetValue(resultado[1])
                    self.txt_apellido.SetValue(resultado[2])
                    self.txt_correo.SetValue(resultado[3] if resultado[3] else "")

    def on_actualizar(self, event):
        if self.validar_campos():
            telefono = self.txt_telefono.GetValue()
            nombre = self.txt_nombre.GetValue()
            apellido = self.txt_apellido.GetValue()
            correo = self.txt_correo.GetValue()
            self.actualizar_cliente(telefono, nombre, apellido, correo)
        else:
            self.mensaje("Advertencia", "Por favor, complete todos los campos.")

    def on_eliminar(self, event):
        telefono = self.txt_telefono.GetValue()
        if not telefono:
            self.mensaje("Advertencia", "Ingrese un teléfono.")
            return

        confirmacion = wx.MessageBox(
            f"¿Está seguro de eliminar al cliente '{telefono}'?",
            "Confirmar eliminación",
            wx.YES_NO | wx.ICON_WARNING
        )
        if confirmacion == wx.YES:
            self.eliminar_cliente(telefono)
            self.limpiar_campos(None)

    def limpiar_campos(self, event):
        self.txt_telefono.Clear()
        self.txt_nombre.Clear()
        self.txt_apellido.Clear()
        self.txt_correo.Clear()
        self.lista_resultados.DeleteAllItems()

    def on_regresar(self, event):
        if self.advertencia_salir():
            self.Close()

    def autocompletar_correo(self, dominio):
        texto = self.txt_correo.GetValue().strip()
        if "@" in texto:
            partes = texto.split("@")
            if partes[1] not in ['gmail.com', 'hotmail.com', 'outlook.com']:
                self.txt_correo.SetValue(f"{partes[0]}@{dominio}")
        else:
            self.txt_correo.SetValue(f"{texto}@{dominio}")

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
                cursor.execute("SELECT * FROM cliente WHERE telefono_cliente = %s", (telefono,))
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
        if conn and cursor:
            try:
                cursor.execute("DELETE FROM cliente WHERE telefono_cliente = %s", (telefono,))
                conn.commit()
                self.mensaje("Éxito", "Cliente eliminado correctamente.")
            except Exception as e:
                conn.rollback()
                self.mensaje("Error", f"Error al eliminar cliente: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")