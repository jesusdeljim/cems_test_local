-- Crear la base de datos
CREATE DATABASE satc_database;

-- Conectar a la base de datos
\c satc_database;

-- Tabla para almacenar los datos adquiridos
CREATE TABLE datos_adquiridos (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    variable VARCHAR(255),
    valor NUMERIC,
    sensor_id INTEGER REFERENCES sensores(id),
    maquina_id INTEGER REFERENCES maquinas(id)
);

-- Tabla para configuraciones
CREATE TABLE configuraciones (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255),
    valor TEXT
);

-- Tabla para registros de alarmas
CREATE TABLE registros_alarmas (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipo VARCHAR(255),
    mensaje TEXT
);

-- Tabla para las máquinas
CREATE TABLE maquinas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255),
    descripcion TEXT,
    ubicacion VARCHAR(255)
);

-- Tabla para los sensores
CREATE TABLE sensores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255),
    tipo VARCHAR(255),
    unidad_medida VARCHAR(50),
    maquina_id INTEGER REFERENCES maquinas(id)
);

-- Otras tablas adicionales pueden ser añadidas aquí según sea necesario
-- CREATE TABLE ...
