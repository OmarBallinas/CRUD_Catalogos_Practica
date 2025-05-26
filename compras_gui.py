# compras_gui.py
import wx
from conexion import conectar

class CompraGUI(wx.Frame):
    def __init__(self, parent=None, idempleado=None):
        super().__init__(parent, title="Registrar Compra", size=(800, 600))
        self.idempleado = idempleado
        self.panel = wx.Panel(self)
        self.lista_carrito = []
        self.total_general = 0
        self.idempleado = "1"  # Simulando empleado logueado

        self.crear_interfaz()
        self.Centre()
        self.Show()

    def mensaje(self, titulo, mensaje):
        """Muestra un mensaje emergente."""
        wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

    def validar_campos(self):
        return bool(self.txt_proveedor.GetValue())

    def crear_interfaz(self):
        """Construye la interfaz gráfica."""
        lbl_titulo = wx.StaticText(self.panel, label="REGISTRAR COMPRA", pos=(320, 10))
        fuente_titulo = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        lbl_titulo.SetFont(fuente_titulo)

        # Proveedor
        wx.StaticText(self.panel, label="ID Proveedor:", pos=(50, 50))
        self.txt_proveedor = wx.TextCtrl(self.panel, pos=(200, 50), size=(200, -1))

        # Botón buscar proveedor
        self.btn_buscar_prov = wx.Button(self.panel, label="Buscar Proveedor", pos=(410, 45))
        self.btn_buscar_prov.Bind(wx.EVT_BUTTON, self.buscar_proveedor)

        # Código de barras o nombre del artículo
        wx.StaticText(self.panel, label="Código / Nombre:", pos=(50, 90))
        self.txt_codigo = wx.TextCtrl(self.panel, pos=(200, 90), size=(200, -1))
        self.btn_buscar_articulo = wx.Button(self.panel, label="Buscar Artículo", pos=(410, 85))
        self.btn_buscar_articulo.Bind(wx.EVT_BUTTON, self.buscar_articulo)

        # Cantidad ordenada y recibida
        wx.StaticText(self.panel, label="Cantidad Ordenada:", pos=(50, 130))
        self.txt_cant_ordenada = wx.TextCtrl(self.panel, pos=(200, 130), size=(100, -1))
        self.txt_cant_ordenada.SetValue("1")

        wx.StaticText(self.panel, label="Cantidad Recibida:", pos=(320, 130))
        self.txt_cant_recibida = wx.TextCtrl(self.panel, pos=(470, 130), size=(100, -1))
        self.txt_cant_recibida.SetValue("1")

        # Botón Añadir al carrito
        self.btn_agregar = wx.Button(self.panel, label="Agregar al Carrito", pos=(600, 125))
        self.btn_agregar.Bind(wx.EVT_BUTTON, self.agregar_al_carrito)

        # Lista del carrito
        cols = ['Código', 'Nombre', 'Precio', 'Ordenada', 'Recibida', 'Subtotal']
        self.lista = wx.ListCtrl(self.panel, style=wx.LC_REPORT, pos=(50, 170), size=(680, 250))
        for i, col in enumerate(cols):
            self.lista.InsertColumn(i, col, width=113)

        # Totales
        self.lbl_total = wx.StaticText(self.panel, label="Total: $0.00", pos=(600, 430))
        fuente_total = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.lbl_total.SetFont(fuente_total)

        # Botones
        self.btn_finalizar = wx.Button(self.panel, label="Finalizar Compra", pos=(600, 460), size=(150, 40))
        self.btn_finalizar.Bind(wx.EVT_BUTTON, self.finalizar_compra)

        self.btn_limpiar = wx.Button(self.panel, label="Limpiar", pos=(440, 460), size=(120, 40))
        self.btn_limpiar.Bind(wx.EVT_BUTTON, lambda e: self.limpiar_todo())

        # Campos ocultos para almacenamiento temporal
        self.codigo_seleccionado = None
        self.nombre_articulo = ""
        self.precio_articulo = 0

    def buscar_proveedor(self, event):
        idprov = self.txt_proveedor.GetValue().strip()
        if not idprov:
            self.mensaje("Advertencia", "Ingrese un ID de proveedor.")
            return

        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("SELECT nombre FROM proveedor WHERE idproveedor = %s", (idprov,))
                resultado = cursor.fetchone()
                if resultado:
                    self.mensaje("Proveedor encontrado", f"{resultado[0]}")
                else:
                    self.mensaje("Error", "Proveedor no encontrado.")
            except Exception as e:
                self.mensaje("Error", f"No se pudo buscar el proveedor: {e}")
            finally:
                cursor.close()
                conn.close()

    def buscar_articulo(self, event):
        valor = self.txt_codigo.GetValue().strip()
        if not valor:
            self.mensaje("Advertencia", "Ingrese un código o nombre.")
            return

        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    SELECT codigo_barras, nombre, precio FROM articulo 
                    WHERE codigo_barras = %s OR nombre LIKE %s
                """, (valor, f"%{valor}%"))
                resultado = cursor.fetchone()

                if resultado:
                    self.codigo_seleccionado = resultado[0]
                    self.nombre_articulo = resultado[1]
                    self.precio_articulo = resultado[2]
                else:
                    self.codigo_seleccionado = None
                    self.mensaje("Error", "Artículo no encontrado.")

            except Exception as e:
                self.mensaje("Error", f"Error al buscar artículo: {e}")
            finally:
                cursor.close()
                conn.close()

    def agregar_al_carrito(self, event):
        if not self.codigo_seleccionado:
            self.mensaje("Advertencia", "Primero busque un artículo válido.")
            return

        try:
            cant_ord = int(self.txt_cant_ordenada.GetValue())
            cant_rec = int(self.txt_cant_recibida.GetValue())
            if cant_ord <= 0 or cant_rec < 0:
                raise ValueError

            subtotal = self.precio_articulo * cant_rec
            fila = [
                self.codigo_seleccionado,
                self.nombre_articulo,
                f"{self.precio_articulo:.2f}",
                str(cant_ord),
                str(cant_rec),
                f"{subtotal:.2f}"
            ]

            self.lista.InsertItem(self.lista.GetItemCount(), fila[0])
            for c in range(1, len(fila)):
                self.lista.SetItem(self.lista.GetItemCount() - 1, c, fila[c])

            self.lista_carrito.append({
                "codigo": self.codigo_seleccionado,
                "nombre": self.nombre_articulo,
                "precio": self.precio_articulo,
                "cant_ord": cant_ord,
                "cant_rec": cant_rec,
                "subtotal": subtotal
            })

            self.codigo_seleccionado = None
            self.actualizar_total()
            self.txt_codigo.SetValue("")
            self.txt_cant_ordenada.SetValue("1")
            self.txt_cant_recibida.SetValue("1")
            self.txt_codigo.SetFocus()

        except ValueError:
            self.mensaje("Error", "Ingrese cantidades válidas.")

    def actualizar_total(self):
        self.total_general = sum(item["subtotal"] for item in self.lista_carrito)
        impuestos = self.total_general * 0.16
        self.lbl_total.SetLabel(f"Total: ${self.total_general + impuestos:.2f}")

    def finalizar_compra(self, event):
        if not self.lista_carrito:
            self.mensaje("Advertencia", "El carrito está vacío.")
            return

        if not self.validar_campos():
            self.mensaje("Advertencia", "Ingrese un proveedor válido.")
            return

        try:
            conn, cursor = conectar()
            cursor.execute("START TRANSACTION")

            # Insertar en compra
            idproveedor = self.txt_proveedor.GetValue()
            cursor.execute("""
                INSERT INTO compra (fecha_compra, total, impuestos, cantidad_articulos, tipo_pago, idproveedor)
                VALUES (NOW(), %s, %s, %s, %s, %s)
            """, (
                round(self.total_general * 1.16, 2),
                round(self.total_general * 0.16, 2),
                sum(item["cant_rec"] for item in self.lista_carrito),
                "Efectivo",
                idproveedor
            ))
            folio = cursor.lastrowid

            # Insertar en detalles_compra
            for item in self.lista_carrito:
                cursor.execute("""
                    INSERT INTO detalles_compra (
                        folio_compra, codigo_barras, cantidad_ordenada,
                        cantidad_recibida, precio_unitario_compra,
                        impuesto_unitario, subtotal_compra
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    folio,
                    item["codigo"],
                    item["cant_ord"],
                    item["cant_rec"],
                    item["precio"],
                    round(item["precio"] * 0.16, 2),
                    item["subtotal"]
                ))

                # Actualizar inventario solo si se recibió cantidad > 0
                if item["cant_rec"] > 0:
                    cursor.execute("""
                        UPDATE inventario SET existencia_actual = existencia_actual + %s
                        WHERE codigo_barras = %s
                    """, (item["cant_rec"], item["codigo"]))

            conn.commit()
            cursor.close()
            conn.close()
            self.mensaje("Éxito", f"Compra registrada. Folio: {folio}")
            self.limpiar_todo()

        except Exception as e:
            conn.rollback()
            self.mensaje("Error", f"Ocurrió un error al registrar la compra:\n{e}")
        finally:
            cursor.close()
            conn.close()

    def limpiar_todo(self):
        self.lista.DeleteAllItems()
        self.lista_carrito.clear()
        self.total_general = 0
        self.lbl_total.SetLabel("Total: $0.00")
        self.txt_proveedor.SetValue("")
        self.txt_codigo.SetValue("")
        self.txt_cant_ordenada.SetValue("1")
        self.txt_cant_recibida.SetValue("1")
        self.txt_codigo.SetFocus()