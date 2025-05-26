# articulo_crud.py
import wx
from conexion import conectar

class ArticuloCRUD(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title='Catálogo de Artículos', size=(600, 450))
        self.panel = wx.Panel(self)
        self.crear_interfaz()
        self.Centre()
        self.Show()

    def mensaje(self, titulo, mensaje):
        """Muestra un mensaje emergente."""
        wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

    def validar_campos(self):
        """Valida que todos los campos obligatorios tengan datos."""
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
        # Título
        lbl_titulo = wx.StaticText(self.panel, label="CATÁLOGO DE ARTÍCULOS", pos=(220, 10))
        lbl_titulo.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        tamano_texto = (200, -1)

        # Campos de entrada
        wx.StaticText(self.panel, label="Código de Barras:", pos=(50, 50))
        self.txt_codigo = wx.TextCtrl(self.panel, pos=(200, 50), size=tamano_texto)
        self.txt_codigo.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Nombre:", pos=(50, 90))
        self.txt_nombre = wx.TextCtrl(self.panel, pos=(200, 90), size=tamano_texto)
        self.txt_nombre.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Descripción:", pos=(50, 130))
        self.txt_descripcion = wx.TextCtrl(self.panel, pos=(200, 130), size=(200, 60), style=wx.TE_MULTILINE)
        self.txt_descripcion.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Precio:", pos=(50, 200))
        self.txt_precio = wx.TextCtrl(self.panel, pos=(200, 200), size=tamano_texto)
        self.txt_precio.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Unidad:", pos=(50, 240))
        self.txt_unidad = wx.TextCtrl(self.panel, pos=(200, 240), size=tamano_texto)
        self.txt_unidad.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Descuento:", pos=(50, 280))
        self.txt_descuento = wx.TextCtrl(self.panel, pos=(200, 280), size=tamano_texto)
        self.txt_descuento.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="ID Categoría:", pos=(50, 320))
        self.txt_id_categoria = wx.TextCtrl(self.panel, pos=(200, 320), size=tamano_texto)
        self.txt_id_categoria.SetBackgroundColour(wx.Colour(255, 255, 230))

        # Botones
        self.btn_crear = wx.Button(self.panel, label=" Crear ", pos=(50, 360), size=(120, 40))
        self.btn_buscar = wx.Button(self.panel, label=" Buscar ", pos=(180, 360), size=(120, 40))
        self.btn_actualizar = wx.Button(self.panel, label=" Actualizar ", pos=(310, 360), size=(120, 40))
        self.btn_eliminar = wx.Button(self.panel, label=" Eliminar ", pos=(440, 360), size=(120, 40))

        # Eventos
        self.btn_crear.Bind(wx.EVT_BUTTON, self.on_crear)
        self.btn_buscar.Bind(wx.EVT_BUTTON, self.on_buscar)
        self.btn_actualizar.Bind(wx.EVT_BUTTON, self.on_actualizar)
        self.btn_eliminar.Bind(wx.EVT_BUTTON, self.on_eliminar)

    def on_crear(self, event):
        if self.validar_campos():
            self.agregar_articulo(
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

    def on_buscar(self, event):
        codigo = self.txt_codigo.GetValue()
        if codigo:
            resultado = self.buscar_articulo(codigo)
            if resultado:
                self.txt_nombre.SetValue(resultado[1])
                self.txt_descripcion.SetValue(resultado[2])
                self.txt_precio.SetValue(str(resultado[3]))
                self.txt_unidad.SetValue(resultado[4])
                self.txt_descuento.SetValue(str(resultado[5]))
                self.txt_id_categoria.SetValue(str(resultado[6]))
        else:
            self.mensaje("Advertencia", "Por favor, ingrese el código de barras.")

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
        if codigo:
            self.eliminar_articulo(codigo)
            self.limpiar_campos()
        else:
            self.mensaje("Advertencia", "Por favor, ingrese el código de barras.")

    def limpiar_campos(self):
        self.txt_codigo.Clear()
        self.txt_nombre.Clear()
        self.txt_descripcion.Clear()
        self.txt_precio.Clear()
        self.txt_unidad.Clear()
        self.txt_descuento.Clear()
        self.txt_id_categoria.Clear()

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
                resultado = cursor.fetchone()
                return resultado
            except Exception as e:
                self.mensaje("Error", f"Error al buscar el artículo: {e}")
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
                    SET nombre = %s, descripcion = %s, precio = %s, unidad = %s, descuento = %s, idcategoria = %s
                    WHERE codigo_barras = %s
                """, (nombre, descripcion, float(precio), unidad, float(descuento), int(id_categoria), codigo))
                conn.commit()
                self.mensaje("Éxito", "Artículo actualizado exitosamente.")
            except Exception as e:
                self.mensaje("Error", f"Error al actualizar el artículo: {e}")
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

            confirmacion = wx.MessageBox(f"¿Deseas eliminar el artículo '{nombre_articulo}' y todos sus registros relacionados (inventario)?",
                                         "Confirmar eliminación", wx.YES_NO | wx.ICON_WARNING)
            if confirmacion != wx.YES:
                self.mensaje("Cancelado", "Operación cancelada por el usuario.")
                return

            cursor.execute("DELETE FROM inventario WHERE codigo_barras = %s", (codigo,))
            cursor.execute("DELETE FROM articulo WHERE codigo_barras = %s", (codigo,))
            conn.commit()
            self.mensaje("Éxito", f"Artículo '{nombre_articulo}' eliminado correctamente.")
        except Exception as e:
            conn.rollback()
            self.mensaje("Error", f"Error al eliminar el artículo: {e}")
        finally:
            cursor.close()
            conn.close()