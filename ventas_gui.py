# ventas_gui.py
import wx
from conexion import conectar

class VentaGUI(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title="Registrar Venta", size=(800, 600))
        self.panel = wx.Panel(self)
        self.lista_carrito = []
        self.total_general = 0
        self.idempleado = "1"
        self.telefono_cliente = ""

        self.crear_interfaz()
        self.Centre()
        self.Show()

    def mensaje(self, titulo, mensaje):
        wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

    def crear_interfaz(self):
        lbl_titulo = wx.StaticText(self.panel, label="REGISTRAR VENTA", pos=(320, 10))
        fuente_titulo = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        lbl_titulo.SetFont(fuente_titulo)

        wx.StaticText(self.panel, label="Teléfono Cliente:", pos=(50, 50))
        self.txt_cliente = wx.TextCtrl(self.panel, pos=(200, 50), size=(200, -1))

        wx.StaticText(self.panel, label="Código / Nombre:", pos=(50, 90))
        self.txt_codigo = wx.TextCtrl(self.panel, pos=(200, 90), size=(200, -1), style=wx.TE_PROCESS_ENTER)
        self.txt_codigo.Bind(wx.EVT_TEXT_ENTER, self.buscar_articulo)  # Escáner externo simula Enter
        self.txt_codigo.SetFocus()  # Cursor listo para escanear

        self.btn_buscar = wx.Button(self.panel, label="Buscar", pos=(410, 85))
        self.btn_buscar.Bind(wx.EVT_BUTTON, self.buscar_articulo)

        wx.StaticText(self.panel, label="Cantidad:", pos=(50, 130))
        self.txt_cantidad = wx.TextCtrl(self.panel, pos=(200, 130), size=(100, -1))
        self.txt_cantidad.SetValue("1")

        self.btn_agregar = wx.Button(self.panel, label="Agregar al Carrito", pos=(320, 125))
        self.btn_agregar.Bind(wx.EVT_BUTTON, self.agregar_al_carrito)

        cols = ['Código', 'Nombre', 'Precio', 'Cantidad', 'Subtotal']
        self.lista = wx.ListCtrl(self.panel, style=wx.LC_REPORT, pos=(50, 170), size=(680, 250))
        for i, col in enumerate(cols):
            self.lista.InsertColumn(i, col, width=150)

        self.lbl_total = wx.StaticText(self.panel, label="Total: $0.00", pos=(600, 430))
        fuente_total = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.lbl_total.SetFont(fuente_total)

        self.btn_finalizar = wx.Button(self.panel, label="Finalizar Venta", pos=(600, 460), size=(150, 40))
        self.btn_finalizar.Bind(wx.EVT_BUTTON, self.finalizar_venta)

        self.btn_limpiar = wx.Button(self.panel, label="Limpiar", pos=(440, 460), size=(120, 40))
        self.btn_limpiar.Bind(wx.EVT_BUTTON, lambda e: self.limpiar_todo())

        self.codigo_seleccionado = None

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
                    self.mensaje("Artículo encontrado", f"{self.nombre_articulo} - ${self.precio_articulo:.2f}")
                    self.txt_cantidad.SetFocus()
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
            cantidad = int(self.txt_cantidad.GetValue())
            if cantidad <= 0:
                raise ValueError

            conn, cursor = conectar()
            cursor.execute("SELECT existencia_actual FROM inventario WHERE codigo_barras = %s",
                           (self.codigo_seleccionado,))
            inv = cursor.fetchone()
            cursor.close()
            conn.close()

            if not inv or inv[0] < cantidad:
                self.mensaje("Stock Insuficiente", "No hay suficiente stock.")
                return

            subtotal = self.precio_articulo * cantidad
            fila = [self.codigo_seleccionado, self.nombre_articulo,
                    f"{self.precio_articulo:.2f}", str(cantidad), f"{subtotal:.2f}"]
            self.lista.InsertItem(self.lista.GetItemCount(), fila[0])
            for c in range(1, len(fila)):
                self.lista.SetItem(self.lista.GetItemCount() - 1, c, fila[c])

            self.lista_carrito.append({
                "codigo": self.codigo_seleccionado,
                "nombre": self.nombre_articulo,
                "precio": self.precio_articulo,
                "cantidad": cantidad,
                "subtotal": subtotal
            })

            self.codigo_seleccionado = None
            self.actualizar_total()
            self.txt_codigo.SetValue("")
            self.txt_cantidad.SetValue("1")
            self.txt_codigo.SetFocus()

        except ValueError:
            self.mensaje("Error", "Ingrese una cantidad válida.")

    def actualizar_total(self):
        self.total_general = sum(item["subtotal"] for item in self.lista_carrito)
        iva = self.total_general * 0.16
        self.lbl_total.SetLabel(f"Total: ${self.total_general + iva:.2f}")

    def finalizar_venta(self, event):
        if not self.lista_carrito:
            self.mensaje("Advertencia", "El carrito está vacío.")
            return

        try:
            conn, cursor = conectar()
            cursor.execute("START TRANSACTION")

            cursor.execute("""
                INSERT INTO venta (fecha, total, tipo_pago, idempleado, telefono_cliente)
                VALUES (NOW(), %s, %s, %s, %s)
            """, (round(self.total_general * 1.16, 2), "Efectivo", self.idempleado, self.telefono_cliente))
            folio = cursor.lastrowid

            for item in self.lista_carrito:
                cursor.execute("""
                    INSERT INTO detalles_venta (folio_de_ticket, codigo_barras, cantidad_articulo,
                                              precio_unitario_venta, impuesto_unitario, subtotal_venta)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    folio,
                    item["codigo"],
                    item["cantidad"],
                    item["precio"],
                    round(item["precio"] * 0.16, 2),
                    item["subtotal"]
                ))

                cursor.execute("""
                    UPDATE inventario SET existencia_actual = existencia_actual - %s
                    WHERE codigo_barras = %s
                """, (item["cantidad"], item["codigo"]))

            conn.commit()
            cursor.close()
            conn.close()
            self.mensaje("Éxito", f"Venta registrada. Folio: {folio}")
            self.limpiar_todo()

        except Exception as e:
            conn.rollback()
            self.mensaje("Error", f"Ocurrió un error al registrar la venta:\n{e}")
        finally:
            cursor.close()
            conn.close()

    def limpiar_todo(self):
        self.lista.DeleteAllItems()
        self.lista_carrito.clear()
        self.total_general = 0
        self.lbl_total.SetLabel("Total: $0.00")
        self.txt_codigo.SetValue("")
        self.txt_cantidad.SetValue("1")
        self.txt_cliente.SetValue("")
        self.txt_codigo.SetFocus()
