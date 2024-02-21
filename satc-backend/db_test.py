from faker import Faker
import random
import psycopg2
from db_connect import db_config


# Conectar a la base de datos
conn = psycopg2.connect(**db_config)
cursor = conn.cursor()

# Crear una instancia de Faker
faker = Faker()

# Lista de variables posibles
variables = ['temperatura', 'presion', 'humedad', 'velocidad']

# Generar y insertar datos aleatorios en la base de datos
for _ in range(100):  # Generar 100 registros aleatorios
    timestamp = faker.date_time_this_month()  # Generar una fecha y hora aleatoria en el mes actual
    variable = random.choice(variables)  # Seleccionar una variable aleatoria de la lista
    valor = random.uniform(0, 100)  # Generar un valor numérico aleatorio entre 0 y 100

    # Insertar datos en la tabla
    cursor.execute("INSERT INTO datos_adquiridos (timestamp, variable, valor) VALUES (%s, %s, %s)", (timestamp, variable, valor))

# Confirmar la transacción y cerrar la conexión
conn.commit()
cursor.close()
conn.close()
