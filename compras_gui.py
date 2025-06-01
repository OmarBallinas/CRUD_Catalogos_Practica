# compras_gui.py
import wx
from conexion import conectar
from ProveedorDelSol import ProveedorCRUD
from ArticuloDelSol import ArticuloCRUD
import os
from reportlab.pdfgen import canvas
from datetime import datetime


class CompraGUI(wx.Frame):
    def __init__(self, parent=None, idempleado=None):
        super().__init__(parent, title="Registro de Compra - Del Sol", size=(1200, 800))
        self.idempleado = idempleado
        self.nombre_empleado = ""
        self.apellidos_empleado = ""
        self.proveedor_seleccionado = None
        self.lista_carrito = []
        self.total_general = 0.0
        self.panel = wx.Panel(self)
        self.SetBackgroundColour(wx.Colour(245, 247, 250))

        # Cargar datos del empleado
        self.obtener_datos_empleado()

        # Interfaz gráfica
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
        lbl_titulo = wx.StaticText(self.panel, label="REGISTRO DE COMPRA")
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
        btn_regresar_menu = wx.Button(self.panel, label="Regresar al Menú", size=(150, 40))
        btn_cancelar = wx.Button(self.panel, label="Cancelar Compra", size=(150, 40))
        btn_regresar_menu.Bind(wx.EVT_BUTTON, self.on_regresar_menu)
        btn_cancelar.Bind(wx.EVT_BUTTON, self.on_cancelar_compra)
        nav_sizer.Add(btn_regresar_menu, 0, wx.ALL, 5)
        nav_sizer.Add(btn_cancelar, 0, wx.ALL, 5)
        sizer_principal.Add(nav_sizer, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.TOP, 10)

        # Sección de proveedor
        box_proveedor = wx.StaticBox(self.panel, label="Datos del Proveedor")
        box_proveedor.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sizer_proveedor = wx.StaticBoxSizer(box_proveedor, wx.HORIZONTAL)
        grid_proveedor = wx.FlexGridSizer(rows=1, cols=3, vgap=5, hgap=10)

        self.txt_id_proveedor = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.txt_id_proveedor.Bind(wx.EVT_TEXT, self.buscar_proveedor_auto)
        self.txt_id_proveedor.Bind(wx.EVT_TEXT_ENTER, self.buscar_proveedor_auto)

        btn_proveedor_default = wx.Button(self.panel, label="Proveedor General", size=(150, 40))
        btn_proveedor_default.SetBackgroundColour(wx.Colour(52, 152, 219))
        btn_proveedor_default.SetForegroundColour(wx.WHITE)
        btn_proveedor_default.Bind(wx.EVT_BUTTON, self.seleccionar_proveedor_default)

        btn_agregar_proveedor = wx.Button(self.panel, label="Gestionar Proveedor", size=(150, 40))
        btn_agregar_proveedor.SetBackgroundColour(wx.Colour(46, 204, 113))
        btn_agregar_proveedor.SetForegroundColour(wx.WHITE)
        btn_agregar_proveedor.Bind(wx.EVT_BUTTON, self.abrir_proveedor_crud)

        self.lista_proveedores = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, size=(-1, 100))
        self.lista_proveedores.InsertColumn(0, "ID", width=100)
        self.lista_proveedores.InsertColumn(1, "Nombre", width=200)
        self.lista_proveedores.InsertColumn(2, "Contacto", width=200)
        self.lista_proveedores.InsertColumn(3, "Teléfono", width=100)
        self.lista_proveedores.InsertColumn(4, "Correo", width=200)
        self.lista_proveedores.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_proveedor_seleccionado)

        grid_proveedor.Add(self.txt_id_proveedor, 1, wx.EXPAND)
        grid_proveedor.Add(btn_proveedor_default, 0, wx.EXPAND)
        grid_proveedor.Add(btn_agregar_proveedor, 0, wx.EXPAND)
        sizer_proveedor.Add(grid_proveedor, 0, wx.EXPAND | wx.ALL, 5)
        sizer_proveedor.Add(self.lista_proveedores, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        sizer_principal.Add(sizer_proveedor, 0, wx.EXPAND | wx.ALL, 10)

        # Sección de artículo
        box_articulo = wx.StaticBox(self.panel, label="Buscar Artículo")
        box_articulo.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sizer_articulo = wx.StaticBoxSizer(box_articulo, wx.HORIZONTAL)

        self.txt_codigo = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.txt_codigo.Bind(wx.EVT_TEXT_ENTER, self.buscar_articulo)
        self.txt_codigo.Bind(wx.EVT_TEXT, self.busqueda_rapida_articulos)

        self.spin_cantidad = wx.SpinCtrl(self.panel, value="1", min=1, max=9999, size=(60, -1))
        self.txt_precio_compra = wx.TextCtrl(self.panel, value="0.00", size=(80, -1))

        self.btn_agregar = wx.Button(self.panel, label="Agregar al Carrito", size=(150, 40))
        self.btn_agregar.SetBackgroundColour(wx.Colour(230, 126, 34))
        self.btn_agregar.SetForegroundColour(wx.WHITE)
        self.btn_agregar.Bind(wx.EVT_BUTTON, self.agregar_al_carrito)

        btn_eliminar_carrito = wx.Button(self.panel, label="Eliminar Artículo", size=(150, 40))
        btn_eliminar_carrito.SetBackgroundColour(wx.Colour(192, 57, 43))
        btn_eliminar_carrito.SetForegroundColour(wx.WHITE)
        btn_eliminar_carrito.Bind(wx.EVT_BUTTON, self.eliminar_articulo)

        self.lista_articulos = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, size=(-1, 100))
        self.lista_articulos.InsertColumn(0, "Código", width=120)
        self.lista_articulos.InsertColumn(1, "Nombre", width=200)
        self.lista_articulos.InsertColumn(2, "Precio", width=100)
        self.lista_articulos.InsertColumn(3, "Stock Actual", width=100)
        self.lista_articulos.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_articulo_seleccionado)

        sizer_articulo.Add(self.txt_codigo, 1, wx.EXPAND | wx.ALL, 5)
        sizer_articulo.Add(self.spin_cantidad, 0, wx.ALL, 5)
        sizer_articulo.Add(self.txt_precio_compra, 0, wx.ALL, 5)
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
        box_carrito = wx.StaticBox(self.panel, label="Carrito de Compra")
        box_carrito.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sizer_carrito = wx.StaticBoxSizer(box_carrito, wx.VERTICAL)

        self.lista_carrito_view = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, size=(-1, 200))
        self.lista_carrito_view.InsertColumn(0, "Código", width=120)
        self.lista_carrito_view.InsertColumn(1, "Nombre", width=200)
        self.lista_carrito_view.InsertColumn(2, "Precio Compra", width=120)
        self.lista_carrito_view.InsertColumn(3, "Cantidad", width=80)
        self.lista_carrito_view.InsertColumn(4, "Subtotal", width=120)

        sizer_carrito.Add(self.lista_carrito_view, 1, wx.EXPAND | wx.ALL, 5)
        tabla_sizer.Add(sizer_carrito, 1, wx.EXPAND | wx.ALL, 5)

        sizer_principal.Add(tabla_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # Botón Realizar Compra
        btn_comprar = wx.Button(self.panel, label="Realizar Compra", size=(150, 40))
        btn_comprar.SetBackgroundColour(wx.Colour(46, 134, 69))
        btn_comprar.SetForegroundColour(wx.WHITE)
        btn_comprar.Bind(wx.EVT_BUTTON, self.realizar_compra)
        sizer_principal.Add(btn_comprar, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # Total
        self.lbl_total = wx.StaticText(self.panel, label="Total: $0.00")
        font_total = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.lbl_total.SetFont(font_total)
        self.lbl_total.SetForegroundColour(wx.Colour(44, 62, 80))
        sizer_principal.Add(self.lbl_total, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 20)

        self.panel.SetSizer(sizer_principal)

    # --- PROVEEDORES ---
    def seleccionar_proveedor_default(self, event):
        self.proveedor_seleccionado = ("9999999999", "PROVEEDOR GENERAL", "Sin Contacto", "9999999999", "")
        self.txt_id_proveedor.SetValue("9999999999")

    def buscar_proveedor_auto(self, event):
        valor = self.txt_id_proveedor.GetValue().strip()
        if not valor:
            self.lista_proveedores.DeleteAllItems()
            return
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    SELECT * FROM proveedor 
                    WHERE idproveedor LIKE %s OR nombre LIKE %s LIMIT 5
                """, (f"{valor}%", f"%{valor}%"))
                resultados = cursor.fetchall()
                self.lista_proveedores.DeleteAllItems()
                for row in resultados:
                    idx = self.lista_proveedores.InsertItem(self.lista_proveedores.GetItemCount(), str(row[0]))
                    self.lista_proveedores.SetItem(idx, 1, row[1])
                    self.lista_proveedores.SetItem(idx, 2, row[2])
                    self.lista_proveedores.SetItem(idx, 3, row[3])
                    self.lista_proveedores.SetItem(idx, 4, row[4] or "")
            finally:
                cursor.close()
                conn.close()

    def on_proveedor_seleccionado(self, event):
        index = event.GetIndex()
        id_proveedor = self.lista_proveedores.GetItem(index, 0).GetText()
        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("SELECT * FROM proveedor WHERE idproveedor = %s", (id_proveedor,))
                resultado = cursor.fetchone()
                self.proveedor_seleccionado = resultado
                self.txt_id_proveedor.SetValue(str(resultado[0]))
            finally:
                cursor.close()
                conn.close()

    def abrir_proveedor_crud(self, event):
        ProveedorCRUD(parent=self)

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
        try:
            cantidad = int(self.spin_cantidad.GetValue())
            precio_compra = float(self.txt_precio_compra.GetValue())
        except ValueError:
            self.mensaje("Error", "Precio o cantidad inválidos.")
            return
        if cantidad <= 0:
            self.mensaje("Error", "La cantidad debe ser mayor a 0.")
            return
        subtotal = precio_compra * cantidad
        fila = [
            self.codigo_seleccionado,
            self.nombre_articulo,
            f"{precio_compra:.2f}",
            str(cantidad),
            f"{subtotal:.2f}"
        ]
        self.lista_carrito.append({
            "codigo": self.codigo_seleccionado,
            "nombre": self.nombre_articulo,
            "precio_compra": precio_compra,
            "cantidad": cantidad,
            "subtotal": subtotal
        })
        idx = self.lista_carrito_view.InsertItem(self.lista_carrito_view.GetItemCount(), fila[0])
        for i, val in enumerate(fila[1:], start=1):
            self.lista_carrito_view.SetItem(idx, i, val)
        self.actualizar_total()
        self.txt_codigo.Clear()
        self.spin_cantidad.SetValue(1)
        self.txt_precio_compra.SetValue("0.00")
        self.codigo_seleccionado = None
        self.lista_articulos.DeleteAllItems()

    def eliminar_articulo(self, event):
        index = self.lista_carrito_view.GetFirstSelected()
        if index == -1:
            self.mensaje("Advertencia", "Seleccione un artículo del carrito.")
            return
        self.lista_carrito.pop(index)
        self.lista_carrito_view.DeleteItem(index)
        self.actualizar_total()

    def actualizar_total(self):
        self.total_general = sum(item["subtotal"] for item in self.lista_carrito)
        self.lbl_total.SetLabel(f"Total: ${self.total_general:.2f}")

    # --- COMPRAR ---
    def realizar_compra(self, event):
        if not self.lista_carrito:
            self.mensaje("Advertencia", "El carrito está vacío.")
            return

        conn, cursor = conectar()
        if conn and cursor:
            try:
                cursor.execute("""
                    INSERT INTO compra (fecha_compra, total, impuestos, cantidad_articulos, tipo_pago, idproveedor)
                    VALUES (NOW(), %s, 0.0, %s, %s, %s)
                """, (
                    self.total_general,
                    len(self.lista_carrito),
                    "Efectivo",
                    self.proveedor_seleccionado[0] if self.proveedor_seleccionado else "9999999999"
                ))
                folio_compra = cursor.lastrowid

                for item in self.lista_carrito:
                    cursor.execute("""
                        INSERT INTO detalles_compra 
                        (folio_compra, codigo_barras, cantidad_ordenada, cantidad_recibida, precio_unitario_compra, impuesto_unitario, subtotal_compra)
                        VALUES (%s, %s, %s, %s, %s, 0.0, %s)
                    """, (
                        folio_compra,
                        item["codigo"],
                        item["cantidad"],
                        item["cantidad"],
                        item["precio_compra"],
                        item["subtotal"]
                    ))

                    # Incrementar el inventario
                    cursor.execute("""
                        UPDATE inventario SET existencia_actual = existencia_actual + %s
                        WHERE codigo_barras = %s
                    """, (item["cantidad"], item["codigo"]))

                conn.commit()
                self.generar_ticket(folio_compra)
                self.limpiar_compra()
            except Exception as e:
                conn.rollback()
                self.mensaje("Error", f"No se pudo completar la compra: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            self.mensaje("Error", "No se pudo conectar a la base de datos.")

    def generar_ticket(self, folio):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ticket_texto = f"""
{'-'*40}
TIENDA DEL SOL
Folio: {folio}
Fecha: {fecha}
PROVEEDOR:
"""
        if self.proveedor_seleccionado:
            ticket_texto += f"{self.proveedor_seleccionado[1]} ({self.proveedor_seleccionado[0]})\n"
        else:
            ticket_texto += "General\n"

        ticket_texto += f"Atendido por:\n{self.nombre_empleado} {self.apellidos_empleado}\nARTÍCULOS:\n"
        for item in self.lista_carrito:
            ticket_texto += f"{item['nombre']} x{item['cantidad']} @ ${item['precio_compra']:.2f} = ${item['subtotal']:.2f}\n"

        ticket_texto += f"\n{'-'*40}\nTOTAL: ${self.total_general:.2f}\n{'-'*40}\n¡Compra registrada!\n"

        self.mensaje("Ticket de Compra", ticket_texto)
        self.guardar_ticket_pdf(folio, ticket_texto)

    def guardar_ticket_pdf(self, folio, texto):
        carpeta = "tickets_compras"
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        ruta = os.path.join(carpeta, f"compra_{folio}.pdf")
        c = canvas.Canvas(ruta)
        c.setFont("Helvetica", 10)
        lineas = texto.strip().split('\n')
        y = 750
        for linea in lineas:
            c.drawString(50, y, linea)
            y -= 15
        c.save()
        self.mensaje("Éxito", f"Ticket guardado como {ruta}")

    def limpiar_compra(self):
        self.lista_carrito.clear()
        self.lista_carrito_view.DeleteAllItems()
        self.actualizar_total()
        self.txt_codigo.Clear()
        self.spin_cantidad.SetValue(1)
        self.txt_precio_compra.SetValue("0.00")
        self.codigo_seleccionado = None
        self.proveedor_seleccionado = None
        self.txt_id_proveedor.Clear()
        self.lista_proveedores.DeleteAllItems()
        self.lista_articulos.DeleteAllItems()

    def on_regresar_menu(self, event):
        self.Close()
        from MenuPrincipal import MenuPrincipal
        MenuPrincipal(idempleado=self.idempleado)

    def on_cancelar_compra(self, event):
        confirmacion = wx.MessageBox("¿Está seguro de cancelar esta compra?", "Cancelar Compra", wx.YES_NO | wx.ICON_QUESTION)
        if confirmacion == wx.YES:
            self.limpiar_compra()