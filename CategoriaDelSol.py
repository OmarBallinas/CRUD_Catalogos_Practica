# categorias.py
import wx
from conexion import conectar

class CategoriaCRUD(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title='Catálogo de Categorías', size=(600, 250))
        self.panel = wx.Panel(self)
        self.crear_interfaz()
        self.Centre()
        self.Show()

    def mensaje(self, titulo, mensaje):
        """Muestra un mensaje emergente."""
        wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

    def validar_campos(self):
        """Verifica que los campos obligatorios no estén vacíos."""
        return all([
            self.txt_id_categoria.GetValue(),
            self.txt_nombre.GetValue()
        ])

    def crear_interfaz(self):
        """Construye la interfaz gráfica."""
        lbl_titulo = wx.StaticText(self.panel, label="CATÁLOGO DE CATEGORÍAS", pos=(220, 10))
        lbl_titulo.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        tamano_texto = (200, -1)

        # Campos de entrada
        wx.StaticText(self.panel, label="ID Categoría:", pos=(50, 50))
        self.txt_id_categoria = wx.TextCtrl(self.panel, pos=(200, 50), size=tamano_texto)
        self.txt_id_categoria.SetBackgroundColour(wx.Colour(255, 255, 230))

        wx.StaticText(self.panel, label="Nombre:", pos=(50, 100))
        self.txt_nombre = wx.TextCtrl(self.panel, pos=(200, 100), size=tamano_texto)
        self.txt_nombre.SetBackgroundColour(wx.Colour(255, 255, 230))

        # Botones
        self.btn_crear = wx.Button(self.panel, label=" Crear ", pos=(50, 150), size=(120, 40))
        self.btn_buscar = wx.Button(self.panel, label=" Buscar ", pos=(180, 150), size=(120, 40))
        self.btn_actualizar = wx.Button(self.panel, label=" Actualizar ", pos=(310, 150), size=(120, 40))
        self.btn_eliminar = wx.Button(self.panel, label=" Eliminar ", pos=(440, 150), size=(120, 40))

        # Eventos
        self.btn_crear.Bind(wx.EVT_BUTTON, self.on_crear)
        self.btn_buscar.Bind(wx.EVT_BUTTON, self.on_buscar)
        self.btn_actualizar.Bind(wx.EVT_BUTTON, self.on_actualizar)
        self.btn_eliminar.Bind(wx.EVT_BUTTON, self.on_eliminar)

    def on_crear(self, event):
        if self.validar_campos():
            self.crear_categoria(
                self.txt_id_categoria.GetValue(),
                self.txt_nombre.GetValue()
            )
        else:
            self.mensaje("Advertencia", "Por favor, complete todos los campos.")

    def on_buscar(self, event):
        id_categoria = self.txt_id_categoria.GetValue()
        if id_categoria:
            resultado = self.buscar_categoria(id_categoria)
            if resultado:
                self.txt_nombre.SetValue(resultado[1])
            else:
                self.mensaje("Información", "Categoría no encontrada.")
        else:
            self.mensaje("Advertencia", "Por favor, ingrese un ID de categoría.")

    def on_actualizar(self, event):
        if self.validar_campos():
            self.actualizar_categoria(
                self.txt_id_categoria.GetValue(),
                self.txt_nombre.GetValue()
            )
        else:
            self.mensaje("Advertencia", "Por favor, complete todos los campos.")

    def on_eliminar(self, event):
        id_categoria = self.txt_id_categoria.GetValue()
        if id_categoria:
            self.eliminar_categoria(id_categoria)
            self.limpiar_campos()
        else:
            self.mensaje("Advertencia", "Por favor, ingrese un ID de categoría.")

    def limpiar_campos(self):
        self.txt_id_categoria.Clear()
        self.txt_nombre.Clear()

    def crear_categoria(self, id_categoria, nombre):
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("INSERT INTO categoria (idcategoria, nombre) VALUES (%s, %s)",
                               (id_categoria, nombre))
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
                cursor.execute("SELECT idcategoria, nombre FROM categoria WHERE idcategoria = %s",
                               (id_categoria,))
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
                cursor.execute("UPDATE categoria SET nombre = %s WHERE idcategoria = %s",
                               (nombre, id_categoria))
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
                mensaje = f"La categoría tiene {cantidad} artículo(s) asociado(s).\n¿Deseas eliminar todo junto con los artículos e inventario?"
                confirmacion = wx.MessageBox(mensaje, "Confirmar eliminación", wx.YES_NO | wx.ICON_WARNING)
                if confirmacion == wx.NO:
                    self.mensaje("Cancelado", "Operación cancelada por el usuario.")
                    return

                # Eliminar relaciones en cascada
                cursor.execute("""
                    DELETE inventario FROM inventario
                    INNER JOIN articulo ON inventario.codigo_barras = articulo.codigo_barras
                    WHERE articulo.idcategoria = %s
                """, (id_categoria,))
                cursor.execute("DELETE FROM articulo WHERE idcategoria = %s", (id_categoria,))

            cursor.execute("DELETE FROM categoria WHERE idcategoria = %s", (id_categoria,))
            conn.commit()
            self.mensaje("Éxito", "Categoría y artículos relacionados eliminados correctamente.")

        except Exception as e:
            conn.rollback()
            self.mensaje("Error", f"Error al eliminar categoría: {e}")
        finally:
            cursor.close()
            conn.close()