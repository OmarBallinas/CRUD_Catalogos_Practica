# ventas_gui.py
import wx
from conexion import conectar
from ClienteDelSol import ClienteCRUD  # Asegúrate de tener esta clase
from ArticuloDelSol import ArticuloCRUD  # O reutiliza parte del código

class VentaGUI(wx.Frame):
    def __init__(self, parent=None, idempleado=None):
        super().__init__(parent, title="Punto de Venta - Del Sol", size=(1200, 800))
        self.idempleado = idempleado
        self.cliente_seleccionado = None
        self.lista_carrito = []
        self.total_general = 0.0
        self.panel = wx.Panel(self)
        self.SetBackgroundColour(wx.Colour(245, 247, 250))
        self.crear_interfaz()
        self.Centre()
        self.Show()

    def mensaje(self, titulo, mensaje):
        wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

    def crear_interfaz(self):
        sizer_principal = wx.BoxSizer(wx.VERTICAL)

        # Título
        lbl_titulo = wx.StaticText(self.panel, label="PUNTO DE VENTA")
        fuente_titulo = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        lbl_titulo.SetFont(fuente_titulo)
        lbl_titulo.SetForegroundColour(wx.Colour(44, 62, 80))  # Azul oscuro
        sizer_principal.Add(lbl_titulo, 0, wx.ALIGN_CENTER | wx.ALL, 20)

        # Sección de cliente
        box_cliente = wx.StaticBox(self.panel, label="Datos del Cliente")
        sizer_cliente = wx.StaticBoxSizer(box_cliente, wx.HORIZONTAL)

        grid_cliente = wx.FlexGridSizer(rows=1, cols=4, vgap=5, hgap=10)

        self.txt_telefono = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.txt_telefono.Bind(wx.EVT_TEXT, self.buscar_cliente_auto)
        self.txt_telefono.Bind(wx.EVT_TEXT_ENTER, self.buscar_cliente_manual)

        btn_cliente_general = wx.Button(self.panel, label="Cliente General")
        btn_cliente_general.SetBackgroundColour(wx.Colour(52, 152, 219))
        btn_cliente_general.SetForegroundColour(wx.WHITE)
        btn_cliente_general.Bind(wx.EVT_BUTTON, self.seleccionar_cliente_general)

        btn_agregar_cliente = wx.Button(self.panel, label="Agregar Cliente")
        btn_agregar_cliente.SetBackgroundColour(wx.Colour(46, 204, 113))
        btn_agregar_cliente.SetForegroundColour(wx.WHITE)
        btn_agregar_cliente.Bind(wx.EVT_BUTTON, self.abrir_cliente_crud)

        self.lista_clientes = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, size=(-1, 100))
        self.lista_clientes.InsertColumn(0, "Teléfono", width=150)
        self.lista_clientes.InsertColumn(1, "Nombre", width=200)
        self.lista_clientes.InsertColumn(2, "Apellido", width=200)
        self.lista_clientes.InsertColumn(3, "Correo", width=250)

        self.lista_clientes.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_cliente_seleccionado)

        grid_cliente.Add(self.txt_telefono, 1, wx.EXPAND)
        grid_cliente.Add(btn_cliente_general, 0, wx.EXPAND)
        grid_cliente.Add(btn_agregar_cliente, 0, wx.EXPAND)
        sizer_cliente.Add(grid_cliente, 0, wx.EXPAND | wx.ALL, 5)
        sizer_cliente.Add(self.lista_clientes, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        sizer_principal.Add(sizer_cliente, 0, wx.EXPAND | wx.ALL, 10)

        # Sección de artículo
        box_articulo = wx.StaticBox(self.panel, label="Buscar Artículo")
        sizer_articulo = wx.StaticBoxSizer(box_articulo, wx.HORIZONTAL)

        self.txt_codigo = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.txt_codigo.Bind(wx.EVT_TEXT_ENTER, self.buscar_articulo)

        self.btn_buscar_articulo = wx.Button(self.panel, label="Buscar Artículo")
        self.btn_buscar_articulo.Bind(wx.EVT_BUTTON, self.buscar_articulo)

        self.txt_cantidad = wx.TextCtrl(self.panel, value="1", size=(60, -1))

        self.btn_agregar = wx.Button(self.panel, label="Agregar al Carrito")
        self.btn_agregar.SetBackgroundColour(wx.Colour(230, 126, 34))
        self.btn_agregar.SetForegroundColour(wx.WHITE)
        self.btn_agregar.Bind(wx.EVT_BUTTON, self.agregar_al_carrito)

        sizer_articulo.Add(self.txt_codigo, 1, wx.EXPAND | wx.ALL, 5)
        sizer_articulo.Add(self.btn_buscar_articulo, 0, wx.ALL, 5)
        sizer_articulo.Add(wx.StaticText(self.panel, label=" Cantidad:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        sizer_articulo.Add(self.txt_cantidad, 0, wx.ALL, 5)
        sizer_articulo.Add(self.btn_agregar, 0, wx.ALL, 5)
        sizer_principal.Add(sizer_articulo, 0, wx.EXPAND | wx.ALL, 10)

        # Carrito
        self.lista_carrito_view = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, size=(-1, 200))
        self.lista_carrito_view.InsertColumn(0, "Código", width=120)
        self.lista_carrito_view.InsertColumn(1, "Nombre", width=200)
        self.lista_carrito_view.InsertColumn(2, "Precio", width=100)
        self.lista_carrito_view.InsertColumn(3, "Cantidad", width=80)
        self.lista_carrito_view.InsertColumn(4, "Subtotal", width=100)

        sizer_principal.Add(self.lista_carrito_view, 0, wx.EXPAND | wx.ALL, 10)

        # Botones de acción
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        btn_eliminar = wx.Button(self.panel, label="Eliminar Artículo")
        btn_eliminar.SetBackgroundColour(wx.Colour(192, 57, 43))
        btn_eliminar.SetForegroundColour(wx.WHITE)
        btn_eliminar.Bind(wx.EVT_BUTTON, self.eliminar_articulo)

        btn_pagar = wx.Button(self.panel, label="Pagar")
        btn_pagar.SetBackgroundColour(wx.Colour(46, 134, 69))
        btn_pagar.SetForegroundColour(wx.WHITE)
        btn_pagar.Bind(wx.EVT_BUTTON, self.realizar_pago)

        btn_sizer.Add(btn_eliminar, 0, wx.ALL, 5)
        btn_sizer.AddStretchSpacer()
        btn_sizer.Add(btn_pagar, 0, wx.ALL, 5)

        sizer_principal.Add(btn_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # Total
        self.lbl_total = wx.StaticText(self.panel, label="Total: $0.00")
        self.lbl_total.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.lbl_total.SetForegroundColour(wx.Colour(44, 62, 80))
        sizer_principal.Add(self.lbl_total, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 20)

        self.panel.SetSizer(sizer_principal)

    # --- Funcionalidad de cliente ---
    def buscar_cliente_auto(self, event):
        telefono = self.txt_telefono.GetValue().strip()
        if len(telefono) >= 2:
            conn, cursor = conectar()
            if conn and cursor:
                try:
                    cursor.execute("SELECT * FROM cliente WHERE telefono_cliente LIKE %s LIMIT 5",
                                   (f"{telefono}%",))
                    resultados = cursor.fetchall()
                    self.lista_clientes.DeleteAllItems()
                    for row in resultados:
                        idx = self.lista_clientes.InsertItem(self.lista_clientes.GetItemCount(), row[0])
                        self.lista_clientes.SetItem(idx, 1, row[1])
                        self.lista_clientes.SetItem(idx, 2, row[2])
                        self.lista_clientes.SetItem(idx, 3, row[3] or "")
                finally:
                    cursor.close()
                    conn.close()

    def on_cliente_seleccionado(self, event):
        index = event.GetIndex()
        telefono = self.lista_clientes.GetItem(index, 0).GetText()
        self.txt_telefono.SetValue(telefono)
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("SELECT * FROM cliente WHERE telefono_cliente = %s", (telefono,))
                resultado = cursor.fetchone()
                self.cliente_seleccionado = resultado
            finally:
                cursor.close()
                conn.close()

    def buscar_cliente_manual(self, event):
        self.buscar_cliente_auto(event)

    def seleccionar_cliente_general(self, event):
        self.cliente_seleccionado = ("0000000000", "General", "", "")  # Teléfono general
        self.txt_telefono.SetValue("0000000000")

    def abrir_cliente_crud(self, event):
        ClienteCRUD(parent=self)

    # --- Funcionalidad de artículo ---
    def buscar_articulo(self, event):
        valor = self.txt_codigo.GetValue().strip()
        if not valor:
            return
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    SELECT codigo_barras, nombre, precio 
                    FROM articulo 
                    WHERE codigo_barras = %s OR nombre LIKE %s""",
                               (valor, f"%{valor}%"))
                resultado = cursor.fetchone()
                if resultado:
                    self.codigo_seleccionado = resultado[0]
                    self.nombre_articulo = resultado[1]
                    self.precio_articulo = resultado[2]
                else:
                    self.mensaje("Error", "Artículo no encontrado.")
            finally:
                cursor.close()
                conn.close()

    def agregar_al_carrito(self, event):
        if not hasattr(self, 'codigo_seleccionado') or not self.codigo_seleccionado:
            self.mensaje("Advertencia", "Primero busque un artículo válido.")
            return
        try:
            cantidad = int(self.txt_cantidad.GetValue())
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            self.mensaje("Error", "La cantidad debe ser un número positivo.")
            return

        subtotal = self.precio_articulo * cantidad
        fila = [
            self.codigo_seleccionado,
            self.nombre_articulo,
            f"{self.precio_articulo:.2f}",
            str(cantidad),
            f"{subtotal:.2f}"
        ]
        self.lista_carrito.append({
            "codigo": self.codigo_seleccionado,
            "nombre": self.nombre_articulo,
            "precio": self.precio_articulo,
            "cantidad": cantidad,
            "subtotal": subtotal
        })
        idx = self.lista_carrito_view.InsertItem(self.lista_carrito_view.GetItemCount(), fila[0])
        for i, val in enumerate(fila[1:], start=1):
            self.lista_carrito_view.SetItem(idx, i, val)
        self.actualizar_total()

    def eliminar_articulo(self, event):
        index = self.lista_carrito_view.GetFirstSelected()
        if index == -1:
            self.mensaje("Advertencia", "Seleccione un artículo del carrito.")
            return
        item = self.lista_carrito[index]
        dlg = wx.NumberEntryDialog(self, "¿Cuántas unidades desea eliminar?", "Eliminar:", "Eliminar Artículo", item["cantidad"], 1, item["cantidad"])
        if dlg.ShowModal() == wx.ID_OK:
            eliminar = dlg.GetValue()
            if eliminar == item["cantidad"]:
                self.lista_carrito.pop(index)
                self.lista_carrito_view.DeleteItem(index)
            else:
                item["cantidad"] -= eliminar
                item["subtotal"] = item["precio"] * item["cantidad"]
                self.lista_carrito_view.SetItem(index, 3, str(item["cantidad"]))
                self.lista_carrito_view.SetItem(index, 4, f"{item['subtotal']:.2f}")
            self.actualizar_total()
        dlg.Destroy()

    def actualizar_total(self):
        self.total_general = sum(item["subtotal"] for item in self.lista_carrito)
        self.lbl_total.SetLabel(f"Total: ${self.total_general:.2f}")

    # --- Pago y registro ---
    def realizar_pago(self, event):
        if not self.lista_carrito:
            self.mensaje("Advertencia", "El carrito está vacío.")
            return

        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    INSERT INTO venta (fecha, total, tipo_pago, idempleado, telefono_cliente)
                    VALUES (NOW(), %s, %s, %s, %s)
                """, (
                    self.total_general,
                    "Efectivo",
                    self.idempleado,
                    self.cliente_seleccionado[0] if self.cliente_seleccionado else "0000000000"
                ))
                folio_venta = cursor.lastrowid

                for item in self.lista_carrito:
                    cursor.execute("""
                        INSERT INTO detalles_venta (folio_de_ticket, codigo_barras, cantidad_articulo, precio_unitario_venta, subtotal_venta)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        folio_venta,
                        item["codigo"],
                        item["cantidad"],
                        item["precio"],
                        item["subtotal"]
                    ))
                    cursor.execute("""
                        UPDATE inventario SET existencia_actual = existencia_actual - %s
                        WHERE codigo_barras = %s
                    """, (item["cantidad"], item["codigo"]))

                conn.commit()
                self.generar_ticket(folio_venta)
                self.limpiar_venta()
            except Exception as e:
                conn.rollback()
                self.mensaje("Error", f"No se pudo completar la venta: {e}")
            finally:
                cursor.close()
                conn.close()

    def generar_ticket(self, folio):
        ticket = f"Folio: {folio}\nFecha: {wx.DateTime.Now().FormatISODate()}\n\n"
        ticket += "CLIENTE:\n"
        if self.cliente_seleccionado:
            ticket += f"{self.cliente_seleccionado[1]} {self.cliente_seleccionado[2]}\n"
            ticket += f"{self.cliente_seleccionado[0]}\n\n"
        ticket += "ARTÍCULOS:\n"
        for item in self.lista_carrito:
            ticket += f"{item['nombre']} x{item['cantidad']} @ ${item['precio']:.2f} = ${item['subtotal']:.2f}\n"
        ticket += "\n"
        ticket += f"TOTAL: ${self.total_general:.2f}"
        self.mensaje("Ticket de Venta", ticket)

    def limpiar_venta(self):
        self.lista_carrito.clear()
        self.lista_carrito_view.DeleteAllItems()
        self.actualizar_total()
        self.txt_codigo.Clear()
        self.txt_cantidad.SetValue("1")
        self.codigo_seleccionado = None
        self.cliente_seleccionado = None
        self.txt_telefono.Clear()
        self.lista_clientes.DeleteAllItems()