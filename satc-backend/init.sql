-- Crear la base de datos
CREATE DATABASE satc_database;

-- Conectar a la base de datos
\c satc_database;


-- Tabla para las máquinas
CREATE TABLE maquina (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255),
    ubicacion VARCHAR(255),
    descripcion TEXT,
    sensores INTEGER[]  -- Lista de IDs de los sensores asociados con la máquina
);

-- Tabla para los sensores
CREATE TABLE sensor (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255),
    tipo VARCHAR(255),
    unidad_medida VARCHAR(50),
    maquina_id INTEGER REFERENCES maquina(id)
);
-- Tabla para almacenar los datos adquiridos
CREATE TABLE datos_adquiridos (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    variable VARCHAR(255),
    valor NUMERIC,
    sensor_id INTEGER REFERENCES sensor(id),
    maquina_id INTEGER REFERENCES maquina(id)
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




-- Otras tablas adicionales pueden ser añadidas aquí según sea necesario
-- CREATE TABLE ...
