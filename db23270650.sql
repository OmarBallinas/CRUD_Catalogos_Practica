CREATE DATABASE IF NOT EXISTS delsol DEFAULT CHARACTER SET utf8;
USE delsol;

CREATE TABLE IF NOT EXISTS cliente (
  telefono_cliente CHAR(10) NOT NULL,
  nombre VARCHAR(80) NOT NULL,
  apellido VARCHAR(80) NOT NULL,
  correo_electronico VARCHAR(100),
  PRIMARY KEY (telefono_cliente)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS empleado (
  idempleado INT NOT NULL,
  nombre VARCHAR(80) NOT NULL,
  apellidos VARCHAR(80) NOT NULL,
  telefono CHAR(10),
  correo_electronico VARCHAR(100),
  contraseña VARCHAR(255) NOT NULL,
  PRIMARY KEY (idempleado)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS categoria (
  idcategoria INT NOT NULL,
  nombre VARCHAR(70) NOT NULL,
  PRIMARY KEY (idcategoria)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS articulo (
  codigo_barras CHAR(13) NOT NULL,
  nombre VARCHAR(70) NOT NULL,
  descripcion VARCHAR(150),
  precio FLOAT NOT NULL,
  unidad VARCHAR(50),
  descuento FLOAT,
  idcategoria INT NOT NULL,
  PRIMARY KEY (codigo_barras),
  FOREIGN KEY (idcategoria) REFERENCES categoria(idcategoria)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS proveedor (
  idproveedor INT NOT NULL,
  nombre VARCHAR(80),
  contacto VARCHAR(100) NOT NULL,
  telefono CHAR(10) NOT NULL,
  correo_electronico VARCHAR(80),
  direccion VARCHAR(150),
  PRIMARY KEY (idproveedor)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS venta (
  folio_de_ticket INT NOT NULL AUTO_INCREMENT,
  fecha DATETIME NOT NULL,
  total FLOAT NOT NULL,
  tipo_pago VARCHAR(50),
  impuesto_IVA FLOAT,
  idempleado INT NOT NULL,
  telefono_cliente CHAR(10),
  PRIMARY KEY (folio_de_ticket),
  FOREIGN KEY (idempleado) REFERENCES empleado(idempleado),
  FOREIGN KEY (telefono_cliente) REFERENCES cliente(telefono_cliente)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS detalles_venta (
  folio_de_ticket INT NOT NULL,
  codigo_barras CHAR(13) NOT NULL,
  cantidad_articulo INT NOT NULL,
  precio_unitario_venta FLOAT NOT NULL,
  impuesto_unitario FLOAT,
  subtotal_venta FLOAT,
  PRIMARY KEY (folio_de_ticket, codigo_barras),
  FOREIGN KEY (folio_de_ticket) REFERENCES venta(folio_de_ticket),
  FOREIGN KEY (codigo_barras) REFERENCES articulo(codigo_barras)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS compra (
  folio_compra INT NOT NULL AUTO_INCREMENT,
  fecha_compra DATETIME NOT NULL,
  total FLOAT NOT NULL,
  impuestos FLOAT NOT NULL,
  cantidad_articulos INT,
  tipo_pago VARCHAR(45),
  idproveedor INT NOT NULL,
  PRIMARY KEY (folio_compra),
  FOREIGN KEY (idproveedor) REFERENCES proveedor(idproveedor)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS detalles_compra (
  folio_compra INT NOT NULL,
  codigo_barras CHAR(13) NOT NULL,
  cantidad_ordenada INT,
  cantidad_recibida INT,
  precio_unitario_compra FLOAT NOT NULL,
  impuesto_unitario FLOAT NOT NULL,
  subtotal_compra FLOAT,
  PRIMARY KEY (folio_compra, codigo_barras),
  FOREIGN KEY (folio_compra) REFERENCES compra(folio_compra),
  FOREIGN KEY (codigo_barras) REFERENCES articulo(codigo_barras)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS inventario (
  codigo_barras CHAR(13) NOT NULL,
  existencia_actual INT NOT NULL,
  minimo_requerido INT NOT NULL,
  temporada VARCHAR(65) NOT NULL,
  ultimo_reabastecimiento DATETIME,
  PRIMARY KEY (codigo_barras),
  FOREIGN KEY (codigo_barras) REFERENCES articulo(codigo_barras)
) ENGINE = InnoDB;


INSERT INTO categoria (idcategoria, nombre) VALUES
(0001, 'Bebidas'),
(0002, 'Botanas'),
(0003, 'Limpieza del hogar'),
(0004, 'Cuidado personal'),
(0005, 'Panadería'),
(0006, 'Jugueteria'),
(0007, 'Ropa y Calzado');

INSERT INTO articulo (codigo_barras, nombre, descripcion, precio, unidad, descuento, idcategoria) VALUES
('7501000132153', 'Coca-Cola 600ml', 'Refresco sabor cola en botella de PET', 16.00, 'botella', 0.0, 0001),
('7501020510148', 'Doritos Nacho 65g', 'Botana de maíz sabor nacho', 19.50, 'bolsa', 1.5, 0002),
('7501035910012', 'Fabuloso Lavanda 1L', 'Limpiador líquido multiusos', 23.90, 'litro', 0.0, 0003),
('7501058604521', 'Colgate Triple Acción 75ml', 'Pasta dental protección total', 28.00, 'tubo', 0.0, 0004),
('7503012345678', 'Concha Azucarada', 'Pan dulce sabor vainilla con cobertura', 11.00, 'pieza', 0.0, 0005),
('7501000132160', 'Pepsi 600ml', 'Refresco sabor cola en botella de PET', 15.50, 'botella', 0.0, 0001),
('7501020510149', 'Cheetos Flamin Hot 65g', 'Botana de maíz sabor picante', 20.00, 'bolsa', 1.0, 0002),
('7501035910013', 'Pinol Limón 1L', 'Limpiador líquido multiusos con aroma a limón', 25.00, 'litro', 0.0, 0003),
('7501058604522', 'Colgate Herbal 75ml', 'Pasta dental con extractos naturales', 27.00, 'tubo', 0.0, 0004),
('7503012345679', 'Concha Chocolate', 'Pan dulce con cobertura de chocolate', 12.00, 'pieza', 0.0, 0005),
('7501000132177', 'Jarritos Naranja 600ml', 'Refresco sabor naranja en botella de vidrio', 18.00, 'botella', 0.0, 0001),
('7501020510150', 'Sabritas Original 150g', 'Botana de papas clásicas', 22.50, 'bolsa', 0.0, 0002),
('7501035910014', 'Cloralex 1L', 'Cloro líquido para limpieza', 28.00, 'litro', 0.0, 0003),
('7501058604523', 'Sensodyne 75ml', 'Pasta dental para dientes sensibles', 35.00, 'tubo', 0.0, 0004),
('7503012345680', 'Cuernito', 'Pan dulce en forma de cuerno', 10.00, 'pieza', 0.0, 0005),
('7504000132150', 'Playera Blanca Talla M', 'Camiseta de algodón cuello redondo', 89.00, 'pieza', 5.0, 0007),
('7504000132151', 'Pantalón Mezclilla Talla 32', 'Pantalón de mezclilla azul oscuro', 249.00, 'pieza', 0.0, 0007),
('7504000132152', 'Calcetas Deportivas (3 pares)', 'Calcetas blancas unisex', 59.00, 'paquete', 0.0, 0007),
('7505000132153', 'Carrito de Juguete', 'Carro de plástico con fricción', 45.00, 'pieza', 0.0, 0006),
('7505000132154', 'Muñeca Clásica', 'Muñeca de vinil con vestido rosa', 120.00, 'pieza', 10.0, 0006),
('7505000132155', 'Lego Mini Set 50pcs', 'Juego de bloques armables', 99.00, 'caja', 0.0, 0006);

INSERT INTO inventario (codigo_barras, existencia_actual,minimo_requerido, temporada, ultimo_reabastecimiento) VALUES
('7501000132153', 95, 10, 'Todo el año', '2025-02-28'),
('7501020510148', 65, 10, 'Todo el año', '2025-01-10'),
('7501035910012', 40, 10, 'Todo el año', '2025-03-15'),
('7501058604521', 55, 10, 'Todo el año', '2025-05-01'),
('7503012345678', 30, 8, 'Todo el año', '2025-03-05'),
('7501000132160', 100, 2, 'Todo el año', '2025-02-24'),
('7501020510149', 80, 15, 'Todo el año', '2025-01-15'),
('7501035910013', 50, 12, 'Todo el año', '2025-01-20'),
('7501058604522', 60, 10, 'Todo el año', '2025-07-10'),
('7503012345679', 40, 9, 'Todo el año', '2025-05-12'),
('7501000132177', 75, 15, 'Todo el año', '2025-01-25'),
('7501020510150', 90, 20, 'Todo el año', '2025-02-05'),
('7501035910014', 45, 11, 'Todo el año', '2025-02-28'),
('7501058604523', 30, 8, 'Todo el año', '2025-04-15'),
('7503012345680', 50, 10, 'Todo el año', '2025-03-20'),
('7504000132150', 50, 15, 'Todo el año', '2025-04-10'),
('7504000132151', 60, 7, 'Todo el año', '2025-04-12'),
('7504000132152', 30, 10, 'Todo el año', '2025-03-09'),
('7505000132153',  40, 4, 'Todo el año', '2025-02-18'),
('7505000132154',  71, 10, 'Todo el año', '2025-02-21'),
('7505000132155',  41, 10, 'Todo el año', '2025-02-08');

INSERT INTO cliente (telefono_cliente, nombre, apellido, correo_electronico) VALUES
('9615556232', 'Carolina', 'Ortega', 'caritoarqui@gmail.com'),
('9615556111', 'Gabriel', 'Urbina', 'gabrielosky@yahoo.com'),
('9615556222', 'Luis', 'Burguete', 'burguetuis@hotmail.com'),
('9615556333', 'Felipe', 'Espinosa', 'lfespin@outlook.com'),
('9615556444', 'Adriana', 'Lara', 'adri.lara@gmail.com'),
('9615556555', 'María', 'López', 'maria.lopez@gmail.com'),
('9615556666', 'José', 'Martínez', 'jose.martinez@hotmail.com'),
('9615556777', 'Maria', 'González', 'mari.gonzalez@yahoo.com'),
('9615556888', 'Carlos', 'Ramírez', 'carlos.ramirez@gmail.com'),
('9615556999', 'Laura', 'Hernández', 'laura.hernandez@outlook.com'),
('9615512333', 'Alan', 'Ichin', 'alansillo.ichin@gmail.com'),
('9617622667', 'Verónica', 'Sánchez', 'veronica.sanchez@hotmail.com'),
('9619877112', 'Arnol', 'Torres', 'eduardo.torres@gmail.com');


INSERT INTO empleado (idempleado, nombre, apellidos, telefono, correo_electronico, contraseña) VALUES
(1, 'Jorge', 'Hernández Díaz', '9615423111', 'jorge.hdz@tienda.mx', 'jorgehernandez'),
(2, 'Gustavo', 'Zenteno Mendoza', '9617754232', 'gust.zent@tienda.mx', 'gustavozenteno'),
(3, 'Pedro', 'García León', '9678896542', 'pedro.gl@tienda.mx', 'pedrogarcia'),
(4, 'Valeria', 'Martinez Diaz', '9615425322', 'valeria.martin@tienda.mx', 'valeriamartinez'),
(5, 'Andrés', 'Zapata Cruz', '9613345334', 'andres.zc@tienda.mx', 'andreszapata');

INSERT INTO proveedor (idproveedor, nombre, contacto, telefono, correo_electronico, direccion) VALUES
(1, 'Coca-Cola FEMSA', 'Marisa Rios', '9615426354', 'ventas@coca-cola.com', 'Col. Vida Mejor, TGZ'),
(2, 'PepsiCo México', 'Daniel Rincon', '9617624353', 'contacto@pepsico.com', 'Calz. del Sumidero, TGZ'),
(3, 'Colgate-Palmolive', 'Ana De la Torre', '9675412634', 'ventas@colgate.com', 'San pedro Porgresivo, TGZ'),
(4, 'Bimbo S.A.', 'Emilio Soberano', '9675436273', 'ventas@bimbo.com', 'Av. Panadería 456, Terán, TGZ'),
(5, 'Fabuloso Distribuciones', 'Nadia Artemisa', '9615624532', 'contacto@fabuloso.mx', 'Calle Higiene 789, TGZ'),
(6, 'Ropa y Calzado', 'Mario Alfredo', '9615426343', 'contacto@fabuloso.mx', 'Calle Higiene 789, TGZ');
