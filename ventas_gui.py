# ventas_gui.py
import wx
from conexion import conectar
from ClienteDelSol import ClienteCRUD
from ArticuloDelSol import ArticuloCRUD
import os
from reportlab.pdfgen import canvas
from datetime import datetime

class VentaGUI(wx.Frame):
    def __init__(self, parent=None, idempleado=None, nombre_empleado=""):
        super().__init__(parent, title="Punto de Venta - Del Sol", size=(1200, 800))
        self.idempleado = idempleado
        self.nombre_empleado = nombre_empleado
        self.obtener_datos_empleado()
        self.cliente_seleccionado = None
        self.lista_carrito = []
        self.total_general = 0.0
        self.panel = wx.Panel(self)
        self.SetBackgroundColour(wx.Colour(245, 247, 250))

        # Obtenemos los datos del empleado desde la BD
        self.nombre_empleado = ""
        self.apellidos_empleado = ""
        self.obtener_datos_empleado()

        self.crear_interfaz()
        self.Centre()
        self.Show()

    def obtener_datos_empleado(self):
        """Obtiene nombre y apellidos del empleado desde la BD"""
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("SELECT nombre, apellidos FROM empleado WHERE idempleado = %s", (self.idempleado,))
                resultado = cursor.fetchone()
                if resultado:
                    self.nombre_empleado = resultado[0]
                    self.apellidos_empleado = resultado[1]
                else:
                    self.nombre_empleado = "Desconocido"
                    self.apellidos_empleado = ""
            finally:
                cursor.close()
                conn.close()

    def mensaje(self, titulo, mensaje):
        wx.MessageBox(mensaje, titulo, wx.OK | wx.ICON_INFORMATION)

    def crear_interfaz(self):
        sizer_principal = wx.BoxSizer(wx.VERTICAL)

        # Título principal
        lbl_titulo = wx.StaticText(self.panel, label="PUNTO DE VENTA")
        fuente_titulo = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        lbl_titulo.SetFont(fuente_titulo)
        lbl_titulo.SetForegroundColour(wx.Colour(44, 62, 80))  # Azul oscuro
        sizer_principal.Add(lbl_titulo, 0, wx.ALIGN_CENTER | wx.ALL, 20)

        # Datos del empleado
        datos_empleado_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.lbl_datos_empleado = wx.StaticText(
            self.panel,
            label=f"Atendido por: {self.nombre_empleado} {self.apellidos_empleado}"
        )
        font_datos = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.lbl_datos_empleado.SetFont(font_datos)
        self.lbl_datos_empleado.SetForegroundColour(wx.Colour(44, 62, 80))
        datos_empleado_sizer.Add(self.lbl_datos_empleado, 0, wx.ALL, 5)
        sizer_principal.Add(datos_empleado_sizer, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 10)

        # Botones de navegación
        nav_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_regresar = wx.Button(self.panel, label="Regresar al Menú", size=(150, 40))
        btn_cancelar = wx.Button(self.panel, label="Cancelar Venta", size=(150, 40))
        btn_regresar.Bind(wx.EVT_BUTTON, self.on_regresar)
        btn_cancelar.Bind(wx.EVT_BUTTON, self.on_cancelar_venta)
        nav_sizer.Add(btn_regresar, 0, wx.ALL, 5)
        nav_sizer.Add(btn_cancelar, 0, wx.ALL, 5)
        sizer_principal.Add(nav_sizer, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.TOP, 10)

        # Sección de cliente
        box_cliente = wx.StaticBox(self.panel, label="Datos del Cliente")
        box_cliente.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sizer_cliente = wx.StaticBoxSizer(box_cliente, wx.HORIZONTAL)
        grid_cliente = wx.FlexGridSizer(rows=1, cols=3, vgap=5, hgap=10)

        self.txt_telefono = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.txt_telefono.Bind(wx.EVT_TEXT, self.buscar_cliente_auto)
        self.txt_telefono.Bind(wx.EVT_TEXT_ENTER, self.buscar_cliente_auto)

        btn_cliente_general = wx.Button(self.panel, label="Cliente General", size=(150, 40))
        btn_cliente_general.SetBackgroundColour(wx.Colour(52, 152, 219))
        btn_cliente_general.SetForegroundColour(wx.WHITE)
        btn_cliente_general.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        btn_cliente_general.Bind(wx.EVT_BUTTON, self.seleccionar_cliente_general)

        btn_agregar_cliente = wx.Button(self.panel, label="Agregar Cliente", size=(150, 40))
        btn_agregar_cliente.SetBackgroundColour(wx.Colour(46, 204, 113))
        btn_agregar_cliente.SetForegroundColour(wx.WHITE)
        btn_agregar_cliente.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
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
        box_articulo.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sizer_articulo = wx.StaticBoxSizer(box_articulo, wx.HORIZONTAL)

        self.txt_codigo = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.txt_codigo.Bind(wx.EVT_TEXT_ENTER, self.buscar_articulo)
        self.txt_codigo.Bind(wx.EVT_TEXT, self.busqueda_rapida_articulos)

        self.spin_cantidad = wx.SpinCtrl(self.panel, value="1", min=1, max=9999, size=(60, -1))

        self.btn_agregar = wx.Button(self.panel, label="Agregar al Carrito", size=(150, 40))
        self.btn_agregar.SetBackgroundColour(wx.Colour(230, 126, 34))
        self.btn_agregar.SetForegroundColour(wx.WHITE)
        self.btn_agregar.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.btn_agregar.Bind(wx.EVT_BUTTON, self.agregar_al_carrito)

        btn_eliminar_carrito = wx.Button(self.panel, label="Eliminar Artículo", size=(150, 40))
        btn_eliminar_carrito.SetBackgroundColour(wx.Colour(192, 57, 43))
        btn_eliminar_carrito.SetForegroundColour(wx.WHITE)
        btn_eliminar_carrito.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        btn_eliminar_carrito.Bind(wx.EVT_BUTTON, self.eliminar_articulo)

        self.lista_articulos = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, size=(-1, 100))
        self.lista_articulos.InsertColumn(0, "Código", width=120)
        self.lista_articulos.InsertColumn(1, "Nombre", width=200)
        self.lista_articulos.InsertColumn(2, "Precio", width=100)
        self.lista_articulos.InsertColumn(3, "Stock", width=80)
        self.lista_articulos.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_articulo_seleccionado)

        sizer_articulo.Add(self.txt_codigo, 1, wx.EXPAND | wx.ALL, 5)
        sizer_articulo.Add(self.spin_cantidad, 0, wx.ALL, 5)
        sizer_articulo.Add(self.btn_agregar, 0, wx.ALL, 5)
        sizer_articulo.Add(btn_eliminar_carrito, 0, wx.ALL, 5)
        sizer_principal.Add(sizer_articulo, 0, wx.EXPAND | wx.ALL, 10)

        # Tablas diferenciadas
        tabla_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Artículos Disponibles
        box_disponibles = wx.StaticBox(self.panel, label="Artículos Disponibles")
        box_disponibles.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sizer_disponibles = wx.StaticBoxSizer(box_disponibles, wx.VERTICAL)
        sizer_disponibles.Add(self.lista_articulos, 1, wx.EXPAND | wx.ALL, 5)
        tabla_sizer.Add(sizer_disponibles, 1, wx.EXPAND | wx.ALL, 5)

        # Carrito Actual
        box_carrito = wx.StaticBox(self.panel, label="Carrito Actual")
        box_carrito.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sizer_carrito = wx.StaticBoxSizer(box_carrito, wx.VERTICAL)

        self.lista_carrito_view = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, size=(-1, 200))
        self.lista_carrito_view.InsertColumn(0, "Código", width=120)
        self.lista_carrito_view.InsertColumn(1, "Nombre", width=200)
        self.lista_carrito_view.InsertColumn(2, "Precio", width=100)
        self.lista_carrito_view.InsertColumn(3, "Cantidad", width=80)
        self.lista_carrito_view.InsertColumn(4, "Subtotal", width=100)

        sizer_carrito.Add(self.lista_carrito_view, 1, wx.EXPAND | wx.ALL, 5)
        tabla_sizer.Add(sizer_carrito, 1, wx.EXPAND | wx.ALL, 5)

        sizer_principal.Add(tabla_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # Botón Pagar
        btn_pagar = wx.Button(self.panel, label="Pagar", size=(150, 40))
        btn_pagar.SetBackgroundColour(wx.Colour(46, 134, 69))
        btn_pagar.SetForegroundColour(wx.WHITE)
        btn_pagar.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        btn_pagar.Bind(wx.EVT_BUTTON, self.realizar_pago)
        sizer_principal.Add(btn_pagar, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # Total
        self.lbl_total = wx.StaticText(self.panel, label="Total: $0.00")
        self.lbl_total.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.lbl_total.SetForegroundColour(wx.Colour(44, 62, 80))
        sizer_principal.Add(self.lbl_total, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 20)

        self.panel.SetSizer(sizer_principal)

    # --- CLIENTES ---
    def seleccionar_cliente_general(self, event):
        self.cliente_seleccionado = ("9999999999", "CLIENTE", "GENERAL", "")
        self.txt_telefono.SetValue("9999999999")

    def buscar_cliente_auto(self, event):
        telefono = self.txt_telefono.GetValue().strip()
        if not telefono:
            self.lista_clientes.DeleteAllItems()
            return
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("SELECT * FROM cliente WHERE telefono_cliente LIKE %s LIMIT 5", (f"{telefono}%",))
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

    def abrir_cliente_crud(self, event):
        ClienteCRUD(parent=self)

    # --- ARTÍCULOS ---
    def buscar_articulo(self, event):
        valor = self.txt_codigo.GetValue().strip()
        if not valor:
            return
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    SELECT a.codigo_barras, a.nombre, a.precio, i.existencia_actual 
                    FROM articulo a LEFT JOIN inventario i ON a.codigo_barras = i.codigo_barras
                    WHERE a.codigo_barras = %s OR a.nombre LIKE %s""",
                               (valor, f"%{valor}%"))
                resultado = cursor.fetchone()
                if resultado:
                    self.codigo_seleccionado = resultado[0]
                    self.nombre_articulo = resultado[1]
                    self.precio_articulo = resultado[2]
                    self.stock_articulo = resultado[3] or 0
                else:
                    self.mensaje("Error", "Artículo no encontrado.")
            finally:
                cursor.close()
                conn.close()

    def busqueda_rapida_articulos(self, event):
        valor = self.txt_codigo.GetValue().strip()
        if not valor:
            self.lista_articulos.DeleteAllItems()
            return
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    SELECT a.codigo_barras, a.nombre, a.precio, i.existencia_actual 
                    FROM articulo a LEFT JOIN inventario i ON a.codigo_barras = i.codigo_barras
                    WHERE a.codigo_barras LIKE %s OR a.nombre LIKE %s
                    LIMIT 5""", (f"%{valor}%", f"%{valor}%"))
                resultados = cursor.fetchall()
                self.lista_articulos.DeleteAllItems()
                for row in resultados:
                    idx = self.lista_articulos.InsertItem(self.lista_articulos.GetItemCount(), row[0])
                    self.lista_articulos.SetItem(idx, 1, row[1])
                    self.lista_articulos.SetItem(idx, 2, f"{row[2]:.2f}")
                    self.lista_articulos.SetItem(idx, 3, str(row[3] or 0))
            finally:
                cursor.close()
                conn.close()

    def on_articulo_seleccionado(self, event):
        index = event.GetIndex()
        codigo = self.lista_articulos.GetItem(index, 0).GetText()
        self.txt_codigo.SetValue(codigo)
        self.buscar_articulo(None)

    # --- CARRITO ---
    def agregar_al_carrito(self, event):
        if not hasattr(self, 'codigo_seleccionado') or not self.codigo_seleccionado:
            self.mensaje("Advertencia", "Primero busque un artículo válido.")
            return

        cantidad = self.spin_cantidad.GetValue()
        if cantidad <= 0:
            self.mensaje("Error", "La cantidad debe ser mayor a 0.")
            return

        if cantidad > self.stock_articulo:
            self.mensaje("Advertencia", f"Solo hay {self.stock_articulo} unidades disponibles.")
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
        self.txt_codigo.Clear()
        self.spin_cantidad.SetValue(1)
        self.codigo_seleccionado = None
        self.lista_articulos.DeleteAllItems()

    def eliminar_articulo(self, event):
        index = self.lista_carrito_view.GetFirstSelected()
        if index == -1:
            self.mensaje("Advertencia", "Seleccione un artículo del carrito.")
            return
        item = self.lista_carrito[index]
        dlg = wx.NumberEntryDialog(
            self,
            "¿Cuántas unidades desea eliminar?",
            "Eliminar:",
            "Eliminar Artículo",
            item["cantidad"],
            1,
            item["cantidad"]
        )
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

    # --- PAGO Y TICKET ---
    def realizar_pago(self, event):
        if not self.lista_carrito:
            self.mensaje("Advertencia", "El carrito está vacío.")
            return

        # Diálogo para seleccionar el método de pago
        dlg = wx.SingleChoiceDialog(
            self,
            "Seleccione el método de pago:",
            "Método de Pago",
            ['Efectivo', 'Tarjeta', 'Transferencia']
        )

        if dlg.ShowModal() == wx.ID_OK:
            tipo_pago = dlg.GetStringSelection()
        else:
            dlg.Destroy()
            return
        dlg.Destroy()

        monto_recibido = None
        cambio = 0.0

        if tipo_pago == "Efectivo":
            # Pedir el monto recibido si es efectivo
            dlg_monto = wx.TextEntryDialog(
                self,
                f"Monto total: ${self.total_general:.2f}\nIngrese el monto recibido:",
                "Pago en Efectivo"
            )
            if dlg_monto.ShowModal() == wx.ID_OK:
                try:
                    monto_recibido = float(dlg_monto.GetValue())
                    if monto_recibido < self.total_general:
                        self.mensaje("Error", "El monto recibido es menor al total.")
                        return
                    cambio = monto_recibido - self.total_general
                except ValueError:
                    self.mensaje("Error", "Monto inválido.")
                    return
            else:
                return
            dlg_monto.Destroy()
            
        # Guardar venta en la base de datos
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    INSERT INTO venta (fecha, total, tipo_pago, idempleado, telefono_cliente, impuesto_IVA)
                    VALUES (NOW(), %s, %s, %s, %s, 0.0)
                """, (
                    self.total_general,
                    tipo_pago,
                    self.idempleado,
                    self.cliente_seleccionado[0] if self.cliente_seleccionado else "9999999999"
                ))
                folio_venta = cursor.lastrowid  # Obtenemos el ID de la venta recién creada

                # Guardar cada artículo del carrito en detalles_venta
                for item in self.lista_carrito:
                    cursor.execute("""
                        INSERT INTO detalles_venta 
                        (folio_de_ticket, codigo_barras, cantidad_articulo, precio_unitario_venta, subtotal_venta, impuesto_unitario)
                        VALUES (%s, %s, %s, %s, %s, 0.0)
                    """, (
                        folio_venta,
                        item["codigo"],
                        item["cantidad"],
                        item["precio"],
                        item["subtotal"]
                    ))

                    # Actualizar el inventario
                    cursor.execute("""
                        UPDATE inventario SET existencia_actual = existencia_actual - %s
                        WHERE codigo_barras = %s
                    """, (item["cantidad"], item["codigo"]))

                conn.commit()
                
                # Llamar a generar_ticket con todos los datos
                self.generar_ticket(folio_venta, tipo_pago, monto_recibido if tipo_pago == "Efectivo" else None, cambio)

                self.limpiar_venta()

            except Exception as e:
                conn.rollback()
                self.mensaje("Error", f"No se pudo completar la venta: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def generar_ticket(self, folio, tipo_pago, monto_recibido=None, cambio=None):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ticket_texto = f"""
    {'-'*40}
    TIENDA DEL SOL
    Folio: {folio}
    Fecha: {fecha}
    CLIENTE:
    """

        if self.cliente_seleccionado:
            ticket_texto += f"{self.cliente_seleccionado[1]} {self.cliente_seleccionado[2]}\n"
            ticket_texto += f"{self.cliente_seleccionado[0]}\n"
        else:
            ticket_texto += "General\n"

        ticket_texto += f"Atendido por:\n{self.nombre_empleado} {self.apellidos_empleado}\n"
        ticket_texto += f"Método de pago: {tipo_pago}\n"

        if tipo_pago == "Efectivo" and monto_recibido is not None:
            ticket_texto += f"Monto recibido: ${monto_recibido:.2f}\n"
            ticket_texto += f"Cambio:         ${cambio:.2f}\n"

        ticket_texto += "ARTÍCULOS:\n"

        for item in self.lista_carrito:
            ticket_texto += f"{item['nombre']} x{item['cantidad']} @ ${item['precio']:.2f} = ${item['subtotal']:.2f}\n"

        ticket_texto += "\n"
        ticket_texto += f"{'-'*40}\n"
        ticket_texto += f"Subtotal:       ${self.total_general:.2f}\n"
        ticket_texto += f"Impuesto (IVA): $0.00\n"
        ticket_texto += f"TOTAL:          ${self.total_general:.2f}\n"
        ticket_texto += f"{'-'*40}\n"
        ticket_texto += "¡Gracias por su compra!\n"

        self.mensaje("Ticket de Venta", ticket_texto)
        self.guardar_ticket_pdf(folio, ticket_texto)

    def guardar_ticket_pdf(self, folio, texto):
        carpeta = "tickets"
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        ruta = os.path.join(carpeta, f"ticket_{folio}.pdf")
        c = canvas.Canvas(ruta)
        c.setFont("Helvetica", 10)
        lineas = texto.strip().split('\n')
        y = 750
        for linea in lineas:
            c.drawString(50, y, linea)
            y -= 15
        c.save()
        self.mensaje("Éxito", f"Ticket guardado como {ruta}")

    def limpiar_venta(self):
        self.lista_carrito.clear()
        self.lista_carrito_view.DeleteAllItems()
        self.actualizar_total()
        self.txt_codigo.Clear()
        self.spin_cantidad.SetValue(1)
        self.codigo_seleccionado = None
        self.cliente_seleccionado = None
        self.txt_telefono.Clear()
        self.lista_clientes.DeleteAllItems()
        self.lista_articulos.DeleteAllItems()

    def on_regresar(self, event):
        self.Close()
        from MenuPrincipal import MenuPrincipal
        MenuPrincipal(idempleado=self.idempleado)

    def on_cancelar_venta(self, event):
        confirmacion = wx.MessageBox("¿Está seguro de cancelar esta venta?", "Cancelar Venta", wx.YES_NO | wx.ICON_QUESTION)
        if confirmacion == wx.YES:
            self.limpiar_venta()