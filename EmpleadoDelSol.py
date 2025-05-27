import wx
from conexion import conectar

class EmpleadoCRUD(wx.Frame):
    def __init__(self, parent=None, es_gerente=False, modo_registro=False):
        super().__init__(parent, title='Catálogo de Empleados', size=(1200, 800))
        self.es_gerente = es_gerente
        self.modo_registro = modo_registro
        self.panel = wx.Panel(self)
        self.lista_resultados = None
        self.txt_idempleado = None
        self.txt_nombre = None
        self.txt_apellidos = None
        self.txt_telefono = None
        self.txt_correo = None
        self.txt_contrasena = None
        self.txt_conf_contrasena = None
        self.btn_consultar = None

        # Llama a crear_interfaz después de inicializar atributos
        self.crear_interfaz()
        self.Centre()
        self.Show()

    def mensaje(self, titulo, mensaje):
        """Muestra un mensaje emergente."""
        wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

    def advertencia_salir(self):
        """Pregunta si desea salir si hay datos ingresados."""
        if any([
            self.txt_idempleado.GetValue(),
            self.txt_nombre.GetValue(),
            self.txt_apellidos.GetValue(),
            self.txt_telefono.GetValue(),
            self.txt_correo.GetValue(),
            self.txt_contrasena.GetValue(),
            self.txt_conf_contrasena.GetValue()
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
        idemp = self.txt_idempleado.GetValue().strip()
        nombre = self.txt_nombre.GetValue().strip()
        apellidos = self.txt_apellidos.GetValue().strip()
        telefono = self.txt_telefono.GetValue().strip()
        correo = self.txt_correo.GetValue().strip()
        contrasena = self.txt_contrasena.GetValue().strip()
        conf_contrasena = self.txt_conf_contrasena.GetValue().strip()

        if not idemp.isdigit():
            return "El ID debe ser un número entero."
        if not nombre or not apellidos:
            return "Nombre y apellidos son obligatorios."
        if telefono and (len(telefono) != 10 or not telefono.isdigit()):
            return "Teléfono debe tener 10 dígitos."
        if correo and '@' not in correo:
            return "Correo electrónico no válido."
        if len(contrasena) < 6 and contrasena:
            return "La contraseña debe tener al menos 6 caracteres."
        if contrasena and contrasena != conf_contrasena:
            return "Las contraseñas no coinciden."

        return None

    def crear_interfaz(self):
        sizer_principal = wx.BoxSizer(wx.VERTICAL)

        # Título
        lbl_titulo = wx.StaticText(self.panel, label="CATÁLOGO DE EMPLEADOS", style=wx.ALIGN_CENTER)
        fuente_titulo = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        lbl_titulo.SetFont(fuente_titulo)
        lbl_titulo.SetForegroundColour(wx.Colour(44, 62, 80))  # Azul oscuro
        sizer_principal.Add(lbl_titulo, 0, wx.EXPAND | wx.ALL, 20)

        # Campos de entrada
        grid_sizer = wx.FlexGridSizer(cols=2, vgap=15, hgap=10)
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

        # Campo Correo + botones de autocompletado
        sizer_correo_btns = wx.BoxSizer(wx.HORIZONTAL)
        self.txt_correo = wx.TextCtrl(self.panel, size=(180, -1))
        self.txt_correo.SetBackgroundColour(wx.Colour(255, 255, 230))

        btn_gmail = wx.Button(self.panel, label="gmail.com", size=(90, 25))
        btn_hotmail = wx.Button(self.panel, label="hotmail.com", size=(90, 25))
        btn_outlook = wx.Button(self.panel, label="outlook.com", size=(90, 25))
        for btn in [btn_gmail, btn_hotmail, btn_outlook]:
            btn.SetBackgroundColour(wx.Colour(44, 62, 80))
            btn.SetForegroundColour(wx.WHITE)
            btn.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        sizer_correo_btns.Add(self.txt_correo, flag=wx.EXPAND)
        sizer_correo_btns.Add(btn_gmail, flag=wx.LEFT, border=5)
        sizer_correo_btns.Add(btn_hotmail, flag=wx.LEFT, border=5)
        sizer_correo_btns.Add(btn_outlook, flag=wx.LEFT, border=5)

        grid_sizer.Add(wx.StaticText(self.panel, label="Correo Electrónico:"), flag=wx.ALIGN_CENTER_VERTICAL)
        grid_sizer.Add(sizer_correo_btns, flag=wx.EXPAND)

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

        sizer_principal.Add(grid_sizer, 0, wx.CENTER | wx.ALL, 20)

        # Botón Consultar Contraseña
        sizer_consulta = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_consultar = wx.Button(self.panel, label="Consultar Contraseña", size=(180, 30))
        self.btn_consultar.SetBackgroundColour(wx.Colour(44, 62, 80))
        self.btn_consultar.SetForegroundColour(wx.WHITE)
        self.btn_consultar.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        sizer_consulta.Add(self.btn_consultar)
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

        self.txt_idempleado.Bind(wx.EVT_TEXT, self.busqueda_rapida)
        self.txt_idempleado.Bind(wx.EVT_TEXT_ENTER, self.on_buscar)

        self.lista_resultados.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.rellenar_desde_tabla)

        self.btn_consultar.Bind(wx.EVT_BUTTON, self.consultar_contrasena)

        # Eventos de autocompletado de correo
        btn_gmail.Bind(wx.EVT_BUTTON, lambda e: self.autocompletar_correo("gmail.com"))
        btn_hotmail.Bind(wx.EVT_BUTTON, lambda e: self.autocompletar_correo("hotmail.com"))
        btn_outlook.Bind(wx.EVT_BUTTON, lambda e: self.autocompletar_correo("outlook.com"))

    def autocompletar_correo(self, dominio):
        texto = self.txt_correo.GetValue().strip()
        if "@" in texto:
            partes = texto.split("@")
            if partes[1] not in ['gmail.com', 'hotmail.com', 'outlook.com']:
                self.txt_correo.SetValue(f"{partes[0]}@{dominio}")
        else:
            self.txt_correo.SetValue(f"{texto}@{dominio}")

    def consultar_contrasena(self, event):
        id_empleado = self.txt_idempleado.GetValue().strip()
        if not id_empleado:
            self.mensaje("Error", "Ingrese el ID del empleado.")
            return

        dlg = wx.TextEntryDialog(
            self,
            "Ingrese la clave del gerente:",
            "Autenticación Requerida",
            "",
            style=wx.TE_PASSWORD | wx.OK | wx.CANCEL
        )

        if dlg.ShowModal() == wx.ID_OK:
            clave = dlg.GetValue()
            if clave != "1234":
                self.mensaje("Acceso Denegado", "Clave incorrecta.")
                dlg.Destroy()
                return
            conn, cursor = conectar()
            if conn and cursor:
                try:
                    cursor.execute("SELECT contraseña FROM empleado WHERE idempleado = %s", (int(id_empleado),))
                    resultado = cursor.fetchone()
                    if resultado:
                        self.mensaje("Contraseña", f"La contraseña del empleado '{id_empleado}' es:\n\n{resultado[0]}")
                    else:
                        self.mensaje("No encontrado", "Empleado no encontrado.")
                except Exception as e:
                    self.mensaje("Error", f"No se pudo recuperar la contraseña: {e}")
                finally:
                    cursor.close()
                    conn.close()
            else:
                self.mensaje("Error", "No se pudo conectar a la base de datos.")
        else:
            self.mensaje("Cancelado", "Operación cancelada por el usuario.")

        dlg.Destroy()

    def on_crear(self, event):
        error = self.validar_campos()
        if error:
            self.mensaje("Advertencia", error)
            return

        if not self.es_gerente:
            self.mensaje("Acceso denegado", "Solo el gerente puede registrar nuevos empleados.")
            return

        try:
            idempleado = int(self.txt_idempleado.GetValue())
        except ValueError:
            self.mensaje("Error", "El ID debe ser un número entero.")
            return

        self.agregar_empleado(
            idempleado,
            self.txt_nombre.GetValue(),
            self.txt_apellidos.GetValue(),
            self.txt_telefono.GetValue(),
            self.txt_correo.GetValue(),
            self.txt_contrasena.GetValue()
        )

    def on_buscar(self, event):
        idempleado = self.txt_idempleado.GetValue().strip()
        if not idempleado:
            self.mensaje("Advertencia", "Ingrese un ID de empleado.")
            return

        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    SELECT * FROM empleado WHERE idempleado = %s
                """, (int(idempleado),))
                resultado = cursor.fetchone()
                if resultado:
                    self.lista_resultados.DeleteAllItems()
                    idx = self.lista_resultados.InsertItem(0, str(resultado[0]))
                    self.lista_resultados.SetItem(idx, 1, resultado[1])
                    self.lista_resultados.SetItem(idx, 2, resultado[2])
                    self.lista_resultados.SetItem(idx, 3, str(resultado[3]) if resultado[3] else "")
                    self.lista_resultados.SetItem(idx, 4, str(resultado[4]) if resultado[4] else "")

                    # Rellenar campos
                    self.txt_nombre.SetValue(resultado[1])
                    self.txt_apellidos.SetValue(resultado[2])
                    self.txt_telefono.SetValue(str(resultado[3]) if resultado[3] else "")
                    self.txt_correo.SetValue(str(resultado[4]) if resultado[4] else "")
                    self.txt_contrasena.SetValue(resultado[5])
                    self.txt_conf_contrasena.SetValue(resultado[5])
                    if self.modo_registro:
                        self.txt_conf_contrasena.SetValue(resultado[5])
                else:
                    self.lista_resultados.DeleteAllItems()
                    self.mensaje("Información", "Empleado no encontrado.")
            except Exception as e:
                self.mensaje("Error", f"No se pudo buscar el empleado: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def busqueda_rapida(self, event):
        valor = self.txt_idempleado.GetValue().strip()
        if not valor:
            self.lista_resultados.DeleteAllItems()
            return

        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    SELECT idempleado, nombre, apellidos, telefono, correo_electronico 
                    FROM empleado 
                    WHERE idempleado LIKE %s OR nombre LIKE %s OR apellidos LIKE %s
                    LIMIT 10
                """, (f"%{valor}%", f"%{valor}%", f"%{valor}%"))
                resultados = cursor.fetchall()
                self.lista_resultados.DeleteAllItems()
                for row in resultados:
                    idx = self.lista_resultados.InsertItem(self.lista_resultados.GetItemCount(), str(row[0]))
                    self.lista_resultados.SetItem(idx, 1, row[1])
                    self.lista_resultados.SetItem(idx, 2, row[2])
                    self.lista_resultados.SetItem(idx, 3, str(row[3]) if row[3] else "")
                    self.lista_resultados.SetItem(idx, 4, str(row[4]) if row[4] else "")
            except Exception as e:
                self.mensaje("Error", f"Error al buscar empleado: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def rellenar_desde_tabla(self, event):
        index = self.lista_resultados.GetFirstSelected()
        if index >= 0:
            confirmacion = wx.MessageBox(
                "¿Desea rellenar los campos con este empleado?",
                "Confirmar",
                wx.YES_NO | wx.ICON_QUESTION
            )
            if confirmacion == wx.YES:
                idemp = self.lista_resultados.GetItem(index, 0).GetText()
                resultado = self.buscar_empleado(int(idemp))
                if resultado:
                    self.txt_idempleado.SetValue(str(resultado[0]))
                    self.txt_nombre.SetValue(resultado[1])
                    self.txt_apellidos.SetValue(resultado[2])
                    self.txt_telefono.SetValue(str(resultado[3]) if resultado[3] else "")
                    self.txt_correo.SetValue(str(resultado[4]) if resultado[4] else "")
                    self.txt_contrasena.SetValue(resultado[5])
                    self.txt_conf_contrasena.SetValue(resultado[5])

    def on_actualizar(self, event):
        error = self.validar_campos()
        if error:
            self.mensaje("Advertencia", error)
        else:
            self.actualizar_empleado(
                int(self.txt_idempleado.GetValue()),
                self.txt_nombre.GetValue(),
                self.txt_apellidos.GetValue(),
                self.txt_telefono.GetValue(),
                self.txt_correo.GetValue(),
                self.txt_contrasena.GetValue()
            )

    def on_eliminar(self, event):
        idempleado = self.txt_idempleado.GetValue().strip()
        if not idempleado:
            self.mensaje("Advertencia", "Ingrese un ID válido.")
            return

        confirmacion = wx.MessageBox(
            f"¿Está seguro de eliminar al empleado '{idempleado}'?",
            "Confirmar eliminación",
            wx.YES_NO | wx.ICON_WARNING
        )
        if confirmacion == wx.YES:
            self.eliminar_empleado(int(idempleado))
            self.limpiar_campos(None)

    def limpiar_campos(self, event):
        self.txt_idempleado.Clear()
        self.txt_nombre.Clear()
        self.txt_apellidos.Clear()
        self.txt_telefono.Clear()
        self.txt_correo.Clear()
        self.txt_contrasena.Clear()
        self.txt_conf_contrasena.Clear()
        self.lista_resultados.DeleteAllItems()

    def on_regresar(self, event):
        if self.advertencia_salir():
            self.Close()

    def agregar_empleado(self, idempleado, nombre, apellidos, telefono, correo, contrasena):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    INSERT INTO empleado (idempleado, nombre, apellidos, telefono, correo_electronico, contraseña)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    idempleado,
                    nombre,
                    apellidos,
                    telefono if telefono else None,
                    correo if correo else None,
                    contrasena
                ))
                conn.commit()
                self.mensaje("Éxito", "Empleado creado exitosamente.")
            except Exception as e:
                self.mensaje("Error", f"Error al crear empleado: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def buscar_empleado(self, idempleado):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("SELECT * FROM empleado WHERE idempleado = %s", (idempleado,))
                return cursor.fetchone()
            except Exception as e:
                self.mensaje("Error", f"Error al buscar empleado: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")
        return None

    def actualizar_empleado(self, idempleado, nombre, apellidos, telefono, correo, contrasena):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    UPDATE empleado SET
                        nombre = %s,
                        apellidos = %s,
                        telefono = %s,
                        correo_electronico = %s,
                        contraseña = %s
                    WHERE idempleado = %s
                """, (nombre, apellidos, telefono, correo, contrasena, idempleado))
                conn.commit()
                self.mensaje("Éxito", "Empleado actualizado exitosamente.")
            except Exception as e:
                self.mensaje("Error", f"Error al actualizar empleado: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def eliminar_empleado(self, idempleado):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("DELETE FROM empleado WHERE idempleado = %s", (idempleado,))
                conn.commit()
                self.mensaje("Éxito", "Empleado eliminado correctamente.")
            except Exception as e:
                self.mensaje("Error", f"Error al eliminar empleado: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")