from faker import Faker
import random
import asyncpg
import asyncio
from db_connect import db_config

async def insert_random_data(conn, n=100):
    # Crear una instancia de Faker
    faker = Faker()

    # Lista de variables posibles
    variables = ['temperatura', 'presion', 'humedad', 'velocidad']

    # Generar y insertar datos aleatorios en la base de datos
    for _ in range(n):  # Generar n registros aleatorios
        timestamp = faker.date_time_this_month()  # Generar una fecha y hora aleatoria en el mes actual
        variable = random.choice(variables)  # Seleccionar una variable aleatoria de la lista
        valor = random.uniform(0, 100)  # Generar un valor numérico aleatorio entre 0 y 100

        # Insertar datos en la tabla
        await conn.execute("INSERT INTO datos_adquiridos (timestamp, variable, valor) VALUES ($1, $2, $3)", timestamp, variable, valor)

async def main():
    # Conectar a la base de datos
    conn = await asyncpg.connect(**db_config)
    
    try:
        # Insertar datos aleatorios
        await insert_random_data(conn, 100)
        
        # Confirmar la transacción
        await conn.execute('COMMIT')
    except Exception as e:
        print(f"Error al insertar datos: {e}")
        await conn.execute('ROLLBACK')
    finally:
        # Cerrar la conexión
        await conn.close()

# Ejecutar la función principal en el bucle de eventos
loop = asyncio.get_event_loop()
loop.run_until_complete(main())