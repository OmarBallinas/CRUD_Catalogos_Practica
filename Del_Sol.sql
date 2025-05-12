CREATE DATABASE IF NOT EXISTS DelSol DEFAULT CHARACTER SET utf8;
USE DelSol;

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
  dirección VARCHAR(150),
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
