# empleados.py
import wx
from conexion import conectar

class EmpleadoCRUD(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title='Catálogo de Empleados', size=(600, 470))
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
            self.txt_idempleado.GetValue(),
            self.txt_nombre.GetValue(),
            self.txt_apellidos.GetValue(),
        ])

    def crear_interfaz(self):
        """Construye la interfaz gráfica."""
        lbl_titulo = wx.StaticText(self.panel, label="CATÁLOGO DE EMPLEADOS", pos=(220, 10))
        lbl_titulo.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        tamano_texto = (200, -1)

        # Campos de entrada
        wx.StaticText(self.panel, label="ID Empleado:", pos=(50, 50))
        self.txt_idempleado = wx.TextCtrl(self.panel, pos=(200, 50), size=tamano_texto)
        self.txt_idempleado.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Nombre:", pos=(50, 90))
        self.txt_nombre = wx.TextCtrl(self.panel, pos=(200, 90), size=tamano_texto)
        self.txt_nombre.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Apellidos:", pos=(50, 130))
        self.txt_apellidos = wx.TextCtrl(self.panel, pos=(200, 130), size=tamano_texto)
        self.txt_apellidos.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Teléfono:", pos=(50, 170))
        self.txt_telefono = wx.TextCtrl(self.panel, pos=(200, 170), size=tamano_texto)
        self.txt_telefono.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Correo Electrónico:", pos=(50, 210))
        self.txt_correo = wx.TextCtrl(self.panel, pos=(200, 210), size=tamano_texto)
        self.txt_correo.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Contraseña:", pos=(50, 250))
        self.txt_contrasena = wx.TextCtrl(self.panel, pos=(200, 250), size=tamano_texto, style=wx.TE_PASSWORD)
        self.txt_contrasena.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Confirmar Contraseña:", pos=(50, 290))
        self.txt_conf_contrasena = wx.TextCtrl(self.panel, pos=(200, 290), size=tamano_texto, style=wx.TE_PASSWORD)
        self.txt_conf_contrasena.SetBackgroundColour(wx.Colour(255, 255, 230))

        # Botones
        self.btn_crear = wx.Button(self.panel, label=" Crear ", pos=(50, 350), size=(120, 40))
        self.btn_buscar = wx.Button(self.panel, label=" Buscar ", pos=(180, 350), size=(120, 40))
        self.btn_actualizar = wx.Button(self.panel, label=" Actualizar ", pos=(310, 350), size=(120, 40))
        self.btn_eliminar = wx.Button(self.panel, label=" Eliminar ", pos=(440, 350), size=(120, 40))

        # Eventos
        self.btn_crear.Bind(wx.EVT_BUTTON, self.on_crear)
        self.btn_buscar.Bind(wx.EVT_BUTTON, self.on_buscar)
        self.btn_actualizar.Bind(wx.EVT_BUTTON, self.on_actualizar)
        self.btn_eliminar.Bind(wx.EVT_BUTTON, self.on_eliminar)

    def on_crear(self, event):
        campos = [
            self.txt_idempleado.GetValue(),
            self.txt_nombre.GetValue(),
            self.txt_apellidos.GetValue(),
            self.txt_telefono.GetValue(),
            self.txt_correo.GetValue(),
            self.txt_contrasena.GetValue(),
            self.txt_conf_contrasena.GetValue(),
        ]
        error = self.validar_campos_completos(campos)
        if error:
            self.mensaje("Advertencia", error)
        else:
            self.agregar_empleado(*campos[:-1])  # Sin confirmación de contraseña

    def on_buscar(self, event):
        idemp = self.txt_idempleado.GetValue()
        if not idemp:
            self.mensaje("Advertencia", "Por favor, ingrese el ID del empleado.")
            return
        empleado = self.buscar_empleado(idemp)
        if empleado:
            self.txt_nombre.SetValue(empleado[1])
            self.txt_apellidos.SetValue(empleado[2])
            self.txt_telefono.SetValue(str(empleado[3]) if empleado[3] else "")
            self.txt_correo.SetValue(str(empleado[4]) if empleado[4] else "")
            self.txt_contrasena.SetValue(empleado[5])
            self.txt_conf_contrasena.SetValue(empleado[5])
        else:
            self.mensaje("Información", "Empleado no encontrado.")

    def on_actualizar(self, event):
        campos = [
            self.txt_idempleado.GetValue(),
            self.txt_nombre.GetValue(),
            self.txt_apellidos.GetValue(),
            self.txt_telefono.GetValue(),
            self.txt_correo.GetValue(),
            self.txt_contrasena.GetValue(),
            self.txt_conf_contrasena.GetValue(),
        ]
        error = self.validar_campos_completos(campos)
        if error:
            self.mensaje("Advertencia", error)
        else:
            self.actualizar_empleado(*campos[:-1])

    def on_eliminar(self, event):
        idemp = self.txt_idempleado.GetValue()
        if not idemp:
            self.mensaje("Advertencia", "Por favor, ingrese el ID del empleado.")
        else:
            self.eliminar_empleado(idemp)
            self.limpiar_campos()

    def validar_campos_completos(self, campos):
        """Valida que los campos obligatorios no estén vacíos."""
        idempleado, nombre, apellidos, telefono, correo, contrasena, conf_contrasena = campos
        if not idempleado.isdigit():
            return "El ID del empleado debe ser un número entero."
        if not nombre or not apellidos:
            return "Nombre y apellidos son obligatorios."
        if telefono and (not telefono.isdigit() or len(telefono) != 10):
            return "El teléfono debe tener 10 dígitos numéricos."
        if correo and '@' not in correo:
            return "Correo electrónico no válido."
        if len(contrasena) < 6:
            return "La contraseña debe tener al menos 6 caracteres."
        if contrasena != conf_contrasena:
            return "Las contraseñas no coinciden."
        return None

    def limpiar_campos(self):
        self.txt_idempleado.Clear()
        self.txt_nombre.Clear()
        self.txt_apellidos.Clear()
        self.txt_telefono.Clear()
        self.txt_correo.Clear()
        self.txt_contrasena.Clear()
        self.txt_conf_contrasena.Clear()

    def agregar_empleado(self, idempleado, nombre, apellidos, telefono, correo, contrasena):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    INSERT INTO empleado (idempleado, nombre, apellidos, telefono, correo_electronico, contraseña)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    int(idempleado),
                    nombre,
                    apellidos,
                    telefono if telefono else None,
                    correo if correo else None,
                    contrasena
                ))
                conn.commit()
                self.mensaje("Éxito", "Empleado creado exitosamente.")
            except Exception as e:
                self.mensaje("Error", f"Error al crear el empleado: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def buscar_empleado(self, idempleado):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("SELECT * FROM empleado WHERE idempleado = %s", (int(idempleado),))
                resultado = cursor.fetchone()
                return resultado
            except Exception as e:
                self.mensaje("Error", f"Error al buscar el empleado: {e}")
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
                """, (
                    nombre,
                    apellidos,
                    telefono if telefono else None,
                    correo if correo else None,
                    contrasena,
                    int(idempleado)
                ))
                conn.commit()
                self.mensaje("Éxito", "Empleado actualizado exitosamente.")
            except Exception as e:
                self.mensaje("Error", f"Error al actualizar el empleado: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def eliminar_empleado(self, idempleado):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("DELETE FROM empleado WHERE idempleado = %s", (int(idempleado),))
                conn.commit()
                self.mensaje("Éxito", "Empleado eliminado exitosamente.")
            except Exception as e:
                self.mensaje("Error", f"Error al eliminar el empleado: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")