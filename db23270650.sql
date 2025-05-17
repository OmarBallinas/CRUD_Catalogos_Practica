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
  capacidad_maxima INT NOT NULL,
  temporada VARCHAR(65) NOT NULL,
  fecha_caducidad DATETIME,
  PRIMARY KEY (codigo_barras),
  FOREIGN KEY (codigo_barras) REFERENCES articulo(codigo_barras)
) ENGINE = InnoDB;


INSERT INTO categoria (idcategoria, nombre) VALUES
(0001, 'Bebidas'),
(0002, 'Botanas'),
(0003, 'Limpieza del hogar'),
(0004, 'Cuidado personal'),
(0005, 'Panadería');


INSERT INTO articulo (codigo_barras, nombre, descripcion, precio, unidad, descuento, idcategoria) VALUES
('7501000132153', 'Coca-Cola 600ml', 'Refresco sabor cola en botella de PET', 16.00, 'botella', 0.0, 0001),
('7501020510148', 'Doritos Nacho 65g', 'Botana de maíz sabor nacho', 19.50, 'bolsa', 1.5, 0002),
('7501035910012', 'Fabuloso Lavanda 1L', 'Limpiador líquido multiusos', 23.90, 'litro', 0.0, 0003),
('7501058604521', 'Colgate Triple Acción 75ml', 'Pasta dental protección total', 28.00, 'tubo', 0.0, 0004),
('7503012345678', 'Concha Azucarada', 'Pan dulce sabor vainilla con cobertura', 11.00, 'pieza', 0.0, 0005);


INSERT INTO inventario (codigo_barras, existencia_actual, capacidad_maxima, temporada, fecha_caducidad) VALUES
('7501000132153', 95, 200, 'Todo el año', '2025-12-31'),
('7501020510148', 65, 150, 'Todo el año', '2025-11-10'),
('7501035910012', 40, 100, 'Todo el año', '2027-03-15'),
('7501058604521', 55, 100, 'Todo el año', '2026-05-01'),
('7503012345678', 30, 80, 'Todo el año', '2025-06-05');


INSERT INTO cliente (telefono_cliente, nombre, apellido, correo_electronico) VALUES
('5567891234', 'Carolina', 'Ortega', 'caritoarqui@gmail.com'),
('5543216789', 'Gabriel', 'Urbina', 'gabrielosky@yahoo.com'),
('5588123456', 'Luis', 'Burguete', 'burguetuis@hotmail.com'),
('5577654321', 'Felipe', 'Espinosa', 'lfespin@outlook.com'),
('5599988776', 'Adriana', 'Lara', 'adri.lara@gmail.com');


INSERT INTO empleado (idempleado, nombre, apellidos, telefono, correo_electronico, contraseña) VALUES
(1, 'Jorge', 'Hernández Díaz', '5551234567', 'jorge.hdz@tienda.mx', 'jorgehernandez'),
(2, 'Gustavo', 'Zenteno Mendoza', '5562345678', 'gust.zent@tienda.mx', 'gustavozenteno'),
(3, 'Pedro', 'García León', '5573456789', 'pedro.gl@tienda.mx', 'pedrogarcia'),
(4, 'Valeria', 'Martinez Diaz', '5584567890', 'valeria.martin@tienda.mx', 'valeriamartinez'),
(5, 'Andrés', 'Zapata Cruz', '5595678901', 'andres.zc@tienda.mx', 'andreszapata');

INSERT INTO proveedor (idproveedor, nombre, contacto, telefono, correo_electronico, direccion) VALUES
(1, 'Coca-Cola FEMSA', 'Marisa Rios', '5551010101', 'ventas@coca-cola.com', 'Col. Vida Mejor, TGZ'),
(2, 'PepsiCo México', 'Daniel Rincon', '5552020202', 'contacto@pepsico.com', 'Calz. del Sumidero, TGZ'),
(3, 'Colgate-Palmolive', 'Ana De la Torre', '5553030303', 'ventas@colgate.com', 'San pedro Porgresivo, TGZ'),
(4, 'Bimbo S.A.', 'Emilio Soberano', '5554040404', 'ventas@bimbo.com', 'Av. Panadería 456, Terán, TGZ'),
(5, 'Fabuloso Distribuciones', 'Nadia Artemisa', '5555050505', 'contacto@fabuloso.mx', 'Calle Higiene 789, TGZ');
